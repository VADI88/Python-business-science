## Sktime
Docs: https://www.sktime.net/en/stable/examples/00_sktime_intro.html


What is AutoArima ? 

ARIMA and AutoARIMA are statistical methods used for time series forecasting, particularly when the data shows patterns over time (like trends or seasonality).

## ARIMA: AutoRegressive Integrated Moving Average
ARIMA is a model used to analyze and forecast time series data. It combines three components:

AR (AutoRegressive): The model uses the relationship between an observation and a number of lagged observations (past values).
I (Integrated): This part involves differencing the data to make it stationary (i.e., removing trends or seasonality).
MA (Moving Average): The model uses the relationship between an observation and residual errors from a moving average model applied to lagged observations.
Notation: ARIMA(p, d, q)

p: number of autoregressive terms (AR)
d: number of differencing steps (I)
q: number of moving average terms (MA)
Example use case: Forecasting monthly sales, stock prices, weather patterns, etc. 

## AutoARIMA (Automatic ARIMA)
AutoARIMA is a version of ARIMA that automatically selects the best values for p, d, and q by minimizing metrics like AIC (Akaike Information Criterion) or BIC (Bayesian Information Criterion). It simplifies the modeling process by avoiding manual tuning.

Saves time and reduces complexity.
Uses statistical tests (like ADF test for stationarity) and model selection criteria to choose the best model.


