#!/usr/bin/env python3
"""
Simulador MQTT para Pruebas del Sistema SIAM-Yucatán
Permite validar el Dashboard de Node-RED sin necesidad de tener la ESP32 física conectada.
Soporta paho-mqtt (si está instalado) o simulación interactiva local en consola.

Autores: Diego López Pérez (@DiegoLop3z) & Arturo Heredia Martín (@arturoherediam)
Universidad Politécnica de Yucatán (UPY) - 2026
"""

import sys
import time
import math
import json
import random

# Tópicos oficiales SIAM-Yucatán
TOPIC_TELEMETRIA   = "yucatan/bioclima/telemetria"
TOPIC_TEMP         = "yucatan/bioclima/sensor/temperatura"
TOPIC_HUM          = "yucatan/bioclima/sensor/humedad"
TOPIC_HEAT_INDEX   = "yucatan/bioclima/sensor/indice_calor"
TOPIC_LUZ          = "yucatan/bioclima/sensor/luz"
TOPIC_PRESENCIA    = "yucatan/bioclima/sensor/presencia"
TOPIC_FAN_ESTADO   = "yucatan/bioclima/actuador/ventilador/estado"
TOPIC_MODO_ESTADO  = "yucatan/bioclima/actuador/modo/estado"
TOPIC_STATUS       = "yucatan/bioclima/status"

TOPIC_FAN_SET      = "yucatan/bioclima/actuador/ventilador/set"
TOPIC_MODO_SET     = "yucatan/bioclima/actuador/modo/set"
TOPIC_CONFIG_UMBRAL = "yucatan/bioclima/config/umbral_temp"

def calcular_indice_calor(temp_c, hum_rel):
    """Cálculo estricto de Sensación Térmica NOAA Rothfusz."""
    if temp_c < 20.0:
        return temp_c
    tf = (temp_c * 1.8) + 32.0
    rh = hum_rel
    hi = 0.5 * (tf + 61.0 + ((tf - 68.0) * 1.2) + (rh * 0.094))
    if hi >= 80.0:
        hi = (-42.379 
              + 2.04901523 * tf 
              + 10.14333127 * rh 
              - 0.22475541 * tf * rh 
              - 0.00683783 * tf * tf 
              - 0.05481717 * rh * rh 
              + 0.00122874 * tf * tf * rh 
              + 0.00085282 * tf * rh * rh 
              - 0.00000199 * tf * tf * rh * rh)
        if rh < 13.0 and 80.0 <= tf <= 112.0:
            adj = ((13.0 - rh) / 4.0) * math.sqrt((17.0 - abs(tf - 95.0)) / 17.0)
            hi -= adj
        elif rh > 85.0 and 80.0 <= tf <= 87.0:
            adj = ((rh - 85.0) / 10.0) * ((87.0 - tf) / 5.0)
            hi += adj
    return (hi - 32.0) / 1.8

def obtener_alerta(hi):
    if hi < 30.0:
        return "CONFORT"
    elif hi < 38.0:
        return "PRECAUCION"
    else:
        return "PELIGRO"

