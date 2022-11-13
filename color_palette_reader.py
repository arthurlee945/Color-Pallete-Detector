from tkinter import Canvas, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
import numpy as np
from PIL import Image, ImageTk
import scipy
import scipy.misc
import scipy.cluster
import time
import os
import sys


class ColorPaletteReader:
    def __init__(self):
        # set root
        self.root = TkinterDnD.Tk()
        self.root.title("Color Palette Reader")
        self.root.config(padx=25, pady=50, bg='white')
        # title/ instruction
        Label(text="Drop your image below!", font=("Calibri", 14, "bold"), bg="white").grid(row=0, column=0,
                                                                                            columnspan=5, pady=25,
                                                                                            sticky=["e", "w"])
        # canvas to display image
        self.canvas = Canvas(width=600, height=300)
        self.canvas.grid(row=1, column=0, columnspan=5)
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind("<<Drop>>", self.image_drop)
        self.selected_image = None
        self.canvas_image = None

        # warning labels
        self.warning_label = Label(text="", font=("Calibri", 10), fg="red", bg='white')
        self.warning_label.grid(row=2, column=0, columnspan=5, pady=5, sticky=["e", "w"])

    def image_drop(self, e):
        clean_dict = re.sub("[{}]", "", e.data)
        if clean_dict.endswith(".jpg") or clean_dict.endswith(".png") or clean_dict.endswith(".jpeg"):
            f_image = Image.open(clean_dict).convert("RGB")
            r_image = f_image.resize((int(300 * f_image.size[0] / f_image.size[1]), 300))
            self.selected_image = ImageTk.PhotoImage(r_image)
            self.canvas_image = self.canvas.create_image(300, 150, image=self.selected_image)
            self.image_processor(f_image)
        else:
            self.warning_label.config(text="please file type 'jpg','jpeg', or 'png")

    def image_processor(self, image):
        # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
        # https://towardsdatascience.com/k-means-from-scratch-with-numpy-74f79d2b1694
        img_arr = np.array(image)
        c_arr = img_arr.reshape((img_arr.shape[0] * img_arr.shape[1], img_arr.shape[2])).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(c_arr, 5)
        for i in range(5):
            try:
                rgb = self._rgb_convert([int(rgb) for rgb in codes[i]])
            except IndexError:
                Label(bg='white', height=7).grid(row=3, column=i, pady=10, padx=10, sticky=["e", "w"])
                Label(text="", bg='white').grid(row=4, column=i, pady=5, sticky=["e", "w"])
            else:
                Label(bg=rgb, height=7).grid(row=3, column=i, pady=10, padx=10, sticky=["e", "w"])
                Label(text=rgb, bg='white').grid(row=4, column=i, pady=5, sticky=["e", "w"])
        self.warning_label.config(text="processed", fg='blue')

    def _rgb_convert(self, rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'
