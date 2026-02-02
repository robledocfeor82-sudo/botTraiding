import websocket
import json
import requests
import os

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Render leerá estos datos de la "caja fuerte" que configuramos
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
    try:
        requests.get(url)
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

def al_recibir_mensaje(ws, mensaje):
    datos = json.loads(mensaje)
    # Extraemos el precio actual
    precio = float(datos['c'])
    simbolo = datos['s']
    
    # ESTO ES LO QUE VERÁS EN LA PANTALLA NEGRA DE RENDER
    print(f"ACTUALIZACIÓN: {simbolo} - Precio: {precio}")
    
    # Ejemplo de alerta (puedes cambiar el número)
    if precio < 95000: 
        enviar_telegram(f"⚠️ Alerta: {simbolo} bajó de 95000! Precio actual: {precio}")

def al_abrir(ws):
    print("✅ Conectado exitosamente a Binance")

# Conexión al flujo de datos de Binance
socket = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
ws = websocket.WebSocketApp(socket, on_open=al_abrir, on_message=al_recibir_mensaje)
ws.run_forever()
