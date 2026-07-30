import requests

BASE_URL = "https://api.coingecko.com/api/v3"


def get_market_data():
    url = (
        f"{BASE_URL}/coins/markets"
        "?vs_currency=usd"
        "&order=market_cap_desc"
        "&per_page=20"
        "&page=1"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException as e:
        print("MARKET ERROR:", e)

    return []

def search_coin(query):
    url = f"{BASE_URL}/search?query={query}"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()

    return {}

def get_coin_details(coin_id):
    url = f"{BASE_URL}/coins/{coin_id}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException as e:
        print("DETAIL ERROR:", e)

    return None

def get_coin_chart(coin_id, days=7):
    url = (
        f"{BASE_URL}/coins/{coin_id}/market_chart"
        f"?vs_currency=usd&days={days}"
    )

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return response.json()

    return None

def get_global_data():
    url = f"{BASE_URL}/global"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()["data"]

    except requests.RequestException as e:
        print("GLOBAL ERROR:", e)

    return None