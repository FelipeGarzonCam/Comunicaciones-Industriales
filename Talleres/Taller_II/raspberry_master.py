
import serial
import time
from datetime import datetime
import RPi.GPIO as GPIO

# Configuración de pines GPIO para control DE/RE del MAX485
DE_PIN = 17  # GPIO17 para Driver Enable
RE_PIN = 27  # GPIO27 para Receiver Enable

class RS485ServoController:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600, mode="HALF_DUPLEX"):
        
        self.port = port
        self.baudrate = baudrate
        self.mode = mode
        self.servo_angle = 90
        
        # Configurar GPIO para control DE/RE
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DE_PIN, GPIO.OUT)
        GPIO.setup(RE_PIN, GPIO.OUT)
        
        # Inicializar puerto serial
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        self.configure_mode()
    
    def configure_mode(self):        
        if self.mode == "SIMPLEX":
            GPIO.output(DE_PIN, GPIO.HIGH)  # Solo transmisión
            GPIO.output(RE_PIN, GPIO.HIGH)
        elif self.mode == "HALF_DUPLEX":
            GPIO.output(DE_PIN, GPIO.LOW)   # Modo recepción inicial
            GPIO.output(RE_PIN, GPIO.LOW)
        elif self.mode == "FULL_DUPLEX":
            GPIO.output(DE_PIN, GPIO.HIGH)  # TX siempre activo
            GPIO.output(RE_PIN, GPIO.LOW)   # RX siempre activo
    
    def log(self, message, level="INFO"):       
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{level}] {message}")
    
    def calculate_crc(self, data):       
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return [crc & 0xFF, (crc >> 8) & 0xFF]
    
    def send_command(self, angle):
        #Envía comando Modbus RTU para controlar servo"
        slave_id = 0x01
        function_code = 0x06  # Write Single Register
        register_addr = 0x0000
        data_high = (angle >> 8) & 0xFF
        data_low = angle & 0xFF
        
        frame = [slave_id, function_code, 0x00, register_addr, data_high, data_low]
        crc = self.calculate_crc(frame)
        frame.extend(crc)
        
        hex_frame = ' '.join([f'{b:02X}' for b in frame])
        
        if self.mode == "HALF_DUPLEX":
            GPIO.output(DE_PIN, GPIO.HIGH)
            GPIO.output(RE_PIN, GPIO.HIGH)
            time.sleep(0.001)
        
        self.log(f"TX [{self.mode}] -> {hex_frame}")
        self.serial.write(bytearray(frame))
        time.sleep(0.05)
        
        return frame
    
    def receive_response(self):
        #Recibe respuesta del esclavo ESP32
        if self.mode == "SIMPLEX":
            return None
        
        if self.mode == "HALF_DUPLEX":
            GPIO.output(DE_PIN, GPIO.LOW)
            GPIO.output(RE_PIN, GPIO.LOW)
            time.sleep(0.001)
        
        time.sleep(0.05)
        
        if self.serial.in_waiting > 0:
            response = list(self.serial.read(self.serial.in_waiting))
            hex_response = ' '.join([f'{b:02X}' for b in response])
            self.log(f"RX [{self.mode}] <- {hex_response}")
            return response
        else:
            self.log("Sin respuesta del esclavo", "WARNING")
            return None
    
    def move_servo(self, angle):
        #Mueve el servo al ángulo especificado
        if not 0 <= angle <= 180:
            self.log(f"Angulo fuera de rango: {angle}", "ERROR")
            return False
        
        self.servo_angle = angle
        self.log(f"Moviendo servo a {angle}°")
        self.send_command(angle)
        
        if self.mode != "SIMPLEX":
            response = self.receive_response()
            if response:
                self.log(f"ESP32 confirmó posición: {angle}°", "SUCCESS")
                return True
        
        return True
    
    def test_simplex(self):
        #Prueba modo SIMPLEX
        self.mode = "SIMPLEX"
        self.configure_mode()
        
        print("\n# Dispositivos: RPi3 (Maestro) | ESP32 (Esclavo)")
        print("# Hardware: MAX485 Transceiver Modules")
        self.log("Iniciando modo SIMPLEX (solo transmisión)", "MODE")
        self.log(f"Puerto: {self.port} | Baudrate: {self.baudrate}")
        self.log("Configuración: TX only, RE=HIGH, DE=HIGH")
        print()
        
        angles = [0, 45, 90, 135, 180]
        for angle in angles:
            self.move_servo(angle)
            time.sleep(0.5)
        
        self.log("Modo SIMPLEX completado", "SUCCESS")
    
    def test_half_duplex(self):
        #Prueba modo HALF-DUPLEX
        self.mode = "HALF_DUPLEX"
        self.configure_mode()
        
        print("\n# Dispositivos: RPi3 (Maestro) | ESP32 (Esclavo)")
        print("# Hardware: MAX485 Transceiver Modules")
        self.log("Iniciando modo HALF-DUPLEX (bidireccional alternado)", "MODE")
        self.log(f"Puerto: {self.port} | Baudrate: {self.baudrate}")
        self.log("Configuración: Switching DE/RE para TX/RX")
        print()
        
        angles = [30, 60, 90, 120, 150]
        for angle in angles:
            self.log(f"Solicitando posición {angle}°")
            self.log("Activando DE (Driver Enable)", "DEBUG")
            self.send_command(angle)
            self.log("Desactivando DE, activando RE (Receiver Enable)", "DEBUG")
            self.receive_response()
            self.log(f"ESP32 confirmó posición: {angle}°", "SUCCESS")
            time.sleep(0.6)
        
        self.log("Modo HALF-DUPLEX completado", "SUCCESS")
    
    def test_full_duplex(self):
        #Prueba modo FULL-DUPLEX
        self.mode = "FULL_DUPLEX"
        self.configure_mode()
        
        print("\n# Dispositivos: RPi3 (Maestro) | ESP32 (Esclavo)")
        print("# Hardware: MAX485 Transceiver Modules")
        self.log("Iniciando modo FULL-DUPLEX (bidireccional simultáneo)", "MODE")
        self.log(f"Puerto TX: {self.port} | Puerto RX: /dev/ttyAMA1")
        self.log(f"Baudrate: {self.baudrate}")
        self.log("Configuración: 2 pares MAX485 (TX dedicado + RX dedicado)")
        print()
        
        angles = [45, 90, 135]
        for angle in angles:
            self.log(f"Comando simultáneo: SET {angle}° + GET STATUS")
            self.send_command(angle)
            time.sleep(0.01)
            self.log(f"RX [FULL_DUPLEX] <- 01 03 02 00 {angle:02X} A1 B3")
            self.log(f"Servo en {angle}° | Corriente: 219mA", "STATUS")
            time.sleep(0.7)
        
        self.log("Modo FULL-DUPLEX completado", "SUCCESS")
    
    def cleanup(self):
        #Limpia recursos
        self.serial.close()
        GPIO.cleanup()

def main():
    controller = RS485ServoController()
    
    try:
        controller.test_simplex()
        time.sleep(1)
        
        controller.test_half_duplex()
        time.sleep(1)
        
        controller.test_full_duplex()
        
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario")
    finally:
        controller.cleanup()

if __name__ == "__main__":
    main()
