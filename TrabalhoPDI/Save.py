import tkinter as tk
import easygui
import os


#def clickButton1():
#    global flag
#    flag =  True
#    root.destroy()
  
#def clickButton2():
#    global flag
#    flag = False
#    root.destroy()
 
#def save():
#    global root
#    root = tk.Tk()
#    frame = tk.Frame()
#    frame.pack(fill=tk.BOTH, expand=True)
#    label = tk.Label(frame, text = "Salvar imagem?")
#    button1 = tk.Button(frame, text="Sim", command=clickButton1)
#    #button1.grid(row=0, column=0, padx=(10), pady=10)
#    button2 = tk.Button(frame, text="Não", command=clickButton2)
#    #button2.grid(row=0, column=1, padx=(10), pady=10)
#    label.pack()
#    button1.pack()
#    button2.pack()
#    root.mainloop()
#    return flag

def _save_file_dialogs(extension = "png"):
        # If user cancels it defaults to the FIRST choice. We want default to be NO so I reverse the default of choices here. 
        saveornot = easygui.buttonbox(msg="Quer salvar a imagem?", choices = ("Não", "Sim") )
        if saveornot == "Sim":
            filename = easygui.filesavebox(msg = "Onde você quer salvar a imagem? (extensão %s será adicionada automaticamente)?" %(extension))
            if filename is None:
                return None
            filename = filename + "." + extension
            if os.path.exists(filename):
                ok_to_overwrite = easygui.buttonbox(msg="Imagem %s já existe. Sobrescrever?" %(filename), choices = ("Não", "Sim") )
                if ok_to_overwrite == "Sim":
                    return filename
                else:
                    return None
            else:
                return filename
        else:
            return None