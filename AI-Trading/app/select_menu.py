import streamlit as st

from views import show_close_price


from_symbol_list = ["USD", "JPY", "GBP", "EUR", "CAD", "AUD"]
to_symbol_list = ["JPY", "USD", "EUR", "GBP", "AUD", "CAD"]
interval_list = ["1min", "5min", "15min", "30min", "60min"]

def select_pair_interval():
    from_symbol_index = from_symbol_list.index("USD")
    from_symbol = st.sidebar.selectbox("基軸通貨を選択してください", from_symbol_list, index=from_symbol_index)
    to_symbol_index = to_symbol_list.index("JPY")
    to_symbol = st.sidebar.selectbox("決済通貨を選択してください", [to_symbol for to_symbol in to_symbol_list if to_symbol != from_symbol], index=to_symbol_index)
    interval_index = interval_list.index("1min")
    interval = st.sidebar.selectbox("取引間隔を選択してください", interval_list, index=interval_index)

    show_close_price(from_symbol, to_symbol, interval)
