import os, sys
sys.path.append(os.path.join('..', 'machine_learning'))

import streamlit as st

from ml import PredClosePrice


def show_close_price(from_symbol: str, to_symbol: str, interval: str):
    pcp = PredClosePrice(from_symbol, to_symbol, interval)
    df = pcp.df_for_ml()
    fig, rmse, mae = pcp.lstm_model(df)
    pred_close_price = pcp.get_future_close_price(df)

    st.write(f"予測終値: {pred_close_price} RMSE: {rmse} MAE: {mae}")

    st.sidebar.button("更新")

    st.pyplot(fig)