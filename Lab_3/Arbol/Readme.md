# Punto 2: Desarrollo de diferentes conexiones topologicas de red

## Conexion en Arbol

Se implementó una topología en árbol jerárquica de 3 niveles: el ESP32 conectado por puerto serial (COM4) al PC Windows, el PC actúa como puente reenviando datos al smartphone Cel 1 (Access Point), y este último distribuye información a los demás dispositivos conectados vía WiFi.

<img width="1431" height="1047" alt="Topologia" src="https://github.com/user-attachments/assets/7007e3b0-62b4-4f5c-b0ae-965032cc895c" />

**Arquitectura:**
- **Nivel 1 (Hoja):** ESP32 → Puerto Serial USB
- **Nivel 2 (Nodo intermedio):** PC Windows (10.102.14.180) → Puente Serial-HTTP
- **Nivel 3 (Raíz):** Cel 1 Android (100.109.238.82:5000) → Servidor Flask

  ### Flujo de Datos
  ESP32 (Sensores) → Serial USB → PC (Puente Python) → HTTP POST → Cel 1 (Servidor)

  
### Componentes Implementados

**1. ESP32 - Nodo Sensor (Arbol.ino)**
- Envía datos JSON cada 10 segundos vía serial
- Temperatura, Humedad, Luz simulados
- Comandos: status, ledon, ledoff

**2. PC - Puente Serial (Puente_Serial.py)**
Lee puerto COM4 → Extrae JSON → POST a servidor
SERVIDOR_CENTRAL = "http://100.109.238.82:5000/sensor-data"


**3. Cel 1 - Servidor Central (ApServer.py)**
Flask servidor en puerto 5000
Recibe y almacena datos de sensores


### Resultados de Transmisión

<img width="383" height="133" alt="ESP32" src="https://github.com/user-attachments/assets/433f713e-8548-4d96-853b-898ba65f45c0" />

**Datos transmitidos correctamente:**
-  3 paquetes JSON enviados al servidor central
-  Temperatura: ~26°C, Humedad: ~47%, Luz: ~475 lux
-  Confirmación HTTP 200 desde servidor

<img width="1080" height="1392" alt="Pantallazo" src="https://github.com/user-attachments/assets/ba616d1a-724c-4f03-b28b-eb757be44579" />

**Servidor central recibiendo:**
- IP origen: 10.102.14.15 (PC Windows)
- Datos parseados correctamente
- Timestamp registrado
