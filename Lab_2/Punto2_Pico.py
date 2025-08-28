from machine import UART, Pin
import time
import urandom

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
STX = 0x02
ETX = 0x03

def checksum(data):
    return sum(data) & 0xFF


ERROR_PROBABILITY = 0.5 #Cambiar para pruebas
packet_count = 0

print("Pico receptor ARQ ready (SIMPLIFICADO)")
print(f"Probabilidad de error simulado: {ERROR_PROBABILITY*100}%")
print("Respondiendo con ACK ('A') si OK, NACK ('N') si error")
print("=" * 50)


while True:
    try:
        if uart.any() >= 1:
            # Leer primer byte
            b = uart.read(1)
            if not b: 
                continue
            if b[0] != STX: 
                continue
                
            time.sleep_ms(100)  # Esperar trama completa
            
            if uart.any() >= 4:  
                L = uart.read(1)[0]
                payload = uart.read(L)
                cs = uart.read(1)[0]
                etx = uart.read(1)[0]
                
                packet_count += 1
                
                # Validar trama 
                checksum_ok = (checksum(payload) == cs)
                etx_ok = (etx == ETX)
                frame_ok = checksum_ok and etx_ok
                
                print(f"\n--- Paquete #{packet_count} ---")
                print(f"RX: {list(payload)}")
                print(f"Checksum: recv={cs}, calc={checksum(payload)}, OK={checksum_ok}")
                print(f"ETX: OK={etx_ok}")
                
                # Determinar respuesta
                if not frame_ok:
                    # Error real en trama
                    uart.write(b'N')
                    print("ERROR REAL -> NACK")
                elif urandom.getrandbits(16)/65535.0 < ERROR_PROBABILITY:
                    # Error simulado
                    uart.write(b'N')
                    print("ERROR SIMULADO -> NACK")
                else:
                    # Todo OK
                    uart.write(b'A')
                    print("OK -> ACK")
            else:
                print("Trama incompleta, descartando")
        
        time.sleep_ms(10)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep_ms(100)
