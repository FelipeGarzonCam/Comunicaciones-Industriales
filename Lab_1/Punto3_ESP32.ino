// Comunicación SPI - ESP32 como Esclavo
// Controla LED según comandos recibidos del maestro (Raspberry Pi Pico)

#define LED_PIN 2     // LED integrado del ESP32
#define SS_PIN 5      // Chip Select (CS) 
#define SCK_PIN 18    // Reloj SPI
#define MOSI_PIN 23   // Datos del maestro al esclavo
#define MISO_PIN 19   // Datos del esclavo al maestro

void setup() {
  Serial.begin(115200);
  
  // Configurar LED como salida
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Configurar pines SPI
  pinMode(SS_PIN, INPUT_PULLUP);    // CS con pull-up
  pinMode(SCK_PIN, INPUT);          // Reloj como entrada
  pinMode(MOSI_PIN, INPUT);         // Datos como entrada
  pinMode(MISO_PIN, OUTPUT);        // Respuesta como salida
  
  Serial.println("ESP32 SPI Esclavo iniciado");
  Serial.println("Esperando comandos del maestro...");
  
  // Test inicial del LED
  parpadearLED(3);
}

void loop() {
  // Verificar si el maestro activó CS (señal LOW)
  if (digitalRead(SS_PIN) == LOW) {
    
    // Leer comando SPI del maestro
    byte comando = leerComandoSPI();
    
    if (comando != 0xFF) {  // 0xFF indica comando inválido
      procesarComando(comando);
    }
  }
  
  delay(1);  // Pequeña pausa para estabilidad
}

byte leerComandoSPI() {
  byte comando = 0;
  int bitsLeidos = 0;
  
  // Timeout para evitar bloqueos
  unsigned long tiempoLimite = millis() + 100;
  
  // Leer 8 bits del comando
  while (digitalRead(SS_PIN) == LOW && millis() < tiempoLimite && bitsLeidos < 8) {
    
    // Esperar flanco de subida del reloj
    while (digitalRead(SCK_PIN) == LOW && digitalRead(SS_PIN) == LOW && millis() < tiempoLimite) {
      delayMicroseconds(1);
    }
    
    if (digitalRead(SS_PIN) == HIGH || millis() >= tiempoLimite) break;
    
    // Leer bit en el flanco de subida
    if (digitalRead(MOSI_PIN) == HIGH) {
      comando |= (1 << (7 - bitsLeidos));
    }
    
    bitsLeidos++;
    
    // Esperar flanco de bajada del reloj
    while (digitalRead(SCK_PIN) == HIGH && digitalRead(SS_PIN) == LOW && millis() < tiempoLimite) {
      delayMicroseconds(1);
    }
  }
  
  // Retornar comando valido solo si se leyeron 8 bits completos
  return (bitsLeidos == 8) ? comando : 0xFF;
}

void procesarComando(byte comando) {
  Serial.print("Comando recibido: 0x");
  Serial.print(comando, HEX);
  
  switch(comando) {
    case 0x01:
      digitalWrite(LED_PIN, HIGH);
      Serial.println(" - LED ENCENDIDO");
      break;
      
    case 0x00:
      digitalWrite(LED_PIN, LOW);
      Serial.println(" - LED APAGADO");
      break;
      
    default:
      Serial.println(" - Comando desconocido");
      break;
  }
}

// Función auxiliar para test inicial
void parpadearLED(int veces) {
  for(int i = 0; i < veces; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}
