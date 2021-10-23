import scrapy
import re
import csv


class GetinfoSpider(scrapy.Spider):

    name = "getinfo_spider"

    def __init__(self, start_urls, filepath, stock_name, updatefile):
        self.start_urls = start_urls    # Urls to update
        self.stock_name = stock_name   # Ticker name of the stock
        self.filepath = filepath        # File path to the cumulative news content
        self.updatefile = updatefile    # File with the updated news

        # Cleaning the update file for new updates to be posted
        with open(self.updatefile, "w") as update:
            update.truncate()
        update.close()

    def parse(self, response):

        avoid_words = ["Inc.", "Corp.", "Assoc.", "No.", "no.", "U.S.", "U.S.A.", "U.K.", "Co."]

        # Regex to remove all words/number with a period in between
        regex_1st = re.compile(r'\S+[\.,]\S+')
        # Regex to remove alphanumeric
        regex_2nd = re.compile(r'[a-zA-Z]+\d+')
        # to include only period, alphabets and space
        regex_3rd = re.compile(r'[^.a-zA-Z\s]')
        # regex to check if the paragraph ends with a period
        regex_4th = re.compile(r'\.[\'"]?$')

        # List of paragraphs that has the stock name mentioned
        imp_para = ""
        # List of all paragraphs from the news
        orig_content = []

        # Counts the occurrence of stock name
        count = 0

        # # from the div tags Get date and Author and headlines
        date = response.css('.caas-attr-time-style time::text').get()
        author = response.xpath('.//div[@class="caas-attr-meta"]//text()').get()
        headline = response.css('h1::text').get()

        # Get to the 'caas-body' class which homes the news content
        body = response.xpath('//div[@class="caas-body"]')

        # Loop through all the paragraphs in the news and inner loops for each item in the paragraph
        if len(body) > 0:
            for paragraphs in body:
                for item in paragraphs.xpath('.//p')[:]:
                    # Scraps the text of all items
                    portions = item.xpath('.//text()').getall()

                    # loops through all the portion's text and concatenates
                    complete_para = "".join([str(each_element) for each_element in portions])
                    # Adds the paragraph to create full news content
                    orig_content.append(complete_para)

                    # Condition to check if the stock name is mentioned in the paragraph
                    occurrence = sum([complete_para.count(name) for name in self.stock_name])

                    if occurrence > 0:
                        # Adds the number of occurrence
                        count += occurrence
                        # Adds the paragraph to the relevant news content and cleans unwanted words
                        cleaned_para = " ".join([word for word in re.split(r'\s+', complete_para) if not regex_1st.match(word)
                                                 and not regex_2nd.match(word) and word not in avoid_words])
                        # cleans for unwanted characters other that alphabet
                        cleaned_para = regex_3rd.sub("", cleaned_para)
                        # Adds a period if missing at the end of the paragraph
                        if not regex_4th.findall(cleaned_para):
                            imp_para = imp_para + "."
                        # Paragraph that are relevant to the stock
                        imp_para = imp_para + (str(cleaned_para))

                if count < 8:
                    count = round(count/7, 4)
                elif count < 15:
                    count = round((count/14) + 0.5, 4)
                else:
                    count = 1.5

            # File that will contain all news
            with open(self.filepath, "a", newline="", encoding='utf-8',) as f:
                writer = csv.writer(f)
                writer.writerow([date, author, headline, orig_content, imp_para, response.request.url, count])
            # File that will contain the latest update
            with open(self.updatefile, "a", newline="", encoding='utf-8',) as u:
                writer = csv.writer(u)
                writer.writerow([date, author, headline, orig_content, imp_para, response.request.url, count])

            f.close()
            u.close()
        else:
            pass
