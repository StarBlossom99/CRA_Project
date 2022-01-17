import pandas as pd
import numpy as np

df = pd.DataFrame({'One':[100,200],'Two' : [300,400]})
df = df.rename({'One':'New_One', 'Two':'New_Two'}, axis='columns')

df.columns = df.columns.str.replace('_', '+')
# print(df)
df2 = pd.DataFrame(np.random.rand(4,8), columns=list('ABCDEFGH'))
# print(df2)

tit = pd.read_csv("C:/CRAproject/train.csv")
print(tit.loc[:,::-1].head(10))

print(tit.groupby('Pclass').Age.agg(['mean', 'count', 'min', 'max']))

