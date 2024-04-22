import NumberFeed as nf
import Cards

def main():
    img = nf.VideoFeeds()

    on = True
    while on:
        dict_feeds = img.feeds()

        for n, i in dict_feeds.items():
            r,s = Cards.process(i)

            img.save_feed(n+'_rank',r)
            img.save_feed(n+'_suit',s)
        on = False
    img.destroy()

if __name__ == '__main__':
    main()