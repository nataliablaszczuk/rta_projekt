import requests
import json
from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print("Zbyt wiele zapytań – czekam 60 sekund...")
        time.sleep(60)
        return {}
    else:
        print("Błąd pobierania danych:", response.status_code)
        return {}

def send_to_kafka(data):
    for coin, value in data.items():
        message = {"coin": coin, "price_usd": value['usd'], "timestamp": time.time()}
        producer.send('crypto-prices', value=message)
        print("Wysłano:", message)

if __name__ == "__main__":
    while True:
        prices = fetch_crypto_prices()
        if prices:
            send_to_kafka(prices)
        time.sleep(10)
