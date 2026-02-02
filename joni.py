import websocket
import json
import requests
import os

# --- CONFIGURACIÓN SEGURA PARA RENDER ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
    try:
        requests.get(url)
    except:
        pass

def al_recibir_mensaje(ws, mensaje):
    datos = json.loads(mensaje)
    precio = float(datos['c'])
    simbolo = datos['s']
    # Aquí puedes poner tus prints para ver el movimiento en Render
    print(f"{simbolo}: {precio}")
    # Tu lógica de trading aquí...

def al_abrir(ws):
    print("Conexión abierta con Binance")

# Conexión al stream de Binance
socket = "wss://stream.binance.com:9443/ws/btcusdt@ticker/ethusdt@ticker"
ws = websocket.WebSocketApp(socket, on_open=al_abrir, on_message=al_recibir_mensaje)
ws.run_forever()
