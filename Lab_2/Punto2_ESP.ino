void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial2.begin(9600, SERIAL_8N1, 16, 17); 
  delay(1000);
  
  Serial.println("ESP32 Sender ARQ ready");
  Serial.println("Protocolo: Stop-and-Wait ARQ con ACK/NACK");
  Serial.println("Conexiones: GPIO16(RX) <- Pico GP0(TX), GPIO17(TX) -> Pico GP1(RX)");
  Serial.println("============================================================"); 
}

const uint8_t payload[] = {1, 2, 3, 4, 5};
int total_packets = 0;
int total_retries = 0;
int failed_packets = 0;

uint8_t checksum(const uint8_t *p, size_t n) {
  uint16_t s = 0;
  for(size_t i = 0; i < n; i++) {
    s += p[i];
  }
  return s & 0xFF;
}

void send_packet() {
  uint8_t cs = checksum(payload, sizeof(payload));
  
  // Trama
  Serial2.write(0x02);                    // STX
  Serial2.write(sizeof(payload));         // LEN
  Serial2.write(payload, sizeof(payload)); // PAYLOAD
  Serial2.write(cs);                      // CS 
  Serial2.write(0x03);                    // ETX
}

bool wait_ack(unsigned long timeout_ms) {
  unsigned long start = millis();
  while(millis() - start < timeout_ms) {
    if(Serial2.available()) {
      char r = (char)Serial2.read();
      if(r == 'A') return true;  // ACK recibido
      if(r == 'N') return false; // NACK recibido
    }
  }
  return false; // timeout tratar como NACK
}

void loop() {
  total_packets++;
  int tries = 0;
  const int max_tries = 3;
  bool success = false;
  
  Serial.println();
  Serial.println("--- Nuevo Paquete ---");
  Serial.print("Paquete #"); Serial.println(total_packets);
  Serial.print("Payload: [");
  for(int i = 0; i < sizeof(payload); i++) {
    Serial.print(payload[i]);
    if(i < sizeof(payload)-1) Serial.print(", ");
  }
  Serial.println("]");
  
  while(tries < max_tries && !success) {
    tries++;
    Serial.print("Intento "); Serial.print(tries); Serial.print("/"); Serial.print(max_tries);
    Serial.println(" - Enviando paquete...");
    
    send_packet();
    Serial.println("Paquete enviado, esperando ACK/NACK...");
    
    if(wait_ack(500)) { // timeout 500ms
      Serial.println("ACK recibido - Paquete confirmado");
      success = true;
    } else {
      Serial.println("NACK/timeout - Preparando retransmision");
      if(tries < max_tries) {
        total_retries++;
        Serial.print("Reintentos acumulados: "); Serial.println(total_retries);
      }
    }
  }
  
  if(!success) {
    Serial.println("FALLO TRAS TODOS LOS REINTENTOS");
    failed_packets++;
  }
  
  // Mostrar estadísticas actuales
  Serial.println();
  Serial.println("--- ESTADISTICAS ACTUALES ---");
  Serial.print("Paquetes enviados: "); Serial.println(total_packets);
  Serial.print("Reintentos totales: "); Serial.println(total_retries);
  Serial.print("Paquetes perdidos: "); Serial.println(failed_packets);
  if(total_packets > 0) {
    float avg_retries = (float)total_retries / total_packets;
    float loss_rate = (float)failed_packets / total_packets * 100;
    Serial.print("Reintentos promedio: "); Serial.println(avg_retries, 2);
    Serial.print("Tasa de perdida: "); Serial.print(loss_rate, 1); Serial.println("%");
  }
  Serial.println("========================================"); // CORREGIDO: línea fija
  
  delay(2000); // Pausa entre paquetes
}
