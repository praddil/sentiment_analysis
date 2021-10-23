import finviz
import pandas as pd


class GetStockList(object):

    def __init__(self, filename):
        self.stockList = pd.read_csv(filename, sep=";", header=None)

    def show_list(self):
        print(self.stockList)

    def get_list(self):
        return self.stockList


def get_news_urls(ticker, names):
    valid_url = []
    news_content = finviz.get_news(ticker)

    for headline, url in news_content:
        if bool([url for name in names if name in headline]):
            valid_url.append(url)
    return valid_url

