import tkinter
import customtkinter as ctk
import os
import webbrowser
import imageio
import cv2
import threading

if ctk.get_appearance_mode()=="Dark":
    o = 1
else:
    o = 0
    
def openfile():
    global file
    file = tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv']),('All Files', '*.*')])
    if file:
        if len(os.path.basename(file))>=20:
            open_button.configure(fg_color="grey50", text=os.path.basename(file)[:15]+"..."+os.path.basename(file)[-3:])
        else:
            open_button.configure(fg_color="grey50", text=os.path.basename(file))
            
    else:
        open_button.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"][o], text="Import Video")
        
def convert():
    global running
    if not file:
        return
    
    final = tkinter.filedialog.asksaveasfilename(filetypes =[('GIF', ['*gif']),('All Files', '*.*')],
                                                 initialfile=os.path.basename(file)[:-4]+".gif")
    if not final:
        return
    
    open_button.configure(state="disabled")
    convert_button.configure(state="disabled")
    progressbar.grid(row=6, column=1, padx=20, pady=(10,20), sticky="we")
    cam = cv2.VideoCapture(file)
    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    try:
        running = True
        reader = imageio.get_reader(file)
        fps = fps_slider
        writer= imageio.get_writer(final, fps=int(fps_slider.get()), subrectangles=sub_rec.get())

        i=1
        for frames in reader:
            writer.append_data(frames)
            i += 1
            progressbar.set(i/total_frames)
            if running is False:
                break
        writer.close()
        tkinter.messagebox.showinfo("DONE","GIF CREATED: "+final)
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

header = ctk.CTkButton(root, text="VDO TO GIF CONVERTER", fg_color=ctk.ThemeManager.theme["CTkTextbox"]["fg_color"][o],
                       text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"][o], command=open_info)
header.grid(row=0, column=1, pady=(10,0))

open_button = ctk.CTkButton(root, text="Import Video", command=openfile)
open_button.grid(row=0, column=0, rowspan=7, sticky="nsew", padx=20, pady=20)

sub_rec = ctk.CTkCheckBox(root, text="Optimize")
sub_rec.grid(row=2, column=1, pady=10)

label_2 = ctk.CTkLabel(root, text="FPS: 30")
label_2.grid(row=3, column=1, pady=0)

fps_slider = ctk.CTkSlider(root, width=10, from_=5, to=60, command=lambda e: label_2.configure(text="FPS: "+str(int(e))))
fps_slider.grid(row=4, column=1, sticky="nwe", padx=15)
fps_slider.set(30)

convert_button = ctk.CTkButton(root, text="CONVERT", command=lambda: threading.Thread(target=convert).start())
convert_button.grid(row=5, column=1, padx=20, pady=10, sticky="we")

progressbar = ctk.CTkProgressBar(root, width=100, bg_color="transparent")
progressbar.set(0)

root.mainloop()
