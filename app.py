import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

start = '2015-01-01'
today = date.today().strftime('%Y-%m-%d')

st.title("Stock Prediction App")

stocks = ('AAPL','GOOG','MSFT','GME')
selected_stocks = st.selectbox('Select dataset for prediction',stocks)

n_years = st.slider('Years of Prediction :',1,4)
period = n_years*365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker,start,today)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Load Data ...')
data = load_data(selected_stocks)
data_load_state.text('Loading data..done!')

st.subheader('Raw Data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_closed'))
    fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_raw_data()

#Forecasting
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={'Date':'ds','Close':'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

st.subheader('Forecast Data')
st.write(forecast.tail())

st.write('Forecast Data')
fig1 = plot_plotly(m,forecast)
st.plotly_chart(fig1)

st.write('Forecast Components')
fig2 = m.plot_components(forecast)
st.write(fig2)

