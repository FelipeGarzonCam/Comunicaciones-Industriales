void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial2.begin(9600, SERIAL_8N1, 16, 17);
  delay(1000);
  
  Serial.println("ESP32 checksum sender ready (inyección de errores CORREGIDA)");
  Serial.println("Cada 3 paquetes: datos alterados pero checksum original");
}

uint8_t payload[] = {10, 20, 30, 40, 50}; // No const para modificar
int packet_count = 0;

uint8_t checksum(const uint8_t *p, size_t n) {
  uint16_t s = 0;
  for(size_t i = 0; i < n; i++) {
    s += p[i];
  }
  return s & 0xFF;
}

void loop() {
  packet_count++;
  
  
  uint8_t cs = checksum(payload, sizeof(payload)); // 1. Checksum con datos originales
  bool error_inyectado = false;
  
  // 2. DESPUÉS alterar payload para transmisión
  if(packet_count % 3 == 0){
    payload[1] = payload[1] ^ 0xFF; // Alterar byte
    error_inyectado = true;
    Serial.println("*** ERROR INYECTADO: Payload alterado, checksum SIN modificar ***");
  }
  
  Serial.println("\n--- Enviando paquete ---");
  Serial.print("Paquete #"); Serial.print(packet_count);
  if(error_inyectado) Serial.print(" (CON ERROR INTENCIONAL)");
  Serial.println();
  
  Serial.print("Payload a enviar: [");
  for(int i = 0; i < sizeof(payload); i++) {
    Serial.print(payload[i]);
    if(i < sizeof(payload)-1) Serial.print(", ");
  }
  Serial.println("]");
  Serial.print("Checksum (calculado con originales): ");
  Serial.println(cs);
  
  // 3. Enviar datos alterados + checksum original
  Serial2.write(0x02);                    // STX
  Serial2.write(sizeof(payload));         // LEN = 5  
  Serial2.write(payload, sizeof(payload)); // PAYLOAD alterado
  Serial2.write(cs);                      // CS original 
  Serial2.write(0x03);                    // ETX
  
  Serial.println("¡Paquete enviado! (datos alterados + checksum original)");
  
  // 4. Restaurar payload original
  if(error_inyectado){
    payload[1] = payload[1] ^ 0xFF; // Restaurar
    Serial.println("Payload restaurado a valores originales");
  }
  
  delay(3000);
}
