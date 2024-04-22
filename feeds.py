import cv2
import numpy as np

IMG_BOUNDARIES = {
    "c1" : (236,158,10,32),
    "c2" : (271,158,10,32),
    "c3" : (306,158,10,32),
    "c4" : (341,158,10,32),
    "c5" : (377,158,10,32),
    "h1" : (290,300,10,32),
    "h2" : (324,300,10,32)
}

class VideoFeeds:
    def __init__(self) -> None:
        self.img = cv2.VideoCapture(0)
        self.img_feeds = {}

    def destroy(self) -> None:
        self.img.release()
        cv2.destroyAllWindows()

    def feeds(self) -> dict[np.ndarray]:
        _, frame = self.img.read()

        for key in IMG_BOUNDARIES:
            x1, y1, w1, h1 = IMG_BOUNDARIES[key]
            self.img_feeds[key] = frame[y1: y1+h1, x1:x1+w1]

        return self.img_feeds

    def display_dict(self, dict_frame) -> bool:
        for frame in dict_frame:
            cv2.imshow(frame, dict_frame[frame])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def save_feed(self, name, feed):
        if len(feed.shape) == 3:
            feed = cv2.cvtColor(feed, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(name+'.jpg', feed)
