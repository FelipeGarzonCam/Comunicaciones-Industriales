#include <WiFi.h>
#include <ESP32Ping.h>              


const char* ssid     = "Edge50FusiondeFelipe";
const char* password = "Hola1345";

const int ledPin = 2;
WiFiServer server(80);
String header;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.print("Conectando a "); Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  Serial.print("IP ESP32: "); Serial.println(WiFi.localIP());
  Serial.println("\nComandos disponibles:");
  Serial.println("- ping 192.168.137.1    (hace 5 pings a la IP)");
  Serial.println("- ledon                 (enciende LED)");
  Serial.println("- ledoff                (apaga LED)");
  Serial.println("----------------------------------------");

  server.begin();
}

// Función para parsear IP desde string
IPAddress parseIP(String ipStr) {
  IPAddress ip;
  if (ip.fromString(ipStr)) {
    return ip;
  }
  return IPAddress(0, 0, 0, 0);  // IP inválida
}

// Función para ejecutar ping con estadísticas
void ejecutarPing(IPAddress targetIP) {
  if (targetIP == IPAddress(0, 0, 0, 0)) {
    Serial.println("IP inválida");
    return;
  }

  Serial.print("PING "); Serial.print(targetIP); 
  Serial.println(" 56 bytes de datos:");
  
  int pingsEnviados = 0;
  int pingsRecibidos = 0;
  float tiempoTotal = 0;
  float tiempoMin = 999999;
  float tiempoMax = 0;
  
  for (int i = 0; i < 5; i++) {
    pingsEnviados++;
    unsigned long startTime = millis();
    
    if (Ping.ping(targetIP, 1)) {  // 1 ping por vez
      pingsRecibidos++;
      float tiempo = Ping.averageTime();
      tiempoTotal += tiempo;
      
      if (tiempo < tiempoMin) tiempoMin = tiempo;
      if (tiempo > tiempoMax) tiempoMax = tiempo;
      
      Serial.print("64 bytes desde "); Serial.print(targetIP);
      Serial.print(": tiempo="); Serial.print(tiempo, 1); 
      Serial.println("ms");
    } else {
      Serial.println("Tiempo de espera agotado para solicitud ICMP.");
    }
    
    delay(1000);  
  }
  
  // Mostrar estadísticas finales
  Serial.println();
  Serial.print("--- estadísticas de ping de "); Serial.print(targetIP); 
  Serial.println(" ---");
  Serial.print(pingsEnviados); Serial.print(" paquetes transmitidos, ");
  Serial.print(pingsRecibidos); Serial.print(" recibidos, ");
  
  int perdida = ((pingsEnviados - pingsRecibidos) * 100) / pingsEnviados;
  Serial.print(perdida); Serial.println("% de pérdida de paquetes");
  
  if (pingsRecibidos > 0) {
    float promedio = tiempoTotal / pingsRecibidos;
    Serial.print("rtt min/avg/max = ");
    Serial.print(tiempoMin, 1); Serial.print("/");
    Serial.print(promedio, 1); Serial.print("/");
    Serial.print(tiempoMax, 1); Serial.println(" ms");
  }
  Serial.println();
}

void loop() {
  // Procesar comandos desde el monitor serie
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    
    if (comando.startsWith("ping ")) {
      String ipStr = comando.substring(5);  // Extraer IP después de "ping "
      IPAddress targetIP = parseIP(ipStr);
      ejecutarPing(targetIP);
    }
    else if (comando == "ledon") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED encendido");
    }
    else if (comando == "ledoff") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED apagado");
    }
    else if (comando.length() > 0) {
      Serial.println("Comando no reconocido");
      Serial.println("Uso: ping 192.168.137.1");
    }
  }

  // Servidor web para controlar el LED
  WiFiClient client = server.available();
  if (client) {
    String currentLine = "";
    unsigned long currentTime = millis();
    unsigned long previousTime = currentTime;
    const long timeoutTime = 2000;

    while (client.connected() && currentTime - previousTime <= timeoutTime) {
      currentTime = millis();
      if (client.available()) {
        char c = client.read();
        header += c;
        if (c == '\n') {
          if (currentLine.length() == 0) {
            if (header.indexOf("GET /on")  >= 0) { 
              digitalWrite(ledPin, HIGH); 
              Serial.println("LED encendido vía HTTP");
            }
            if (header.indexOf("GET /off") >= 0) { 
              digitalWrite(ledPin, LOW);  
              Serial.println("LED apagado vía HTTP");
            }

            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/html; charset=UTF-8");
            client.println("Connection: close");
            client.println();
            client.println("<!DOCTYPE html><html><head>"
                           "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                           "<style>body{font-family:Arial;text-align:center;margin-top:40px}"
                           "a{padding:14px 32px;text-decoration:none;color:#fff;border-radius:4px;margin:10px}"
                           ".on{background:#4CAF50}.off{background:#555}</style></head><body>");
            client.println("<h2>ESP32 Control LED</h2>");
            client.print("<p>IP: "); client.print(WiFi.localIP()); client.println("</p>");
            client.println("<p><a href=\"/on\"  class=\"on\">ENCENDER</a></p>");
            client.println("<p><a href=\"/off\" class=\"off\">APAGAR</a></p>");
            client.println("</body></html>");
            break;
          } else { currentLine = ""; }
        } else if (c != '\r') { currentLine += c; }
      }
    }
    header = "";
    client.stop();
  }
}
