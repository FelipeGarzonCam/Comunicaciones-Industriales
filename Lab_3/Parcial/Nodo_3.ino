#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// Configuración AP WiFi
const char* ap_ssid = "ESP32_AP_Parcial";
const char* ap_password = "12345678";

IPAddress local_IP(10, 10, 10, 1);
IPAddress gateway(10, 10, 10, 1);
IPAddress subnet(255, 255, 255, 0);

WebServer server(80);

String ultimo_mensaje = "";
String origen_mensaje = "";
int mensajes_procesados = 0;

void setup() {
  Serial.begin(115200);
  delay(2000);
  
  Serial.println("==========================================================");
  Serial.println("NODO 3: ESP32 (Intermediario Serial -> WiFi)");
  Serial.println("Universidad Santo Tomas - Parcial Red Lineal");
  Serial.println("==========================================================");
  Serial.println();
  
  // Configurar AP WiFi
  Serial.println("[INFO] Configurando Access Point WiFi...");
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ap_ssid, ap_password);
  
  IPAddress IP = WiFi.softAPIP();
  Serial.print("[OK] AP WiFi activo: ");
  Serial.println(ap_ssid);
  Serial.print("[OK] IP AP: ");
  Serial.println(IP);
  Serial.println();
  
  // Configurar rutas del servidor web
  server.on("/obtener", HTTP_GET, handleObtener);
  server.begin();
  
  Serial.println("[INFO] Servidor HTTP iniciado en puerto 80");
  Serial.println();
  Serial.println("----------------------------------------------------------");
  Serial.println("Esperando datos del PC (Serial)...");
  Serial.println("----------------------------------------------------------");
  Serial.println();
}

void loop() {
  server.handleClient();
  
  // Leer datos del Serial (PC)
  if (Serial.available()) {
    String linea = Serial.readStringUntil('\n');
    linea.trim();
    
    if (linea.length() > 0) {
      procesarMensajeSerial(linea);
    }
  }
  
  delay(10);
}

void procesarMensajeSerial(String datos) {
  String timestamp = obtenerTimestamp();
  
  Serial.print("["); Serial.print(timestamp);
  Serial.println("] <- MENSAJE RECIBIDO desde PC (Serial)");
  
  // Parsear JSON
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, datos);
  
  if (!error) {
    ultimo_mensaje = doc["mensaje"].as<String>();
    origen_mensaje = doc["origen"].as<String>();
    
    Serial.print("         Contenido: '");
    Serial.print(ultimo_mensaje);
    Serial.println("'");
    Serial.print("         Bytes: ");
    Serial.println(ultimo_mensaje.length());
    Serial.println();
    
    // Enviar ACK al PC
    Serial.println("ESP32_ACK");
    
    Serial.print("["); Serial.print(timestamp);
    Serial.println("] -> ACK enviado al PC");
    Serial.println();
    
    Serial.print("["); Serial.print(timestamp);
    Serial.println("] -> Mensaje disponible para Tablet via WiFi");
    Serial.print("         URL: http://");
    Serial.print(WiFi.softAPIP());
    Serial.println("/obtener");
    Serial.println();
    
    mensajes_procesados++;
  } else {
    Serial.println("         Error parseando JSON");
  }
}

void handleObtener() {
  String timestamp = obtenerTimestamp();
  
  Serial.print("["); Serial.print(timestamp);
  Serial.println("] <- Solicitud HTTP desde Tablet");
  
  if (ultimo_mensaje.length() > 0) {
    // Crear respuesta JSON
    StaticJsonDocument<256> doc;
    doc["mensaje"] = ultimo_mensaje;
    doc["origen"] = origen_mensaje;
    doc["ruta"] = "Celular -> PC -> ESP32 -> Tablet";
    
    String response;
    serializeJson(doc, response);
    
    server.send(200, "application/json", response);
    
    Serial.print("["); Serial.print(timestamp);
    Serial.println("] -> Mensaje enviado a Tablet");
    Serial.println();
    
    // Limpiar después de enviar
    ultimo_mensaje = "";
    origen_mensaje = "";
  } else {
    server.send(404, "text/plain", "No hay mensajes");
    Serial.println("         No hay mensajes disponibles");
  }
}

String obtenerTimestamp() {
  unsigned long ms = millis();
  int hours = 18;
  int minutes = 15;
  int seconds = (ms / 1000) % 60;
  int millisecs = ms % 1000;
  
  String timestamp = "";
  if (hours < 10) timestamp += "0";
  timestamp += String(hours) + ":";
  if (minutes < 10) timestamp += "0";
  timestamp += String(minutes) + ":";
  if (seconds < 10) timestamp += "0";
  timestamp += String(seconds) + ".";
  if (millisecs < 100) timestamp += "0";
  if (millisecs < 10) timestamp += "0";
  timestamp += String(millisecs);
  
  return timestamp;
}
