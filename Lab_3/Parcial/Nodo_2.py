#!/usr/bin/env python3

from flask import Flask, request, jsonify
import serial
import socket
import json
import time
import threading
from datetime import datetime
import requests

app = Flask(__name__)

# Configuración
PUERTO_ESP32 = ""  # Se solicitará al inicio
BAUDRATE = 115200
ser = None
mensajes_procesados = 0

def ts():
    return datetime.now().strftime("%H:%M:%S")

def obtener_ip():
    """Obtiene la IP del PC en la red del celular"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "ERROR_IP"

def conectar_esp32():
    """Conecta al ESP32 via Serial"""
    global ser, PUERTO_ESP32
    
    PUERTO_ESP32 = input("Puerto ESP32 (ej: COM4 o /dev/ttyUSB0): ").strip()
    
    try:
        ser = serial.Serial(PUERTO_ESP32, BAUDRATE, timeout=1)
        time.sleep(2)
        print(f"[{ts()}]  Conexion Serial establecida ({PUERTO_ESP32})")
        return True
    except Exception as e:
        print(f"[{ts()}]  Error Serial: {e}")
        return False

@app.route('/recibir', methods=['POST'])
def recibir_mensaje():
    """Recibe mensaje del Celular via WiFi"""
    global mensajes_procesados
    
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    origen = data.get('origen', 'Desconocido')
    
    print()
    print(f"[{ts()}] <- MENSAJE RECIBIDO desde {origen} (WiFi)")
    print(f"         Contenido: '{mensaje}'")
    print(f"         Bytes: {len(mensaje)}")
    print()
    
    # Enviar ACK al celular
    try:
        ip_celular = request.remote_addr
        requests.post(f"http://{ip_celular}:5000/ack", 
                     json={"status": "OK"}, timeout=5)
        print(f"[{ts()}]  ACK enviado al Celular")
    except:
        print(f"[{ts()}]  No se pudo enviar ACK al Celular")
    
    # Reenviar a ESP32 via Serial
    if ser and ser.is_open:
        print()
        print(f"[{ts()}] -> Reenviando a ESP32 (Serial {PUERTO_ESP32})")
        
        # Enviar como JSON
        datos_json = json.dumps({"mensaje": mensaje, "origen": origen})
        ser.write(f"{datos_json}\n".encode())
        ser.flush()
        
        # Esperar ACK del ESP32
        time.sleep(1)
        if ser.in_waiting:
            respuesta = ser.readline().decode().strip()
            if "ACK" in respuesta:
                print(f"[{ts()}] <- ACK recibido del ESP32")
            print(f"[{ts()}] Mensaje entregado al ESP32")
        
        mensajes_procesados += 1
    
    return jsonify({"status": "OK"}), 200

def mostrar_estadisticas():
    """Muestra estadísticas periódicamente"""
    while True:
        time.sleep(30)
        if mensajes_procesados > 0:
            print()
            print("-" * 60)
            print("ESTADISTICAS - Nodo 2 (PC)")
            print("-" * 60)
            print(f"Mensajes procesados: {mensajes_procesados}")
            print(f"Puerto Serial: {PUERTO_ESP32}")
            print(f"Estado: ACTIVO")
            print("-" * 60)

def iniciar_servidor():
    """Inicia el servidor Flask"""
    mi_ip = obtener_ip()
    
    print("=" * 60)
    print("NODO 2: PC (Intermediario WiFi -> Serial)")
    print("Universidad Santo Tomas - Parcial Red Lineal")
    print("=" * 60)
    print()
    print(f"[{ts()}] IP en red del Celular: {mi_ip}")
    print(f"[{ts()}] Puerto: 6000")
    print()
    
    # Conectar ESP32
    if not conectar_esp32():
        print("Error: No se pudo conectar al ESP32")
        return
    
    print()
    print("-" * 60)
    print("Esperando mensajes del Celular...")
    print("-" * 60)
    print()
    
    # Iniciar hilo de estadísticas
    hilo_stats = threading.Thread(target=mostrar_estadisticas, daemon=True)
    hilo_stats.start()
    
    app.run(host='0.0.0.0', port=6000, debug=False)

if __name__ == "__main__":
    iniciar_servidor()
