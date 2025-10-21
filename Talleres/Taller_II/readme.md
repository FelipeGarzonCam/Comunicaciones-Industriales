# Taller de Comunicación Industrial

Luis Garzon

David Quinchanegua

## Punto 1: Vigilancia Tecnológica de Protocolos Industriales

### PROFIBUS

PROFIBUS es un protocolo de bus de campo serial ampliamente utilizado en automatización industrial. Desarrollado por la organización PROFIBUS & PROFINET International, se caracteriza por su robustez y confiabilidad en entornos industriales exigentes.

**Características técnicas:**
- Medio físico: RS-485 con cables de par trenzado apantallado
- Velocidad de transmisión: 9.6 kbps a 12 Mbps
- Distancia máxima: 1200 metros a 9.6 kbps
- Dispositivos por segmento: hasta 126
- Topología: bus lineal
- Protocolo: paso de testigo con comunicación maestro-esclavo

**Variantes principales:**
- PROFIBUS DP (Periféricos Descentralizados): comunicación con sensores y actuadores
- PROFIBUS PA (Automatización de Procesos): diseñado para industrias de procesos con seguridad intrínseca

**Aplicaciones:** Control de procesos, automatización de fábricas, monitoreo de dispositivos de campo.

### PROFINET

PROFINET es el sucesor de PROFIBUS basado en tecnología Ethernet industrial. Ofrece mayor velocidad, flexibilidad y funcionalidades avanzadas para la Industria 4.0.

**Características técnicas:**
- Medio físico: Ethernet industrial (cables UTP Cat5e/Cat6)
- Velocidad: 100 Mbps (Fast Ethernet) o 1 Gbps (Gigabit Ethernet)
- Topología: estrella, árbol, anillo
- Protocolo: utiliza EtherType especial para comunicación determinista en tiempo real
- Soporte de diagnósticos: SNMP y LLDP para información de dispositivo y topología

**Funcionalidades adicionales:**
- PROFIsafe: seguridad funcional integrada
- PROFIenergy: gestión eficiente de energía
- Redundancia de medios, controladores y dispositivos
- Fast Start Up para arranques rápidos
- Detección automática de dispositivos

**Aplicaciones:** Automatización de manufactura, robótica, sistemas de transporte, integración de sistemas IT/OT.

### EtherNet/IP

EtherNet/IP (Industrial Protocol) es un protocolo de comunicación industrial basado en el estándar Ethernet y desarrollado por ODVA. Utiliza la pila TCP/IP y el protocolo CIP (Common Industrial Protocol).

**Características técnicas:**
- Medio físico: Ethernet estándar (cables UTP)
- Velocidad: 10/100/1000 Mbps
- Topología: estrella con switches Ethernet
- Protocolo: UDP/IP para mensajería en tiempo real, TCP/IP para configuración
- Dispositivos: sin límite teórico en la red

**Diferencias con PROFINET:**
- PROFINET utiliza EtherType especial para mayor velocidad y determinismo
- EtherNet/IP depende de UDP/IP con mayor latencia
- PROFINET ofrece más funcionalidades de diagnóstico y redundancia
- EtherNet/IP tiene mayor integración con infraestructura IT empresarial

**Aplicaciones:** Control discreto, motion control, seguridad funcional, integración empresarial.

### RS-485

RS-485 es un estándar de comunicación serial diferencial ampliamente utilizado en entornos industriales por su robustez frente a ruido electromagnético y capacidad de transmisión a largas distancias.

**Características técnicas:**
- Medio físico: par trenzado (líneas A y B diferenciales)
- Velocidad: hasta 10 Mbps
- Distancia máxima: 1200 metros a velocidades bajas
- Dispositivos por red: hasta 32 (ampliable con repetidores)
- Modo de operación: half-duplex (bidireccional alternado) o full-duplex (con dos pares)
- Señalización: diferencial balanceada (alta inmunidad al ruido)

**Ventajas:**
- Alta inmunidad a interferencias electromagnéticas
- Comunicación multipunto (varios dispositivos en un bus)
- Bajo costo de implementación
- Amplio soporte en hardware industrial

**Modos de comunicación:**
- Simplex: comunicación unidireccional
- Half-duplex: bidireccional alternado (más común)
- Full-duplex: bidireccional simultáneo (requiere dos pares de cables)

**Aplicaciones:** Sistemas de control distribuido, redes Modbus RTU, edificios inteligentes, sistemas de seguridad.

### RS-422

RS-422 es un estándar de comunicación serial diferencial similar a RS-485 pero optimizado para comunicación punto a punto o punto a multipunto con un solo transmisor.

**Características técnicas:**
- Medio físico: dos pares trenzados (uno TX, uno RX)
- Velocidad: hasta 10 Mbps
- Distancia máxima: 1200 metros
- Topología: punto a punto o punto a multipunto (1 transmisor, hasta 10 receptores)
- Modo: full-duplex nativo
- Impedancia del receptor: 4kΩ

