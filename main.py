import NumberFeed as nf
import Cards
import os

path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks( path + '/train_ranks/')
train_suits = Cards.load_suits( path + '/train_suits/')

def main():
    img = nf.VideoFeeds()

    on = True
    while on:
        k = 0

        dict_feeds = img.feeds()
        cards = []
        # on = img.display_dict(dict_feeds)
        for _, img in dict_feeds.items():
            cards.append(Cards.process(img))
            cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

            print(cards[k].best_rank_match, cards[k].best_suit_match)
            k = k + 1
        on = False
    # img.destroy()

if __name__ == '__main__':
    main()
