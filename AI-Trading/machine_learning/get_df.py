import os

import requests
import pandas as pd
from datetime import datetime

from settings import url, api_key, period, csv_path


class GetDataFrame():
    def __init__(self, from_symbol: str, to_symbol: str, interval: str) -> None:
        self.from_symbol = from_symbol
        self.to_symbol = to_symbol
        self.interval = interval

    def get_fx_data(self) -> dict:
        """ticker情報を返す

        Returns:
            dict: Json data from Alpha Vantege.
        """
        req_url = f"{url}function={period}&from_symbol={self.from_symbol}&to_symbol={self.to_symbol}&interval={self.interval}&outputsize=full&apikey={api_key}"
        res = requests.get(req_url)
        res_json = res.json()
        return res_json[f"Time Series FX ({self.interval})"]


    def create_df(self, tickers: dict) -> pd.DataFrame:
        """ticker情報からDataFrameを作成する

        Args:
            tickers (dict): Json data from Alpha Vantege.

        Returns:
            pd.DataFrame: columns=["datetime", "open", "high", "low", "close"]
        """
        dframe = []
        for dtime, ticker in tickers.items():
            index = []
            index.append(datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S"))
            open = float(ticker["1. open"])
            index.append(open)
            high = float(ticker["2. high"])
            index.append(high)
            low = float(ticker["3. low"])
            index.append(low)
            close = float(ticker["4. close"])
            index.append(close)
            dframe.append(index)

        df = pd.DataFrame(dframe)
        df = df.set_axis(["datetime", "open", "high", "low", "close"], axis=1)
        df = df.sort_values(by="datetime", axis=0, ascending=True, ignore_index=True)

        if not os.path.exists(f"{csv_path}hist_data_{self.from_symbol}{self.to_symbol}_{self.interval}.csv"):
            df.to_csv(f"{csv_path}hist_data_{self.from_symbol}{self.to_symbol}_{self.interval}.csv", index=False)

            return df

        hist_df = pd.read_csv(f"{csv_path}hist_data_{self.from_symbol}{self.to_symbol}_{self.interval}.csv", parse_dates=["datetime"])
        concat_df = pd.concat([df, hist_df], ignore_index=True)
        concat_df = concat_df.drop_duplicates()

        concat_df.to_csv(f"{csv_path}hist_data_{self.from_symbol}{self.to_symbol}_{self.interval}.csv", index=False)

        return concat_df
