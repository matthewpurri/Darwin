import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
import cv2
from PIL import Image, ImageTk

# https://www.youtube.com/watch?v=lt78_05hHSk

def getSpeciesNames():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder_path = dir_path+'/Dataset/'
    p = Path(folder_path)
    subdirectories = [x for x in p.iterdir() if x.is_dir()]
    names = []
    for path in subdirectories:
        names.append(os.path.basename(path))
    return names

def loadImage(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (250,250))
    b,g,r = cv2.split(image)
    img = cv2.merge((r,g,b))

    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk

class Selector_GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Species Viewer")

        container = tk.Frame(self)

        container.pack()
        self.frames = {}

        for F in (StartPage, SelectorPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(StartPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Select a program:")
        label.grid(row=0, column=0)

        button_mark_images = ttk.Button(self, text="Mark Images",
                                command=lambda: controller.showFrame(SelectorPage))
        button_mark_images.grid(row=2, column=0, sticky='nsew')


class SelectorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Selector a species:")
        label.grid(row=0, column=0)

        species_names = getSpeciesNames()

        self.var_species = tk.StringVar()
        self.var_species.set(species_names[0])
        menu_species = ttk.OptionMenu(self, self.var_species, *species_names)
        menu_species.grid(row=1,column=0, sticky='nsew')

        run_button = ttk.Button(self, text="Run", command=self.Selector)
        run_button.grid(row=2, column=0)

        button_back = ttk.Button(self, text="Back",
                            command=lambda: controller.showFrame(StartPage))
        button_back.grid(row=5, column=0)

        button_quit = ttk.Button(self, text="Quit", command=quit)
        button_quit.grid(row=6, column=0)

        # Images
        self.label_example = None
        self.label_current = None

        ttk.Label(self, text="Example image of species").grid(row=2, column=1)
        ttk.Label(self, text="Question image").grid(row=2, column=2)

    def Selector(self):
        species = self.var_species.get()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        folder_path = dir_path+'/Dataset/'
        example_path = folder_path+species+'/example.jpg'

        # Show example image for species
        ex_img = loadImage(example_path)
        if(self.label_example==None):
            self.label_example = tk.Label(self, image=ex_img)
            self.label_example.grid(row=3, column=1, sticky='nsew')
            self.label_example.image=ex_img
        else:
            self.label_example.configure(image=ex_img)
            self.label_example.image = ex_img

        # Find keword folder paths and save to a dictionary

        # For all folders in species
            # Create a txt document
            # For all images in a folder
                # View image
                # button is pushed
                # When button pushed it adds to the txt file



app = Selector_GUI()
app.mainloop()
