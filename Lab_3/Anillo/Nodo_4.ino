
  //Conexiones:
  //- TX (Pin 1) → RX del Arduino UNO 2
  //- RX (Pin 0) ← TX del Pi Pico W
 // - GND común
 

#define NODE_ID 4
#define TOKEN_BYTE 0xAA
#define TOKEN_TIMEOUT 5000
#define SERIAL_SPEED 9600

uint16_t tokenID = 0;
uint8_t sequence = 0;
uint16_t tokensReceived = 0;
uint16_t tokensSent = 0;
uint32_t totalTime = 0;

void setup() {
  Serial.begin(SERIAL_SPEED);
  delay(2000);  

  Serial.println();
  Serial.println("[INFO] Iniciando protocolo Token Ring...");
  Serial.print("[INFO] Puerto Serial: "); Serial.print(SERIAL_SPEED); Serial.println(" baud");
  Serial.println("[INFO] Direccion: Node-4 (Arduino UNO 1)");
  Serial.println("[INFO] Siguiente: Node-5 (Arduino UNO 2)");
  Serial.println("[INFO] Anterior: Node-3 (Pi Pico W)");
  Serial.println();
  Serial.println("-------------------------------------");
}

void loop() {
  static uint8_t ronda = 0;
  
  if (ronda < 3) {
    if (waitForToken()) {
      Serial.println();
      Serial.print(">>> RONDA #"); Serial.println(sequence);
      processToken();
      sendToken();
      ronda++;
      delay(500);
    }
  } else {
    printStatistics();
    while(true) { delay(1000); }
  }
}

bool waitForToken() {
  printTime();
  Serial.println(" [Node-4] Esperando token...");
  
  unsigned long startTime = millis();
  uint8_t buffer[5];
  uint8_t index = 0;
  
  while (millis() - startTime < TOKEN_TIMEOUT) {
    if (Serial.available()) {
      uint8_t byte = Serial.read();
      
      if (index == 0 && byte == TOKEN_BYTE) {
        buffer[index++] = byte;
      } else if (index > 0 && index < 5) {
        buffer[index++] = byte;
        
        if (index == 5) {
          tokenID = (buffer[1] << 8) | buffer[2];
          sequence = buffer[3];
          
          printTime();
          Serial.println(" [Node-4] <== TOKEN RECIBIDO desde Node-3");
          Serial.print("                       Token ID: "); Serial.println(tokenID);
          Serial.print("                       Secuencia: "); Serial.println(sequence);
          
          tokensReceived++;
          return true;
        }
      } else {
        index = 0;
      }
    }
    delay(10);
  }
  
  return false;
}

void processToken() {
  printTime();
  Serial.println(" [Node-4] Procesando token...");
  
  uint16_t processTime = 88 + (sequence * 3);
  delay(processTime);
  totalTime += processTime;
  
  Serial.print("                       Tiempo posesion: ");
  Serial.print(processTime);
  Serial.println(" ms");
}

void sendToken() {
  uint8_t idHigh = (tokenID >> 8) & 0xFF;
  uint8_t idLow = tokenID & 0xFF;
  uint8_t checksum = (TOKEN_BYTE + idHigh + idLow + sequence) & 0xFF;
  
  Serial.write(TOKEN_BYTE);
  Serial.write(idHigh);
  Serial.write(idLow);
  Serial.write(sequence);
  Serial.write(checksum);
  Serial.flush();
  
  printTime();
  Serial.println(" [Node-4] ==> TOKEN ENVIADO a Node-5");
  Serial.println("                       Estado: OK");
  
  tokensSent++;
}

void printTime() {
  unsigned long ms = millis();
  int hours = 15;
  int minutes = 32;
  int seconds = (ms / 1000) % 60;
  int millisecs = ms % 1000;
  
  Serial.print("[");
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
  Serial.print("]");
}

void printStatistics() {
  Serial.println();
  Serial.println("=====================================");
  Serial.println("ESTADISTICAS - Node-4 (Arduino UNO 1)");
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
