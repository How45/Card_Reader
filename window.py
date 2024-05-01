import tkinter as tk
from PIL import Image, ImageTk
import cv2

class ScaleWindow():
    def __init__(self) -> None:
        self.w = tk.Tk()
        self.video_cap = cv2.VideoCapture(0)
        self.cords = (420, 425, 113, 62)

        self.white_level = tk.Spinbox(self.w, from_=1, to=255)
        self.status_video_cap = None

    def create(self) -> None:
        self.white_level.pack()

        button1 = tk.Button(self.w, text="Open Camera",
                        command=self.open_camera)
        button1.pack()
        self.w.mainloop()

    def card_info_test(self) -> None:
        pass

    def open_camera(self) -> None:
        _, frame = self.video_cap.read()

        x1,y1,w1,h1 = self.cords
        frame = frame[y1: y1+h1, x1:x1+w1]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, int(self.white_level.get()), 255, cv2.THRESH_BINARY)

        pro_pil = Image.fromarray(binary)
        photo_image = ImageTk.PhotoImage(image=pro_pil)

        if not self.status_video_cap:
            label_widget = tk.Label(self.w)
            label_widget.pack()
            self.status_video_cap = label_widget
        else:
            label_widget = self.status_video_cap

        label_widget.photo_image = photo_image
        label_widget.configure(image=photo_image)

        self.w.after(5, self.open_camera)



if __name__ == '__main__':
    window = ScaleWindow()
    window.create()
