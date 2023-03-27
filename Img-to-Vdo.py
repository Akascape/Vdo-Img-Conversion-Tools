import tkinter
import customtkinter as ctk
import os
import sys
import glob
import pkg_resources
import webbrowser
import cv2
import re
import threading

if ctk.get_appearance_mode()=="Dark":
    o = 1
else:
    o = 0
    
def openfile():
    global folder
    folder = tkinter.filedialog.askdirectory()
    if folder:
        if len(os.path.basename(folder))>=20:
            open_button.configure(fg_color="grey50", text=os.path.basename(folder)[:15]+"..."+os.path.basename(folder)[-3:])
        else:
            open_button.configure(fg_color="grey50", text=os.path.basename(folder))
            
    else:
        open_button.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][o], text="Import Image \nSequence")
        
def convert():
    global running
    if not folder:
        return
    
    final = tkinter.filedialog.asksaveasfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv','*gif']),('All Files', '*.*')],
                                                 initialfile=os.path.basename(folder)+"."+exportbox.get())
    if not final:
        return
    
    if len(os.listdir(folder))==0:
        tkinter.messagebox.showinfo("Uh!", "Folder is empty!")
        return
    
    open_button.configure(state="disabled")
    convert_button.configure(state="disabled")
    progressbar.grid(row=6, column=1, padx=20, pady=(10,20), sticky="we")
    
    firstitem = os.listdir(folder)[0]
    ext = os.path.basename(firstitem).split('.')[-1]
    
    try:
        img = cv2.imread(os.path.join(folder, firstitem))
        frameSize = (img.shape)[1::-1]
        fps = int(fps_slider.get())
        out = cv2.VideoWriter(final,cv2.VideoWriter_fourcc(*'mp4v'), fps, frameSize)
        files = glob.glob(os.path.join(folder,"*."+ext))              
        files.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
        count = 1
        for filename in files:
            if running is False:
                break
            progressbar.set(count/len(files))
            img = cv2.imread(filename)
            out.write(img)
            count+=1
        out.release()
        running = True
        tkinter.messagebox.showinfo("DONE", "Video Created: "+final)
    except:
        tkinter.messagebox.showerror("ERROR", "Something went wrong!")
        
    progressbar.grid_forget()
    open_button.configure(state="normal")
    convert_button.configure(state="normal")
    
def stop_process():
    global running
    running = False
    
def open_info():
    # About window 
    header.configure(state="disabled")
    
    def open_program():
        ch = "Vdo-to-Img.py"
        root.destroy()
        os.system('"%s"' % ch)     
            
    def exit_top_level():
        top_level.destroy()
        header.configure(state="normal")
        
    def web(link):
        webbrowser.open_new_tab(link)
        
    top_level = ctk.CTkToplevel(root)
    top_level.protocol("WM_DELETE_WINDOW", exit_top_level)
    top_level.title("About")
    top_level.attributes("-topmost", True)
    top_level.resizable(width=False, height=False)
    top_level.wm_iconbitmap("Programicon.ico")
    
    label_top = ctk.CTkLabel(top_level, text="VDO-IMG TOOLS", font=("Roboto",15))
    label_top.grid(padx=20, pady=(20,0), sticky="w")
        
    desc = "\n\nDeveloped by Akash Bora (Akascape)"
    
    label_disc = ctk.CTkLabel(top_level,  text=desc, justify="left", font=("Roboto",12))
    label_disc.grid(padx=20, pady=0, sticky="wn")
    
    link = ctk.CTkLabel(top_level, text="Official Page", justify="left", font=("",13), text_color="#1f6aa5")
    link.grid(padx=20, pady=0, sticky="wn")   
    link.bind("<Button-1>", lambda event: web("https://github.com/Akascape/Vdo-Img-Conversion-Tools"))
    link.bind("<Enter>", lambda event: link.configure(font=("", 13, "underline"), cursor="hand2"))
    link.bind("<Leave>", lambda event: link.configure(font=("", 13), cursor="arrow"))
    
    button_switch = ctk.CTkButton(top_level, text="Open VDO-TO-IMG", fg_color=ctk.ThemeManager.theme["CTkTextbox"]["fg_color"][o],
                                  text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][o], command=open_program)
    button_switch.grid(padx=20, pady=(10,20))
    
root= ctk.CTk()
root.geometry("450x240")
root.title("Vdo & Img Tools")
root.resizable(width=False, height=False)
root.columnconfigure((0,1),weight=1)
root.rowconfigure((0,1,2,3,4,5,6),weight=1)
root.wm_iconbitmap("Programicon.ico")
root.bind('<Escape>', lambda e: stop_process())

folder = ""
running = True

header = ctk.CTkButton(root, text="IMG TO VDO CONVERTER", fg_color=ctk.ThemeManager.theme["CTkTextbox"]["fg_color"][o],
                       text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][o], command=open_info)
header.grid(row=0, column=1, pady=(10,0))

open_button = ctk.CTkButton(root, text="Import Image \nSequence", command=openfile)
open_button.grid(row=0, column=0, rowspan=7, sticky="nsew", padx=20, pady=20)

label_2 = ctk.CTkLabel(root, text="Choose Format")
label_2.grid(row=1, column=1, pady=0)

exportchoices = ["mp4","avi","mov","mkv","wmv"]
exportbox = ctk.CTkComboBox(root, values=exportchoices, state="readonly")
exportbox.set("mp4")
exportbox.grid(row=2, column=1, sticky="we", padx=20)

label_3 = ctk.CTkLabel(root, text="FPS: 30")
label_3.grid(row=3, column=1, pady=0)

fps_slider = ctk.CTkSlider(root, width=10, from_=10, to=60, command=lambda e: label_3.configure(text="FPS: "+str(int(e))))
fps_slider.grid(row=4, column=1, sticky="nwe", padx=15)
fps_slider.set(30)

convert_button = ctk.CTkButton(root, text="CONVERT", command=lambda: threading.Thread(target=convert).start())
convert_button.grid(row=5, column=1, padx=20, pady=10, sticky="we")

progressbar = ctk.CTkProgressBar(root, width=100, bg_color="transparent")
progressbar.set(0)

root.mainloop()
