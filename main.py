import helper_scripts.cardsInfo as cInfo
import helper_scripts.card_feeds as card_feeds
import os

path = os.path.dirname(os.path.abspath(__file__))
train_ranks = cInfo.load_ranks( path + '/train_ranks/')
train_suits = cInfo.load_suits( path + '/train_suits/')

def main():
    img = card_feeds.VideoFeeds()

    on = True
    while on:
        k = 0

        dict_feeds = img.get_feeds()
        cards = []
        for _, img in dict_feeds.items():
            cards.append(cInfo.process(img))
            cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = cInfo.match_card(cards[k],train_ranks,train_suits)

            print(f"""{cards[k].best_rank_match} | {cards[k].rank_diff}
{cards[k].best_suit_match} | {cards[k].suit_diff}
------------------------------------------------""")
            k += 1
        on = False
    # img.destroy()
if __name__ == '__main__':
    main()
