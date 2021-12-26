import tkinter
from tkinter import *
from tkinter import Tk, Button, Label, ttk, messagebox, filedialog
import os
import glob
import shutil
import sys
import pkg_resources
import webbrowser
required = {'opencv-python-headless'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
missingset=[*missing,]
if missing:
    res2=messagebox.askquestion("Module not found!","Opencv is not installed, do you want to download it now?")
    if res2=="yes":
        for x in range(len(missingset)):
            y=missingset[x]
            os.system('python -m pip install '+y)
        import cv2
    elif res2=="no":
        messagebox.showerror("Error Opening the program","Required modules not available! \nWithout the modules you can't use this program. Please install them first!")
        sys.exit()
else:
    import cv2
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def openfile():
    global folder, path2
    folder=tkinter.filedialog.askdirectory()
    if(len(folder)>=1):
        Img['text']='OPEN AGAIN'
        Img['bg']='#D0CECE'
        path2 = os.path.dirname(folder)
    else:
        print(folder)
        Img['text']='OPEN'
        Img['bg']="#82CC6C"
def Convert():
    try:
        if (Img['text']=='OPEN AGAIN'):
            def Extract():
                Disabled()
                try:
                    Log.place(x=165,y=160)
                    Log.config(text="Converting...")
                    root.update_idletasks()
                    firstitem=os.listdir(folder+"/")[0]
                    ext=(os.path.basename(firstitem).split('.')[1])
                    img = cv2.imread(folder+"/"+firstitem)
                    frameSize = (img.shape)[1::-1]
                    fps=int(exportbox.get())
                    out = cv2.VideoWriter(final,cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)
                    for filename in glob.glob(folder+"/*."+ext):
                        img = cv2.imread(filename)
                        out.write(img)
                    out.release()
                    Log.config(text="Converted!")
                    root.update_idletasks()
                    Enabled()
                    messagebox.showinfo("DONE", "Video Created! \nPlease check in-"+path2)
                    Log.place_forget()
                except:
                   Enabled()
                   Log.place_forget()
            exs=exportbox2.get()
            final=folder+"."+exs
            if os.path.exists(final):
                res=messagebox.askquestion("Warning!","Do you want to replace the file with the new one? \n(Process not reversible!)")
                if res=='yes':
                    os.remove(final)
                    Extract()         
                elif res=='no':
                    return()
            else:
                Extract()
        else:
            messagebox.showwarning("OOPS", "Please choose the folder first!")
    except:
        Enabled()
        Log.place_forget()
        messagebox.showwarning("OOPS", "Please choose the folder again!")
def Disabled():
    btn['state']=DISABLED
    exportbox['state']=DISABLED
    Img['state']=DISABLED
    switchbtn['state']=DISABLED
    exportbox2['state']=DISABLED
    infobtn['state']=DISABLED
    btn['cursor']='watch'
def Enabled():
    btn['state']=NORMAL
    exportbox['state']=NORMAL
    Img['state']=NORMAL
    switchbtn['state']=NORMAL
    exportbox2['state']=NORMAL
    infobtn['state']=NORMAL
    btn['cursor']=''
def info():
    messagebox.showinfo("Help",
    "This program can convert image sequence to video files. \nHow To Use?"
    "\n➤Click the OPEN button and choose your video file"
    "\n➤Then choose the FPS and export format"
    "\n➤Then simply click the CONVERT button, the video will be saved in the same root diretory"
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you have any issue then contact me on Github."
    "\nVersion-1.0")
def switch():
    ch="Vdo-to-Img.py"
    root.destroy()
    os.system('"%s"' % ch)
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Vdo-Img-Tools")
root= Tk()
root.title("Vdo & Img Tools")
root.resizable(width=False, height=False)
path=resource_path0("Programicon.ico")
root.wm_iconbitmap(path)
root.geometry("400x200")
root.columnconfigure(0,weight=1)
root.configure(bg='#FFFFFF')
Label(root, text="IMG TO VDO CONVERTER", font=("Impact",17),bd=0, fg="#5DBCD2", bg="#FFFFFF").grid()
Label(root, text="Choose Folder", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").grid()
Img=Button(root, width=20,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="OPEN",relief="groove", command=openfile)
Img.grid()
Label(root, text="Choose FPS", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").place(x=100,y=73)
Label(root, text="Choose Format", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").place(x=210,y=73)
exportchoices=["24","30","60"]
exportformats=["mp4","avi","mov","mkv","wmv"]
exportbox=ttk.Combobox(root,values=exportchoices, font="Verdana 10", width=8)
exportbox.current(0)
exportbox.place(x=95,y=93)
exportbox2=ttk.Combobox(root,values=exportformats, font="Verdana 10", width=8)
exportbox2.current(0)
exportbox2.place(x=210,y=93)
btn=Button(width=25, height=2,text="CONVERT",font=("Cambria", 10),bg="#5DBCD2",fg="#FFFFFF",borderwidth=0,highlightthickness=2,padx=0,pady=0,command=Convert)
btn.place(x=107,y=122)
Log=Label(root,text="", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF")
infobtn= Button(root, width=2,bg="#FFFFFF",fg="black", text="ⓘ",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=info)
infobtn.place(x=377,y=175)
switchbtn= Button(root, width=2,bg="#FFFFFF",fg="black", text="🔃",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=switch)
switchbtn.place(x=377,y=0)
dev=Label(root, text='Developed by Akascape | ',bg='#FFFFFF',fg="#6D76CD", font=("Impact",10))
dev.place(x=5,y=180)
link=Label(root, text="Github Link",font=('Impact',10),bg='#FFFFFF',fg="#6D76CD", cursor="hand2")
link.place(x=140,y=180)
link.bind("<Button-1>", lambda e:
callback("https://github.com/Akascape/Vdo-Img-Tools"))
root.mainloop()
