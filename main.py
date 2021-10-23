import pandas as pd

from utils import GetStockList
from stock import Stock
from multiprocessing import Process, Lock

# If the user would like to display the detail in the console
display_detail = True

# Print Lock
lock = Lock()

# Maximum length of the panda dataframe to be displayed
pd.set_option('display.max_colwidth', 100)

stockList = GetStockList('stockList.csv').get_list()
stockList.columns = ["Ticker", "Names"]

process = []
for i in range(stockList.shape[0]):
    ticker, names = (stockList['Ticker'][i]), (stockList['Names'][i]).split(',')
    process.append(Process(target=Stock, args=(ticker, names, display_detail, lock)))

if __name__ == '__main__':
    for p in process:
        p.start()

    for p in process:
        p.join()
