// Punto_3_ESP32_SINCRONIZADO.ino
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  delay(1000);
  
  Serial.println("ESP32 VRC/LRC Transmisor SINCRONIZADO");
  Serial.println("Usando delimitadores para sincronización");
  Serial.println("===========================================");
}

byte dataBlock[] = {0x48, 0x65, 0x6C, 0x6C, 0x6F}; // "Hello"
int cycle_count = 0;

byte calculateVRC(byte data) {
  byte parity = 0;
  for (int i = 0; i < 8; i++) {
    parity ^= (data >> i) & 1;
  }
  return parity;
}

byte calculateLRC(byte *data, int length) {
  byte lrc = 0;
  for (int i = 0; i < length; i++) {
    lrc ^= data[i];
  }
  return lrc;
}

void loop() {
  cycle_count++;
  
  Serial.println("\n=== NUEVO CICLO ===");
  Serial.print("Ciclo #"); Serial.println(cycle_count);
  
  // ===== FASE VRC =====
  Serial.println("\n--- Enviando VRC ---");
  
  // Enviar marcador de inicio VRC
  Serial2.write(0xAA); // Marcador VRC START
  delay(10);
  
  for (int i = 0; i < 5; i++) {
    byte data = dataBlock[i];
    byte vrc = calculateVRC(data);
    
    Serial2.write(data);
    Serial2.write(vrc);
    
    Serial.print("Data: 0x"); Serial.print(data, HEX);
    Serial.print(", VRC: "); Serial.println(vrc);
    delay(20);
  }
  
  // Enviar marcador de fin VRC
  Serial2.write(0xBB); // Marcador VRC END
  delay(500);
  
  // ===== FASE LRC =====
  Serial.println("\n--- Enviando LRC ---");
  
  // Enviar marcador de inicio LRC
  Serial2.write(0xCC); // Marcador LRC START
  delay(10);
  
  for (int i = 0; i < 5; i++) {
    Serial2.write(dataBlock[i]);
    Serial.print("Data: 0x"); Serial.println(dataBlock[i], HEX);
    delay(20);
  }
  
  byte lrc = calculateLRC(dataBlock, 5);
  Serial2.write(lrc);
  Serial.print("LRC: 0x"); Serial.println(lrc, HEX);
  
  // Enviar marcador de fin LRC
  Serial2.write(0xDD); // Marcador LRC END
  
  Serial.println("\n--- OVERHEAD CALCULADO ---");
  Serial.println("VRC: 10 bytes datos+VRC + 2 marcadores = 12 bytes");
  Serial.println("LRC: 6 bytes datos+LRC + 2 marcadores = 8 bytes");
  Serial.println("Eficiencia VRC: 41.7% (5/12), LRC: 62.5% (5/8)");
  
  delay(3000);
}
