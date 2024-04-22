import numpy as np
import cv2

class CardsInfo:
    def __init__(self) -> None:
        self.warp = [] # 200x300, flattened, grayed, blurred image
        self.rank_img = [] # Thresholded, sized image of card's rank
        self.suit_img = [] # Thresholded, sized image of card's suit
        self.best_rank_match = "Unknown" # Best matched rank
        self.best_suit_match = "Unknown" # Best matched suit
        self.rank_diff = 0 # Difference between rank image and best matched train rank image
        self.suit_diff = 0 # Difference between suit image and best matched train suit image

class TrainRanks:
    def __init__(self) -> None:
        self.img = []
        self.name = "Placeholder"

class TrainSuits:
    def __init__(self) -> None:
        self.img = []
        self.name = "Placeholder"

def load_ranks(filepath):
    train_ranks = []
    i = 0

    for rank in ['ace','two','three','four','five','six','seven',
                 'eight','nine','ten','jack','queen','king']:
        train_ranks.append(TrainRanks())
        train_ranks[i].name = rank
        filename = rank + '.jpg'
        train_ranks[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_ranks

def load_suits(filepath):
    train_suits = []
    i = 0
    x = ['spade_1','spade_2','spade_3','diamond_1','diamond_2','diamond_3',
         'club_1','club_2','club_3','heart_1','heart_2','heart_3']
    for suit in x:
        train_suits.append(TrainSuits())
        train_suits[i].name = suit
        filename = suit + '.jpg'
        train_suits[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits

def process(frame, white_level = 200, level = 1) -> CardsInfo:
    card_info = CardsInfo()

    card_info.warp = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # Turn frame colour to gray
    zoom_img = cv2.resize(card_info.warp, (0,0), fx=4, fy=4) # Get resize of image with rescale increase of 4*

    # white_level = zoom_img[0, int(np.shape(frame)[1])] # h, w

    thresh_level = white_level - level # Need to determine whats a good lvl

    if thresh_level <= 0:
        thresh_level = 1
    _, query_thresh = cv2.threshold(zoom_img, thresh_level, 255, cv2.THRESH_BINARY_INV)

    card_ranks = query_thresh[0:66, 0:40]
    card_suit = query_thresh[65:129, 0:40]
    # return zoom_img
    # return card_ranks, card_suit
    # return query_thresh
    for rank_roi, suit_roi in zip(card_ranks, card_suit):
        countours_r, _ = cv2.findContours(card_ranks, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        countours_s, _ = cv2.findContours(card_suit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        countours_r = sorted(countours_r, key=cv2.contourArea,reverse=True)
        countours_s = sorted(countours_s, key=cv2.contourArea,reverse=True)

        if countours_r and countours_s:
            # x1,y1,w1,h1 = cv2.boundingRect(countours_r[0])
            # x2,y2,w2,h2 = cv2.boundingRect(countours_s[0])

            resized_r = cv2.resize(card_ranks, (40, 66), 0, 0) # card_ranks[y1:y1+h1, x1:x1+w1]
            resized_s = cv2.resize(card_suit, (40, 63), 0, 0) # card_suit[y2:y2+h2, x2:x2+w2]
            card_info.rank_img = resized_r
            card_info.suit_img = resized_s
    # return card_info.rank_img
    # return card_info.suit_img
    return card_info

def match_card(card_info, t_ranks, t_suits):
    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    best_rank_match_name = "Unknown"
    best_suit_match_name = "Unknown"
    i = 0

    if len(card_info.rank_img) != 0 and len(card_info.suit_img) != 0:
        for rank in t_ranks:
            # print(card_info.rank_img.shape , rank.img.shape)
            diff_img = cv2.absdiff(card_info.rank_img, rank.img)
            rank_diff = int(np.sum(diff_img)/255)

            if rank_diff < best_rank_match_diff:
                best_rank_diff_img = diff_img
                best_rank_match_diff = rank_diff
                best_rank_name = rank.name

        for suit in t_suits:
            # print(card_info.suit_img.shape , suit.img.shape)
            diff_img = cv2.absdiff(card_info.suit_img, suit.img)
            suit_diff = int(np.sum(diff_img)/255)

            if suit_diff < best_suit_match_diff:
                best_suit_diff_img = diff_img
                best_suit_match_diff = suit_diff
                best_suit_name = suit.name

    if (best_rank_match_diff < 2000): # Might need to change!!!!!!
        best_rank_match_name = best_rank_name

    if (best_suit_match_diff < 700): # Might need to change!!!!!
        best_suit_match_name = best_suit_name

    return best_rank_match_name, best_suit_match_name, best_rank_match_diff, best_suit_match_diff