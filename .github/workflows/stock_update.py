import os
import requests

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

token_url = (
    f"https://login.microsoftonline.com/"
    f"{TENANT_ID}/oauth2/v2.0/token"
)

token = requests.post(
    token_url,
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    },
)

access_token = token.json()["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

r = requests.get(
    "https://graph.microsoft.com/v1.0/sites/ncu365.sharepoint.com:/sites/StockAnalysis",
    headers=headers
)

print(r.status_code)
print(r.text)
