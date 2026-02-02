import websocket
import json
import requests

# === CONFIGURACIÓN ===
TOKEN = "8015147350:AAHEWPnd4VT8q5ZcE-pcd2mn0IfSGXNIfhc"
CHAT_ID = "7816327526"

# Memoria extendida para mayor precisión
memorias = {"BTCUSDT": [], "ETHUSDT": [], "SOLUSDT": []}
PERIODOS_PROMEDIO = 20 # Cantidad de datos para calcular la base

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
        requests.get(url)
    except:
        pass

def al_recibir_mensaje(ws, mensaje):
    datos = json.loads(mensaje)
    simbolo = datos['s']
    precio = float(datos['c'])
    
    memorias[simbolo].append(precio)
    if len(memorias[simbolo]) > PERIODOS_PROMEDIO:
        memorias[simbolo].pop(0)

    # Solo analizamos si tenemos la memoria llena para que sea preciso
    if len(memorias[simbolo]) == PERIODOS_PROMEDIO:
        promedio = sum(memorias[simbolo]) / PERIODOS_PROMEDIO # El precio "justo" actual
        
        # Filtro de Precisión: ¿Qué tan lejos está el precio del promedio?
        distancia = precio - promedio
        
        # Umbrales de precisión (ajustados por moneda)
        umbrales = {"BTCUSDT": 30, "ETHUSDT": 2, "SOLUSDT": 0.40}
        u = umbrales.get(simbolo, 10)

        # Solo enviamos alerta si el precio ROMPE el promedio con fuerza
        if distancia > u:
            msg = f"✅ PRECISIÓN: {simbolo} rompió al ALZA\nPrecio: ${precio:.2f}\nPromedio: ${promedio:.2f}"
            print(msg)
            enviar_telegram(msg)
        elif distancia < -u:
            msg = f"❌ PRECISIÓN: {simbolo} rompió a la BAJA\nPrecio: ${precio:.2f}\nPromedio: ${promedio:.2f}"
            print(msg)
            enviar_telegram(msg)

def al_abrir(ws):
    print("--- INICIANDO IA DE ALTA PRECISIÓN ---")
    suscripcion = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@ticker", "ethusdt@ticker", "solusdt@ticker"],
        "id": 1
    }
    ws.send(json.dumps(suscripcion))

socket = "wss://stream.binance.com:9443/ws"
ws = websocket.WebSocketApp(socket, on_message=al_recibir_mensaje, on_open=al_abrir)
ws.run_forever()