from Zoom import Zoom
from ResizeRegion import resizeImage
from ZoomAlt import MainWindow
from ROI import getRoi
from Equalization import equalize
from Quantization import quantize
from Save import _save_file_dialogs
import easygui
import unicodedata
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2 as cv2
import matplotlib.pyplot as plt
import os

def pathImage():
    global filepath, enteredImage, baseImage, hasBaseImage
    baseROI = messagebox.askquestion("askquestion", "A imagem é uma região de interesse?")
    uni_img = easygui.fileopenbox()
    filepath = unicodedata.normalize('NFKD', uni_img).encode('ascii','ignore')
    filepath = filepath.decode('utf-8')
    hasBaseImage = False
    enteredImage = True
    if baseROI == 'yes':
        hasBaseImage = True
        baseImage = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    if not changeZoom:
        Zoom(filepath, group1)
    else:
        app = MainWindow(group1, filepath)

def pathSave():
     if not hasBaseImage:
        messagebox.showerror("showerror", "Abra uma região de interesse primeiro")
     else:
        path = _save_file_dialogs()
        if path != None:
            result=cv2.imwrite(path, baseImage)
            if result==True:
                messagebox.showinfo("showinfo", "Arquivo Salvo")
            else:
                messagebox.showerror("showerror", "Erro ao salvar")

def pathRoi():
    if enteredImage:
        roi = getRoi(filepath)
        global hasBaseImage, baseImage
        hasBaseImage = True
        baseImage = roi
        if not changeZoom:
            Zoom(filepath, group1, image=roi, flag=True)
        else:
            result=cv2.imwrite('temp.png', baseImage)
            app = MainWindow(group1, 'temp.png')
    else:
        messagebox.showerror("showerror", "Abra uma imagem primeiro")

def pathResize():
    if not hasBaseImage:
        messagebox.showerror("showerror", "Abra uma região de interesse primeiro")
    else:
        scale = easygui.enterbox("Qual a escala será aplicada na imagem (%)?")
        if scale != None:
            global baseImage
            imageResized = resizeImage(baseImage, int(scale))
            baseImage = imageResized
            if not changeZoom:
                Zoom(filepath, group1, image=imageResized, flag=True)
            else:
                result=cv2.imwrite('temp.png', baseImage)
                app = MainWindow(group1, 'temp.png')

def pathQuantize():
    if not hasBaseImage:
        messagebox.showerror("showerror", "Abra uma região de interesse primeiro")
    else:
        levels = easygui.enterbox("Qual a quantidade de tons de cinza aplicada na imagem (tipo int)?")
        if levels != None:
            global baseImage
            imageQuantized = quantize(baseImage, int(levels))
            baseImage = imageQuantized
            if not changeZoom:
                Zoom(filepath, group1, image=imageQuantized, flag=True)
                plt.show()
            else:
                result=cv2.imwrite('temp.png', baseImage)
                app = MainWindow(group1, 'temp.png')
                plt.show()
         
def pathEqualize(value):
    if not hasBaseImage:
        messagebox.showerror("showerror", "Abra uma região de interesse primeiro")
    else:
        global baseImage
        if value == "Numpy":
            imageEqualized = equalize(baseImage, 'numpy')
        elif value == "Opencv":
            imageEqualized = equalize(baseImage, 'opencv')
        else:
            imageEqualized = equalize(baseImage, 'clahe')

        baseImage = imageEqualized
        if not changeZoom:
            Zoom(filepath, group1, image=imageEqualized, flag=True)
            plt.show()
        else:
            result=cv2.imwrite('temp.png', baseImage)
            app = MainWindow(group1, 'temp.png')
            plt.show()

def pathZoom():
    global changeZoom
    if changeZoom:
        changeZoom = False
        if not hasBaseImage and not enteredImage:
            messagebox.showerror("showerror", "Abra uma imagem primeiro")
        elif hasBaseImage:
            Zoom(filepath, group1, image=baseImage, flag=True)
        elif filepath and not hasBaseImage:
            Zoom(filepath, group1)
    else:
        changeZoom = True
        if not hasBaseImage and not enteredImage:
            messagebox.showerror("showerror", "Abra uma imagem primeiro")
        elif hasBaseImage:
            result=cv2.imwrite('temp.png', baseImage)
            app = MainWindow(group1, 'temp.png')
        elif filepath and not hasBaseImage:
            app = MainWindow(group1, filepath)

def pathSair():
    master_window.destroy()
    temp = cv2.imread('temp.png')
    try:
        if temp != None:
            os.remove('temp.png')
    except:
        print('A imagem temporaria não foi apagada')

filepath = 'KMabWEXvea4P6QSXqDM6.png'
baseImage = cv2.imread('KMabWEXvea4P6QSXqDM6.png', cv2.IMREAD_UNCHANGED)
enteredImage = False
hasBaseImage = False
changeZoom = True

master_window = tk.Tk()
master_window.title("Menu")

# Widget Pai para os botões
buttons_frame = tk.Frame(master_window)
buttons_frame.grid(row=0, column=0, sticky='we')


btn_Image = tk.Button(buttons_frame, text='Imagem', command=pathImage)
btn_Image.grid(row=0, column=0, padx=(10), pady=10)
btn_Image.config(width = 11)

btn_Save = tk.Button(buttons_frame, text='Salvar', command=pathSave)
btn_Save.grid(row=0, column=1, padx=(10), pady=10)
btn_Save.config(width = 11)

btn_ROI = tk.Button(buttons_frame, text='ROI', command=pathRoi)
btn_ROI.grid(row=0, column=2, padx=(10), pady=10)
btn_ROI.config(width = 11)

btn_Resize = tk.Button(buttons_frame, text='Redimensionar', command=pathResize)
btn_Resize.grid(row=0, column=3, padx=(10), pady=10)
btn_Resize.config(width = 11)

btn_Quantize = tk.Button(buttons_frame, text='Quantização', command=pathQuantize)
btn_Quantize.grid(row=0, column=4, padx=(10), pady=10)
btn_Quantize.config(width = 11)


variable = tk.StringVar(buttons_frame)
variable.set("Equalização") # Valor default

btn_Equalize = tk.OptionMenu(buttons_frame, variable, "Numpy", "Opencv", "Clahe", command=pathEqualize)
btn_Equalize.grid(row=0, column=5, padx=(10), pady=10)
btn_Equalize.config(width = 11)

#btn_AltZoom = tk.Button(buttons_frame, text='Alternar Zoom', command=pathZoom)
#btn_AltZoom.grid(row=0, column=6, padx=(10), pady=10)
#btn_AltZoom.config(width = 11)

btn_Sair = tk.Button(buttons_frame, text='Sair', command=pathSair)
btn_Sair.grid(row=0, column=6, padx=(10), pady=10)
btn_Sair.config(width = 11)

# Frame Group1 ----------------------------------------------------
group1 = tk.LabelFrame(master_window, text="Imagem", padx=5, pady=5)
group1.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ewns')

master_window.columnconfigure(0, weight=1)
master_window.rowconfigure(1, weight=1)

group1.rowconfigure(0, weight=1)
group1.columnconfigure(0, weight=1)

# Cria o Canvas da imagem
#Zoom(filepath, group1)
app = MainWindow(group1, filepath)

master_window.mainloop()
