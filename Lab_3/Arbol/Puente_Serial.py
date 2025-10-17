#!/usr/bin/env python3
"""
Puente Serial PC - Lee datos de ESP32 y los envía al Móvil 1
Mantiene topología árbol: ESP32 → PC → Móvil 1
"""

import serial
import json
import requests
import time
import threading
from datetime import datetime

# Configuración
PUERTO_ESP32 = "COM4"  
SERVIDOR_CENTRAL = "http://100.109.238.82:5000/sensor-data"
BAUD_RATE = 115200

class SerialBridge:
    def __init__(self):
        self.ser = None
        self.conectado = False
        self.datos_recibidos = 0
        
    def conectar_esp32(self):
        """Conectar al puerto serie de la ESP32"""
        try:
            self.ser = serial.Serial(PUERTO_ESP32, BAUD_RATE, timeout=1)
            time.sleep(2)  # Esperar estabilización
            self.conectado = True
            print(f"Conectado a ESP32 en {PUERTO_ESP32}")
            return True
        except Exception as e:
            print(f"Error conectando ESP32: {e}")
            return False
    
    def leer_datos_esp32(self):
        """Leer datos JSON de la ESP32"""
        if not self.conectado:
            return None
            
        try:
            buffer = ""
            json_capturando = False
            
            while True:
                if self.ser.in_waiting:
                    linea = self.ser.readline().decode('utf-8').strip()
                    
                    if linea == ">>JSON_START":
                        json_capturando = True
                        buffer = ""
                        continue
                    elif linea == ">>JSON_END":
                        if json_capturando and buffer:
                            try:
                                data = json.loads(buffer)
                                return data
                            except json.JSONDecodeError:
                                print("Error decodificando JSON")
                        json_capturando = False
                        buffer = ""
                    elif json_capturando:
                        buffer = linea
                    else:
                        # Mostrar otros mensajes de la ESP32
                        if linea and not linea.startswith(">>"):
                            print(f"ESP32: {linea}")
                
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error leyendo serial: {e}")
            return None
    
    def enviar_al_servidor_central(self, data):
        """Enviar datos al servidor central (Móvil 1)"""
        try:
            # Agregar información del puente
            data['via_puente'] = "PC_Serial_Bridge"
            data['timestamp_puente'] = datetime.now().isoformat()
            
            response = requests.post(SERVIDOR_CENTRAL, json=data, timeout=10)
            
            if response.status_code == 200:
                self.datos_recibidos += 1
                print(f"✓ Datos enviados al servidor central - Total: {self.datos_recibidos}")
                print(f"  Temp: {data.get('temperatura', 'N/A')}°C, "
                      f"Humedad: {data.get('humedad', 'N/A')}%, "
                      f"Luz: {data.get('luz', 'N/A')}")
                return True
            else:
                print(f"✗ Error servidor central: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error conexión servidor: {e}")
            return False
    
    def enviar_comando_esp32(self, comando):
        """Enviar comando a la ESP32"""
        if self.conectado:
            try:
                self.ser.write((comando + '\n').encode('utf-8'))
                print(f"Comando enviado a ESP32: {comando}")
            except Exception as e:
                print(f"Error enviando comando: {e}")
    
    def ejecutar(self):
        """Loop principal del puente"""
        print("=== PUENTE SERIAL ESP32 → PC → MÓVIL 1 ===")
        print("Topología: ÁRBOL")
        print(f"Puerto ESP32: {PUERTO_ESP32}")
        print(f"Servidor Central: {SERVIDOR_CENTRAL}")
        print("=" * 45)
        
        if not self.conectar_esp32():
            return
        
        # Hilo para comandos del usuario
        def comandos_usuario():
            while True:
                try:
                    cmd = input().strip()
                    if cmd:
                        self.enviar_comando_esp32(cmd)
                except:
                    break
        
        threading.Thread(target=comandos_usuario, daemon=True).start()
        print("Puedes enviar comandos a la ESP32: status, test, ledon, ledoff")
        print("-" * 45)
        
        # Loop principal de lectura
        while True:
            try:
                data = self.leer_datos_esp32()
                if data:
                    self.enviar_al_servidor_central(data)
                    
            except KeyboardInterrupt:
                print("\nDeteniendo puente...")
                break
            except Exception as e:
                print(f"Error en loop principal: {e}")
                time.sleep(5)
        
        if self.ser:
            self.ser.close()

if __name__ == "__main__":
    puente = SerialBridge()
    puente.ejecutar()
