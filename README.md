 
# Sentiment Analysis of Stock News  
___  
 
### Description  
This program aims to analyze the polarity of news sentiment. News can greatly influence trading patterns in the stock market.  
The objective of this program is to analyze such sentiment to a certain extent. It utilizes SENTIMENT INTENSITY ANALYZER from Natural Language Toolkit. <br/>  
There are two types of scores calculated: Mean Score and Weighted Score.<br/>  
 
1. Mean Score: This score is the average sentiment from all news article for a particular company. It does not take consideration about the relevancy of a news article.  
2. Weighted Score: Weighted score is calculated after evaluation of relevancy of a news article. Each article is broken down into paragraphs and then into sentences.  
Irrelevant paragraphs are discarded. It records the number of times a company is mentioned in a paragraph and generates a relevance score. This score is then utilized to calculate  
the weighted score.  
<br/>  
The news articles are scrapped from Yahoo Finance and the links to the news are extracted from FINVIZ.com

 
### Output 
To display the background process, follow Note 2 mentioned below.<br/> 
Once the news articles are processed their outputs are displayed in the "tickers" folder under the respective company's symbol.<br/> 
1. latest_update.csv: The hyperlink of news that is processed in the last run. 
2. news_content.csv: Cumulative content for all the runs. 
3. scoreCard.csv: Scores card for the company by date. 
4. sentiment_analysis.csv: Information pertaining to each news article and the scores for each line of the paragraph. 
 
 
### Update RUN 
The program will display " NO update news since........", it means all the latest news are processed and there are no new ones in yahoo news for the particular ticker. <br/> 
To process the company's news again delete "news_content.csv"  
 
### Dependencies  
1. python 3.9  
2. pandas~=1.2.3  
3. Scrapy~=2.4.1  
4. finviz~=1.3.4  
5. itemadapter~=0.2.0  
6. nltk~=3.5  
7. scrapy~=2.4.1  
 
### Note *  
1. The program runs from main.py. <br/>  
2. Main.py has an option to display details of the process. (display_detail = True). False to hide the background process.  
3. The program is preloaded with three company ticker symbol and company's name. More companies can be added as desired.  
4. Reminder: - For better accuracy include a general name used for the company. For example: Google or Alphabet for Google LLC  
5. Avoid inserting company's full name like NVIDIA Corporation, only insert NVIDIA  
6. Check stockList.csv for the format  
 
### Author  
@praddil  
I am a student in computer science. I do these projects to expand my knowledge outside of classroom environment. 


#### DISCLAIMER 
The sentiment calculated in this project is mere estimation. There are numerous other factors that affect the stock market.