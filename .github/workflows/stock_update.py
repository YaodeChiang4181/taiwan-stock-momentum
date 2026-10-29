import requests
import pandas as pd
from datetime import datetime

# 測試版資料
stocks = [
    {"Ticker": "2330", "Name": "台積電"},
    {"Ticker": "2454", "Name": "聯發科"},
    {"Ticker": "2308", "Name": "台達電"},
]

result = []

for s in stocks:

    score = 80

    result.append({
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Ticker": s["Ticker"],
        "Name": s["Name"],
        "Market": "上市",
        "Score": score,
        "MomentumScore": score,
        "FlowScore": 70,
        "MAScore": 75,
        "MACDScore": 80,
        "RSIScore": 65,
        "RiskFlag": "TEST"
    })

df = pd.DataFrame(result)

df.to_csv(
    "momentum_ranking.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df)
