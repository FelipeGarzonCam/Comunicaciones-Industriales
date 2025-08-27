from machine import Pin, I2C
import time

# Configurar I2C
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)

# Dirección del esclavo ESP32
ESP32_ADDRESS = 0x08

# Configurar LEDs
led_pins = [16, 17, 18]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Apagar LEDs inicialmente
for led in leds:
    led.value(0)

def mostrar_binario(valor):
    """Muestra valor de 3 bits en LEDs"""
    for i, led in enumerate(leds):
        bit = (valor >> i) & 1
        led.value(bit)

def leer_potenciometro():
    """Lee valor del ESP32 via I2C"""
    try:
        data = i2c.readfrom(ESP32_ADDRESS, 1)
        return data[0]
    except OSError:
        return None

def main():    
    print("Buscando ESP32...")
    
    ciclo = 0
    esp32_conectado = False
    
    while True:
        try:
            # Escanear dispositivos I2C
            dispositivos = i2c.scan()
            
            if ESP32_ADDRESS not in dispositivos:
                if esp32_conectado:  # Solo mostrar cuando cambie el estado
                    print(" ESP32 desconectado")
                    esp32_conectado = False
                
                # Apagar LEDs cuando no hay conexión
                for led in leds:
                    led.value(0)
                
                print("Buscando ESP32...", end="\r")
                time.sleep(1)
                continue
            
            # ESP32 encontrado
            if not esp32_conectado:
                print("ESP32 encontrado!")
                esp32_conectado = True
            
            # Leer datos del potenciómetro
            valor = leer_potenciometro()
            
            if valor is not None:
                ciclo += 1
                
                # Usar 3 bits más significativos para LEDs
                bits_led = valor >> 5
                
                # Actualizar LEDs
                mostrar_binario(bits_led)
                
                # Mostrar información
                print(f"Ciclo {ciclo}: Pot={valor:3d}, LEDs={bits_led:03b} ({bin(bits_led)})")
                
            else:
                print("Error al leer datos")
                
        except KeyboardInterrupt:
            print("\n Programa detenido por usuario")
            break
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(0.5)
    
    # Cleanup al salir
    for led in leds:
        led.value(0)
    print("LEDs apagados")

# Ejecutar programa
main()
