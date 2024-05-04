import helper_scripts.card_info as cInfo
import helper_scripts.card_bounderies as card_bounderies

def main():
    img = card_bounderies.VideoFeeds()

    on = True
    while on:
        dict_feeds = img.get_feeds()

        for n, i in dict_feeds.items():
            r,s = cInfo.process(i)

            img.save_feed(n+'_rank',r)
            img.save_feed(n+'_suit',s)
        on = False
    img.destroy()

if __name__ == '__main__':
    main()