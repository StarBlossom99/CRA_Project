import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
import logging
import seaborn as sns
from fbprophet.plot import plot_plotly, plot_components_plotly
# from statsmodels.tsa.arima_model import ARIMA
# import statsmodels.api as sm

data = pd.read_csv("C:/CRAproject/today_20220203/005930.csv", parse_dates=['일자'], dtype={'종목코드' : str}, header = 0, index_col=0, squeeze=True)
data = data.fillna(0)
data = data.loc[:,['일자', '현재가', '시가', '고가', '저가', '거래량']]
print(data)
data.rename(columns= {'현재가':'y', '일자':'day', '시가':'open', '고가':'high', '저가':'low', '거래량':'volume'}, inplace=True)
data['ds'] = data['day'].apply(lambda x : x)
print(data)
data.set_index('day', inplace=True)

print(data)

plt.figure(figsize=(16, 9))
sns.lineplot(x=data.index, y='y', data=data)
plt.show()

logger = logging.getLogger('fbprophet')
logger.setLevel(logging.DEBUG)

m = Prophet()
print(m.stan_backend)
# model = Prophet()
# model.fit(data)

# future = model.make_future_dataframe(periods=30)
# print(future)

# prophet = Prophet(seasonality_mode = 'multiplicative',
#                  yearly_seasonality=True, 
#                  weekly_seasonality=True,
#                  daily_seasonality=True,
#                  changepoint_prior_scale=0.5)

# prophet.fit(data)

# future_data = prophet.make_future_dataframe(periods = 5, freq = 'd')
# forecast_data = prophet.predict(future_data)
# forecast_data[['ds','yhat', 'yhat_lower', 'yhat_upper']].tail(5)



# plt.xlabel("일자")
# plt.ylabel("현재가")
# ax = plt.gca()

# data.plot(kind='line', ax=ax, y = '현재가', x = '일자')
# plt.show()
# model = ARIMA(data.price.values, order=(2,1,2))
# model_fit = model.fit(trend = 'c', full_output = True, disp = True)
# print(model_fit.summary())