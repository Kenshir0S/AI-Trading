# AI-Trading
## 設定

```
pip install -r requirements.txt
```
を実行して、アプリ起動に必要なパッケージをインストールしてください。

[AlphaVantage](https://www.alphavantage.co/support/#api-key) からAPIキーを取得してください。  
取得したAPIキーをAI-Trading/config.iniのapi_keyに設定してください。

## 実行・終了

```
cd AI-Trading/app
streamlit run main.py
```
でアプリが起動します。  
Ctrl + Cでアプリを終了します。

## 補足

CSVファイルのTickerデータは起動、または更新ボタンを押すたびに新しいTickerデータが蓄積されていきます。  
なので、段々と予測の精度が上がっていくと思います。