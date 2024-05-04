import tkinter as tk
from PIL import Image, ImageTk

import text_read.player_bounderies as player_feeds

class CordsPrint:
    def __init__(self) -> None:
        self.window = tk.Tk()

        self.player_dict = player_feeds.PLAYERS
        self.img = player_feeds.Reader()
        self.img_status = None
        self.index = 0

    def create_window(self) -> None:
        self.project_image()
        self.window.mainloop()

    def project_image(self) -> None:
        key = list(self.player_dict)
        if self.index < len(key):
            input = self.player_dict[key[self.index]]
            frame = self.img.spec_feed(input[0], input[1], input[2], input[3])

            image = Image.fromarray(frame)
            photo_image = ImageTk.PhotoImage(image=image)

            if not self.img_status:
                self.player_image = tk.Label(self.window)
                self.player_image.pack()

                self.next = tk.Button(self.window, text="next image", command=self.next_window)
                self.next.pack()
                self.img_status = self.player_image

                self.player_image.bind("<Button-1>", self.print_coordinates)

            self.player_image.photo_image = photo_image
            self.player_image.configure(image=photo_image)
        else:
            self.window.destroy()

        self.window.after(1000, self.project_image)

    def print_coordinates(self, event) -> None:
        x, y = event.x, event.y
        print(f"Coordinates: ({x}, {y})")

    def next_window(self) -> None:
        self.index += 1
        self.img_status = None

        self.player_image.destroy()
        self.next.destroy()
        self.project_image()

c = CordsPrint()
c.create_window()
