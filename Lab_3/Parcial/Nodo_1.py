#!/usr/bin/env python3
from flask import Flask, request, jsonify
import socket
import json
from datetime import datetime

app = Flask(__name__)

# Configuración
MENSAJE = "Hola desde el Celular - Parcial Redes"
mensajes_enviados = 0
acks_recibidos = 0

def obtener_ip():
    """Obtiene la IP del hotspot (generalmente 192.168.43.1)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.43.1"  

@app.route('/ack', methods=['POST'])
def recibir_ack():
    """Recibe ACK del PC"""
    global acks_recibidos
    data = request.get_json()
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] <- ACK recibido del PC")
    print(f"         Status: {data.get('status', 'OK')}")
    acks_recibidos += 1
    
    return jsonify({"status": "ACK_received"}), 200

def iniciar_servidor():
    """Inicia el servidor Flask"""
    mi_ip = obtener_ip()    

    print(f"[INFO] Modo Access Point activo")
    print(f"[INFO] IP: {mi_ip}")
    print(f"[INFO] Puerto: 5000")
    print(f"[INFO] Esperando conexion del PC...")
    print()
    print("IMPORTANTE: Conectar PC al hotspot del celular")
    print()
    print("-" * 55)
    
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    iniciar_servidor()
