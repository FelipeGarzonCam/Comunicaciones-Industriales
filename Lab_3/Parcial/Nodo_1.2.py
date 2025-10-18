#!/usr/bin/env python3
"""
Script para enviar mensaje desde Celular
Ejecutar en otra sesión de Termux
"""
import requests
import sys

# Configurar IP del PC (debe estar conectado al hotspot)
IP_PC = input("IP del PC (ej: 192.168.43.100): ").strip()
if not IP_PC:
    print("Error: Debe ingresar IP del PC")
    sys.exit(1)

MENSAJE = "Hola desde el Celular - Parcial Redes"

print()
print(f"Enviando mensaje al PC ({IP_PC})...")

try:
    response = requests.post(
        f"http://{IP_PC}:6000/recibir",
        json={"mensaje": MENSAJE, "origen": "Celular"},
        timeout=10
    )
    
    if response.status_code == 200:
        print(f"✓ Mensaje enviado exitosamente")
        print(f"✓ Bytes: {len(MENSAJE)}")
    else:
        print(f"✗ Error: {response.status_code}")
except Exception as e:
    print(f"✗ Error de conexion: {e}")
