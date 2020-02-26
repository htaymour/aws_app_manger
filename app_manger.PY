from os import path
import time
from six.moves import configparser
from aws_conn import *
from tkinter import *
import yaml
import system



bucket_names()
get_bucket()


def move(move_type):
    status = ''
    global leb
    if move_type == "prod_beta":
        for f in list_prod.curselection():
            source_file_name = 'apps/prod/' + list_prod.get(f)
            dest_file_name = 'apps/beta/' + list_prod.get(f)
            status = move_to_dir(source_file_name, dest_file_name)
    if move_type == "beta_prod":
        for f in list_beta.curselection():
            source_file_name = 'apps/beta/' + list_beta.get(f)
            dest_file_name = 'apps/prod/' + list_beta.get(f)
            status = move_to_dir(source_file_name, dest_file_name)         
    if move_type == "alpha_beta":
        for f in list_alpha.curselection():
            source_file_name = 'apps/alpha/' + list_alpha.get(f)
            dest_file_name = 'apps/beta/' + list_alpha.get(f)
            status = move_to_dir(source_file_name, dest_file_name)
    if move_type == "beta_alpha":
        for f in list_beta.curselection():
            source_file_name = 'apps/beta/' + list_beta.get(f)
            dest_file_name = 'apps/alpha/' + list_beta.get(f)
            status = move_to_dir(source_file_name, dest_file_name)
    if leb !='': leb.distroy()                 
    leb = Label(gui,fg = "gray", text=status+'             ',bg='dodgerblue4')
    leb.place (x= 10 , y = 575)
    time.sleep(3)
    refresh()


def refresh():
    global file_dict
    status = get_yaml()
    file_dict = list_dict_files()
    Label(gui,fg = "gray", text=status+'             ',bg='dodgerblue4').place (x= 10 , y = 590)
    ###########################
    file_list = list_app_files('apps/prod/')
    list_prod.delete(0,END)
    for x in file_list:
        f = x.replace('apps/prod/','')
        if f != '':list_prod.insert(END, f)
    ###########################
    file_list = list_app_files('apps/alpha/')
    list_alpha.delete(0,END)
    for x in file_list:
        f = x.replace('apps/alpha/','')
        if f != '':list_alpha.insert(END, f)
    ###########################
    file_list = list_app_files('apps/beta/')
    list_beta.delete(0,END)
    for x in file_list:
        f = x.replace('apps/beta/','')
        if f != '': list_beta.insert(END,f)

def refresh_mytest():
    global file_dict
    status = get_yaml()
    file_dict = list_dict_files()
    Label(gui,fg = "gray", text=status+'             ',bg='dodgerblue4').place (x= 10 , y = 590)
    ###########################
    file_list = list_files('apps/prod/')
    list_prod.delete(0,END)
    for x in file_list:
        f = x.replace('apps/prod/','')
        if f != '':list_prod.insert(END, f)
    ###########################
    file_list = list_files('apps/alpha/')
    list_alpha.delete(0,END)
    for x in file_list:
        f = x.replace('apps/alpha/','')
        if f != '':list_alpha.insert(END, f)
    ###########################
    file_list = list_files('apps/beta/')
    list_beta.delete(0,END)
    for x in file_list:
        f = x.replace('apps/beta/','')
        if f != '': list_beta.insert(END,f)

def app_info(app_key):
    global frame_info
    global file_dict
    try:
        frame_info.destroy()
    except:
        pass
    frame_info = Frame(gui)
    frame_info = Frame(gui,width=150, height=500,bg='dodgerblue4')
    frame_info.place(x = 10, y = 500 ,width=370, height=70)
    for f in file_dict['apps']:
        if f['filename'] == app_key:
            appinfo = Label(frame_info,fg = 'cadet blue1', text="Package Name        : " + f['filename'],bg='gray')
            appinfo1 = Label(frame_info,fg = 'cadet blue1', text="Version Name       : " + f['version_name'],bg='gray')
            appinfo2 = Label(frame_info,fg = 'cadet blue1', text="Compatible Products: " + ','.join(f['compatible_products']),bg='gray')
            appinfo.place (x= 10 , y = 10)
            appinfo1.place (x= 10 , y = 30)
            appinfo2.place (x= 10 , y = 50)


