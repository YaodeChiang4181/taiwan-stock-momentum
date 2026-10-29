import pandas as pd
import requests
from datetime import datetime

WATCHLIST = [
    ("2330", "台積電"),
    ("2454", "聯發科"),
    ("2308", "台達電"),
    ("2382", "廣達"),
    ("3661", "世芯-KY"),
    ("3231", "緯創")
]

def get_month_data(stock_no):

    url = (
        "https://www.twse.com.tw/exchangeReport/STOCK_DAY"
    )

    params = {
        "response": "json",
        "stockNo": stock_no
    }

    r = requests.get(url, params=params, timeout=30)

    data = r.json()

    if "data" not in data:
        return None

    rows = []

    for row in data["data"]:
        try:
            rows.append(
                float(
                    row[6].replace(",", "")
                )
            )
        except:
            pass

    return rows


def calc_score(close_list):

    if len(close_list) < 20:
        return None

    latest = close_list[-1]

    r5 = (latest / close_list[-5] - 1) * 100
    r10 = (latest / close_list[-10] - 1) * 100
    r20 = (latest / close_list[0] - 1) * 100

    score = (
        r5 * 0.4
        + r10 * 0.3
        + r20 * 0.3
    )

    return round(score, 2)


result = []

for ticker, name in WATCHLIST:

    closes = get_month_data(ticker)

    if not closes:
        continue

    score = calc_score(closes)

    if score is None:
        continue

    result.append({
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Ticker": ticker,
        "Name": name,
        "Market": "TWSE",
        "Score": score
    })

df = pd.DataFrame(result)

df = df.sort_values(
    "Score",
    ascending=False
)

df.to_csv(
    "momentum_ranking.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df)
