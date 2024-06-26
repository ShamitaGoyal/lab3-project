from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk

class Img(ctk.CTkFrame):
    def __init__(self, parent, png, sizeW, sizeH):
        super().__init__(parent)
        self.parent = parent
        self.png = png
        self.sizeW = sizeW
        self.sizeH = sizeH
        self.imageDisplay()

    def imageDisplay(self):
        image_path = self.png
        self.image = Image.open(image_path)

        width, height = self.image.size
        new_width = int(width * self.sizeW)
        new_height = int(height * self.sizeH)
        self.image = self.image.resize((new_width, new_height))

        # Convert the Image object into a Tkinter-compatible photo image
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label widget to display the image
        self.label = tk.Label(self, image=self.photo, bd=0)
        self.label.grid()

