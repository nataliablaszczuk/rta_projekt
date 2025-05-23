from kafka import KafkaConsumer
import json
import threading

crypto_data = {}

consumer = KafkaConsumer(
    'crypto-prices',
    bootstrap_servers='localhost:29092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='crypto-group'
)

def consume():
    for message in consumer:
        data = message.value
        coin = data['coin']
        crypto_data[coin] = {
            'price_usd': data['price_usd'],
            'timestamp': data['timestamp']
        }
        print("Odebrano:", data)

# Uruchomienie konsumenta w tle
thread = threading.Thread(target=consume, daemon=True)
thread.start()
