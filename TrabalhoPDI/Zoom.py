from tkinter import *
from tkinter import ALL, EventType
from PIL import Image, ImageTk

class LoadImage:
    def __init__(self,root, filepath, image=None, flag=False):
        #frame = Frame(root)
        self.canvas = Canvas(root,width=40,height=100)
        self.canvas.grid(row=0, column=0,   sticky='EWNS')
        #self.canvas.pack()
        #frame.pack()
        if flag:
            self.orig_img = Image.fromarray(image)
        else:
            self.orig_img = Image.open(filepath)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.background = Label(image=self.img)
        #self.background.pack(fill=BOTH, expand=YES)
        self.canvas.create_image(2,2,image=self.img, anchor="nw")
        #self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        #self.frame = Frame(root, bd=2, relief=SUNKEN)
        #self.frame.grid_rowconfigure(0, weight=1)
        #self.frame.grid_columnconfigure(0, weight=1)
        #self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
        #self.xscroll.grid(row=1, column=0, sticky=E+W)
        #self.yscroll = Scrollbar(self.frame)
        #self.yscroll.grid(row=0, column=1, sticky=N+S)
        #self.canvas = Canvas(self.frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        #self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        #self.xscroll.config(command=self.canvas.xview)
        #self.yscroll.config(command=self.canvas.yview)
        #self.frame.pack(fill=BOTH,expand=1)
        #File = filepath
        ##File = "C:/Users/user/Desktop/Imagens Trabalho/1.png"
        #self.orig_img = Image.open(File)
        #self.img = ImageTk.PhotoImage(self.orig_img)
        #self.canvas.create_image(1,1,image=self.img,anchor="nw")
        self.width, self.height = self.orig_img.size
        ##self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        self.zoomcycle = 0
        self.zimg_id = None

        self.canvas.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)
        #self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
        self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<ButtonRelease-1>', self.offset)
        self.x1 = 0
        self.y1 = 0
        self.xOffset = 0
        self.yOffset = 0

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)
        #self.xOffset = 0
        #self.yOffset = 0
        self.x1 = event.x
        self.y1 = event.y

    def offset(self, event):
       self.xOffset += event.x - self.x1
       self.yOffset += event.y - self.y1
 
    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle < 10: self.zoomcycle += 1
            elif self.zoomcycle >= 10: self.zoomcycle = 0
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0 and (self.zoomcycle) < 10:
            x,y = event.x - self.xOffset, event.y - self.yOffset
            size = self.width, self.height
            factor = self.height / self.width
            #x = root.winfo_pointerx() - self.xOffset
            #y = root.winfo_pointery() - self.yOffset
            n = min(self.width, self.height)
            #x = root.winfo_pointerx() - root.winfo_rootx()
            #y = root.winfo_pointery() - root.winfo_rooty()
        

            #if self.zoomcycle == 1:
            tmp = self.orig_img.crop((x-(n/(self.zoomcycle + 2)),y-(factor*n/(self.zoomcycle + 2)),x+(n/(self.zoomcycle + 2)),y+(factor*n/(self.zoomcycle + 2))))
            #if self.zoomcycle == 2:
            #    tmp = self.orig_img.crop((x-128,y-128,x+128,y+128))
            #elif self.zoomcycle == 3:
            #    tmp = self.orig_img.crop((x-64,y-64,x+64,y+64))
            #elif self.zoomcycle == 4:
            #    tmp = self.orig_img.crop((x-32,y-32,x+32,y+32))
            #elif self.zoomcycle == 5:
            #    tmp = self.orig_img.crop((x-16,y-16,x+16,y+16))
            widthTmp, heightTmp = tmp.size
            flag = min(widthTmp, heightTmp)
            if flag > 0:
                self.zimg = ImageTk.PhotoImage(tmp.resize(size))
                self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)


#if __name__ == '__main__':
#    root = Tk()
#    root.title("Crop Test")
#    App = LoadImage(root)
#    root.mainloop()

def Zoom(filepath, root, image=None, flag=False):
    #root = Tk()
    #root.title("Crop Test")
    #path = filepath
    App = LoadImage(root, filepath, image, flag)