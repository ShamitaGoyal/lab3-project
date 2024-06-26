import tkinter as tk
from PIL import Image, ImageTk

class GIFLabel(tk.Label):
    def __init__(self, master=None, gif_path="", width=200, height=200, delay=100):
        tk.Label.__init__(self, master, bg="white", highlightthickness=0)
        self.gif_path = gif_path
        self.delay = delay
        self.width = width
        self.height = height
        self._frames = []
        self._frame_index = 0
        self._load_frames()
        self._animate()

    def _load_frames(self):
        gif = Image.open(self.gif_path)
        try:
            while True:
                frame = gif.copy()
                frame.thumbnail((self.width, self.height))
                self._frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self._frames)) # Move to next frame
        except EOFError:
            pass # end of sequence

    def _animate(self):
        self.config(image=self._frames[self._frame_index])
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        self.after(self.delay, self._animate)