def main():
    print("=" * 65, flush=True)
    print("  SIMULADOR DE TELEMETRÍA Y CONTROL MQTT — SIAM-Yucatán (UPY)", flush=True)
    print("  Autores: Diego López Pérez & Arturo Heredia Martín", flush=True)
    print("=" * 65, flush=True)

    has_paho = False
    try:
        import paho.mqtt.client as mqtt
        has_paho = True
        print("[INFO] Librería paho-mqtt detectada.")
    except ImportError:
        print("[WARN] Librería 'paho-mqtt' no encontrada.")
        print("       Para conectar directamente al broker Mosquitto ejecute:")
        print("       pip install paho-mqtt")
        print("       Ejecutando en modo SIMULACIÓN LOCAL INTERNA (Dry-Run)...")

    # Estado del simulador
    estado = {
        "fan": "OFF",
        "modo": "AUTO",
        "umbral_temp": 32.0,
        "tiempo_inicio_manual": 0,
        "tiempo_ultima_presencia": time.time()
    }

    client = None
    if has_paho:
        broker_host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        broker_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1883
        client = mqtt.Client(client_id="simulador-siam-py")

        def on_connect(c, userdata, flags, rc):
            if rc == 0:
                print(f"[MQTT] Conectado exitosamente al broker {broker_host}:{broker_port}")
                c.publish(TOPIC_STATUS, "online", retain=True)
                c.publish(TOPIC_FAN_ESTADO, estado["fan"], retain=True)
                c.publish(TOPIC_MODO_ESTADO, estado["modo"], retain=True)
                c.subscribe(TOPIC_FAN_SET, qos=1)
                c.subscribe(TOPIC_MODO_SET, qos=1)
                c.subscribe(TOPIC_CONFIG_UMBRAL, qos=1)
                print("[MQTT] Suscrito a comandos de control de actuadores.")
            else:
                print(f"[MQTT] Error de conexión, código: {rc}")

        def on_message(c, userdata, msg):
            payload = msg.payload.decode('utf-8', errors='ignore').strip().upper()
            topic = msg.topic
            print(f"\n[COMANDO RECIBIDO] Topic: {topic} | Valor: {payload}")
            if topic == TOPIC_FAN_SET:
                if payload in ("ON", "OFF"):
                    estado["fan"] = payload
                    if payload == "ON" and estado["modo"] == "AUTO":
                        estado["modo"] = "MANUAL"
                        estado["tiempo_inicio_manual"] = time.time()
                        c.publish(TOPIC_MODO_ESTADO, "MANUAL", retain=True)
                        print("[AUTO-CAMBIO] Ventilador forzado manualmente. Modo conmutado a MANUAL.")
                    c.publish(TOPIC_FAN_ESTADO, estado["fan"], retain=True)
                    print(f"[CONFIRMACIÓN] Ventilador -> {estado['fan']}")
            elif topic == TOPIC_MODO_SET:
                if payload in ("AUTO", "MANUAL"):
                    estado["modo"] = payload
                    if payload == "MANUAL":
                        estado["tiempo_inicio_manual"] = time.time()
                    c.publish(TOPIC_MODO_ESTADO, estado["modo"], retain=True)
                    print(f"[CONFIRMACIÓN] Modo -> {estado['modo']}")
            elif topic == TOPIC_CONFIG_UMBRAL:
                try:
                    val = float(payload)
                    estado["umbral_temp"] = val
                    print(f"[CONFIG] Umbral de temperatura actualizado a: {val} °C")
                except ValueError:
                    pass

        client.on_connect = on_connect
        client.on_message = on_message
        try:
            client.will_set(TOPIC_STATUS, "offline", retain=True)
            client.connect(broker_host, broker_port, 60)
            client.loop_start()
        except Exception as e:
            print(f"[ERROR] No se pudo conectar al broker ({e}). Continuando en modo local.")
            client = None

    t_start = time.time()
    step = 0

    print("\nIniciando ciclo de telemetría (Ctrl+C para detener)...\n")
    try:
        while True:
            ahora = time.time()
            elapsed = ahora - t_start

            # Variación climática realista (ondas sinusoidales + ruido)
            temp = round(31.0 + 3.5 * math.sin(step * 0.1) + random.uniform(-0.3, 0.3), 1)
            hum = round(72.0 + 8.0 * math.cos(step * 0.08) + random.uniform(-1.0, 1.0), 1)
            hum = max(30.0, min(95.0, hum))
            hi = round(calcular_indice_calor(temp, hum), 1)
            alerta = obtener_alerta(hi)
            luz = int(60 + 25 * math.sin(step * 0.15) + random.uniform(-3, 3))
            luz = max(5, min(98, luz))
            presencia = 1 if (step % 12 < 8) else 0

            # Lógica de automatización simulada
            if estado["modo"] == "AUTO":
                if (hi >= 38.0 or temp >= estado["umbral_temp"]) and presencia == 1:
                    if estado["fan"] != "ON":
                        estado["fan"] = "ON"
                        if client:
                            client.publish(TOPIC_FAN_ESTADO, "ON", retain=True)
                        print("  >> [AUTO ACTIVA] Ventilador ON por Calor + Presencia")
                elif estado["fan"] == "ON":
                    if presencia == 0 and (ahora - estado["tiempo_ultima_presencia"] >= 10): # 10s acelerado en sim
                        estado["fan"] = "OFF"
                        if client:
                            client.publish(TOPIC_FAN_ESTADO, "OFF", retain=True)
                        print("  >> [AUTO DESACTIVA] Ventilador OFF por Desocupación")
                    elif temp < (estado["umbral_temp"] - 2.0) and hi < 35.0:
                        estado["fan"] = "OFF"
                        if client:
                            client.publish(TOPIC_FAN_ESTADO, "OFF", retain=True)
                        print("  >> [AUTO DESACTIVA] Ventilador OFF por Histéresis Térmica")
            elif estado["modo"] == "MANUAL":
                # Temporizador anti-olvido (60 s conforme al firmware y especificacion de demo)
                if (ahora - estado["tiempo_inicio_manual"] >= 60):
                    print("  >> [PROTECCION ANTI-OLVIDO] Expiro tiempo manual (60 s). Retorno autonomo a AUTO.")
                    estado["modo"] = "AUTO"
                    if client:
                        client.publish(TOPIC_MODO_ESTADO, "AUTO", retain=True)
                    condicion_activa = (hi >= 38.0 or temp >= estado["umbral_temp"]) and presencia == 1
                    if not condicion_activa:
                        estado["fan"] = "OFF"
                        if client:
                            client.publish(TOPIC_FAN_ESTADO, "OFF", retain=True)
            if presencia == 1:
                estado["tiempo_ultima_presencia"] = ahora

            # Payload JSON
            payload_json = {
                "temp": temp,
                "hum": hum,
                "hi": hi,
                "luz": luz,
                "pres": presencia,
                "fan": 1 if estado["fan"] == "ON" else 0,
                "modo": estado["modo"],
                "alerta": alerta
            }
            json_str = json.dumps(payload_json)

            # Publicación MQTT
            if client:
                client.publish(TOPIC_TEMP, str(temp))
                client.publish(TOPIC_HUM, str(hum))
                client.publish(TOPIC_HEAT_INDEX, str(hi))
                client.publish(TOPIC_LUZ, str(luz))
                client.publish(TOPIC_PRESENCIA, str(presencia))
                client.publish(TOPIC_TELEMETRIA, json_str)

            print(f"[{time.strftime('%H:%M:%S')}] Step {step:03d} | Temp: {temp}°C | Hum: {hum}% | HI: {hi}°C [{alerta:10s}] | Luz: {luz}% | Pres: {presencia} | Fan: {estado['fan']} | Modo: {estado['modo']}", flush=True)

            step += 1
            time.sleep(2.0)

    except KeyboardInterrupt:
        print("\n[INFO] Simulación finalizada por el usuario.")
        if client:
            client.publish(TOPIC_STATUS, "offline", retain=True)
            client.loop_stop()
            client.disconnect()

if __name__ == "__main__":
    main()
