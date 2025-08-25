HardwareSerial mySerial(2); // Usar UART2

#define TXD2 17  // Pin TX para comunicación con Pico
#define RXD2 16  // Pin RX para comunicación con Pico
#define LED_BUILTIN 2  // LED interno del ESP32

int counter = 0;
unsigned long lastSend = 0;
const unsigned long sendInterval = 3000; // Enviar cada 3 segundos

void setup() {
  // Inicializar Serial USB para monitor
  Serial.begin(115200);
  while(!Serial) delay(10);
  
  // Configurar LED interno
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  // Configurar UART2 para comunicación con Pico
  mySerial.begin(9600, SERIAL_8N1, RXD2, TXD2);
  
  // Mensajes de inicio
  Serial.println("");
  Serial.println("╔══════════════════════════════════════╗");
  Serial.println("║          ESP32 UART READY           ║");
  Serial.println("╚══════════════════════════════════════╝");
  Serial.println("");
  Serial.println("Configuración:");
  Serial.println("• TX: GPIO17 → Pico GP1(RX)");
  Serial.println("• RX: GPIO16 ← Pico GP0(TX)");
  Serial.println("• UART Baudrate: 9600");
  Serial.println("• USB Serial: 115200");
  Serial.println("");
  Serial.println("Iniciando comunicación con Raspberry Pi Pico...");
  Serial.println("════════════════════════════════════════");
  
  // Parpadeo inicial
  for(int i = 0; i < 3; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
  }
}

void loop() {
  unsigned long currentTime = millis();
  
  // Enviar mensaje al Pico cada 3 segundos
  if (currentTime - lastSend >= sendInterval) {
    String message = "ESP32→Pico: MSG_" + String(counter) + " [" + String(currentTime) + "ms]";
    mySerial.println(message);
    
    Serial.println("📤 ENVIADO: " + message);
    Serial.println("   └─ Esperando respuesta del Pico...");
    
    // Parpadeo corto al enviar
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    
    counter++;
    lastSend = currentTime;
  }
  
  // Escuchar respuestas del Pico
  if (mySerial.available()) {
    String received = mySerial.readStringUntil('\n');
    received.trim(); // Eliminar espacios en blanco
    
    if (received.length() > 0) {
      Serial.println("📥 RECIBIDO: " + received);
      
      // Verificar si es respuesta válida del Pico
      if (received.indexOf("Pico") != -1) {
        Serial.println("   ✅ Comunicación EXITOSA con Pico!");
        
        // LED más largo para éxito
        digitalWrite(LED_BUILTIN, HIGH);
        delay(300);
        digitalWrite(LED_BUILTIN, LOW);
      } else {
        Serial.println("   ⚠️  Mensaje inesperado del Pico");
      }
      
      Serial.println("────────────────────────────────────────");
    }
  }
  
  // Pequeña pausa para no saturar
  delay(50);
}
