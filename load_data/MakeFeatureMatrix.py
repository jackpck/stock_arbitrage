import technicals as Tech
from datetime import datetime
from LoadData_API import LoadData
import time

def MakeFeatureMatrix(ticker,startdate,enddate):
    P = LoadData(startdate, enddate)
    df_stock = P.getstocks(ticker)
    P.Aclose = df_stock['Adj Close']
    P.Volume = df_stock['Volume']

    lag = 2

    df_joint = P.Aclose.to_frame().join(Tech.MA(P.Aclose, lag))

    df_joint = df_joint.join(Tech.MMT(P.Aclose, lag))
    df_joint = df_joint.join(Tech.MACD(P.Aclose, lag, lag + lag))
    df_joint = df_joint.join(Tech.MA(P.Volume, lag, suffix = '_VOL'))
    df_joint = df_joint.join(Tech.MMT(P.Volume, lag, suffix = '_VOL'))
    df_joint = df_joint.join(Tech.MACD(P.Volume, lag, lag + lag, suffix = '_VOL'))


    Close_return = P.Aclose.shift(-1).pct_change(1) # return if buy today and sell tomorrow
    Close_return.name = 'Yreturn'
    df_joint = df_joint.join(Close_return, how='inner')

    df_joint.pop('Adj Close')
    Y = df_joint.pop('Yreturn')

    return df_joint[2*lag:], Y[2*lag:]




if __name__ == '__main__':
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import r2_score

    startdate = datetime(2017, 1, 1)
    enddate = datetime(2020, 1, 1)

    df_X, df_Y = MakeFeatureMatrix('^GSPC',startdate,enddate)

    N = len(df_X)
    Ntrain = int(0.7*N)
    Ntest = N - Ntrain

    X = df_X.values
    Y = df_Y.values
    Xtrain, Xtest = X[:Ntrain], X[Ntrain:]
    Ytrain, Ytest = Y[:Ntrain], Y[Ntrain:]

    params = {'n_estimators':[10,20,30,40,50],'max_depth':[2,3,4,5,6,7]}
    regr_cv = GridSearchCV(RandomForestRegressor(),
                           param_grid=params,
                           cv=5)

    regr_cv.fit(Xtrain,Ytrain)

    Ytrain_pred = regr_cv.predict(Xtrain)
    Ytest_pred = regr_cv.predict(Xtest)

    print('r2 score: ',r2_score(Ytest,Ytest_pred))

