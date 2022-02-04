import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
# from statsmodels.tsa.arima_model import ARIMA
# import statsmodels.api as sm

data = pd.read_csv("C:/CRAproject/today_20220128/005930.csv", parse_dates=['일자'], dtype={'종목코드' : str}, header = 0, index_col=0, squeeze=True)
data = data.fillna(0)
data = data.loc[:,['일자', '현재가']]
print(data)
data.rename(columns= {'현재가':'y', '일자':'ds'}, inplace=True)
# data.set_index('day', inplace=True)
print(data)


prophet = Prophet(seasonality_mode = 'multiplicative',
                 yearly_seasonality=True, 
                 weekly_seasonality=True,
                 daily_seasonality=True,
                 changepoint_prior_scale=0.5)

prophet.fit(data)

future_data = prophet.make_future_dataframe(periods = 5, freq = 'd')
forecast_data = prophet.predict(future_data)
forecast_data[['ds','yhat', 'yhat_lower', 'yhat_upper']].tail(5)
# plt.xlabel("일자")
# plt.ylabel("현재가")
# ax = plt.gca()

# data.plot(kind='line', ax=ax, y = '현재가', x = '일자')
# plt.show()
# model = ARIMA(data.price.values, order=(2,1,2))
# model_fit = model.fit(trend = 'c', full_output = True, disp = True)
# print(model_fit.summary())