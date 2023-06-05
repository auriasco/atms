import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
from tkinter import *

# To get the space above for message
from tkinter.messagebox import *

# To get the dialog box to open when required
from tkinter.filedialog import *
def cut():
    textPad.event_generate("<<Cut>>")
def copy():
    textPad.event_generate("<<Copy>>")
def paste():
    textPad.event_generate("<<Paste>>")
def redo():
    textPad.event_generate("<<Redo>>")
def undo():
    textPad.event_generate("<<Undo>>")
def select_all():
    textPad.tag_add('sel','1.0','end')
def search_for(needle,cssntv,textPad,t2,e):
    textPad.tag_remove('match','1.0',END)
    count=0
    if needle:
        pos = '1.0'
        while True:
            pos = textPad.search(needle,pos,nocase=cssntv,stopindex=END)
            if not pos: break
            lastpos= '%s+%dc' %(pos,len(needle))
            textPad.tag_add('match',pos,lastpos)
            count += 1
            pos = lastpos
            
    textPad.tag_config('match',foreground='red',background='yellow')
    e.focus_set()
    t2.title('%d matches found' %count)
def find_text():
    t2 = Toplevel(w)
    t2.title('Find')
    t2.geometry('262x65+200+250')
    t2.transient(w)
    Label(t2,text="Find All:").grid(row=0,column=0,sticky='e')
    v=StringVar()
    e=Entry(t2,width=25,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    e.focus_set()
    c=IntVar()
    Checkbutton(t2,text='Ignore Case',variable=c).grid(row=1,column=1,sticky='e',padx=2,pady=2)
    Button(t2,text="Find All",underline=0,command=lambda:search_for(v.get(),c.get(),textPad,t2,e)).grid(row=0,column=2,sticky='e'+'w',padx=2,pady=2)
def close_search():
    textPad.tag_remove('match','1.0',END)
    t2.destroy()
def open_file():
    global filename
    filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if filename== "": 
        filename = None
    else:
        w.title(os.path.basename(filename)+" - pyPad")
        #return basename of file
        textPad.delete(1.0,END)
        fh = open(filename,"r")
        textPad.insert(1.0,fh.read())
        fh.close()
def save_as():
    try:
        f = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt',filetypes=[("All Files","*.*"),("Text Documents","*.txt*")])
        fh = open(f,'w')
        textoutput = textPad.get(1.0,END)
        fh.write(textoutput)
        fh.close()
        w.title(os.path.basename(f)+" - pyPad")
    except:
        pass
def save():
    global filename
    try:
        f=open(filename,'w')
        letter = textPad.get(1.0,'end')
        f.write(letter)
        f.close()
    except:
        save_as()
def new_file():
    w.title("Untitled")
    global filename
    filename = None
    textPad.delete(1.0,END)
def about(event=None):
    messagebox.showinfo("About","Tkinter GUI Application\nAutomatic Time Management System")
def help_box(event=None):
    messagebox.showinfo("Help","For help refer to book:\nATMS\n")
def exit_editor(event=None):
    if messagebox.askokcancel("Quit","Do you really want to quit?"):
        w.destroy()
def update_line_number(event=None):
    txt = ''
    if showIn.get():
        endline,endcolumn = textPad.index('end-1c').split('.')
        txt  = '\n'.join(map(str,range(1,int(endline))))
    Inlabel.config(text=txt,anchor='nw')
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s' %(currline,curcolumn))
def highlight_line(interval=100):
    textPad.tag_remove("active_line",1.0,"end")
    textPad.tag_add("active_line","insert linestart","insertlineend+1c")
    textPad.after(interval,toggle_highlight)
def undo_highlight():
    textPad.tag_remove("active_line",1.0,"end")
def toggle_highlight(event=None):
    val = hltIn.get()
    undo_highlight() if not val else highlight_line()
def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO,fill=None,side=RIGHT,anchor='se')
    elif not val:
        infobar.pack_forget()
def theme():
    global bgc,fgc
    val = themechoice.get()
    clrs = clrschms.get(val)
    fgc, bgc = clrs.split('.')
    fgc, bgc = '#'+fgc, '#'+bgc
    textPad.config(bg=bgc,fg=fgc)
def popup(event):
    cmenu.tk_popup(event.x_root,event.y_root,0)
# Add controls(widget)
w = Tk()
menubar = Menu(w)

#menubar.add_command(label="File",accelerator='Ctrl + E',compound=LEFT)
w.config(menu=menubar)
filemenu = Menu(menubar)
editmenu = Menu(menubar)
viewmenu = Menu(menubar)
aboutmenu = Menu(menubar)

