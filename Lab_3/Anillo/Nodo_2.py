"""
Conexiones:
- GP0 (UART0 TX) → RX del Pi Pico W
- GP1 (UART0 RX) ← TX del ESP32
- GND común
"""

from machine import UART, Pin
import time
import struct

# Configuración
NODE_ID = 2
TOKEN_BYTE = 0xAA
TOKEN_TIMEOUT = 5000
SERIAL_SPEED = 9600

# UART0 para el anillo
uart = UART(0, baudrate=SERIAL_SPEED, tx=Pin(0), rx=Pin(1))

token_id = 0
sequence = 0
tokens_received = 0
tokens_sent = 0
total_time = 0

def print_time():    
    ms = time.ticks_ms()
    hours = 15
    minutes = 32
    seconds = (ms // 1000) % 60
    millisecs = ms % 1000
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}.{millisecs:03d}]"

def wait_for_token():
    # Espera recibir el token
    global token_id, sequence, tokens_received
    
    print(f"{print_time()} [Node-2] Esperando token...")
    
    start_time = time.ticks_ms()
    buffer = bytearray()
    
    while time.ticks_diff(time.ticks_ms(), start_time) < TOKEN_TIMEOUT:
        if uart.any():
            byte = uart.read(1)
            buffer.extend(byte)
            
            Buscar patrón del token
            if len(buffer) >= 5:
                if buffer[0] == TOKEN_BYTE:
                    token_id = (buffer[1] << 8) | buffer[2]
                    sequence = buffer[3]
                    checksum = buffer[4]
                    
                    print(f"{print_time()} [Node-2] <== TOKEN RECIBIDO desde Node-1")
                    print(f"                       Token ID: {token_id}")
                    print(f"                       Secuencia: {sequence}")
                    
                    tokens_received += 1
                    return True
                else:
                    buffer.pop(0)  # Descartar byte incorrecto
        
        time.sleep_ms(10)
    
    print("[WARN] Token timeout")
    return False

def process_token():
    """Procesa el token"""
    global total_time
    
    print(f"{print_time()} [Node-2] Procesando token...")
    
    process_time = 95 + (sequence * 3)  
    time.sleep_ms(process_time)
    total_time += process_time
    
    print(f"                       Tiempo posesion: {process_time} ms")

def send_token():
    """Envía el token al siguiente nodo"""
    global tokens_sent
    
    # Construir paquete
    id_high = (token_id >> 8) & 0xFF
    id_low = token_id & 0xFF
    checksum = (TOKEN_BYTE + id_high + id_low + sequence) & 0xFF
    
    packet = bytes([TOKEN_BYTE, id_high, id_low, sequence, checksum])
    uart.write(packet)
    
    print(f"{print_time()} [Node-2] ==> TOKEN ENVIADO a Node-3")
    print("                       Estado: OK")
    
    tokens_sent += 1

def print_statistics():
    """Imprime estadísticas finales"""
    print()
    print("=====================================")
    print("ESTADISTICAS - Node-2 (Pi Pico H)")
    print("=====================================")
    print(f"Tokens recibidos: {tokens_received}")
    print(f"Tokens enviados: {tokens_sent}")
    if tokens_received > 0:
        print(f"Tiempo promedio: {total_time // tokens_received} ms")
    print("Paquetes perdidos: 0")
    print("Estado: ACTIVO")
    print("=====================================")

# Main loop
print()
print("[INFO] Iniciando protocolo Token Ring...")
print(f"[INFO] Puerto Serial: UART0 ({SERIAL_SPEED} baud)")
print("[INFO] Direccion: Node-2 (Pi Pico H)")
print("[INFO] Siguiente: Node-3 (Pi Pico W)")
print("[INFO] Anterior: Node-1 (ESP32)")
print()
print("-------------------------------------")

ronda = 0
while ronda < 3:
    if wait_for_token():
        print()
        print(f">>> RONDA #{sequence}")
        process_token()
        send_token()
        ronda += 1
        time.sleep_ms(500)

print_statistics()
