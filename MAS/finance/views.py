from django.shortcuts import render
import pandas_datareader.data as web
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from .forms import ForeignExchangeForm, SearchStockByName
import warnings
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from django.contrib.auth.decorators import login_required

warnings.filterwarnings("ignore")


@login_required
def foreign_exchange(request):

    if request.method == 'POST':
        form = ForeignExchangeForm(request.POST)
        curr1 = request.POST['curr1']
        curr2 = request.POST['curr2']
        if form.is_valid():
            ends = datetime.today()
            ends = datetime(ends.year, ends.month, ends.day)
            currfinal = curr1 + "/" + curr2

            df = web.DataReader(currfinal, "av-forex-daily", start=datetime(2016, 1, 1), end=ends,
                                api_key='O8R4CJHM0DC8Y9XR')

            new_data = df[['close']]
            # dataset = new_data.values

            dataset = new_data.values

            t = int(len(df) * 0.8)

            train = dataset[0:t, :]
            valid = dataset[t:, :]

            # converting dataset into x_train and y_train
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            x_train, y_train = [], []
            for i in range(60, len(train)):
                x_train.append(scaled_data[i - 60:i, 0])
                y_train.append(scaled_data[i, 0])
            x_train, y_train = np.array(x_train), np.array(y_train)

            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            # create and fit the LSTM network
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(units=50))
            model.add(Dense(1))

            model.compile(loss='mean_squared_error', optimizer='adam')
            model.fit(x_train, y_train, epochs=2, batch_size=1, verbose=2)

            inputs = new_data[len(new_data) - len(valid) - 60:].values
            inputs = inputs.reshape(-1, 1)
            inputs = scaler.transform(inputs)

            X_test = []
            for i in range(60, inputs.shape[0]):
                X_test.append(inputs[i - 60:i, 0])
            X_test = np.array(X_test)

            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            closing_price = model.predict(X_test)
            closing_price = scaler.inverse_transform(closing_price)

           #  rms = np.sqrt(np.mean(np.power((valid - closing_price), 2)))

            train = new_data[:t]
            valid = new_data[t:]
            valid['Predictions'] = closing_price

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train.index, y=train['close'], mode='lines', line=dict(color="#ff0000"),
                                     name='Historical'))
            fig.add_trace(
                go.Scatter(x=valid.index, y=valid['close'], mode='lines', line=dict(color="#0000ff"), name='Known'))
            fig.add_trace(go.Scatter(x=valid.index, y=valid['Predictions'], mode='lines', line=dict(color="#00ff00"),
                                     name='Predictions'))

            fig.update_layout(
                title= curr1 + "/" + curr2 + " FOREIGN EXCHANGE RATE PREDICTION",
                xaxis_title="TIME",
                yaxis_title="FX RATES")
            graph = fig.to_html(full_html=False, default_height=600, default_width=1000)
            future = df.iloc[-1]['close']

            return render(request, "finance/foreign_exchange.html", context={'graph': graph, 'future': future})
    else:
        form = ForeignExchangeForm()
    return render(request, 'finance/search_currency.html', context={'form': form})


@login_required
def stock_prediction(request):
    if request.method == 'POST':
        form = SearchStockByName(request.POST)
        stock_name = request.POST['stock_name']
        if form.is_valid():
            key = "12b47fa6f88e699ef0dd902373f1fbe5d8068127"
            df1 = pdr.get_data_tiingo(stock_name, api_key=key)
            df1.reset_index(inplace=True)
            df1.set_index('date', inplace=True)
            new_data = df1[['adjClose']]
            dataset = new_data.values
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            t = int(len(df1) * 0.8)

            train = dataset[0:t, :]
            valid = dataset[t:, :]

            x_train, y_train = [], []
            for i in range(60, len(train)):
                x_train.append(scaled_data[i - 60:i, 0])
                y_train.append(scaled_data[i, 0])
            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
            model.add(LSTM(units=50))
            model.add(Dense(1))

            model.compile(loss='mean_squared_error', optimizer='adam')
            model.fit(x_train, y_train, epochs=2, batch_size=1, verbose=2)

            inputs = new_data[len(new_data) - len(valid) - 60:].values
            inputs = inputs.reshape(-1, 1)
            inputs = scaler.transform(inputs)

            X_test = []
            for i in range(60, inputs.shape[0]):
                X_test.append(inputs[i - 60:i, 0])
            X_test = np.array(X_test)

            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            closing_price = model.predict(X_test)
            closing_price = scaler.inverse_transform(closing_price)

            #  rms = np.sqrt(np.mean(np.power((valid - closing_price), 2)))
            train = new_data[:t]
            valid = new_data[t:]
            valid['Predictions'] = closing_price
            import plotly.graph_objects as go

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=train.index, y=train['adjClose'], mode='lines', line=dict(color="#ff0000"),
                                     name='Historical'))
            fig.add_trace(
                go.Scatter(x=valid.index, y=valid['adjClose'], mode='lines', line=dict(color="#0000ff"), name='Known'))
            fig.add_trace(go.Scatter(x=valid.index, y=valid['Predictions'], mode='lines', line=dict(color="#00ff00"),
                                     name='Predictions'))

            fig.update_layout(
                title=stock_name + " STOCK PREDICTION DYNAMICALLY",
                xaxis_title = "TIME",
                yaxis_title = "MARKET VALUE")
            graph = fig.to_html(full_html=False, default_height=600, default_width=1000)
            future = df1.iloc[-1]['adjClose']
            return render(request, "finance/stock_prediction_result.html", context={'graph': graph, 'future': future})

    else:
        form = SearchStockByName()
    return render(request, 'finance/stock_prediction.html', context={'form': form})