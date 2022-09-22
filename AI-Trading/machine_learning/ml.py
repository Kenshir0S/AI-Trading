from cProfile import label
import datetime
from typing import Any

import more_itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation
from keras.callbacks import EarlyStopping

from get_df import GetDataFrame


class PredClosePrice:
    def __init__(self, from_symbol: str, to_symbol: str, interval: str) -> None:
        """基軸通貨、決済通貨、取引間隔を設定

        Args:
            from_symbol (str): base currency
            to_symbol (str): payment currency
            interval (str): interval for trading
        """
        self.from_symbol = from_symbol
        self.to_symbol = to_symbol
        self.interval = interval
        self.scaler: MinMaxScaler
        self.model: Sequential

    def df_for_ml(self) -> pd.DataFrame:
        """機械学習用データフレーム作成

        Returns:
            pd.DataFrame: dataframe for machine learning
        """
        gdf = GetDataFrame(self.from_symbol, self.to_symbol, self.interval)
        fx_data = gdf.get_fx_data()
        df = gdf.create_df(fx_data)
        df = df.set_index("datetime")

        return df

    def lstm_model(self, df: pd.DataFrame) -> Any:
        """LSTMモデルとグラフを返す

        Args:
            df (pd.DataFrame): dataframe created from Alpha Vantage

        Returns:
            Any: Figure
        """
        data = list(map(lambda close_price: [close_price], df["close"]))

        self.scaler = MinMaxScaler()
        scaled_data = self.scaler.fit_transform(data)

        # TODO: 修正いるかも
        train_data = np.array(list(more_itertools.windowed(scaled_data[:-1], 100)))
        test_data = np.array(scaled_data[100:])

        early_stopping = EarlyStopping()

        self.model = Sequential()
        self.model.add(LSTM(300))
        # self.model.add(LSTM(300, return_sequences=True))
        # self.model.add(Dropout(0.2))
        # self.model.add(LSTM(300, return_sequences=False))
        # self.model.add(Dense(75))
        # self.model.add(Dense(50))
        # self.model.add(Dense(25))
        self.model.add(Dense(3))
        self.model.add(Dense(1, activation='linear'))
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(train_data, test_data, batch_size=600, epochs=10, validation_split=0.3, callbacks=[early_stopping])
        pred = self.model.predict(test_data)
        pred = list(map(lambda pred_price: [pred_price[0] * 10], pred))

        rmse = mean_squared_error(test_data, pred, squared=False)
        print("RMSE:", rmse)
        mae = mean_absolute_error(test_data, pred)
        print("MAE:", mae)

        fig = plt.figure(figsize=(16, 8))
        plt.title(f"{self.interval} {self.from_symbol}/{self.to_symbol}")
        plt.xticks(rotation=45)
        plt.ylabel(f"Close Price {self.to_symbol}", fontsize=14)
        plt.plot(self.scaler.inverse_transform(test_data), label="test")
        plt.plot(self.scaler.inverse_transform(pred), label="pred")
        plt.legend(loc="best")

        return fig, rmse, mae

    def get_future_close_price(self, df: pd.DataFrame) -> float:
        """終値の予測値を返す

        Args:
            df (pd.DataFrame): _description_
            model (Sequential): _description_

        Returns:
            float: next close price
        """
        data = list(map(lambda close_price: [close_price], df["close"]))

        scaled_data = self.scaler.transform(data)

        pred = self.model.predict(scaled_data)
        next_close_price = self.scaler.inverse_transform(pred)[0][0]

        return next_close_price