#file menu
filemenu.add_command(label='New',command=new_file)
filemenu.add_command(label='Save',command=save,accelerator='Ctrl+S')
filemenu.add_command(label='Save as',command=save_as,accelerator='Ctrl+Shift+S')
filemenu.add_command(label='Open',accelerator='Ctrl+O',compound=LEFT,underline=0,command=open_file)
exit_command = filemenu.add_command(label='Exit',command=exit_editor)
w.protocol('WM_DELETE_WINDOW',exit_command)

menubar.add_cascade(label ='File',menu = filemenu, accelerator='Ctrl+S',underline=0)
#edit menu
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',compound=LEFT,command=undo)
editmenu.add_command(label='Redo',accelerator='Ctrl+Y',command=redo)
editmenu.add_command(label='Cut',command=cut)
editmenu.add_command(label='Copy',command=copy)
editmenu.add_command(label='Paste',command=paste)
editmenu.add_command(label='Find',command=find_text)
editmenu.add_command(label='Select All',command=select_all)
menubar.add_cascade(label='Edit',menu=editmenu,accelerator='Ctrl+E')
#view menu
#viewmenu.add_command(label='Show Line Number')
showIn = IntVar()
hltIn = IntVar()
showinbar = IntVar()
showIn.set(1)
showinbar.set(0)
viewmenu.add_radiobutton(label='Show Line Number',variable=showIn,command=update_line_number)
viewmenu.add_radiobutton(label='Show Info Bar at Bottom',variable=showinbar,command=show_info_bar)
viewmenu.add_checkbutton(label='Highlight Current Line',onvalue=1,offvalue=0,variable=hltIn,command=toggle_highlight)
#theme menu
thememenu = Menu(viewmenu)

clrschms = {
    '1. Default White': '000000.FFFFFF',
    '2. Greygarious Grey': '83406A.D1D4D1',
    '3. Lovely Lavender': '202B4B.E1E1FF',
    '4. Aquamarine': '5B8340.D1E7E0',
    '5. Bold Beige': '4B4620.FFF0E1',
    '6. Cobalt Blue': 'ffffBB.3333aa',
    '7. Olive Green': 'D1E7E0.5B8340',
}
themechoice = StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    thememenu.add_radiobutton(label=k,variable=themechoice,command=theme)
viewmenu.add_cascade(label="Themes",menu=thememenu)
menubar.add_cascade(label="View",menu=viewmenu)

aboutmenu = Menu(menubar)
aboutmenu.add_command(label='About',command=about)
aboutmenu.add_command(label='Help',command=help)
menubar.add_cascade(label='About',menu=aboutmenu)



shortcutbar = Frame(w, height=25, bg = 'light sea green')
icon_d = {'command':'filepath'}
icons = ['new_file','open_file','save','cut','copy','paste','undo','redo','find_text']
for i in icons:
    icon_d[i] ="atmsM\icons\h"+i+".gif"
    #print(icon_d[i])
for i,icon in enumerate(icons):
    #tbicon=PhotoImage(file='icons/'+icon+'.png')
    #tbicon = PhotoImage(file='atmsM\icons\copy.gif')
    tbicon = PhotoImage(file='atmsM\icons\h'+icons[i]+'.gif')
    cmd = eval(icon)
    toolbar = Button(shortcutbar,image=tbicon,command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO,fill=X)

shortcutbar.pack(expand=NO,fill=X)
Inlabel = Label(w, width=2, height = 10, bg = 'antique white')
Inlabel.pack(side=LEFT,anchor='nw',fill=Y)




textPad = Text(w,undo=True)
textPad.bind("<Any-KeyPress>",update_line_number)
textPad.bind('<Control-N>',new_file)
textPad.bind('<Control-n>',new_file)
textPad.bind('<Control-O>',open_file)
textPad.bind('<Control-o>',open_file)
textPad.bind('<Control-S>',save)
textPad.bind('<Control-s>',save)
textPad.bind('<Control-A>',select_all)
textPad.bind('<Control-f>',find_text)
textPad.bind('<Control-F>',find_text)
textPad.bind('<KeyPress-F1>', help_box)
textPad.bind("<Button-3>",popup)
textPad.pack(expand=YES, fill=BOTH)
cmenu = Menu(textPad)
for i in ('cut','copy','paste','undo','redo'):
    cmd = eval(i)
    cmenu.add_command(label=i,compound=LEFT,command=cmd)
    
cmenu.add_separator() 
cmenu.add_command(label='Select All',underline=7,command=select_all)
scroll=Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT,fill=Y)
infobar = Label(textPad,text='Line: 1 | Column: 0')
infobar.pack(expand=NO,fill=None,side=RIGHT,anchor='se')
w.config(menu=menubar)
#w.iconbitmap('icons/pypad.ico')
w.mainloop()