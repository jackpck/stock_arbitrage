import numpy as np
import pandas as pd
import math as m
from sklearn import linear_model

'''
Convention: 
technical on day n is computed from n-lag to n-1.
return on day n is the profit if buy on day n and sell on day n + 1
'''

# Moving Average
def MA(df,lag,suffix=''):
	df_ma = df.shift(1).rolling(lag).mean()
	df_ma.name = 'MA' + suffix
	return df_ma

# Moving Stdev
def MSTD(df,lag,suffix=''):
	df_mstd = df.shift(1).rolling(lag).std()
	df_mstd.name = 'MSTD' + suffix
	return df_mstd

# Exponential Moving Average
def EMA(df,lag,suffix=''):
	df_ema = df.shift(1).ewm(span=lag,min_periods=lag).mean()
	df_ema.name = 'EMA' + suffix
	return df_ema

#Momentum
def MMT(df,lag,suffix=''):
	'''
	use lag-1 compare to other technicals
	'''
	df_mmt = df.shift(1).pct_change(lag-1) # pct_change: percentage change
	df_mmt.name = 'MMT' + suffix
	return df_mmt

#MACD
def MACD(df,lag_short,lag_long,suffix=''):
	df_macd =  EMA(df,lag_long) - EMA(df,lag_short)
	df_macd.name = 'MACD' + suffix
	return df_macd

#Bollinger Bands
def BBANDS(df,lag,fstd=2,suffix=''):
	'''
	distance to upper and lower Bollinger bands
	'''
	temp_MA = MA(df,lag)
	temp_MSTD = MSTD(df,lag)
	df_bolu = temp_MA + fstd*temp_MSTD - df
	df_bold = temp_MA - fstd*temp_MSTD - df

	df_bolu.name = 'BOLU' + suffix
	df_bold.name = 'BOLD' + suffix

	return df_bold,df_bolu



if __name__ == '__main__':
	from datetime import datetime
	from LoadData_API import LoadData
	import time

	startdate = datetime(2019, 1, 1)
	enddate = datetime(2020, 1, 1)
	P = LoadData(startdate, enddate)
	df_stock = P.getstocks('^GSPC')
	P.Aclose = df_stock['Adj Close']

	df_tech = MA(P.Aclose,2)
	df_mmt = MMT(P.Aclose,2)

	df_joint = P.Aclose.to_frame().join(df_tech,how='inner')
	df_joint = df_joint.join(df_mmt,how='inner')

	print(df_joint)
