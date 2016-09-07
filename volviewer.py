#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

This script shows a simple window
on the screen.

Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""

from Tkinter import *
from ttk import Button
import ttk
import nibabel as nib
import PIL
from PIL import ImageTk, Image
from imageUtils import matUtilTools as mut


class Example(Frame):

    def __init__(self, parent, img = None):
        Frame.__init__(self, parent, background="black")

        self.parent = parent
        self.img = None
        self.data = None
        self.__pos_z = 1

        if not img is None:
            self.load_image(img)

        self.init_ui()

    def load_image(self, img):
        self.img = img
        self.data = mut.norm0255(img.get_data())
        self.__pos_z = 70
        self.__img_size = self.data.shape
        self.__pos_z = int(round(self.__img_size[2]/2, 0))

    def init_ui(self):
        self.parent.title("VV-VolumeViewer")
        self.pack(fill=BOTH, expand=1)

        # Menu stuff
        menu_bar = Menu(self.parent)
        menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File",menu=menu)
        menu_bar.add_cascade(label="Help",menu=menu)
        self.parent.config(menu=menu_bar)

        # Left frame
        left_frame = Frame(self)
        left_frame.configure(borderwidth=1.5, background='black', width=200)

        # volume frame
        canvas_frame = Frame(self)
        canvas_frame.configure(borderwidth=1.5,background='white')
        self.canvas = Canvas(canvas_frame, highlightthickness=0, background='black')
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)


        test_button = Button(left_frame, text="PrintSize",
                            command=self.print_size,style="TButton")
        self.bind("<Configure>", self.print_size)
        self.canvas.bind("<Configure>", self.render_image)


        # canvas.pack(side = TOP, expand=True, fill=BOTH)
        # canvas.place(x=20, y=10)

        console = Text(self, height=12)

        left_frame.pack(side=LEFT, fill=Y)
        canvas_frame.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, expand=1)
        console.pack(side=BOTTOM, fill=X)
        test_button.pack()
        test_button.place(x=10, y=10)

    def print_size(self,event = None):
            print self.winfo_width()
            print self.winfo_height()

    def render_image(self, event = None):
        img = Image.fromarray(self.data[:, :, self.__pos_z])
        # img = img.resize((200, 200))
        self.renderImg = ImageTk.PhotoImage(img)
        ca_width = self.canvas.winfo_width()
        ca_height = self.canvas.winfo_height()

        self.canvas.delete(ALL)
        self.canvas.create_image(ca_width/2, ca_height/2, image=self.renderImg)

    def _on_mousewheel(self, event = None):
        if event.num is 4:
            self.__pos_z = min(self.__pos_z+1,self.__img_size[2]-1)
        elif event.num is 5:
            self.__pos_z = max(self.__pos_z-1,0)

        self.render_image()



def main():

    root = Tk()

    ttk.Style().configure("TButton", padding=6, relief='solid', # White
                          lightcolor='#FF0000', # Red
                          darkcolor='#0000FF', # Blue
                          borderwidth=0,
                          foreground='#000000', # Cyan
                          bordercolor='white' # Green
                          )
    ttk.Style().configure("TButton.border", borderwidth=10)

    print ttk.Style().layout('TButton')
    print ttk.Style().element_options('TButton.border')
    print ttk.Style().element_options('TButton')

# ttk.Style().configure("TButton", padding=6, relief="flat", foreground="#fff",
    #                      background="#000", borderwidth=10,  bordercolor='#fff')
    root.geometry("1024x768+500+300")
    img = nib.load('/home/jhofmanninger/testData/vol1.nii.gz')
    app = Example(root,img)
    app.render_image()
    root.mainloop()


if __name__ == '__main__':
    main()