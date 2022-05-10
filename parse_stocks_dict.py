#try to combine all data into stock dictionary
#stock dictionary is a files where you can reference stock code to their page
import os, re
import pandas as pd
import numpy as np

directory = './data'
files = os.listdir(directory)
#filter files
files = [file for file in files if re.search('stocks_page_\d+.csv', file)]
data_list = []
for file in files:
    data = pd.read_csv('./data/{}'.format(file))
    data_list.append(data)
stock_data = pd.concat(data_list)
columsn = stock_data.columns
stock_data.rename(columns = {"Mã CK▲": "Mã CK", "Khối lượng NY/ĐKGD": "Khối lượng niên yết", "link": "Link"}, inplace=True)
columns = ["Mã CK", "Tên công ty", "Ngành", "Sàn", "Khối lượng niên yết", "Link"]
stock_data = stock_data[columns]
stock_data.to_csv('./data/stocks_dict.csv')