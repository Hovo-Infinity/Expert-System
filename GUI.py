#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 01:15:19 2020

@author: hovhannesstepanyan
"""

from tkinter import *
from tkinter.ttk import Frame, Button
from tkinter import filedialog
import csv
from PIL import ImageTk, Image
from Fuzzy import path
from InteligentSystems import InteligentSystems
from copy import deepcopy

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()
        
        
    def open_file(self):
        csv_file_path = filedialog.askopenfilename()
        self.v.set(csv_file_path)
        
    def read_csv(self, path):
        global datas
        f = open(path.get(),"rb")
        with open(f.name, "r", encoding="UTF-8") as f:
            datas = list(csv.reader(f))
        

    def show_image(self):
        InteligentSystems.dis_help_sys(deepcopy(datas))
        global img
        img = ImageTk.PhotoImage(Image.open(path + "result.png"))
        self.canvas.create_image(20, 20, anchor=NW, image=img)

    def initUI(self):

        self.master.title('Система поддержки принятия решений')

        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        self.v = StringVar()
        self.v.trace('w', lambda *_, var=self.v: self.read_csv(self.v))
        menuBar = Menu(self)

        open_button = Button(self, text='Open file', command=self.open_file)
        open_button.grid(row=1, column=3)
        calc_button = Button(self, text='Calculate', command=lambda: self.show_image())
        calc_button.grid(row=2, column=3, pady=4)
                
        self.canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, columnspan=2, rowspan=4,
                         padx=5, sticky=E+W+S+N)


def main():

    root = Tk()
    root.geometry("700x500+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
