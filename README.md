# Stock selection and arbitrage

## Introduciton
One of the golden rules in finance is the no-arbitrage principle: if there is a way to make money in a riskless way, people
will exploit this strategy until it is no longer profitable. This is usually true for heavily traded stocks or indices like
GOOG, AMZN, S&P500 etc. as they are constantly under scrutiny of a highly competitive market. However, stocks which are
thinnly traded might offer arbitrage opporunities, simply because less people are looking at it. In this project I will
look at the possibility of aribrage, and ultimately profit for over 3000 US stocks, which consist of stocks of all cap size.

## Autocorrelation
Autocorrelation is probably the simpliest source of arbitrage. But despite its simplicity, it is often misused to draw a
conclusion to profitability. In `./notebook/arbitrage.ipynb`, I first showed how easy it is to conclude significant
autocorrelation if one did not pay close attention to the data. I explored the autocorrelation of 3522 US stocks and chose
stocks which have significant autocorrelation. I backtested it by deploying a simple autocorrelation arbitrage strategy in the
year after the stocks were chosen based on their autocorrelations. I showed that an autocorrelation arbitrage strategy using
daily returns is not profitable but the same strategy using weekly returns is, in theory, profitable.