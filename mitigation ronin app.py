# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:06:05 2022
@author: curtis.m.dufour
"""
import tkinter as tk
import tksheet
from re import search, sub
from tkinter import scrolledtext, ttk, messagebox, filedialog
import xlsxwriter
from openpyxl.utils import datetime as dt
from urllib.parse import urlparse
import pandas as pd
import ipaddress
from datetime import datetime
from datetime import date as date
import uwuify
import os

########Fixed the input of the file to the pandas df. Consequently broke the upload and f_lbl stuff. 
######## It also creates an empty tkinter frame upon opening the filedialog filename popup
######## Sorry if I don't get to fixing that anytime soon.
# TODO: update function
username = os.getlogin().title().split('.')[0]

class App(tk.Tk):
    
    file = filedialog.askopenfilename(filetypes =[("Excel Files", '*.xlsx')])
    f = pd.ExcelFile(file)
    df_dict = f.parse(sheet_name=[0, 1, 2, 3, 4, 5, 6]) # imports dictionary
    df1, df2, df3, df4, df5, df6, df7 = list(df_dict.values())
    # df2 is the whitelist
    # df3 is the army ip list
    # df6 is domain whitelist
    df1['First Binary'] = df1['First Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df1['Last Binary'] = df1['Last Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df1['Date Issued'] = df1['Date Issued'].apply(lambda x: datetime.strftime(dt.from_excel(x), "%d-%b-%Y"))
    #list(map(lambda i: datetime.strftime(dt.from_excel(int(i)), "%d-%b-%Y"), [i.strip() for i in dates.splitlines() if i != ''])))
    df2['First Binary'] = df2['First Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df2['Last Binary'] = df2['Last Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df2['Date Issued'] = df2['Date Issued'].apply(lambda x: datetime.strftime(dt.from_excel(x), "%d-%b-%Y"))
    df3['First Binary'] = df3['First Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df3['Last Binary'] = df3['Last Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df4['First Binary'] = df4['First Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df4['Last Binary'] = df4['Last Binary'].apply(lambda x: str(ipaddress.ip_address(x)))
    df5['Date Issued'] = df5['Date Issued'].apply(lambda x: datetime.strftime(dt.from_excel(x), "%d-%b-%Y"))
    df6['Date Issued'] = df6['Date Issued'].apply(lambda x: datetime.strftime(dt.from_excel(x), "%d-%b-%Y"))
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    def __init__(self):
        super().__init__()
         # Title and geometry
        self.title("Mitigation Ronin v47.py")
        self.config(bg='#242526')
        #label
        self.lbl = tk.Label(self, text=f"Welcome to Mitigation Ronin (v47), {username}!", 
                            font=('Arial', 14), 
                            bg='#050505', 
                            fg='lightgreen')
        self.lbl.grid(column=1, row=0, padx=10, pady=10, sticky='ns')
        # This is all broken
        self.my_str = tk.StringVar()
        self.my_str.set("placeholder")
        self.my_str.set(self.file)
        
        # Label for chosen reference sheet 
        self.f_lbl = tk.Label(self, text=f"Reference Sheet Version: {self.file}", bg='black', fg='limegreen')
        self.f_lbl.grid(column=1, row=1, sticky='nse', padx=200)
        
        self.ip_headers = ['Mitigated', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]
        self.ipwhite_headers = ['Mitigated', 'Whitelist', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes"]
        self.army_headers = ['First Binary', 'Last Binary', "CIDR", "NET NAME", "HANDLE", "REG DATE", "ORG HANDLE", "ORG NAME", "ORG CITY", "ORG STATE", "ORG ZIP"]
        self.dom_headers = ["Mitigated", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]
        self.domwhite_headers = ["Mitigate", "Whitelist", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]
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
        def change_file():
            self.file = filedialog.askopenfilename(filetypes =[("Excel Files", '*.xlsx')])
            self.my_str.set(self.file)
        self.upload_btn = tk.Button(self, text="Upload Reference", 
                                    command=change_file).grid(column=1, row=2, sticky="nsw")
        
        # IP Mitigation Search
        self.ip_btn = tk.Button(self, text="IP Mitigation") 
        self.ip_btn.bind("<Enter>", func=lambda e: self.ip_btn.config(background='#00FF00'))
        self.ip_btn.bind("<Leave>", func=lambda e: self.ip_btn.config(background='gray'))
        self.ip_btn.grid(column=1, row=6, sticky='nsw', padx=400)
        self.ip_btn['command'] = self.clicked_ip

        # Domain Mitigation Search
        self.dom_btn = tk.Button(self, text="Domain Mitigation")
        self.dom_btn.bind("<Enter>", func=lambda e: self.dom_btn.config(background='#00FF00'))
        self.dom_btn.bind("<Leave>", func=lambda e: self.dom_btn.config(background='gray'))
        self.dom_btn['command'] = self.clicked_dom
        self.dom_btn.grid(column=1, row=8, sticky='nsw', padx=400)
        #Update Reference Sheet Button
        self.update_btn = tk.Button(self, text="Update Reference Sheet")
        self.update_btn.bind("<Enter>", func=lambda e: self.update_btn.config(background='#00FF00'))
        self.update_btn.bind("<Leave>", func=lambda e: self.update_btn.config(background='gray'))
        self.update_btn['command'] = self.clicked_update
        self.update_btn.grid(column=1, row=13, sticky='ns', padx=500, pady=15)
        self.update_dom_cache = {}
        self.update_ip_cache = {}
        self.dom_mit_res = []
        self.ip_mit_res = []
        
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
        self.sheet.set_sheet_data([[i for i in "  mitigation"],
                                   [i for i in "     ronin"]])
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
        self.sub_sheet.set_sheet_data([[i for i in "  mitigation"],
                                      [i for i in "    ronin"]])
        self.sub_sheet.headers(newheaders=self.ip_headers)
        self.sub_sheet.create_header_checkbox(c=0,
                                              checked = False,
                                              check_function = self.sub_sheet.click_checkbox(r="all", 
                                                                                             c=0, 
                                                                                             checked=False),
                                              text = "Mitigate")
        self.sub_sheet.create_header_dropdown(c=1,
                                              values = ["Block", "Whitelist", "Unblock"],
                                              set_value= " ",
                                              selection_function= self.header_dropdown_selected)
        self.sub_sheet.highlight_columns(columns=[0, 1], bg=None, fg="white", overwrite = True)
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
        self.sub_sheet.grid(column=1, row=11, padx=30, pady=5, sticky="nswe")
        
        ######################################## TKSHEET Functions ########################################
        
    def header_dropdown_selected(self, event = None):
        dropdown_list = ['Block', 'Unblock', 'Whitelist']
        self.sub_sheet.create_dropdown(r="all",
                                       c=1,
                                       values=dropdown_list,
                                       set_value=None,# This is the one I need to fix
                                       state="readonly",
                                       redraw=True,
                                       selection_function=None)
    
    def check_all(self, r="all", c=0, checked=True):
        self.sub_sheet.create_checkbox(r="all",
                                       c=0,      
                                       checked=True, 
                                       redraw=True,
                                       text="selected")

    ########################################### Button Functions ############################
    def upload_file(self):
        #file = filedialog.askopenfilename(filetypes =[("Excel Files", '*.xlsx')])#, ("All Files"), ("*.*")])
        if self.file:
            self.my_str.set(self.file)
            return self.file
        else:
            messagebox.showerror("Error", "File not selected")
            print("File not chosen.")
            return "File not chosen"
        
        ############################## in process #######################################
        ##################################################################################
        
    def clicked_update(self):
        ip_df = pd.DataFrame(columns=['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]) 
        dom_df = pd.DataFrame(columns=['Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
        ip_df = ip_df.append(self.df1, ignore_index=False)
        dom_df = dom_df.append(self.df5, ignore_index=False)
        self.uwu_it()
        save_date = datetime.now().strftime("%Y%m%d")
        update_dom_cache = {f"Domain {i[2]}":i for i in self.dom_mit_res}
        update_ip_cache = {f"IP {i[4]}":i for i in self.ip_mit_res}
        update_dict = {**update_dom_cache, **update_ip_cache}
        doms = []
        ips = []
        domwhites = []
        ipwhites = []
        for k,v in update_dict.items():

            if search('Domain', k):
                if v[0]==True and v[1]=="Block":
                    # need to... create a df_block
                    doms.append(v[2:])
                    continue
                elif v[1]=="Whitelist":
                    domwhites.append(v[2:])
                    continue
                elif v[1]=="Unblock":
                    #print(dom_df.loc[dom_df['Domain']==v[2]])
                    dom_df.drop(dom_df.loc[dom_df['Domain']==v[2]].index, inplace=True)
                    continue
            elif search('IP', k):
                if v[0]==True and v[1]=="Block":
                    ips.append(v[2:])
                    continue
                elif v[0]==True and v[1]=="Whitelist":
                    ipwhites.append(v[2:])
                    continue
                elif v[1]=="Unblock":
                    ip_df.drop(ip_df.loc[ip_df['CIDR'] == v[4]].index, inplace=True)
                    continue
            else:
                messagebox.showinfo("No Results", message="Did you mean to press the update button?")
        domwhite_df = self.df6
        ipwhite_df = self.df2
        dom_df = dom_df.append(pd.DataFrame(doms, columns=['Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]), ignore_index=True)
        ip_df = ip_df.append(pd.DataFrame(ips, columns = ['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"]), ignore_index=True)
        domwhite_df = domwhite_df.append(pd.DataFrame(domwhites, columns=['Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"]), ignore_index=True)
        ipwhite_df = ipwhite_df.append(pd.DataFrame(ipwhites, columns=['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes"]), ignore_index=True)
        root = tk.Tk()
        root.geometry("500x500")
        root.pack_propagate(False)
        root.resizable( 0, 0)
        top = tk.Frame(root)
        bottom= tk.Frame(root)
        top.pack(side="top")
        bottom.pack(side="bottom")
        frame1 = tk.LabelFrame(root, text="IP Data")
        frame1.place(height=250, width=500)
        frame2 = tk.LabelFrame(root, text="Domain Data")
        frame2.place(height=250, width=500, rely=0.455, relx=0)
        root.title("Please Confirm Mitigation Updates")
        def onClick(): # update button command
            # Popup to tell you it's going to save it as this file
            tk.messagebox.askokcancel(title=f"References_{save_date}", message=f"Saving to References_{save_date}.xlsx")
            #updating the df's for the new excel file
            df1 = ip_df
            df1['First Binary'] = df1['First Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df1['Last Binary'] = df1['Last Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df1['Date Issued'] = df1['Date Issued'].apply(lambda x: (datetime.strptime(x, "%d-%b-%Y").date() - date(1899, 12, 30)).days)
            df2 = ipwhite_df
            df2['First Binary'] = df2['First Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df2['Last Binary'] = df2['Last Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df2['Date Issued'] = df2['Date Issued'].apply(lambda x: (datetime.strptime(x, "%d-%b-%Y").date() - date(1899, 12, 30)).days)
            df3 = self.df3
            df3['First Binary'] = df3['First Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df3['Last Binary'] = df3['Last Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df4 = self.df4
            df4['First Binary'] = df4['First Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df4['Last Binary'] = df4['Last Binary'].apply(lambda x: int(ipaddress.ip_address(x)))
            df5 = dom_df
            df5['Date Issued'] = df5['Date Issued'].apply(lambda x: (datetime.strptime(x, "%d-%b-%Y").date() - date(1899, 12, 30)).days)
            df6 = domwhite_df
            df6['Date Issued'] = df6['Date Issued'].apply(lambda x: (datetime.strptime(x, "%d-%b-%Y").date() - date(1899, 12, 30)).days)
            df7 = self.df7
            dflist = [df1, df2, df3, df4, df5, df6, df7] #pack them
            save_file = filedialog.asksaveasfilename(initialdir=self.file,
                                                     filetypes=[('Excel files', "*.xlsx")],
                                                     title=f"References_{save_date}.xlsx")
            excelwriter = pd.ExcelWriter(save_file, engine="xlsxwriter")
            for i, df in enumerate(dflist):
                df.to_excel(excelwriter, sheet_name="Sheet" + str(i+1), index=False)
            excelwriter.save()
            

        button = tk.Button(root, text="proceed with update?", command=onClick) # update button
        button.pack(in_=bottom, side="left")
        butt = tk.Button(root, text="cancel", command=root.destroy)
        butt.pack(in_=bottom, side="right")
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        treescrolly1= tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
        treescrollx1 = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx1.set, yscrollcommand=treescrolly1.set)
        treescrollx1.pack(side="bottom", fill="x")
        # known issue - the x scroll won't show on top frame
        treescrolly1.pack(side="right", fill="y")
        tv1['column'] = list(ip_df.columns)
        tv1['show'] = "headings"
        
        tv2 = ttk.Treeview(frame2)
        tv2.place(relheight=1, relwidth=1)
        treescrolly2= tk.Scrollbar(frame2, orient="vertical", command=tv2.yview)
        treescrollx2 = tk.Scrollbar(frame2, orient="horizontal", command=tv2.xview)
        tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
        treescrollx2.pack(side="bottom", fill="x")
        treescrolly2.pack(side="right", fill="y")
        
        tv1['column'] = list(ip_df.columns)
        tv1['show'] = "headings"
        tv2['column'] = list(dom_df.columns)
        tv2['show'] = "headings"
        
        for column in tv1['columns']:
            tv1.heading(column, text=column)
        
        ip_df_rows = ip_df.tail(len(self.ip_mit_res)).to_numpy().tolist()
        for row in ip_df_rows:
            tv1.insert("", "end", values=row)
            
        for column in tv2['columns']:
            tv2.heading(column, text=column)
            
        dom_df_rows = dom_df.tail(len(self.dom_mit_res)).to_numpy().tolist()
        for row in dom_df_rows:
            tv2.insert("", "end", values=row)
                        
        root.mainloop()

    
                    ##################################################################################
    def clicked_ip(self):
        # Data must be expressed as a list of lists...
        #print(self.ip_search().values.tolist()[0])
        self.uwu_it()
        self.ip_ref_res = [i for i in self.ip_search().values.tolist()]
        self.sheet.set_sheet_data(self.ip_ref_res)
        self.sheet.headers(newheaders = self.ip_headers)
        self.ip_mit_res = [i for i in self.ip_mit.values.tolist()]
        self.sub_sheet.set_sheet_data(self.ip_mit_res)
        self.sub_sheet.headers(newheaders=['Mitigated', 'Whitelist', 'First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=False, check_function=self.check_all)
        self.sub_sheet.create_dropdown(r="all",
                                       c=1,
                                       values=['Whitelist', 'Block', 'Unblock'],
                                       set_value=None,
                                       state="readonly",
                                       redraw=True,
                                       selection_function=None)
        
        
        
    def clicked_dom(self):
        try:
            # pandas data has to be expressed as list of lists
            self.dom_ref_res = [d for d in self.dom_search().values.tolist()]
            self.dom_mit_res = [n for n in self.df_mit.values.tolist()]
            self.sheet.set_sheet_data(self.dom_ref_res)
            self.sub_sheet.set_sheet_data(self.dom_mit_res)
            ## I think I can create a function in the header checkbox to check all for the other boxes...
            self.sheet.headers(newheaders = ["Mitigated", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
            self.sub_sheet.headers(newheaders = ["Mitigated", "Block", "Domain", "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
            self.sub_sheet.create_header_checkbox(c=0, text="Mitigate", checked=False, check_function=self.check_all)
            self.sub_sheet.create_checkbox(r="all",
                                           c=0,
                                           checked = False,
                                           text = "Checkbox")
            self.sub_sheet.create_dropdown(r="all",
                                       c=1,
                                       values=['Whitelist', 'Block', 'Unblock'],
                                       set_value="Action",
                                       state="readonly",
                                       redraw=True,
                                       selection_function=None)
            
            self.sub_sheet.create_header_dropdown(c=1,
                                                  values = ["Block", "Whitelist", "Unblock"],
                                                  set_value= " ",
                                                  selection_function= self.header_dropdown_selected)
        except:
            messagebox.showinfo("No Results", message="No results were found in the domain search. ")
            #self.sheet.set_sheet_data([f"{d} returns no results" for d in self.dom_search.values.tolist()][0])
        
        ######################################  This seems to work ###############################
    def ip_search(self):
        #input ip addresses
        ip_input = self.txt_ip.get("1.0","end-1c").splitlines() #split lines of input
        ip_input = [i.strip() for i in ip_input if i.strip() != ""] # clean up in case of spaces
        ip_input = [sub(r'[\[\]]', "", ip) for ip in ip_input]
        for ip in ip_input:
            if ip_input[0] == "paste your IP's here: ":
                continue
            else:
                pass
        cidr_list = self.df1['CIDR'].tolist()# badguys IP's
        white_list = self.df2['CIDR'].tolist() # Whitelist IP's
        army_list = self.df3['CIDR'].tolist() #Army IP's
        res_list = self.df4['CIDR'].tolist()
        #print(len(cidr_list))
        mitigations = []
        unmitigated = []
        cidr_resp = []
        for cidr in cidr_list: # This iterates through to check ip in each cidr range
            for ip in ip_input:
                if ipaddress.ip_address(ip) in ipaddress.ip_interface(cidr).network and ip not in mitigations:
                    cidr_resp.append(cidr) # the CIDRs from our IP block list
                    mitigations.append(ip)  # moving the ip_input to mitigations if it's a match
                    continue
                elif ip not in unmitigated:
                    unmitigated.append(ip) #moving ip_input to unmitigated if not a match
                    continue
        unmitigated = [x for x in unmitigated if x not in mitigations] # grabs ones not in the mitigation list already
        mbox = f"Kawaii~! {len(unmitigated)} unmitigated IP's found! I'm checking the whitelist now, {username} sempai!"
        flags = uwuify.SMILEY | uwuify.YU
        messagebox.askokcancel(title='Results', message=uwuify.uwu(mbox, flags=flags))
        for cidr in white_list:
            for ip in unmitigated:
                if ipaddress.ip_address(ip) in ipaddress.ip_interface(cidr).network and ip not in mitigations:
                    cidr_resp.append(cidr)
                    mitigations.append(ip)
                    continue
                elif ip not in unmitigated:
                    unmitigated.append(ip)
        for cidr in army_list:
            for ip  in unmitigated:
                if ipaddress.ip_address(ip) in ipaddress.ip_interface(cidr).network and ip not in mitigations:
                    cidr_resp.append(cidr)
                    mitigations.append(ip)
                    continue
                elif ip not in unmitigated:
                    unmitigated.append(ip)
        for cidr in res_list:
            for ip  in unmitigated:
                if ipaddress.ip_address(ip) in ipaddress.ip_interface(cidr).network and ip not in mitigations:
                    cidr_resp.append(cidr)
                    mitigations.append(ip)
                    continue
                elif ip not in unmitigated:
                    unmitigated.append(ip)
        
        unmitigated = [x for x in unmitigated if x not in mitigations]

        self.ip_mit = pd.DataFrame(columns=['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"])
        self.ip_mit['CIDR'] = pd.Series(unmitigated, index=list(range(0, len(unmitigated))), dtype='object')
        self.ip_mit.insert(1, 'Block', [i for i in list(range(0, len(unmitigated)))])
        self.ip_mit.fillna('', inplace=True)
        df_ref = pd.DataFrame(columns=['First Binary', "Last Binary", "CIDR", "Task Order", "Date Issued", "EvalReason","Threat Report", "Comments", "Notes", "Scope"], dtype='object')
        df_ref = self.df1.loc[self.df1['CIDR'].isin(cidr_resp)]
        df_ref = df_ref.append(self.df2.loc[self.df2['CIDR'].isin(cidr_resp)])
        df_ref = df_ref.append(self.df3.loc[self.df3['CIDR'].isin(cidr_resp)])
        df_ref = df_ref.append(self.df4.loc[self.df4['CIDR'].isin(cidr_resp)])
        df_ref.insert(0, 'Mitigated', mitigations) # Adds mitigated IP's to df_ref for clicked_ips func
        df_ref.fillna('', inplace=True)
        return df_ref

    def dom_search(self): 
        doms = self.txt_dom.get("1.0", "end-1c").splitlines()
        doms = [url.replace('www.', '') for url in doms]
        doms = [sub(r"[\[\]]+", "", url) for url in doms]
        doms = [str(urlparse(url).hostname) if urlparse(url).hostname !=None else url for url in doms]
        doms = [i.strip() for i in doms] # input validations
        self.df_mit = pd.DataFrame(columns=['Mitigate', "Whitelist", 'Domain', "Task Order", "Date Issued", "Threat Report", "Comments", "Notes"])
        
        try:
            #find matches in reference sheet that match self.doms
            dom_list = self.df5["Domain"].tolist() # badboy IP's
            white_list = self.df6['Domain'].tolist()
            mitigations = [i for i in doms if i not in dom_list]
            mitigations = [i for i in mitigations if i not in white_list] # I don't think this is right
            self.df_mit['Domain'] = [i for i in mitigations]
            self.df_mit.fillna('', inplace=True)
            df_ref = self.df5.loc[self.df5["Domain"].isin(doms)]
            mbox = f"Mitigation Ronin found {len(self.df_mit['Domain'].tolist())} unmitigated domains! Checking the whitelist now, senpai!~"
            flags = uwuify.SMILEY | uwuify.YU
            resp = uwuify.uwu(mbox, flags=flags)
            messagebox.askokcancel(title='Test', message=resp)
            df_ref = df_ref.append(self.df6.loc[self.df6["Domain"].isin(doms)])
            df_ref.insert(0, "Mitigate", ["Mitigated" for i in range(len(df_ref.index))])
            df_ref.fillna('', inplace=True)
            return df_ref
        except:
            messagebox.showerror("Error", f"{[i for i in doms]} is not a valid domain.")

    # Trying to write a function to tie to header checkbox
    def uwu_it(self):
        flags = uwuify.SMILEY | uwuify.YU
        resp = uwuify.uwu(self.lbl['text'], flags=flags)
        self.lbl["text"] = resp

if __name__ == "__main__":
    app = App()
    app.mainloop()
