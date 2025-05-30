from kafka import KafkaConsumer
import json
import threading
from datetime import datetime

crypto_data = {}
previous_prices = {}
threshold = 0.01

consumer = KafkaConsumer(
    'crypto-prices',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='crypto-group'
)

def log_alert(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {message}\n"
    with open("alerts.log", "a") as file:
        file.write(entry)
        
def consume():
    for message in consumer:
        data = message.value
        coin = data['coin']
        current_price = data['price_usd']

        crypto_data[coin] = {
            'price_usd': current_price,
            'timestamp': data['timestamp']
        }

        if coin in previous_prices:
            previous_price = previous_prices[coin]
            change = (current_price - previous_price) / previous_price

            if abs(change) >= threshold:
                direction = "wzrost" if change > 0 else "spadek"
                percent = round(change * 100, 2)
                alert_msg = f"ALERT: {coin.upper()} {direction} o {percent}% ({previous_price} → {current_price})"
                print(f"🔔 {alert_msg}")
                log_alert(alert_msg)

        previous_prices[coin] = current_price
        print("Odebrano:", data)
