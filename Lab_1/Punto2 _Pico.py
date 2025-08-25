from machine import Pin, UART, Timer
import time

# Configurar UART0 para comunicación con ESP32
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Configurar LEDs de estado
led_onboard = Pin(25, Pin.OUT)      # LED onboard del Pico
led_comm_ok = Pin(2, Pin.OUT)       # LED Verde - Comunicación OK
led_comm_fail = Pin(3, Pin.OUT)     # LED Rojo - Sin Comunicación

# Variables de control
message_count = 0
last_received_time = 0
communication_timeout = 8000  # 8 segundos timeout
is_communication_active = False
heartbeat_timer = None

def blink_led(led_pin, times=1, delay_ms=200):
    """Función para hacer parpadear un LED específico"""
    for _ in range(times):
        led_pin.on()
        time.sleep_ms(delay_ms)
        led_pin.off()
        time.sleep_ms(delay_ms)

def update_communication_status():
    """Actualizar el estado de los LEDs según la comunicación"""
    current_time = time.ticks_ms()
    
    if last_received_time == 0:
        # No se ha recibido ningún mensaje aún
        is_active = False
    else:
        # Verificar si el último mensaje fue hace menos del timeout
        time_diff = time.ticks_diff(current_time, last_received_time)
        is_active = time_diff < communication_timeout
    
    global is_communication_active
    
    # Solo cambiar estado si es diferente al actual
    if is_active != is_communication_active:
        is_communication_active = is_active
        
        if is_communication_active:
            # Comunicación activa: LED verde ON, LED azul OFF
            led_comm_ok.on()
            led_comm_fail.off()
            print("🟢 ESTADO: Comunicación ACTIVA")
        else:
            # Sin comunicación: LED verde OFF, LED azul ON
            led_comm_ok.off()
            led_comm_fail.on()
            print("🔴 ESTADO: Sin comunicación - Esperando ESP32...")

def heartbeat_callback(timer):
    """Callback del timer para verificar estado de comunicación"""
    update_communication_status()
    
    # Parpadeo del LED onboard como heartbeat
    led_onboard.on()
    time.sleep_ms(50)
    led_onboard.off()

def print_header():
    """Imprimir encabezado de inicio"""
    print("")
    print("╔══════════════════════════════════════╗")
    print("║       RASPBERRY PI PICO READY       ║")
    print("║        CON LEDs DE ESTADO            ║")
    print("╚══════════════════════════════════════╝")
    print("")
    print("Configuración:")
    print("• TX: GP0 → ESP32 GPIO16(RX)")
    print("• RX: GP1 ← ESP32 GPIO17(TX)")
    print("• UART Baudrate: 9600")
    print("")
    print("LEDs de Estado:")
    print("• GP2 (LED Verde): Comunicación OK")
    print("• GP3 (LED Rojo):  Sin Comunicación")
    print("• GP25 (Onboard):  Heartbeat")
    print("")
    print("Timeout de comunicación: 8 segundos")
    print("════════════════════════════════════════")

def send_response_to_esp32(original_msg):
    """Enviar respuesta al ESP32"""
    try:
        response = f"Pico→ESP32: ACK_{message_count} [OK]"
        uart.write(f"{response}\n".encode('utf-8'))
        print(f"📤 ENVIADO: {response}")
        
        # Parpadeo rápido del LED verde al enviar
        for _ in range(3):
            led_comm_ok.off()
            time.sleep_ms(50)
            led_comm_ok.on()
            time.sleep_ms(50)
            
        return True
    except Exception as e:
        print(f"❌ Error enviando respuesta: {e}")
        blink_led(led_comm_fail, 3, 100)
        return False

# Inicialización
print_header()

# Estado inicial: Sin comunicación
led_comm_ok.off()
led_comm_fail.on()
led_onboard.off()

print("🔴 ESTADO INICIAL: Esperando primera comunicación...")
print("────────────────────────────────────────")

# Configurar timer para heartbeat y verificación de estado
heartbeat_timer = Timer()
heartbeat_timer.init(period=2000, mode=Timer.PERIODIC, callback=heartbeat_callback)

# Parpadeo inicial de todos los LEDs
print("🔧 Probando LEDs...")
for led in [led_comm_ok, led_comm_fail, led_onboard]:
    blink_led(led, 2, 200)
time.sleep(1)

# Bucle principal
while True:
    try:
        # Verificar si hay datos del ESP32
        if uart.any():
            received = uart.readline()
            if received:
                try:
                    # Decodificar mensaje
                    decoded_msg = received.decode('utf-8').strip()
                    current_time = time.ticks_ms()
                    
                    if len(decoded_msg) > 0:
                        print(f"📥 RECIBIDO: {decoded_msg}")
                        print(f"   └─ Timestamp: {current_time}ms")
                        
                        # Actualizar tiempo de último mensaje recibido
                        last_received_time = current_time
                        
                        # Verificar si es mensaje válido del ESP32
                        if "ESP32" in decoded_msg and "Pico" in decoded_msg:
                            print("   ✅ Comunicación EXITOSA con ESP32!")
                            
                            # Enviar respuesta
                            if send_response_to_esp32(decoded_msg):
                                message_count += 1
                                
                                # Forzar actualización inmediata del estado
                                update_communication_status()
                            
                        else:
                            print("   ⚠️  Formato de mensaje inesperado")
                            # Parpadeo del LED Azul para mensaje inesperado
                            blink_led(led_comm_fail, 2, 100)
                        
                        print("────────────────────────────────────────")
                        
                except UnicodeDecodeError:
                    print("   ❌ Error al decodificar mensaje")
                    blink_led(led_comm_fail, 3, 50)
        
        # Pequeña pausa para no saturar el procesador
        time.sleep_ms(100)
        
    except Exception as e:
        print(f"❌ Error en bucle principal: {e}")
        # Error crítico: parpadear ambos LEDs
        for _ in range(3):
            led_comm_ok.on()
            led_comm_fail.on()
            time.sleep_ms(200)
            led_comm_ok.off()
            led_comm_fail.off()
            time.sleep_ms(200)
        time.sleep(1)


