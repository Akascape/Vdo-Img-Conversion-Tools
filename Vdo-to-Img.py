import tkinter
from tkinter import *
from tkinter import Tk, Button, Label, ttk, messagebox, filedialog
import os
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
    global file, folder, Common
    file=tkinter.filedialog.askopenfilename(filetypes =[('MP4', '*.mp4'),('All Files', '*.*')])
    if(len(file)>=1):
        Vdo['text']='OPEN AGAIN'
        Vdo['bg']='#D0CECE'
        Common=(os.path.basename(file).split('.')[0])
        path1=os.path.dirname(file)
        folder=path1+"/"+Common+"-Image sequence"
    else:
        Vdo['text']='OPEN'
        Vdo['bg']="#82CC6C"
def Convert():
    try:
        if (Vdo['text']=='OPEN AGAIN'):
            def Extract():
                Disabled()
                try:
                    cam = cv2.VideoCapture(file)
                    currentframe = 0
                    os.mkdir(folder)
                    while(True):
                        ret,frame = cam.read()
                        if ret:
                            targetformat=exportbox.get()
                            if currentframe<10:
                                name = folder+'/Frame-' + "0" + str(currentframe) + "." + targetformat
                            else:
                                name = folder+'/Frame-' + str(currentframe) + "." + targetformat
                            Log.place(x=140,y=160)
                            Log.config(text="Extracted: Frame-" + str(currentframe))
                            root.update_idletasks()
                            cv2.imwrite(name, frame)
                            currentframe += 1
                        else:
                            break
                    cam.release()
                    Enabled()
                    messagebox.showinfo("DONE", "Frames extracted! \nPlease check the folder-"+folder)
                    Log.place_forget()
                except:
                    Enabled()
                    Log.place_forget()
                    os.rmdir(Common+"-Image sequence")
            if os.path.isdir(folder):
                res=messagebox.askquestion("Warning!","Do you want to replace the folder with the new one? \n(Process not reversible!)")
                if res=='yes':
                    shutil.rmtree(folder)
                    Extract()         
                elif res=='no':
                    return()
            else:
                Extract()
        else:
            messagebox.showwarning("OOPS", "Please choose the video file first!")
    except:
       Enabled()
       Log.place_forget()
       messagebox.showwarning("OOPS", "Please choose the video file again!")
def Disabled():
    btn['state']=DISABLED
    exportbox['state']=DISABLED
    Vdo['state']=DISABLED
    switchbtn['state']=DISABLED
    infobtn['state']=DISABLED
    btn['cursor']='watch'
def Enabled():
    btn['state']=NORMAL
    exportbox['state']=NORMAL
    Vdo['state']=NORMAL
    switchbtn['state']=NORMAL
    infobtn['state']=NORMAL
    btn['cursor']=''
def info():
    messagebox.showinfo("Help",
    "This program can extract image sequence from video files. \nHow To Use?"
    "\n➤Click the OPEN button and choose your video file"
    "\n➤Then choose the export format"
    "\n➤Then simply click the EXTRACT button, all your frames will be saved in a new folder with the same video name and location"
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you have any issue then contact me on Github."
    "\nVersion-1.0")
def switch():
    ch="Img-to-Vdo.py"
    root.destroy()
    os.system('"%s"' % ch)
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Vdo-Img-Tools")
root= Tk()
root.title("Vdo & Img Tools")
root.resizable(width=False, height=False)
root.columnconfigure(0,weight=1)
path=resource_path0("Programicon.ico")
root.wm_iconbitmap(path)
root.geometry("400x200")
root.configure(bg='#FFFFFF')
Label(root, text="VDO TO IMG CONVERTER", font=("Impact",17),bd=1, fg="#5DBCD2", bg="#FFFFFF").grid()
Label(root, text="Choose Video", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").grid()
Vdo=Button(root, width=20,bg="#82CC6C",fg="white",highlightthickness=1,borderwidth=0.2,text="OPEN",relief="groove", command=openfile)
Vdo.grid()
Label(root, text="Choose Format", font=("Calibri",10), fg="#5DBCD2", bg="#FFFFFF").grid()
exportchoices=["jpg","png","bmp"]
exportbox=ttk.Combobox(root,values=exportchoices, font="Verdana 10", width=8)
exportbox.current(0)
exportbox.grid()
btn=Button(width=25, height=2,text="EXTRACT",font=("Cambria", 9),bg="#5DBCD2",fg="#FFFFFF",borderwidth=0,highlightthickness=2,padx=0,pady=0,command=Convert)
btn.place(x=106,y=122)
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
