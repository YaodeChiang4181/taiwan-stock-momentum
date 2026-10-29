import pandas as pd
import requests
from datetime import datetime

WATCHLIST = [
    ("2330", "台積電"),
    ("2454", "聯發科"),
    ("2308", "台達電"),
    ("2382", "廣達"),
    ("3231", "緯創"),
    ("3661", "世芯-KY"),
]

def get_twse_data(stock_no):

    url = (
        "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
    )

    params = {
        "response": "json",
        "stockNo": stock_no
    }

    r = requests.get(
        url,
        params=params,
        timeout=30
    )

    data = r.json()

    closes = []

    if "data" not in data:
        return closes

    for row in data["data"]:

        try:
            close_price = float(
                row[6].replace(",", "")
            )

            closes.append(close_price)

        except:
            pass

    return closes


def calc_score(close):

    if len(close) < 20:
        return None

    last = close[-1]

    r5 = (last / close[-5] - 1) * 100
    r10 = (last / close[-10] - 1) * 100
    r20 = (last / close[0] - 1) * 100

    return round(
        r5 * 0.4 +
        r10 * 0.3 +
        r20 * 0.3,
        2
    )

result = []

for ticker, name in WATCHLIST:

    closes = get_twse_data(ticker)

    score = calc_score(closes)

    if score is None:
        continue

    result.append({
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Ticker": ticker,
        "Name": name,
        "Market": "上市",
        "Score": score
    })

df = pd.DataFrame(result)

df = df.sort_values(
    "Score",
    ascending=False
)

print(df)

df.to_csv(
    "momentum_ranking.csv",
    index=False,
    encoding="utf-8-sig"
)
