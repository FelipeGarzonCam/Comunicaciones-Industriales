
#include <HardwareSerial.h>
#include <ESP32Servo.h>

// Pines de configuración
#define DE_PIN 4           // Driver Enable del MAX485
#define RE_PIN 5           // Receiver Enable del MAX485
#define RX_PIN 16          // UART2 RX
#define TX_PIN 17          // UART2 TX
#define SERVO_PIN 18       // PWM para servo

// Configuración Modbus
#define SLAVE_ID 0x01
#define BAUDRATE 9600

HardwareSerial RS485Serial(2);
Servo servoMotor;

int currentAngle = 90;
uint8_t rxBuffer[8];
int rxIndex = 0;

void setup() {
  Serial.begin(115200);
  
  // Configurar pines DE/RE
  pinMode(DE_PIN, OUTPUT);
  pinMode(RE_PIN, OUTPUT);
  
  // Modo recepción por defecto
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);
  
  // Inicializar RS-485
  RS485Serial.begin(BAUDRATE, SERIAL_8N1, RX_PIN, TX_PIN);
  
  // Inicializar servo
  servoMotor.attach(SERVO_PIN);
  servoMotor.write(currentAngle);
  
  Serial.println("ESP32 Esclavo RS-485 iniciado");
  Serial.println("ID: 0x01 | Baudrate: 9600");
  Serial.println("Esperando comandos del maestro...");
}

void loop() {
  if (RS485Serial.available() > 0) {
    uint8_t byte = RS485Serial.read();
    rxBuffer[rxIndex++] = byte;
    
    // Trama Modbus completa: 8 bytes
    if (rxIndex >= 8) {
      processModbusFrame();
      rxIndex = 0;
    }
  }
}

void processModbusFrame() {
  // Verificar ID del esclavo
  if (rxBuffer[0] != SLAVE_ID) {
    return;
  }
  
  uint8_t functionCode = rxBuffer[1];
  
  // Function Code 0x06: Write Single Register
  if (functionCode == 0x06) {
    uint16_t angle = (rxBuffer[4] << 8) | rxBuffer[5];
    
    // Verificar CRC
    if (checkCRC(rxBuffer, 6)) {
      // Mover servo
      if (angle >= 0 && angle <= 180) {
        currentAngle = angle;
        servoMotor.write(currentAngle);
        
        Serial.print("Servo movido a: ");
        Serial.print(currentAngle);
        Serial.println("°");
        
        // Enviar respuesta (echo de la trama recibida)
        sendResponse(rxBuffer, 8);
      }
    }
  }
}

void sendResponse(uint8_t* data, int len) {
  // Cambiar a modo transmisión
  digitalWrite(DE_PIN, HIGH);
  digitalWrite(RE_PIN, HIGH);
  delayMicroseconds(100);
  
  // Enviar trama
  RS485Serial.write(data, len);
  RS485Serial.flush();
  
  delayMicroseconds(100);
  
  // Volver a modo recepción
  digitalWrite(DE_PIN, LOW);
  digitalWrite(RE_PIN, LOW);
}

bool checkCRC(uint8_t* data, int len) {
  uint16_t crc = 0xFFFF;
  
  for (int i = 0; i < len; i++) {
    crc ^= data[i];
    for (int j = 0; j < 8; j++) {
      if (crc & 0x0001) {
        crc = (crc >> 1) ^ 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  
  uint8_t crcLow = crc & 0xFF;
  uint8_t crcHigh = (crc >> 8) & 0xFF;
  
  return (data[len] == crcLow && data[len + 1] == crcHigh);
}
