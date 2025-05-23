# Projekt - RTA

## Aleksandra Kubala i Natalia Błaszczuk

Aplikacja służy do **śledzenia kursów kryptowalut w czasie rzeczywistym**. Co 30 sekund pobiera aktualne ceny wybranych kryptowalut (Bitcoin, Ethereum) z publicznego API CoinGecko, przesyła dane przez Apache Kafka, przechowuje je tymczasowo w pamięci i udostępnia przez REST API zbudowane w Pythonie (we Flasku).

## Jak uruchomić aplikację

### LOKALNE URUCHOMIENIE 

### 1. Lokalne uruchomienie - Docker

Z katalogu `rta_app/`:

```bash
docker-compose up -d
```

Sprawdzenie, czy Kafka działa

```bash
docker ps
```

---

### 2. Aktywacja środowiska - przypadek Macos

```bash
python -m venv venv
source venv/bin/activate
```

Instalacja wymagań na środowisku

```bash
pip install -r requirements.txt
```

---

### 3. Uruchomienie konsumenta (w tle)

```bash
python kafka_consumer.py
```

Proces nasłuchuje cen kryptowalut i zapisuje dane w pamięci.

---

### 4. Uruchomienie producenta

```bash
python kafka_producer.py
```

Proces pobiera dane z CoinGecko i wysyła je do Kafki co 30 sekund.

---

### 5. Uruchomienie backendu Flask

```bash
python app.py
```

API będzie dostępne pod adresem:

[http://localhost:5000/api/prices](http://localhost:5000/api/prices)

Przykładowa odpowiedź:
```json
{
  "bitcoin": {
    "price_usd": 67891,
    "timestamp": 1716460000.0
  },
  "ethereum": {
    "price_usd": 3421,
    "timestamp": 1716460000.0
  }
}
```

---

## Zatrzymywanie

```bash
CTRL + C # w terminalu


# lokalnie
docker-compose down  # zatrzymuje Kafkę i Zookeepera
```

---