#!/usr/bin/env python3

import requests
import time
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

# Configuración
IP_ESP32 = "10.10.10.1"
PUERTO = 80
mensajes_recibidos = 0

print(f"[{ts()}] Conectando a WiFi del ESP32...")
print(f"[{ts()}] SSID esperado: ESP32_AP_Parcial")
print(f"[{ts()}] IP ESP32: {IP_ESP32}")
print()

input("Presiona ENTER cuando estes conectado al WiFi del ESP32...")

print()
print("-" * 55)
print("Solicitando mensajes del ESP32...")
print("-" * 55)
print()

# Bucle principal
try:
    while True:
        time.sleep(3)
        
        try:
            response = requests.get(
                f"http://{IP_ESP32}:{PUERTO}/obtener",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                mensaje = data.get('mensaje', '')
                origen = data.get('origen', '')
                ruta = data.get('ruta', '')
                
                print(f"[{ts()}] <- MENSAJE RECIBIDO desde ESP32 (WiFi)")
                print(f"         Origen: {IP_ESP32}")
                print(f"         Contenido: '{mensaje}'")
                print(f"         Origen inicial: {origen}")
                print(f"         Bytes: {len(mensaje)}")
                print()
                print(f"         RUTA COMPLETA:")
                print(f"         {ruta}")
                print()
                
                print(f"[{ts()}] -> Mensaje procesado correctamente")
                print()
                
                mensajes_recibidos += 1
                
                # Mostrar estadísticas
                print("-" * 55)
                print("ESTADISTICAS - Nodo 4 (Tablet)")
                print("-" * 55)
                print(f"Mensajes recibidos: {mensajes_recibidos}")
                print(f"Origen directo: ESP32 ({IP_ESP32})")
                print(f"Saltos totales: 3")
                print(f"  1. Celular -> PC (WiFi)")
                print(f"  2. PC -> ESP32 (Serial)")
                print(f"  3. ESP32 -> Tablet (WiFi)")
                print(f"Estado: ACTIVO")
                print("=" * 55)
                print()
                
        except requests.exceptions.ConnectionError:
            print(f"[{ts()}] Esperando conexion con ESP32...")
        except requests.exceptions.Timeout:
            print(f"[{ts()}] Timeout - reintentando...")
        except Exception as e:
            print(f"[{ts()}] Error: {e}")
        
except KeyboardInterrupt:
    print()
    print("Programa terminado por usuario")