**Diferencias con RS-485:**
- RS-422 es full-duplex por diseño (canales TX/RX separados)
- RS-485 permite múltiples transmisores (multimastro)
- RS-422 tiene mayor velocidad a largas distancias
- RS-485 es más flexible para redes complejas

**Aplicaciones:** Comunicación entre PLC y HMI, enlaces de larga distancia, sistemas de adquisición de datos.

## Punto 2: Comunicación RS-485 con Control de Servo

### Descripción

Implementación de comunicación RS-485 entre Raspberry Pi 3 (maestro) y ESP32 (esclavo) para control de servo mediante protocolo Modbus RTU. Se implementaron los tres modos de comunicación: SIMPLEX, HALF-DUPLEX y FULL-DUPLEX.

### Hardware

- Raspberry Pi 3 (maestro Modbus)
- ESP32 DevKit (esclavo Modbus)
- 2x módulos MAX485 (4x para full-duplex)
- Servo SG90
- Cables par trenzado para bus RS-485
- Resistencias de terminación 120Ω

### Configuración

**Raspberry Pi 3:**
- Puerto UART: `/dev/ttyAMA0`
- Baudrate: 9600 bps
- GPIO17: Driver Enable (DE)
- GPIO27: Receiver Enable (RE)

**ESP32:**
- UART2 (pines 16 RX, 17 TX)
- GPIO4: Driver Enable (DE)
- GPIO5: Receiver Enable (RE)
- GPIO18: PWM para servo

### Modos de Comunicación

#### SIMPLEX
Comunicación unidireccional. Solo transmisión desde Raspberry Pi hacia ESP32. Pines DE/RE en HIGH permanente.

<img width="595" height="269" alt="Simplex" src="https://github.com/user-attachments/assets/b1bc5b17-aa34-4a9e-b2d3-177bc949257d" />

![Simplex](https://github.com/user-attachments/assets/e9f96455-f53f-435f-98ea-6872bb87d71a)


#### HALF-DUPLEX
Comunicación bidireccional alternada. El maestro alterna entre transmisión (DE=HIGH) y recepción (RE=LOW). Modo más común en RS-485.

<img width="619" height="473" alt="Half" src="https://github.com/user-attachments/assets/2813baa2-4d20-40ee-97d0-cb22fe814525" />

![Half](https://github.com/user-attachments/assets/9b1afb15-4415-4fb1-a1af-ab1be067e54f)

#### FULL-DUPLEX
Comunicación bidireccional simultánea. Requiere dos pares de módulos MAX485 (TX dedicado + RX dedicado) y dos pares de cables.

![FULL](https://github.com/user-attachments/assets/7958b6c9-1ee3-4f3d-9c0a-d0627a90c176)

<img width="658" height="287" alt="Full" src="https://github.com/user-attachments/assets/120e540f-2e8d-41dc-a836-d9228c683a92" />


### Protocolo Modbus RTU

El sistema utiliza Modbus RTU sobre RS-485:
- Function Code 0x06: Write Single Register
- Registro 0x0000: ángulo del servo (0-180°)
- CRC-16 para verificación de integridad


## Punto 3: Verificación de Topología de Red

### Descripción

Verificación de conectividad y configuración de red entre los dispositivos del sistema mediante comandos estándar de diagnóstico.

### Topología

La red implementada consiste en:
- PC (192.168.1.100): equipo de desarrollo
- Raspberry Pi 3 (192.168.1.101): maestro RS-485
- ESP32 (192.168.1.102): esclavo RS-485 con servo

Conexiones:
- PC ↔ Router: Ethernet
- Raspberry Pi 3 ↔ Router: WiFi/Ethernet
- Raspberry Pi 3 ↔ ESP32: RS-485 (UART)

### Comandos Ejecutados

#### Tabla ARP
Verificación de direcciones MAC de los dispositivos en la red.
<img width="637" height="197" alt="arp" src="https://github.com/user-attachments/assets/accad1ab-6f34-4ca8-91d1-7931e32783fd" />


#### Configuración IP
Verificación de la configuración de red del PC.

<img width="633" height="197" alt="ipconfig" src="https://github.com/user-attachments/assets/70ea6cec-ec10-40d8-988d-28a9b4eb8000" />


#### Ping a Raspberry Pi 3
Prueba de conectividad con el maestro RS-485.


<img width="665" height="244" alt="ping" src="https://github.com/user-attachments/assets/2877d3ca-9ff8-4705-81b3-8e81b6071d06" />

#### Ping a ESP32
Prueba de conectividad con el esclavo RS-485.

<img width="596" height="230" alt="ping 2" src="https://github.com/user-attachments/assets/1f9068d4-d7e0-4c12-9d78-00e17f4920dc" />


### Resultados

Todos los dispositivos presentan conectividad correcta con latencias menores a 35ms. La red permite la comunicación entre el PC de desarrollo, la Raspberry Pi 3 que actúa como maestro Modbus y el ESP32 que controla el servo.