def beta_select(evt):
    w = evt.widget
    if len(list_beta.curselection()) > 0:
        f = list_beta.curselection()[-1]
        app_info("apps/beta/" + list_beta.get(f))

def prod_select(evt):
    w = evt.widget
    if len(list_prod.curselection()) > 0:
        f = list_prod.curselection()[-1]
        app_info("apps/prod/"+str(list_prod.get(f)))

def alpha_select(evt):
    w = evt.widget
    if len(list_alpha.curselection()) > 0:
        f = list_alpha.curselection()[-1]
        app_info("apps/alpha/"+list_alpha.get(f))
        

file_dict = {}
leb = ''
frameinfo = ''
gui = Tk()
#gui.resizable(width=False, height=False)
gui.geometry("600x630")
gui.title("Easy APPs Manger")
gui.configure(background='dodgerblue4')
Label(gui,fg = "yellow", text="Production apps                                         Beta apps                                                    Alpha apps",bg='dodgerblue4').place (x= 10 , y = 0)
#frame_Prod = Frame(gui)
#frame_Prod = Frame(gui,width=150, height=500,bd=1, relief=SUNKEN)
#frame_Prod.place(x = 10, y = 30 ,width=150, height=500)
#frame_alpha = Frame(gui)
#frame_alpha = Frame(gui,width=150, height=500,bd=1, relief=SUNKEN)
#frame_alpha.place(x = 220, y = 30 ,width=150, height=500)
#frame_beta = Frame(gui)
#frame_beta = Frame(gui,width=150, height=500,bd=1, relief=SUNKEN)
#frame_beta.place(x = 430, y = 30 ,width=150, height=500)

list_prod = Listbox(gui, width=27, height=30,selectmode = MULTIPLE , font=("Helvetica", 8))
list_prod.place(x=10,y=20)
list_prod.bind('<<ListboxSelect>>', prod_select)
scrollbar_prod = Scrollbar(list_prod, orient="vertical")
scrollbar_prod.config(command=list_prod.yview)
scrollbar_prod.place(x=145,y = 0,height = 510)
list_prod.config(yscrollcommand=scrollbar_prod.set)

list_beta = Listbox(gui, width=27, height=30,selectmode = MULTIPLE, font=("Helvetica", 8))
list_beta.place(x=220,y=20)
list_beta.bind('<<ListboxSelect>>', beta_select)	
scrollbar_beta = Scrollbar(list_beta, orient="vertical")
scrollbar_beta.config(command=list_beta.yview)
scrollbar_beta.place(x=145,y = 0,height = 510)
list_beta.config(yscrollcommand=scrollbar_beta.set)

list_alpha = Listbox(gui, width=27, height=30,selectmode = MULTIPLE, font=("Helvetica", 8))
list_alpha.place(x=430,y=20)
list_alpha.bind('<<ListboxSelect>>', alpha_select)	
scrollbar_alpha = Scrollbar(list_alpha, orient="vertical")
scrollbar_alpha.config(command=list_alpha.yview)
scrollbar_alpha.place(x=145,y = 0,height = 510)
list_alpha.config(yscrollcommand=scrollbar_alpha.set)


btn_prod_beta = Button(gui, text=">", font = ('Sans','20','bold'),height = 1, width = 1 ,command=lambda: move('prod_beta'))
btn_prod_beta.place(x= 185, y = 170)
btn_beta_prod = Button(gui, text="<", font = ('Sans','20','bold'),height = 1, width = 1 ,command=lambda: move('beta_prod'))
btn_beta_prod.place(x= 185, y = 230)

btn_alfa_beta = Button(gui, text=">", font = ('Sans','20','bold'),height = 1, width = 1 ,command=lambda: move('beta_alpha'))
btn_alfa_beta.place(x= 395, y = 170)
btn_beta_alfa = Button(gui, text="<", font = ('Sans','20','bold'),height = 1, width = 1 ,command=lambda: move('alpha_beta'))
btn_beta_alfa.place(x= 395, y = 230)

btn_refresh = Button(gui, text="Refresh", font = ('Sans','10','bold'),height = 1, width = 8 ,command=lambda: refresh())
btn_refresh.place(x= 520, y = 492)

refresh()
gui.mainloop()
