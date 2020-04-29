import numpy as np
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class LoadData:
	def __init__(self,startdate,enddate):
		self.startdate = startdate
		self.enddate = enddate
		self.High = pd.DataFrame()
		self.Low = pd.DataFrame()
		self.Open = pd.DataFrame()
		self.Close = pd.DataFrame()
		self.AClose = pd.DataFrame()
		self.Volume = pd.DataFrame()
		self.Datetime = dict()

	def getstocks(self,ticker):
		_keyerror = 0
		try:
			df = pdr.get_data_yahoo(ticker,
									start=self.startdate,
									end=self.enddate)
			return df

		except pdr._utils.RemoteDataError:
			print('ticker symbol %s does not exist. Skip %s.'%(ticker,ticker))
			return
		except KeyError:
			print('%s does not exist during the time interval. Skip %s'%(ticker,ticker))
			return


	def joinstocks(self,tickers):
		df_bundle = pd.DataFrame()

		for ticker in tickers:
			df_close = self.getstocks(ticker)
			if df_close is not None:
				df_close = df_close['Adj Close'].to_frame()
				df_close.columns = ['Adj Close_%s'%ticker]
				df_bundle = pd.concat([df_bundle, df_close], axis=1)

		return df_bundle


	def loadstocks(self,df,freq='B'):
		df = df.asfreq(freq).fillna(method='pad')  # asfreq('B'): business day (weekday), regardless of holidays
															# fillna(method='pad'): pad NAN by previous value. Pad only Bday

		self.AClose = df['Adj Close']
		self.Volume = df['Volume']
		


if __name__ == "__main__":
	import seaborn as sns
	import time

	sns.set()

	starttime = time.time()

	tickers = []

	for ticker in open('../data/raw/stock_tickers.txt'):
		tickers.append(ticker.rstrip())

	startdate = datetime(2010,1,1)
	enddate = datetime(2020,1,1)
	E1 = LoadData(startdate,enddate)

	for i,ticker in enumerate(tickers):
		print(i,ticker)
		df_stock = E1.getstocks(ticker)
		if df_stock is not None:
			df_stock.to_csv('../data/processed/%i_%i/'%(startdate.year,enddate.year) + '%s.csv'%ticker)


	print('time spent: ',time.time() - starttime)

	#df_bundle.to_csv('../data/processed/%i_%i/stock_data.csv'%(startdate.year,enddate.year))

	#df_bundle.plot(y=df_bundle.columns)
	#plt.show()
