import pandas as pd
import numpy as np
import os


def MakePriceMatrix():
    path = '../data/processed/2010_2020/'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(file))

    df = pd.DataFrame()
    null_fraction = 0.2

    for i, file in enumerate(files):
        df_close = pd.read_csv(path + file, index_col=0)['Adj Close']
        if null_fraction * len(df_close) > df_close.isnull().sum():  # only keep stocks that have > 80% of price recorded
            df_close.name = file.split('.')[0]
            df = pd.concat([df, df_close], axis=1, join='outer')

    df.to_csv('../data/processed/combined/' + 'stock_aclose_2010_2020.csv')


if __name__ == '__main__':
    #MakePriceMatrix()

