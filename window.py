import tkinter as tk
from threading import Thread
import Cards
import NumberFeed as nf
from PIL import Image, ImageTk

class ScaleWindow():
    def __init__(self) -> None:
        self.w = tk.Tk()
        self.img = nf.VideoFeeds()

        self.thresh_level = tk.Spinbox(self.w, from_=1, to=500)
        self.white_level = tk.Spinbox(self.w, from_=0, to=255)
        self.label_widgets = {}

    def create(self) -> None:
        self.thresh_level.pack()
        self.white_level.pack()

        button1 = tk.Button(self.w, text="Open Camera",
                        command=self.open_camera)
        button1.pack()
        self.w.mainloop()


    def open_camera(self) -> None:
        dict_feeds = self.img.feeds()
        for n, feed in dict_feeds.items():
            pro = Cards.process(feed, int(self.white_level.get()),int(self.thresh_level.get()))

            pro_pil = Image.fromarray(pro)
            photo_image = ImageTk.PhotoImage(image=pro_pil)

            if n not in self.label_widgets:
                label_widget = tk.Label(self.w)
                label_widget.pack(side="left")
                self.label_widgets[n] = label_widget
            else:
                label_widget = self.label_widgets[n]

            label_widget.photo_image = photo_image
            label_widget.configure(image=photo_image)

        self.w.after(5, self.open_camera)



if __name__ == '__main__':
    window = ScaleWindow()
    window.create()