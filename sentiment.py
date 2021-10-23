import pandas as pd
import os
import csv
import sys
import textwrap
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
wrapper = textwrap.TextWrapper(width=100)
pd.set_option('display.max_columns', 7)
pd.set_option('display.width', 100)


class SentimentAnalysis:

    def __init__(self, filepath):
        self.filepath = filepath
        self.updateFilePath = os.path.join(self.filepath, 'latest_update.csv')
        self.analyzeFile = os.path.join(self.filepath,  'sentiment_analysis.csv')
        self.scoreFile = os.path.join(self.filepath,  'scoreCard.csv')

        # Check if  sentiment analysis file exists and creates one if not
        if not os.path.exists(self.analyzeFile):
            with open(self.analyzeFile, 'w', newline="", encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Link", "Relevance", "Score", "W_Score", "Detail"])
            file.close()

    def generate_analysis(self):
        news_link = []

        try:
            news = pd.read_csv(self.updateFilePath, header=None)
            sentiment_file = pd.read_csv(self.analyzeFile)

        except Exception as exception:
            print(exception)
            print(f"No update news since the last run for {os.path.basename(self.filepath)}")
            sys.exit(1)

        # New update links to be processed
        updated_links = list(sentiment_file['Link'])
        # Assigns column name for the news Dataframe
        news.columns = ["Date", "Author", "Headline", "Full_Content", "Relevant_Content", "Link", "Relevance"]

        total_entries = news.shape[0]       # Total number of update links

        with open(self.analyzeFile, "a", newline="", encoding='UTF-8') as a:
            writer = csv.writer(a)
            for i in range(total_entries):

                cleaned_para = news['Relevant_Content'][i]

                sentences = cleaned_para.split(".")
                # Find sentiment polarity of the sentences
                news_scores = [(sia.polarity_scores(sentence)['compound']) for sentence in sentences]
                # number of sentences with rating excluding ones with 0.0 rating
                den = 0
                # List of all sentences with rating included
                detail_list = []
                for j in range(len(sentences)):
                    if news_scores[j] != 0.0:
                        den += 1
                    # print(f'{news_scores[j]} : {sentences[j]}')
                    detail_list.append(f'{news_scores[j]} : {sentences[j]}')

                # Calculate mean score of each news

                try:
                    mean_score = round(sum(news_scores)/den, 2)
                    news_link.append([news['Link'][i], "Mean Score {} |  Relevance score {}".format(mean_score, den)])

                except ZeroDivisionError:
                    mean_score = 0.0
                    news_link.append([news['Link'][i], "News content polarity cannot be determined"])

                except Exception as e:
                    news_link.append([news['Link'][i], "Error Found !! Please check the link"])
                    print(f" Error Found !! Please check the link : {news['Link'][i]} \n {e}")

                # Weighted score calculated on the basis of relevance of news
                weighted_score = round(mean_score * news['Relevance'][i], 4)

                # Write a row to the file if the news link is not already included
                if news['Link'][i] not in updated_links:
                    writer.writerow([news['Date'][i], news['Link'][i], news['Relevance'][i], mean_score, weighted_score,
                                     detail_list])
        a.close()

        # Read the sentiment file to calculate the mean of score, weighted score
        sentiment_file = pd.read_csv(self.analyzeFile)
        sentiment_file['Date'] = pd.to_datetime(sentiment_file['Date']).dt.date
        # Group the data by date
        update_df = sentiment_file.groupby('Date')[['Score', 'W_Score', 'Relevance']].mean().round(4).reset_index()

        # Output to a file as score card
        if os.path.exists(self.scoreFile):
            old_df = pd.read_csv(self.scoreFile)

            old_df.set_index(['Date'])
            update_df.set_index(['Date'])

            new_df = update_df.combine_first(old_df)
            new_df['Date'] = pd.to_datetime(new_df['Date'])
            output_df = new_df.sort_values(by=['Date'])
            output_df.to_csv(self.scoreFile, index=False)

        else:
            update_df.to_csv(self.scoreFile, index=False)

        return update_df, news_link
