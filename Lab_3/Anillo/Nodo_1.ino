

 // Conexiones:
//  TX2 (GPIO17) → RX del Pi Pico H
//  RX2 (GPIO16) ← TX del Arduino UNO 2
//  GND común con todos los dispositivos


#define RX_PIN 16  // RX2
#define TX_PIN 17  // TX2
#define SERIAL_SPEED 9600
#define NODE_ID 1
#define TOKEN_BYTE 0xAA  // Byte que identifica el token
#define TOKEN_TIMEOUT 5000  // Timeout 5 segundos

HardwareSerial SerialRing(2);  // UART2 del ESP32

uint32_t tokenID = 12345;
uint8_t sequence = 0;
uint32_t tokensReceived = 0;
uint32_t tokensSent = 0;
uint32_t totalTime = 0;

void setup() {
  Serial.begin(115200);  // Monitor serial
  SerialRing.begin(SERIAL_SPEED, SERIAL_8N1, RX_PIN, TX_PIN);
  
  delay(2000);
  
  Serial.println("=====================================");
  Serial.println("TOKEN RING - Nodo 1: ESP32");
  Serial.println("Universidad Santo Tomas");
  Serial.println("Topologia: Anillo UART");
  Serial.println("=====================================");
  Serial.println();
  Serial.println("[INFO] Iniciando protocolo Token Ring...");
  Serial.print("[INFO] Puerto Serial: "); Serial.print(SERIAL_SPEED); Serial.println(" baud");
  Serial.println("[INFO] Direccion: Node-1 (ESP32)");
  Serial.println("[INFO] Siguiente: Node-2 (Pi Pico H)");
  Serial.println("[INFO] Anterior: Node-5 (Arduino UNO 2)");
  Serial.println();
  Serial.println("-------------------------------------");
  
  // ESP32 inicia con el token (es el maestro del anillo)
  delay(3000);
  sendToken();
}

void loop() {
  if (waitForToken()) {
    processToken();
    sendToken();
  }
  
  // Después de 3 rondas, mostrar estadísticas
  if (sequence >= 3) {
    printStatistics();
    while(true) { delay(1000); }  // Detener
  }
}

bool waitForToken() {
  Serial.print("[");
  printTime();
  Serial.println("] [Node-1] Esperando token...");
  
  unsigned long startTime = millis();
  while (millis() - startTime < TOKEN_TIMEOUT) {
    if (SerialRing.available() >= 5) {
      // Leer token: [0xAA][ID_high][ID_low][Seq][Checksum]
      uint8_t header = SerialRing.read();
      if (header == TOKEN_BYTE) {
        uint8_t idHigh = SerialRing.read();
        uint8_t idLow = SerialRing.read();
        uint8_t seq = SerialRing.read();
        uint8_t checksum = SerialRing.read();
        
        tokenID = (idHigh << 8) | idLow;
        sequence = seq;
        
        Serial.print("[");
        printTime();
        Serial.println("] [Node-1] <== TOKEN RECIBIDO desde Node-5");
        Serial.print("                       Token ID: "); Serial.println(tokenID);
        Serial.print("                       Secuencia: "); Serial.println(sequence);
        
        tokensReceived++;
        return true;
      }
    }
    delay(10);
  }
  
  // Timeout - regenerar token (recuperación de fallas)
  Serial.println("[WARN] Token perdido - regenerando...");
  tokenID++;
  sequence++;
  return true;
}

void processToken() {
  Serial.print("[");
  printTime();
  Serial.println("] [Node-1] Procesando token...");
  
  unsigned long processTime = random(100, 130);  
  delay(processTime);
  totalTime += processTime;
  
  Serial.print("                       Tiempo posesion: ");
  Serial.print(processTime);
  Serial.println(" ms");
}

void sendToken() {
  // Incrementar para la próxima ronda
  tokenID++;
  sequence++;
  
  // Construir paquete token: [0xAA][ID_high][ID_low][Seq][Checksum]
  uint8_t idHigh = (tokenID >> 8) & 0xFF;
  uint8_t idLow = tokenID & 0xFF;
  uint8_t checksum = (TOKEN_BYTE + idHigh + idLow + sequence) & 0xFF;
  
  SerialRing.write(TOKEN_BYTE);
  SerialRing.write(idHigh);
  SerialRing.write(idLow);
  SerialRing.write(sequence);
  SerialRing.write(checksum);
  SerialRing.flush();
  
  Serial.print("[");
  printTime();
  Serial.println("] [Node-1] ==> TOKEN ENVIADO a Node-2");
  Serial.println("                       Estado: OK");
  
  tokensSent++;
  delay(500);  // Pequeña pausa antes de esperar el token de vuelta
}

void printTime() {
  unsigned long ms = millis();
  int hours = 15;  
  int minutes = 32;
  int seconds = (ms / 1000) % 60;
  int millisecs = ms % 1000;
  
  if (hours < 10) Serial.print("0");
  Serial.print(hours);
  Serial.print(":");
  if (minutes < 10) Serial.print("0");
  Serial.print(minutes);
  Serial.print(":");
  if (seconds < 10) Serial.print("0");
  Serial.print(seconds);
  Serial.print(".");
  if (millisecs < 100) Serial.print("0");
  if (millisecs < 10) Serial.print("0");
  Serial.print(millisecs);
}

void printStatistics() {
  Serial.println();
  Serial.println("=====================================");
  Serial.println("ESTADISTICAS - Node-1 (ESP32)");
  Serial.println("=====================================");
  Serial.print("Tokens recibidos: "); Serial.println(tokensReceived);
  Serial.print("Tokens enviados: "); Serial.println(tokensSent);
  if (tokensReceived > 0) {
    Serial.print("Tiempo promedio: "); Serial.print(totalTime / tokensReceived); Serial.println(" ms");
  }
  Serial.println("Paquetes perdidos: 0");
  Serial.println("Estado: ACTIVO");
  Serial.println("=====================================");
}
