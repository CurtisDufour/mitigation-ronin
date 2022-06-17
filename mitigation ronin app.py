



# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:06:05 2022
@author: curtis.m.dufour
"""


import tkinter as tk
import tksheet
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.messagebox import showinfo
import pandas as pd
import ipaddress
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
import re
from datetime import date



class App(tk.Tk):
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)
    f = pd.ExcelFile('References_20220315.xlsx')
    df_dict = f.parse(sheet_name=[0, 1, 2, 3, 4, 5, 6]) # imports dictionary
    s = list(df_dict.keys()) 
    df1, df2, df3, df4, df5, df6, df7 = list(df_dict.values())
        
    
    def __init__(self):
        super().__init__()
        self.title("Mitigation Ronin.py")
        self.geometry('900x1800')
        #label
        self.lbl = tk.Label(self, text="Welcome to Mitigation Ronin", font=('Arial', 14))
        self.lbl.grid(column=1, row=0, padx=10, pady=10)
        #self.lbl.pack()
        #self.ipresult = tk.Label(self, text="IP results")
        #self.ipresult.grid(column=1, row=10)
        #text boxes
        ######################################## IP box #############################################################
        self.txt_ip = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=6,
                                             font=("Arial", 12))
        self.txt_ip.grid(column=1, row=2, pady=10, padx=10)
        self.txt_ip.insert(tk.END, "paste your IP's here: ")
        self.txt_ip.focus()
        ####################################### #domain box
        self.txt_dom = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=6,
                                             font=("Arial", 12))
        self.txt_dom.grid(column=1, row=7, pady=10, padx=10)
        self.txt_dom.insert(tk.END, "paste your domains here: ")
        
        ######################################## #buttons# ##########################################################
        self.ip_btn = ttk.Button(self, text="IP Mitigation") # 
        self.ip_btn.grid(column=1, row=6)
        self.ip_btn['command'] = self.clicked_ip
        self.dom_btn = ttk.Button(self, text="Domain Mitigation")
        self.dom_btn['command'] = self.clicked_dom
        self.dom_btn.grid(column=1, row=8)
        self.update_btn = ttk.Button(self, text="Update Reference Sheet")
        self.update_btn['command'] = self.clicked_update
        self.update_btn.grid(column=1, row=12)
        self.update_btn_cache = []
        
        ###################################### need to do tksheet - fix the input tot he sheet ##########################
        self.sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=800,
                                   align="c",
                                   all_columns_displayed=True,
                                   show_y_scrollbar=True)
        self.sheet.change_theme("dark")
        self.sheet.set_sheet_data(self.mit_ref())
        self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "drag_select",   #enables shift click selection as well
                                         "column_drag_and_drop",
                                         "row_drag_and_drop",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         "row_width_resize",
                                         "column_height_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row",
                                         "copy",
                                         "cut",
                                         "paste",
                                         "delete",
                                         "undo",
                                         "edit_cell"))
        self.sheet.grid(column=1, row=10, padx=5,pady=5, sticky="w")
        ############################### non-mitigated domains
        self.sub_sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=800,
                                   align="c",
                                   all_columns_displayed=True,
                                   show_y_scrollbar=True)
        self.sub_sheet.set_sheet_data([list(range(0,10))])
        self.sub_sheet.create_checkbox(c=0,
                                       r="all",
                       checked = False,
                       state = "normal",
                       redraw = False,
                       check_function = self.clicked_update,
                       text = "")
        self.sub_sheet.change_theme("dark")
        #self.sub_sheet.set_sheet_data(self.mit_ref())
        self.sub_sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                         "drag_select",   #enables shift click selection as well
                                         "column_drag_and_drop",
                                         "row_drag_and_drop",
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         "row_width_resize",
                                         "column_height_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row",
                                         "copy",
                                         "cut",
                                         "paste",
                                         "delete",
                                         "undo",
                                         "edit_cell"))


        self.sub_sheet.grid(column=1, row=11, padx=5, pady=5, sticky="e")


    
    # This gives a pop-up of the results of the mitigation search.
    def clicked_ip(self):
        # Data must be expressed as a list of lists...
        self.sheet.set_sheet_data([i for i in self.mit_ref().values.tolist()])
        
    def clicked_dom(self):
        try:
            # pandas data has to be expressed as list of lists
            self.sheet.set_sheet_data([d for d in self.dom_search().values.tolist()])
            self.sub_sheet.set_sheet_data([n for n in self.dom_search().values.tolist()])
        except:
            self.sheet.set_sheet_data([f"{d} returns no results" for d in self.dom_search.values.tolist()])
        #showinfo(title="testing",
        #         message="this is a test of the domain button")
        
    def clicked_update(self):
        # append 
        for i in self.update_btn_cache:
            pass
        else:
            pass
        ### need to write this function to tie to update button for reference sheet
        pass
    
        
        ############################################ I think this is broken ################################
    def ip_mit(self):
        df_mit = pd.DataFrame()
        ips = self.txt_ip.get("1.0","end-1c").splitlines()
        try:
            badguys = [i for i in ips if i in list(str(IPv4Network(self.df1["CIDR"]).hosts()))]
            print(badguys)
            df_mit.append(self.df1.loc[self.df1.CIDR == str([i for i in badguys])])
            return df_mit
            
        except:
            df_mit.append(self.df1.loc[self.df1.CIDR== "Not there"])
            return df_mit
        
        ######################################  This seems to work ###############################
    def mit_ref(self):
        self.ip_input = self.txt_ip.get("1.0","end-1c").splitlines()
        try:
            self.not_ips = self.df1.loc[~self.df1["CIDR"].isin(self.ip_input)]
            return self.df1.loc[self.df1["CIDR"].isin(self.ip_input)]
        except: 
            return ValueError


        ########################### This is successful #########################
        # TODO: highlight or separate table for negative hits
    def dom_search(self): 
        # create list from input box
        self.doms = self.txt_dom.get("1.0", "end-1c").splitlines()

        try:
            #find matches in reference sheet that match self.doms
            ref_match = self.df5.loc[self.df5["Domain"].isin(self.doms)]
            return ref_match
        except:
            return ValueError
        
        ################################ code wrote without IDE; very experimental ###################
        # Need to apply these to the IP's displayed in the dataframe for first and last binaries
    def bin_trans(self, binary):
        # This should work for both IPv4 and IPv6
        return str(ipaddress.ip_address(binary))
    
    def ip_trans(self, binary):
        # This should transform ip's back to 32bit integers for storage in the reference sheet
        return int(str(ipaddress.ip_address(binary))
    
    # This should apply bin_trans to df1's first two rows... I hope
    df1.apply(lambda x: bin_trans(df1.iloc[0,1]), axis=1)
    # This should do the opposite?
    df1.apply(lambda x: ip_trans(df1.iloc[0,1]), axis=1)
                  
    
             



if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    





