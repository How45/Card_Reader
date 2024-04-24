import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import helper_scripts.cardsInfo as cInfo
import helper_scripts.feeds as feeds
import os

path = os.path.dirname(os.path.abspath(__file__))
train_ranks = cInfo.load_ranks( path + '/train_ranks/')
train_suits = cInfo.load_suits( path + '/train_suits/')

class ScaleWindow():
    def __init__(self) -> None:
        self.w = tk.Tk()
        self.img = feeds.VideoFeeds()

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
        cards = []
        k = 0
        for n, feed in dict_feeds.items():
            pro = cInfo.process(feed, int(self.white_level.get()),int(self.thresh_level.get()))
            # cards.append(cInfo.process(feed, int(self.white_level.get()),int(self.thresh_level.get())))
            # pro = cInfo.match_card(cards[-1],train_ranks,train_suits)

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
            k += 1
        self.w.after(5, self.open_camera)



if __name__ == '__main__':
    window = ScaleWindow()
    window.create()