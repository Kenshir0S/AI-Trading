import streamlit as st

from select_menu import select_pair_interval


def main():
    st.set_page_config(
        page_title = "為替価格予測アプリ",
        page_icon = ":yen:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("為替価格予測アプリ :yen:")

    select_pair_interval()


if __name__ == "__main__":
    main()