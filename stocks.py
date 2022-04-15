from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override()
import pandas as pd
import altair as alt
import altair_viewer
from altair_saver import save





# data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
# print(data.info())
# Tickers list
# We can add and delete any ticker from the list to get desired ticker live data
# ticker_list=['^DJI', 'DOW', 'LB', 'EXPE', 'PXD', 'MCHP', 'CRM', 'JEC' , 'NRG', 'HFC', 'NOW']
ticker_list=['dis']

today = date.today()

# We can get data by our choice by giving days bracket
start_date= "2017-01-01"
end_date="2022-02-28"
files=[]


# Create a data folder in your current dir.
def SaveData(df, filename):
    df.to_csv('./data/'+filename+'.csv')

def SaveImage(chart,ticker):
    chart.save('./data/'+ticker+'.png')

def getData(ticker):

    data = pdr.get_data_yahoo(ticker, start=start_date, end=today).reset_index()
    data['dayofyear']=pd.DatetimeIndex(data['Date']).dayofyear
    data['month'] = pd.DatetimeIndex(data['Date']).month
    data['month_name'] = pd.DatetimeIndex(data['Date']).month_name()
    data['year'] = pd.DatetimeIndex(data['Date']).year
    dataname= ticker+'_'+str(today)
    files.append(dataname)
    print(data.info())
    dayofyear_chart = alt.Chart(data).mark_line().encode(
        x=alt.X('dayofyear', axis = alt.Axis(title = 'Day of the year'.upper())),
        y='mean(Close)',
        color=alt.Color('year:N', legend=alt.Legend(title="Year"), scale=alt.Scale(scheme='spectral',reverse=True))
    ).properties(width =500, height=250)
    month_chart = alt.Chart(data).mark_line().encode(
        x=alt.X('month_name', axis = alt.Axis(title = 'month_name'.upper()),
                sort=alt.SortField("month", order="ascending")),
        y='mean(Close)',
        color=alt.Color('year:N', legend=alt.Legend(title="Year"),
                        scale=alt.Scale(scheme='spectral',reverse=True))
    ).properties(width =500, height=250)
    full_chart= alt.vconcat(dayofyear_chart,month_chart).properties(title=ticker)
    altair_viewer.display(full_chart)
    s = './data/'+ticker+'.png'
    print (s)
    full_chart.save(s)
    # SaveImage(chart,ticker)
    SaveData(data, dataname)


#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as file.
for tik in ticker_list:
    getData(tik)

for i in range(0,1):
    df1= pd.read_csv('./data/'+ str(files[i])+'.csv')
    print (df1.head())