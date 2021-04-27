from tkinter import *
from tkinter import ALL, EventType
from PIL import Image, ImageTk

class LoadImage:
    def __init__(self,root, filepath, image=None, flag=False):
        self.__canvas = Canvas(root,width=40,height=100)
        self.__canvas.grid(row=0, column=0,   sticky='EWNS')
        if flag:
            self.__orig_img = Image.fromarray(image)
        else:
            self.__orig_img = Image.open(filepath)
        self.__img = ImageTk.PhotoImage(self.__orig_img)
        self.__background = Label(image=self.__img)
        self.__canvas.create_image(2,2,image=self.__img, anchor="nw")
        self.__width, self.__height = self.__orig_img.size
        ##self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        self.__zoomcycle = 0
        self.__zimg_id = None

        self.__canvas.bind("<MouseWheel>",self.zoomer)
        self.__canvas.bind("<Motion>",self.crop)
        #self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
        self.__canvas.bind("<B1-Motion>", lambda event: self.__canvas.scan_dragto(event.x, event.y, gain=1))
        self.__canvas.bind('<ButtonPress-1>', self.move_from)
        self.__canvas.bind('<ButtonRelease-1>', self.offset)
        self.__x1 = 0
        self.__y1 = 0
        self.__xOffset = 0
        self.__yOffset = 0

    def move_from(self, event):
        # Lembra das ultimas coordernadas para o scroll do mouse
        self.__canvas.scan_mark(event.x, event.y)
        self.__x1 = event.x
        self.__y1 = event.y

    def offset(self, event): # Diferença da posição inicial da imagem
       self.__xOffset += event.x - self.__x1
       self.__yOffset += event.y - self.__y1
 
    def zoomer(self,event):
        if (event.delta > 0):
            if self.__zoomcycle < 10: self.__zoomcycle += 1 # Maximo de 10 níveis de zoom
            elif self.__zoomcycle >= 10: self.__zoomcycle = 0
        elif (event.delta < 0):
            if self.__zoomcycle != 0: self.__zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.__zimg_id: self.__canvas.delete(self.__zimg_id)
        if (self.__zoomcycle) != 0 and (self.__zoomcycle) < 10:
            x,y = event.x - self.__xOffset, event.y - self.__yOffset
            size = self.__width, self.__height
            factor = self.__height / self.__width
            n = min(self.__width, self.__height)
        
            tmp = self.__orig_img.crop((x-(n/(self.__zoomcycle + 2)),y-(factor*n/(self.__zoomcycle + 2)),x+(n/(self.__zoomcycle + 2)),y+(factor*n/(self.__zoomcycle + 2))))
            widthTmp, heightTmp = tmp.size
            flag = min(widthTmp, heightTmp)
            if flag > 0:
                self.__zimg = ImageTk.PhotoImage(tmp.resize(size))
                self.__zimg_id = self.__canvas.create_image(x,y,image=self.__zimg)


def Zoom(filepath, root, image=None, flag=False):
    App = LoadImage(root, filepath, image, flag)