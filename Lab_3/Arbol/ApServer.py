#!/usr/bin/env python3
"""
Servidor Central - Android 1 (IP automatica)
"""

from flask import Flask, request, jsonify
import json
import datetime
import os
import socket

app = Flask(__name__)

DATA_FILE = "/data/data/com.termux/files/home/sensor_data.json"
datos_recibidos = []

def obtener_ip_real():
    """Obtener IP real del Android automaticamente"""
    try:
        # Conectar a IP externa para obtener la IP local real
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "ERROR_IP"

def cargar_datos():
    global datos_recibidos
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                datos_recibidos = json.load(f)
        except:
            datos_recibidos = []

def guardar_datos():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(datos_recibidos, f, indent=2)
    except Exception as e:
        print(f"Error guardando datos: {e}")

@app.route('/sensor-data', methods=['POST'])
def recibir_datos():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        data['timestamp_central'] = datetime.datetime.now().isoformat()
        data['recibido_en'] = "Android1_Central"
        
        datos_recibidos.append(data)
        
        if len(datos_recibidos) > 100:
            datos_recibidos.pop(0)
        
        guardar_datos()
        
        print("="*50)
        print(f"DATOS RECIBIDOS DE {data.get('node_id', 'DESCONOCIDO')}")
        print(f"Temperatura: {data.get('temperatura', 'N/A')}°C")
        print(f"Humedad: {data.get('humedad', 'N/A')}%") 
        print(f"Luz: {data.get('luz', 'N/A')}")
        print(f"IP Origen: {data.get('ip', 'N/A')}")
        print(f"Timestamp: {data.get('timestamp_central', 'N/A')}")
        print("="*50)
        
        return jsonify({
            "status": "OK", 
            "message": "Datos recibidos",
            "total": len(datos_recibidos)
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def obtener_status():
    return jsonify({
        "servidor": "Android 1 Central",
        "ip": obtener_ip_real(),
        "total_datos": len(datos_recibidos),
        "ultimo_dato": datos_recibidos[-1] if datos_recibidos else None
    })

@app.route('/datos', methods=['GET'])
def obtener_datos():
    return jsonify({
        "total": len(datos_recibidos),
        "datos": datos_recibidos[-10:]  # Ultimos 10
    })

if __name__ == '__main__':
    print("Iniciando Servidor Central")
    cargar_datos()
    
    ip_real = obtener_ip_real()
    print(f"IP DETECTADA AUTOMATICAMENTE: {ip_real}")
    print(f"URL servidor: http://{ip_real}:5000/sensor-data")
    print(f"Ver status: http://{ip_real}:5000/status")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
