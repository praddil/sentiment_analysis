import os
import csv
from pathlib import Path
import pandas as pd
from utils import get_news_urls
from scrapy.crawler import CrawlerProcess
from postExtract.spiders.yahoofinance_scrape import GetinfoSpider
from sentiment import SentimentAnalysis as sa


# Class for each stock to process
class Stock:

    def __init__(self, ticker, names, verbose, lock):
        self.ticker = ticker
        self.common_names = names
        self.path = Path(f'tickers/{self.ticker}/')          # folder path of the Stock
        self.file = os.path.join(self.path, 'news_content.csv')        # File containing Stock's news information
        self.updateFile = os.path.join(self.path, 'latest_update.csv')
        self.scoreFile = os.path.join(self.path, 'scoreCard.csv')
        self.weighted_score = 0.0
        self.mean_score = 0.0
        self.update_df = None
        self.news_analysis = []
        self.verbose = verbose

        # Check if the folder exists for the stock
        if not os.path.exists(f'tickers/{self.ticker}'):
            print(f"Creating folder for the following stock: {self.ticker}")
            os.mkdir(f'tickers/{self.ticker}')

        # Check if the stock file exists
        if os.path.exists(self.file):
            news_content = pd.read_csv(self.file)
            self.urls = list(news_content['Link'])
        else:
            # Creates a file and establishes the header
            with open(self.file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Author", "Headline", "Full_Content", "Relevant_Content", "Link", "Relevance"])
            self.urls = []

        self.update()
        if os.path.exists(self.scoreFile):
            score_df = pd.read_csv(self.scoreFile)
            last_index = score_df.shape[0] - 1
            self.weighted_score = round(score_df.iloc[last_index]['W_Score'], 4)
            self.mean_score = round(score_df.iloc[last_index]['Score'], 4)
        else:
            print("The score card file does not exists yet")

        self.get_info(lock)

    # Update any news news available to process since the last update
    def update(self):
        urls = get_news_urls(self.ticker, self.common_names)
        update_urls = ([url for url in urls if url not in self.urls and 'finance.yahoo' in url])

        if update_urls:
            # Start Crawlprocess with no logs to display in the console
            process = CrawlerProcess(settings={"LOG_ENABLED": False})
            process.crawl(GetinfoSpider, start_urls=update_urls,
                          filepath=self.file, updatefile=self.updateFile, stock_name=self.common_names)
            process.start()
            self.update_df, self.news_analysis = sa(self.path).generate_analysis()

        else:
            print(f"** THERE ARE NO NEWS TO BE UPDATED for : {self.ticker}")
            with open(self.updateFile, "w") as update:
                update.truncate()
            update.close()

    def get_info(self, lock):
        with lock:
            if self.verbose:
                for link in self.news_analysis:
                    print(link)
                print(self.update_df)
            print(f'Ticker symbol: {self.ticker}')
            print(f'Common used names: {self.common_names}')
            print(f'File path: {self.path}')
            print(f'Mean sentiment score: {self.mean_score}')
            print(f'Weighted Score: {self.weighted_score}')
            print('\n')
