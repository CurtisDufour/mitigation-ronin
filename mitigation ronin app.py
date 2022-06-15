



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
        self.geometry('900x900')
        #label
        self.lbl = tk.Label(self, text="Welcome to Mitigation Ronin", font=('Arial', 14))
        self.lbl.grid(column=1, row=0, padx=30, pady=30)
        #self.lbl.pack()
        #self.ipresult = tk.Label(self, text="IP results")
        #self.ipresult.grid(column=1, row=10)
        #text boxes
        ######################################## IP box #############################################################
        self.txt_ip = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=6,
                                             font=("Arial", 12))
        self.txt_ip.grid(column=1, row=2, pady=30, padx=30)
        self.txt_ip.insert(tk.END, "paste your IP's here: ")
        self.txt_ip.focus()
        #domain box
        self.txt_dom = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=6,
                                             font=("Arial", 12))
        self.txt_dom.grid(column=1, row=7, pady=30, padx=30)
        self.txt_dom.insert(tk.END, "paste your domains here: ")
        
        ######################################## #buttons# ##########################################################
        self.ip_btn = ttk.Button(self, text="IP Mitigation") # 
        self.ip_btn.grid(column=1, row=6)
        self.ip_btn['command'] = self.clicked_ip
        self.dom_btn = ttk.Button(self, text="Domain Mitigation")
        self.dom_btn['command'] = self.clicked_dom
        self.dom_btn.grid(column=1, row=8)
        
        ###################################### need to do tksheet - fix the input tot he sheet ##########################
        self.sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=850,
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
        self.sheet.grid(column=1, row=10, sticky="e")
        ############################### non-mitigated domains
        self.nondom_sheet = self.sheet
        self.nondom_sheet.grid(column=1, row=20)


    
    # This gives a pop-up of the results of the mitigation search.
    def clicked_ip(self):
        # Data must be expressed as a list of lists...
        self.sheet.set_sheet_data([i for i in self.mit_ref().values.tolist()])
        
    def clicked_dom(self):
        try:
            self.sheet.set_sheet_data([d for d in self.dom_search().values.tolist()])
        except:
            self.sheet.set_sheet_data([f"{d} returns no results" for d in self.dom_search.values.tolist()])
        #showinfo(title="testing",
        #         message="this is a test of the domain button")
        
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
        # try: 
        #     self.df_mit = pd.DataFrame()
        #     #res_list =[]
        #     for i in ip_input: #self.txt_ip.get("1.0","end-1c").splitlines():
        #         if i in list(self.df1["CIDR"]):
        #             self.res = self.df1.loc[self.df1["CIDR"] == i] # prints the row
        #             #print(f"the type of res variable is {type(res)}")
        #             print(f"{i} is in the Bad Guy list.")
        #             #df_mit.append(res)
        #             #return res

        #         elif i in list(self.df2["CIDR"]):
        #             self.res = self.df2.loc[self.df2["CIDR"] == i] # prints the row
        #             #df_mit.append(res)
        #             #return res
                    
        #         elif i in list(self.df3["CIDR"]):
        #             self.res = self.df3.loc[self.df3["CIDR"] == i] # prints the row
        #             #df_mit.append(res)
        #             #return res
        #         elif i in list(self.df4["CIDR"]):
        #             self.res = self.df4.loc[self.df4["CIDR"] == i] # prints the row
        #             #df_mit.append(res)
        #             #return res
        #         else: 
        #             return f"{i} does not yield results. "
        #             continue
        #         print(type(self.res))
        #         return self.res
                
                
        # except ValueError:
        #     return "I am Error"
        #     pass
        ########################### This is successful #########################
        # TODO: highlight or separate table for negative hits
    def dom_search(self): 
        try:
            self.doms = self.txt_dom.get("1.0", "end-1c").splitlines()
            self.not_dom = self.df5.loc[~self.df5["Domain"].isin(self.doms)]
            return self.df5.loc[self.df5["Domain"].isin(self.doms)]
        except self.not_dom:
            return self.df6.loc[self.df6["Domain"].isin(list(self.not_dom["Domain"]))]
        except not self.df6.loc[self.df6["Domain"].isin(list(self.not_dom["Domain"]))]:
            return 



if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    








