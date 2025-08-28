from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
STX = 0x02
ETX = 0x03

def checksum(data):
    """Calcula checksum suma módulo 256"""
    return sum(data) & 0xFF

buf = bytearray()
MAX_BUFFER_SIZE = 50  # Prevenir crecimiento infinito

print("Pico receptor checksum ready...")
print("Configuración: 9600 baudios, 8N1")
print("Esperando tramas STX-LEN-PAYLOAD-CS-ETX...")
print("=" * 50)

while True:
    try:
        # Verificar si hay datos disponibles
        if uart.any():
            # Leer byte por byte de forma segura
            data = uart.read(1)
            if data:
                buf += data
                
                # Limitar tamaño del buffer para evitar desbordamiento
                if len(buf) > MAX_BUFFER_SIZE:
                    print("Buffer overflow - reiniciando")
                    buf = bytearray()
                    continue
                
                # Buscar inicio de trama
                while len(buf) > 0 and buf[0] != STX:
                    buf.pop(0)
                
                # Si tenemos al menos STX + LEN
                if len(buf) >= 2:
                    L = buf[1]  # Longitud del payload
                    expected = 2 + L + 1 + 1  # STX + LEN + PAYLOAD + CS + ETX
                    
                    # Si tenemos la trama completa
                    if len(buf) >= expected:
                        # Extraer componentes
                        payload = bytes(buf[2:2+L])
                        recv_cs = buf[2+L]
                        recv_etx = buf[2+L+1]
                        
                        # CORRECCIÓN: recv_etx en lugar de recv etx (error del PDF)
                        if recv_etx != ETX:
                            print("Frame mal formado - ETX incorrecto")
                            print("ETX recibido:", hex(recv_etx), "esperado:", hex(ETX))
                        else:
                            # Validar checksum
                            calculated_cs = checksum(payload)
                            ok = (calculated_cs == recv_cs)                           
                            
                            print("=" * 40)
                            print("TRAMA RECIBIDA:")
                            print("RX:", list(payload))
                            print("Checksum recibido:", recv_cs)
                            print("Checksum calculado:", calculated_cs)
                            print("Estado:", "OK" if ok else "ERROR")
                            
                            if not ok:
                                print("*** DETECCIÓN DE ERROR ***")
                                print("El checksum no coincide - datos corruptos")
                            else:
                                print("Trama válida - checksum correcto")
                        
                        # Limpiar buffer para próxima trama
                        buf = bytearray()
        
        # Pausa pequeña para no saturar CPU
        time.sleep_ms(10)
        
    except Exception as e:
        print("Error en recepción:", e)
        buf = bytearray()  # Reiniciar buffer en caso de error
        time.sleep_ms(100)
