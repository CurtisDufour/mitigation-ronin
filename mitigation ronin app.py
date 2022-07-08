# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:06:05 2022
@author: curtis.m.dufour
"""
import tkinter as tk
import tksheet
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import pandas as pd
import ipaddress
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
import re
from datetime import date
import uwuify


########Fixed the input of the file to the pandas df. Consequently broke the upload and f_lbl stuff. 
######## It also creates an empty tkinter frame upon opening the filedialog filename popup
######## Sorry if I don't get to fixing that anytime soon.
# TODO: update function
# TODO: IP address CIDR check
# TODO: containerize this in an exe file for distro
# TODO: bug checks


class App(tk.Tk):
    
    file = filedialog.askopenfilename(filetypes =[("Excel Files", '*.xlsx')])
    f = pd.ExcelFile(file)
        #f = pd.ExcelFile(upload_file)
    df_dict = f.parse(sheet_name=[0, 1, 2, 3, 4, 5, 6]) # imports dictionary
    df1, df2, df3, df4, df5, df6, df7 = list(df_dict.values())
    df1['First Binary'] = df1['First Binary'].apply(lambda x: ipaddress.ip_address(x)) 
    df1['Last Binary'] = df1['Last Binary'].apply(lambda x: ipaddress.ip_address(x))
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    def __init__(self):
        super().__init__()
         # Title and geometry
         
        self.title("Mitigation Ronin.py")
        self.geometry('1000x1200')
        #label
        self.lbl = tk.Label(self, text="Welcome to Mitigation Ronin!", font=('Arial', 14))
        self.lbl.grid(column=1, row=0, padx=10, pady=10, sticky='nswe')
        
        # This is all broken
        #print(self.my_str)
        self.my_str = tk.StringVar()
        self.my_str.set("placeholder")
        # self.my_str.set(self.file)
        
        # Label for chosen reference sheet 
        self.f_lbl = tk.Label(self, textvariable="reference sheet loaded", bg='black', fg='lightgreen')
        self.f_lbl.grid(column=1, row=1, sticky='nse', padx=140)
        self.tk_headers = ['Mitigated', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]
        
        ######################################## IP box #############################################################
        # IP mitigation Textbox
        self.txt_ip = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=5,
                                             font=("Arial", 12))
        self.txt_ip.grid(column=1, row=2, pady=10, padx=10)
        self.txt_ip.insert(tk.END, "paste your IP's here: ")
        self.txt_ip.focus()
        
        ####################################### #domain box
        # Domain Mitigation Textbox
        self.txt_dom = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                             width=40, height=5,
                                             font=("Arial", 12))
        self.txt_dom.grid(column=1, row=7, pady=10, padx=10)
        self.txt_dom.insert(tk.END, "paste your domains here: ")
        
        ######################################## #buttons# ##########################################################
        # IP Mitigation Search
        self.ip_btn = ttk.Button(self, text="IP Mitigation") # 
        self.ip_btn.grid(column=1, row=6)
        self.ip_btn['command'] = self.clicked_ip
        # Domain Mitigation Search
        self.dom_btn = ttk.Button(self, text="Domain Mitigation")
        self.dom_btn['command'] = self.clicked_dom
        self.dom_btn.grid(column=1, row=8)
        #Update Reference Sheet Button
        self.update_btn = ttk.Button(self, text="Update Reference Sheet")
        self.update_btn['command'] = self.clicked_update
        self.update_btn.grid(column=1, row=12)
        self.update_btn_cache = []
        #Upload Reference Sheet Button
        self.upload_btn = ttk.Button(self, text='broken upload_file() button')
        self.upload_btn['command'] = lambda:self.upload_file()
        self.upload_btn.grid(column=1, row=1, sticky='nsw', padx=200)
        # self.uwu_btn = ttk.Button(self, text="UwU")
        # self.uwu_btn['command'] = self.uwu_it
        # self.uwu_btn.grid(column=2, row=12)
        ###################################### need to do tksheet - fix the input tot he sheet ##########################
        self.sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=900,
                                   align="c",
                                   all_columns_displayed=True,
                                   show_y_scrollbar=True)
        self.sheet.change_theme("dark")
        self.sheet.set_sheet_data(self.ip_search())
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
        self.sheet.grid(column=1, row=10, padx=15,pady=5, sticky="nswe")
        ############################### non-mitigated domains; add 
        self.sub_sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=900,
                                   align="c",
                                   all_columns_displayed=True,
                                   show_y_scrollbar=True)
        self.sub_sheet.set_sheet_data([list(range(0,10))])
        self.sub_sheet.create_header_checkbox(c=0,
                                              checked = False,
                                              check_function = self.sub_sheet.click_checkbox(r="all", 
                                                                                             c=0, 
                                                                                             checked=False),
                                              text = "Mitigate")
        self.sub_sheet.highlight_columns(columns=[0], bg=None, fg="white", overwrite = True)
        self.sub_sheet.create_checkbox(c=0,
                                       r="all",
                                       checked = False,
                                       state = "normal",
                                       text = "Checkbox")
        self.sub_sheet.change_theme("dark")
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

        self.sub_sheet.grid(column=1, row=11, padx=15, pady=5, sticky="nswe")
        
    
    def upload_file(self):
        #file = filedialog.askopenfilename(filetypes =[("Excel Files", '*.xlsx')])#, ("All Files"), ("*.*")])
        if self.file:
            self.my_str.set(self.file)
            return self.file
        else:
            messagebox.showerror("Error", "File not selected")
            print("File not chosen.")
            return "File not chosen"
        

    # This gives a pop-up of the results of the mitigation search.
    def clicked_ip(self):
        # Data must be expressed as a list of lists...
        self.uwu_it()
        print([type(i) for i in self.ip_input])
        self.sheet.set_sheet_data([i for i in self.ip_search().values.tolist()])
        self.sub_sheet.set_sheet_data([i for i in self.ip_mit.values.tolist()])

        self.sheet.headers(newheaders = self.tk_headers)
        self.sub_sheet.headers(newheaders=self.tk_headers)
        self.sub_sheet.create_checkbox(r="all",
                                       c=0,
                                       checked = False,
                                       text = "Checkbox")
        self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=True, check_function=self.check_all)

        
    def clicked_dom(self):
        try:
            # pandas data has to be expressed as list of lists
            self.sheet.set_sheet_data([d for d in self.dom_search().values.tolist()])
            self.sub_sheet.set_sheet_data([n for n in self.df_mit.values.tolist()])
            ## I think I can create a function in the header checkbox to check all for the other boxes...
            self.sheet.headers(newheaders = self.tk_headers)
            self.sub_sheet.headers(newheaders = self.tk_headers)
            self.sub_sheet.create_checkbox(r="all",
                                           c=0,
                                           checked = False,
                                           text = "Checkbox")
            self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=True, check_function=self.check_all)
        except:
            self.sheet.set_sheet_data([f"{d} returns no results" for d in self.dom_search.values.tolist()][0])
        #showinfo(title="testing",
        #         message="this is a test of the domain button")
        
    def clicked_update(self):
        self.uwu_it()
        # append 
        for i in self.update_btn_cache:
            pass
        else:
            pass
        ### need to write this function to tie to update button for reference sheet
        pass
    
        
        ######################################  This seems to work ###############################
    def ip_search(self):
        #input ip addresses
        ip_input = self.txt_ip.get("1.0","end-1c").splitlines() #split lines of input
        self.ip_input = [i.strip() for i in ip_input] # clean up in case of spaces
        for i in self.ip_input:
            try:
                i = ipaddress.ip_address(i)
            except ValueError:
                i = i
        else:
            pass
        
        # This should make each ip in ips list an ipnetwork object.
        # If it doesn't already have a cidr notation, it assumes /32
        # for i in ips:
            
            # if ipaddress.ip_interface(i):
            #     i = ipaddress.ip_interface(i)
            #     print(i)
            #     continue
            # elif ipaddress.ip_address(i):
            #     i = ipaddress.ip_address(i)
            #     print(i)
            #     #i = ipaddress.ip_interface(f"{i}/32").network
            # else:
            #     print("IP dork thing")
            #     pass
        ip_list = self.df1['CIDR'].tolist() # mitigation list of IP's
        ip_list = [ipaddress.ip_interface(i).network for i in ip_list]
        # OK IP list is now a list of ip networks
        #print([str(i) for i in ip_list[:4:]])
        # compare ip_input to list of ranges in ip_list
        
            
        # df instantiation and column names
        self.ip_mit = pd.DataFrame(columns=['Mitigate', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        try:

            self.not_ips = [i for i in self.ip_input if i not in ip_list]
            self.df_ref = self.df1.loc[self.df1["CIDR"].isin(self.ip_input)]
            self.ip_mit['CIDR'] = self.not_ips
            self.df_ref.insert(0, "Mitigate", ["Mitigated" for i in range(len(self.df_ref.index))])
            return self.df_ref#self.df1.loc[self.df1["CIDR"].isin(ips)]
        except: 
            messagebox.showerror("I am Error", f"{[i for i in self.ip_input]} encountered an error")

        ########################### This is successful #########################

    def dom_search(self): 
        # create list from input box
        doms = self.txt_dom.get("1.0", "end-1c").splitlines()
        doms = [i.strip() for i in doms] # input validations
        self.df_mit = pd.DataFrame(columns=['Mitigate', 'Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
        
        try:
            #find matches in reference sheet that match self.doms
            dom_list = self.df5["Domain"].tolist()
            self.not_doms = [i for i in doms if i not in dom_list]
            self.df_ref = self.df5.loc[self.df5["Domain"].isin(doms)]
            self.df_mit["Domain"] = self.not_doms
            self.df_ref.insert(0, "Mitigate", ["Mitigated" for i in range(len(self.df_ref.index))])
            return self.df_ref
        except:
            messagebox.showerror("Error", f"{[i for i in doms]} is not a valid domain.")

    # Trying to write a function to tie to header checkbox
    def check_all(self, r="all", c=0, checked=False):
        self.sub_sheet.create_checkbox(r="all",
                                   c=0,      
                                   checked=True, 
                                   redraw=True,
                                   text="selected")
        
    def uwu_it(self):
        flags = uwuify.SMILEY | uwuify.YU
        resp = uwuify.uwu(self.lbl['text'], flags=flags)
        self.lbl["text"] = resp

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    



    









