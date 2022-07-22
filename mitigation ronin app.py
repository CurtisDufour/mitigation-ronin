# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:06:05 2022
@author: curtis.m.dufour
"""
import tkinter as tk
import tksheet
from urllib.parse import urlparse
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import openpyxl
from openpyxl.utils import datetime
import pandas as pd
import ipaddress
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
    df_dict = f.parse(sheet_name=[0, 1, 2, 3, 4, 5, 6]) # imports dictionary
    df1, df2, df3, df4, df5, df6, df7 = list(df_dict.values())
    # df2 is the whitelist
    # df3 is the army ip list
    # df6 is domain whitelist
    #df1['Date Issued'] = df1['']
    df1['First Binary'] = df1['First Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df1['Last Binary'] = df1['Last Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    def __init__(self):
        super().__init__()
         # Title and geometry
         
        self.title("Mitigation Ronin.py")
        self.geometry('1000x1600')
        self.config(bg='#242526')
        #label
        self.lbl = tk.Label(self, text="Welcome to Mitigation Ronin!", 
                            font=('Arial', 14), 
                            bg='#050505', 
                            fg='lightgray')
        self.lbl.grid(column=1, row=0, padx=10, pady=10, sticky='ns')
        
        # This is all broken
        #print(self.my_str)
        self.my_str = tk.StringVar()
        self.my_str.set("placeholder")
        # self.my_str.set(self.file)
        
        # Label for chosen reference sheet 
        self.f_lbl = tk.Label(self, textvariable="reference sheet loaded", bg='black', fg='lightgreen')
        self.f_lbl.grid(column=1, row=1, sticky='nse', padx=140)
        self.tk_headers = ['Mitigated', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]
        self.ipmit_headers = ['Mitigated', 'Whitelist', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]
        self.dom_headers = ["Mitigated", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]
        self.dommit_headers = ["Mitigate", "Whitelist", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]
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
        self.ip_btn = tk.Button(self, text="IP Mitigation") 
        self.ip_btn.bind("<Enter>", func=lambda e: self.ip_btn.config(background='#00FF00'))
        self.ip_btn.bind("<Leave>", func=lambda e: self.ip_btn.config(background='gray'))
        self.ip_btn.grid(column=1, row=6, sticky='ns', padx=600)
        self.ip_btn['command'] = self.clicked_ip
        # Domain Mitigation Search
        self.dom_btn = tk.Button(self, text="Domain Mitigation")
        self.dom_btn.bind("<Enter>", func=lambda e: self.dom_btn.config(background='#00FF00'))
        self.dom_btn.bind("<Leave>", func=lambda e: self.dom_btn.config(background='gray'))
        self.dom_btn['command'] = self.clicked_dom
        self.dom_btn.grid(column=1, row=8, sticky='ns', padx=500)
        #Update Reference Sheet Button
        self.update_btn = tk.Button(self, text="Update Reference Sheet")
        self.update_btn.bind("<Enter>", func=lambda e: self.update_btn.config(background='#00FF00'))
        self.update_btn.bind("<Leave>", func=lambda e: self.update_btn.config(background='gray'))
        self.update_btn['command'] = self.clicked_update
        self.update_btn.grid(column=1, row=13, sticky='ns', padx=500)
        self.update_dom_cache = {}
        self.update_ip_cache = {}
        self.dom_mit_res = []
        self.ip_mit_res = []
        #Upload Reference Sheet Button
        self.upload_btn = tk.Button(self, text='broken upload_file() button')
        self.upload_btn.bind("<Enter>", func=lambda e: self.upload_btn.config(background='#00FF00'))
        self.upload_btn.bind("<Leave>", func=lambda e: self.upload_btn.config(background='gray'))
        self.upload_btn['command'] = self.upload_file()
        self.upload_btn.grid(column=1, row=1, sticky='ns', padx=500)
        self.whitelist_btn = tk.Button(self, text='Check for whitelist')
        self.whitelist_btn.bind("<Enter>", func=lambda e: self.whitelist_btn.config(background='#00FF00'))
        self.whitelist_btn.bind("<Leave>", func=lambda e: self.whitelist_btn.config(background='gray'))
        self.whitelist_btn['command'] = self.whitelst_check
        self.whitelist_btn.grid(column=1, row=12, sticky='ns')
        self.whitelist_ip_cache = {}
        self.whitelist_dom_cache = {}
        
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
        self.sheet.set_sheet_data([[i for i in "mitigation"],
                                      [i for i in "ronin"]])
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
        self.sheet.grid(column=1, row=10, padx=30,pady=5, sticky="nswe")
        self.sheet.headers(newheaders = self.dom_headers)
       
        ############################### non-mitigated domains; add 
        self.sub_sheet = tksheet.Sheet(self, 
                                   show_table=True,
                                   expand_sheet_if_paste_too_big=True,
                                   show_header=True,
                                   width=900,
                                   align="c",
                                   all_columns_displayed=True,
                                   show_y_scrollbar=True)
        self.sub_sheet.set_sheet_data([[i for i in "mitigation"],
                                      [i for i in "ronin"]])
        self.sub_sheet.headers(newheaders=self.ipmit_headers)
        self.sub_sheet.create_header_checkbox(c=0,
                                              checked = False,
                                              check_function = self.sub_sheet.click_checkbox(r="all", 
                                                                                             c=0, 
                                                                                             checked=False),
                                              text = "Mitigate")
        self.sub_sheet.highlight_columns(columns=[0, 1], bg=None, fg="white", overwrite = True)
        self.sub_sheet.create_checkbox(c=0,
                                       r="all",
                                       checked = False,
                                       state = "normal",
                                       text = "Checkbox")
        self.sub_sheet.create_checkbox(c=1,
                                       r="all",
                                       checked = False,
                                       state = "normal",
                                       text = "Whitelist")
        
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
        self.sub_sheet.grid(column=1, row=11, padx=30, pady=5, sticky="nswe")
        
    def header_dropdown_selected(self, event = None):
        #breakpoint()
        hdrs = self.sheet.headers()
        # this function is run before header cell data is set by dropdown selection
        # so we have to get the new value from the event
        hdrs[event.column] = event.text
        #print(hdrs)
        if all(dd == "Block" for dd in hdrs):
            print([dd for dd in hdrs])
            self.sub_sheet.set_sheet_data([n for n in self.df_mit.values.tolist()],
                                      reset_col_positions = False,
                                      reset_row_positions = False)
        else:
            self.sub_sheet.set_sheet_data([row for row in [n for n in self.df_mit.values.tolist()] if all(row[c] == e or e == "Block" for c, e in enumerate(hdrs))],
                                      reset_col_positions = False,
                                      reset_row_positions = False)
        
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
        self.ip_ref_res = [i for i in self.ip_search().values.tolist()]
        self.ip_mit_res = [i for i in self.ip_mit.values.tolist()]
        
        self.sheet.set_sheet_data(self.ip_ref_res)
        self.sub_sheet.set_sheet_data(self.ip_mit_res)

        self.sheet.headers(newheaders = ['Mitigated', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.sub_sheet.headers(newheaders=['Mitigated', 'Whitelist', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.sub_sheet.create_checkbox(r="all",
                                       c=0,
                                       checked = False,
                                       text = "Checkbox")
        self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=False, check_function=self.check_all)
        self.sub_sheet.create_checkbox(r="all",
                                       c=1,
                                       checked=False,
                                       text="Whitelist")
        print(self.ip_mit_res)
        
    def clicked_dom(self):
        try:
            # pandas data has to be expressed as list of lists
            self.dom_ref_res = [d for d in self.dom_search().values.tolist()]
            self.dom_mit_res = [n for n in self.df_mit.values.tolist()]
            self.sheet.set_sheet_data(self.dom_ref_res)
            self.sub_sheet.set_sheet_data(self.dom_mit_res)
            ## I think I can create a function in the header checkbox to check all for the other boxes...
            self.sheet.headers(newheaders = self.dom_headers)
            self.sub_sheet.headers(newheaders = self.dommit_headers)
            self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=False, check_function=self.check_all)
            self.sub_sheet.create_checkbox(r="all",
                                           c=0,
                                           checked = False,
                                           text = "Checkbox")
            self.sub_sheet.create_checkbox(c=1,
                                           r="all",
                                           checked = False,
                                           state = "normal",
                                           text = "Whitelist")
            
            self.sub_sheet.create_header_dropdown(c=1,
                                                  values = ["Block", "Whitelist", "Unblock"],
                                                  set_value= "Whitelist",
                                                  selection_function= self.header_dropdown_selected)
            print(self.dom_mit_res)
            
        except:
            self.sheet.set_sheet_data([f"{d} returns no results" for d in self.dom_search.values.tolist()][0])
        #showinfo(title="testing",
        #         message="this is a test of the domain button")
        
    def clicked_update(self):
        self.uwu_it()
        today = date.today()
        save_date = today.strftime("%Y%m%d")
        self.update_dom_cache = {i[2]:i for i in self.dom_mit_res}
        print(self.update_dom_cache)
        self.update_ip_cache = {i[4]:i for i in self.ip_mit_res}
        print(self.update_ip_cache)
        #for x in update_btn_cache.items():
            
        # with pd.ExcelWriter(App.f) as writer:
        #     pd.DataFrame(self.sub_sheet.get_cell_data()).to_excel(writer, sheet_name=["BadBoyIPs"])
         # We need to use excelwriter here
        # append 
       # print(self.sub_sheet.get_sheet_data())
        #self.df_update = pd.concat([App.f, pd.DataFrame(self.sub_sheet.get_sheet_data())])
        #self.df_update.to_excel(f"References_{save_date}.xlsx") 
   

        ######################################  This seems to work ###############################
    def ip_search(self):
        #breakpoint()
        #input ip addresses
        ip_input = self.txt_ip.get("1.0","end-1c").splitlines() #split lines of input
        ip_input = [i.strip() for i in ip_input] # clean up in case of spaces
        for ip in ip_input:
            if ip_input[0] == "paste your IP's here: ":
                continue
            else:
                pass

        cidr_list = self.df1['CIDR'].tolist()
        mitigations = []
        self.unmitigated = []
        cidr_resp = []
        for cidr in cidr_list:
            for ip in ip_input:
                if ipaddress.ip_address(ip) in ipaddress.ip_interface(cidr).network and ip not in mitigations:
                    #print(f"{ip} is in {ipaddress.ip_interface(cidr).network}")
                    #print(ipaddress.ip_interface(cidr).network[0])
                    #print(ipaddress.ip_interface(cidr).network[-1])
                    cidr_resp.append(cidr)
                    mitigations.append(ip)
                    continue
                elif ip not in self.unmitigated:
                    self.unmitigated.append(ip)
                    continue
            
        self.unmitigated = [x for x in self.unmitigated if x not in mitigations]
        self.ip_mit = pd.DataFrame(columns=['Mitigated', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.ip_mit['CIDR'] = pd.Series(self.unmitigated, index=list(range(0, len(self.unmitigated))))
        self.ip_mit.insert(1, 'Whitelist', [i for i in list(range(0, len(self.unmitigated)))])
        self.df_ref = pd.DataFrame(columns=['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.df_ref = self.df1.loc[self.df1['CIDR'].isin(cidr_resp)]
        self.df_ref.insert(0, 'Mitigated', pd.Series(mitigations))

        return self.df_ref

        ########################### This is successful #########################

    def dom_search(self): 
        # create list from input box
        doms = self.txt_dom.get("1.0", "end-1c").splitlines()
        doms = [i.strip() for i in doms] # input validations
        #doms = [urlparse(i).netloc for i in doms] # This onlyworks if the domain is preceded by a //
        self.df_mit = pd.DataFrame(columns=['Mitigate', "Whitelist", 'Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
        
        try:
            #find matches in reference sheet that match self.doms
            dom_list = self.df5["Domain"].tolist()
            self.df_ref = self.df5.loc[self.df5["Domain"].isin(doms)]
            self.df_mit["Domain"] = [i for i in doms if i not in dom_list]
            self.df_ref.insert(0, "Mitigate", ["Mitigated" for i in range(len(self.df_ref.index))])
            return self.df_ref
        except:
            messagebox.showerror("Error", f"{[i for i in doms]} is not a valid domain.")
            
    def whitelst_check(self):
        print(self.dom_mit_res)
        print(self.ip_mit_res)
        self.whitelist_btn_cache = {i[2]:i for i in self.dom_mit_res}
        print(self.whitelist_btn_cache)
        #self.uwu_it()
        pass

    # Trying to write a function to tie to header checkbox
    def check_all(self, r="all", c=0, checked=True):
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
    
    





    









