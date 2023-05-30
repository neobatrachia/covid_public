import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Prefecture = "ALL"
Prefecture = "Chiba"
#Prefecture = "Tokyo"

n_steps           = 7 #number of rolling steps for the mean/std.
c_interval        = 1 #68.3%
#c_interval        = 2 #95.4%


# https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv

url = 'https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv'
ordata = pd.read_csv(io.BytesIO(requests.get(url).content),sep=",") 


ordata['Date'] = pd.to_datetime(ordata['Date'])
ordata.reset_index(drop=True, inplace=True)
time_series_df = ordata[["Date",Prefecture]]


time_series_df['meanstp'] = time_series_df[Prefecture].rolling(n_steps).mean()
time_series_df['stdstep'] = time_series_df[Prefecture].rolling(n_steps).std() * c_interval
time_series_df['under_line']     = time_series_df['meanstp']-time_series_df['stdstep']
time_series_df['over_line']      = time_series_df['meanstp']+time_series_df['stdstep']

print (time_series_df)

grp=sns.relplot(data=time_series_df,
                x='Date', 
                y=Prefecture,
                size=(1),
                aspect=3)
grp.map(sns.lineplot,data=time_series_df,
                x='Date', 
                y='meanstp',
                color='green' )

plt.fill_between(time_series_df['Date'], time_series_df['under_line'], time_series_df['over_line'],color="red", alpha=0.30)
plt.show()

