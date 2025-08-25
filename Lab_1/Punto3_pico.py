# Comunicación SPI - Raspberry Pi Pico como Maestro
# Envía comandos al ESP32 para controlar LED

from machine import Pin, SPI
import time

# Configuración SPI
spi = SPI(0,
          baudrate=100000,    # 100kHz - velocidad estable
          polarity=0,         # Polaridad del reloj
          phase=0,            # Fase del reloj  
          bits=8,             # 8 bits por transferencia
          firstbit=SPI.MSB,   # Bit más significativo primero
          sck=Pin(18),        # Reloj SPI
          mosi=Pin(19),       # Datos hacia esclavo
          miso=Pin(16))       # Datos desde esclavo

# Pin de control CS (Chip Select)
cs = Pin(17, Pin.OUT)
cs.value(1)  # CS inactivo al inicio

# Definir comandos
CMD_LED_ON = 0x01   # Encender LED
CMD_LED_OFF = 0x00  # Apagar LED

def enviar_comando(comando):
    """
    Envía un comando al ESP32 esclavo via SPI
    """
    print(f"Enviando comando: 0x{comando:02X}")
    
    # Activar esclavo (CS LOW)
    cs.value(0)
    time.sleep_ms(5)  # Tiempo de setup
    
    # Enviar comando y recibir respuesta
    respuesta = bytearray(1)
    spi.write_readinto(bytearray([comando]), respuesta)
    
    # Desactivar esclavo (CS HIGH) 
    time.sleep_ms(5)  # Tiempo de hold
    cs.value(1)
    
    print(f"Respuesta: 0x{respuesta[0]:02X}")
    return respuesta[0]

def main():
    """
    Programa principal - Controla LED del ESP32
    """
    print("=== Raspberry Pi Pico SPI Maestro ===")
    print("Controlando LED del ESP32...")
    time.sleep(2)
    
    ciclo = 0
    
    try:
        while True:
            ciclo += 1
            print(f"\n--- Ciclo {ciclo} ---")
            
            # Encender LED
            print("Encendiendo LED")
            enviar_comando(CMD_LED_ON)
            time.sleep(2)
            
            # Apagar LED
            print("Apagando LED") 
            enviar_comando(CMD_LED_OFF)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario")
        cs.value(1)  # Asegurar CS inactivo
        print("SPI finalizado correctamente")

# Ejecutar programa principal
if __name__ == "__main__":
    main()
