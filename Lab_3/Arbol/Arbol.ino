/*********
  ESP32 - Comunicación Serial para topología árbol
  Envía datos JSON por puerto serial al PC
*********/

#include <ArduinoJson.h>

const int ledPin = 2;

float temperatura = 25.0;
float humedad = 60.0;
int luz = 500;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  
  Serial.println("ESP32 iniciado - Modo Serial");
  Serial.println("Enviando datos JSON al PC cada 10 segundos");
  Serial.println("Comandos: status, test, ledon, ledoff");
  Serial.println("========================================");  
  
  randomSeed(analogRead(0));
}

void enviarDatosSerial() {
  // Crear JSON con datos de sensores
  StaticJsonDocument<300> doc;
  doc["node_id"] = "ESP32_001";
  doc["timestamp"] = millis();
  doc["temperatura"] = temperatura;
  doc["humedad"] = humedad;
  doc["luz"] = luz;
  doc["led_estado"] = digitalRead(ledPin);
  doc["modo"] = "SERIAL_TREE";
  doc["uptime"] = millis() / 1000;
  
  // Enviar JSON por serial
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Marcador para que Python identifique fácilmente los datos
  Serial.println(">>JSON_START");
  Serial.println(jsonString);
  Serial.println(">>JSON_END");
}

void procesarComandosSerial() {
  if (Serial.available()) {
    String comando = Serial.readString();
    comando.trim();
    
    if (comando == "status") {
      Serial.println("=== STATUS ESP32 ===");
      Serial.println("Modo: SERIAL TREE");
      Serial.println("Temp: " + String(temperatura) + "°C");
      Serial.println("Humedad: " + String(humedad) + "%");
      Serial.println("Luz: " + String(luz));
      Serial.println("LED: " + String(digitalRead(ledPin) ? "ON" : "OFF"));
      Serial.println("Uptime: " + String(millis() / 1000) + "s");
    }
    else if (comando == "test") {
      Serial.println("Enviando datos de prueba...");
      enviarDatosSerial();
    }
    else if (comando == "ledon") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED encendido");
    }
    else if (comando == "ledoff") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED apagado");
    }
    else if (comando.startsWith("led ")) {
      String estado = comando.substring(4);
      if (estado == "on") {
        digitalWrite(ledPin, HIGH);
        Serial.println("LED encendido via comando");
      } else if (estado == "off") {
        digitalWrite(ledPin, LOW);
        Serial.println("LED apagado via comando");
      }
    }
    else if (comando.length() > 0) {
      Serial.println("Comando desconocido: " + comando);
    }
  }
}

void simularSensores() {
  // Simular variaciones realistas
  temperatura += random(-5, 6) / 10.0;
  if (temperatura < 18) temperatura = 18;
  if (temperatura > 32) temperatura = 32;
  
  humedad += random(-3, 4);
  if (humedad < 40) humedad = 40;
  if (humedad > 85) humedad = 85;
  
  luz += random(-30, 31);
  if (luz < 100) luz = 100;
  if (luz > 900) luz = 900;
}

void loop() {
  static unsigned long lastSensor = 0;
  static unsigned long lastSend = 0;
  
  procesarComandosSerial();
  
  // Simular sensores cada 3 segundos
  if (millis() - lastSensor > 3000) {
    simularSensores();
    lastSensor = millis();
  }
  
  // Enviar datos cada 10 segundos
  if (millis() - lastSend > 10000) {
    enviarDatosSerial();
    lastSend = millis();
  }
  
  delay(100);  // Pequeña pausa
}
