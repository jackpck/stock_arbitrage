import pandas as pd
import numpy as np
from scipy.stats import t

def autocorrelation(df_return,lag):
    df_autocorr = df_return.apply(lambda col: col.autocorr(lag), axis=0)
    df_autocorr.name = 'autocorr'
    df_autocorr = df_autocorr.to_frame()

    return df_autocorr


def autocorr_ttest(df_autocorr,df_N):
    '''
    df_autocorr: dataframe of autocorr of a collection of stocks
    df_N: number of non-nan return for each stocks.
    df_N = (~df_return.isnull()).sum()  # number of non-nan return
    '''

    p_values = {ticker: 1. -
                        t.cdf(np.abs(df_autocorr['autocorr'][ticker]) * np.sqrt(df_N[ticker] - 2)/
                        np.sqrt(1 - np.abs(df_autocorr['autocorr'][ticker]) ** 2), df_N[ticker])
                        for ticker in df_autocorr.index}

    df_p_value = pd.Series(p_values).to_frame()
    df_p_value.columns = ['p-value']

    return df_p_value

def get_significant_stocks(df_return,startyear,endyear):
    significant_stocks = dict()
    years = np.arange(startyear,endyear,1)

    for yr in years:
        period_mask = df_return.index.year == yr
        df_return_period = df_return[period_mask]
        N = len(df_return_period)

        df_autocorr = autocorrelation(df_return_period,1)
        df_p_value = autocorr_ttest(df_autocorr,N)

        significant_stocks[yr] = df_p_value.index[df_p_value['p-value'] < 0.05].tolist()

    return significant_stocks


def get_consistent_stocks(significant_stocks):
    startyear = min(significant_stocks)
    endyear = max(significant_stocks)
    consistent_stocks = set(significant_stocks[startyear])

    for yr in np.arange(startyear,endyear+1,1):
        consistent_stocks = consistent_stocks.intersection(set(significant_stocks[yr]))

    return consistent_stocks


if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv('../data/processed/combined/' + 'stock_aclose_2010_2020.csv',index_col=0)
    lag = 1
    df_return = df.pct_change(lag)[::lag]

    # if nan (e.g. stop trading, not listed etc), return will be 0
    df_return = df_return.fillna(0)
    df_return.index = pd.to_datetime(df_return.index)

    significant_stocks = get_significant_stocks(df_return,2010,2015)
    consistent_stocks = get_consistent_stocks(significant_stocks)


