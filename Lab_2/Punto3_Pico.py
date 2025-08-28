# vrc_lrc_recv_sync.py - Receptor sincronizado
from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def calculate_vrc(byte_val):
    parity = 0
    for i in range(8):
        parity ^= (byte_val >> i) & 1
    return parity

def calculate_lrc(data_block):
    lrc = 0
    for byte in data_block:
        lrc ^= byte
    return lrc

print("Pico receptor VRC/LRC SINCRONIZADO")
print("Esperando marcadores: 0xAA(VRC), 0xCC(LRC)")
print("=" * 50)

cycle_count = 0

while True:
    if uart.any():
        marker = uart.read(1)[0]
        
        if marker == 0xAA:  # Inicio VRC
            print(f"\n=== INICIO VRC - CICLO #{cycle_count + 1} ===")
            vrc_errors = 0
            
            for i in range(5):
                # Esperar datos
                while not uart.any():
                    time.sleep_ms(5)
                data = uart.read(1)[0]
                
                while not uart.any():
                    time.sleep_ms(5)
                vrc_recv = uart.read(1)[0]
                
                vrc_calc = calculate_vrc(data)
                
                if vrc_recv == vrc_calc:
                    print(f"VRC OK: Data=0x{data:02X}, VRC=0x{vrc_recv:02X}")
                else:
                    print(f"VRC ERROR: Data=0x{data:02X}, recv=0x{vrc_recv:02X}, calc=0x{vrc_calc:02X}")
                    vrc_errors += 1
            
            # Esperar marcador de fin
            while not uart.any():
                time.sleep_ms(5)
            end_marker = uart.read(1)[0]
            
            print(f"VRC Completado. Errores: {vrc_errors}/5")
            
        elif marker == 0xCC:  # Inicio LRC
            print(f"\n=== INICIO LRC - CICLO #{cycle_count + 1} ===")
            lrc_data = []
            
            for i in range(5):
                while not uart.any():
                    time.sleep_ms(5)
                data = uart.read(1)[0]
                lrc_data.append(data)
                print(f"LRC Data[{i}]: 0x{data:02X}")
            
            while not uart.any():
                time.sleep_ms(5)
            lrc_recv = uart.read(1)[0]
            
            lrc_calc = calculate_lrc(lrc_data)
            
            if lrc_recv == lrc_calc:
                print(f"LRC OK: recibido=0x{lrc_recv:02X}")
            else:
                print(f"LRC ERROR: recibido=0x{lrc_recv:02X}, calculado=0x{lrc_calc:02X}")
            
            # Esperar marcador de fin
            while not uart.any():
                time.sleep_ms(5)
            end_marker = uart.read(1)[0]
            
            cycle_count += 1
            
            print(f"\n=== ANALISIS COMPARATIVO CICLO #{cycle_count} ===")
            print("VRC: Verifica cada byte individualmente")
            print("LRC: Verifica bloque completo con un checksum")
            print("Overhead: VRC 140% (12/5), LRC 60% (8/5)")
            print("Eficiencia: VRC 41.7%, LRC 62.5%")
    
    time.sleep_ms(10)
