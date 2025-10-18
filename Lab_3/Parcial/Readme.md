# Punto 2: Desarrollo de diferentes conexiones topologicas de red

## Conexión en Parcial (Lineal)

Se implementó una topología lineal parcial combinando dos tecnologías de comunicación: WiFi y Serial USB. La red consta de 4 nodos en cadena donde cada dispositivo actúa como intermediario crítico, demostrando el impacto de la caída de un nodo en redes lineales.

<img width="886" height="1186" alt="Conexion" src="https://github.com/user-attachments/assets/3d100df9-668a-43ae-b4f4-813bcf329922" />


**Arquitectura:**
Celular (AP WiFi) --[WiFi]--> PC --[Serial USB]--> ESP32 (AP WiFi) --[WiFi]--> Tablet


**Tecnologías combinadas:**
- WiFi (IEEE 802.11) entre Celular-PC y ESP32-Tablet
- Serial UART (115200 baud) entre PC-ESP32
- Flask HTTP servers (Python)
- Arduino WebServer (ESP32)

### Implementación por Nodo

**Nodo 1: Celular (Origen)** - `Node_1.py`
- Access Point WiFi (192.168.43.1)
- Flask server puerto 5000
- Genera mensaje inicial

  
![Nodo_1](https://github.com/user-attachments/assets/758cee58-672b-4758-b124-1b33314202a8)



**Nodo 2: PC (Intermediario WiFi→Serial)** - `Nodo_2.py`
- Cliente WiFi del celular (192.168.43.100)
- Puerto Serial COM4 al ESP32
- Flask server puerto 6000
- Puente crítico de tecnologías
  
<img width="503" height="467" alt="Nodo_2" src="https://github.com/user-attachments/assets/e381c38a-2cef-4138-81f4-c820af88fff3" />



**Nodo 3: ESP32 (Intermediario Serial→WiFi)** - `Nodo_3.ino`
- Recepción Serial USB (115200 baud)
- Access Point WiFi propio (10.10.10.1)
- WebServer HTTP puerto 80
- Arduino IDE + ArduinoJson
  
<img width="463" height="435" alt="Nodo_3" src="https://github.com/user-attachments/assets/bbfcd87b-1934-49c0-90ad-9b73ba67b70f" />


**Nodo 4: Tablet (Destino)** - `Nodo_4.py`
- Cliente WiFi del ESP32 (10.10.10.100)
- Solicita mensajes vía HTTP GET
- Termux Python
  
![Nodo_4](https://github.com/user-attachments/assets/818c7ebe-3464-44f3-bb3a-3a73297ad3aa)


### Flujo de Datos

**Mensaje:** "Hola desde el Celular - Parcial Redes" (37 bytes)

**Ruta completa:**
1. Celular genera mensaje → Flask POST al PC
2. PC recibe (WiFi) → Serial write al ESP32
3. ESP32 recibe (Serial) → HTTP response a Tablet
4. Tablet solicita (HTTP GET) → Mensaje recibido

**Protocolos utilizados:**
- HTTP/1.1 (Flask + WebServer)
- JSON para serialización
- ACK bidireccionales en cada salto

### Resultados

| Nodo | Mensajes Procesados | Tecnología Salida | ACKs | Estado |
|------|---------------------|-------------------|------|--------|
| Celular | 1 enviado | WiFi | 1 | ACTIVO |
| PC | 1 recibido/reenviado | Serial  | 2 | ACTIVO |
| ESP32 | 1 recibido/disponible | WiFi AP  | 1 | ACTIVO |
| Tablet | 1 recibido | N/A  | 0 | ACTIVO |

### Impacto de Falla de Nodo

**Simulación de caída del PC:**
- Celular no puede entregar mensaje (WiFi roto)
- ESP32 no recibe datos (Serial inactivo)
- Tablet queda aislada esperando
-  **Toda la cadena se fragmenta**

**Conclusión crítica:** En topologías lineales, cada nodo es un punto único de falla. La caída de cualquier nodo intermedio (PC o ESP32) interrumpe completamente la comunicación entre extremos.



