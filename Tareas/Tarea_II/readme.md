# Tarea: Vigilancia Tecnológica de Protocolos Industriales

Luis Garzon

David Quinchanegua

## 1. Vigilancia Tecnológica de Protocolos Industriales

### Modbus

Modbus es un protocolo de comunicación serial desarrollado por Modicon en 1979, ampliamente adoptado en automatización industrial por su simplicidad y licencia libre.

**Características técnicas:**
- Arquitectura maestro-esclavo (cliente-servidor)
- Protocolo de capa de aplicación nivel 7 OSI
- Dos variantes principales: Modbus RTU (serial) y Modbus TCP (Ethernet)
- Soporta hasta 247 dispositivos esclavos únicos
- Códigos de función estándar: lectura/escritura de coils, registros holding, registros de entrada

**Modbus RTU:**
- Transmisión serial sobre RS-232, RS-422 o RS-485
- Formato binario compacto
- CRC-16 para detección de errores
- Velocidad típica: 9600-115200 bps

**Modbus TCP/IP:**
- Encapsula tramas Modbus en paquetes TCP/IP
- Puerto estándar: 502
- Sin checksum (TCP maneja integridad)
- Soporta múltiples conexiones simultáneas

**Aplicaciones:** Control de procesos, adquisición de datos SCADA, integración de PLCs, monitoreo de energía.

### AS-Interface (AS-i)

AS-Interface es un sistema de bus de campo de bajo costo diseñado específicamente para conectar actuadores y sensores binarios simples en el nivel más bajo de la pirámide de automatización.

**Características técnicas:**
- Cable de dos hilos no blindado (datos + alimentación 24V DC)
- Topología: cualquiera (bus, árbol, estrella, anillo)
- Longitud máxima: 100 metros (extensible a 300m con repetidores)
- Hasta 62 esclavos por maestro
- Tiempo de ciclo típico: 5ms para 31 esclavos
- Transmisión de datos: modulación de pulsos codificados Manchester sobre línea de alimentación

**Perfil AS-i:**
- AS-i 2.0: 4 bits entrada/4 bits salida por esclavo
- AS-i 2.1: añade modo analógico
- AS-i 3.0: hasta 31 bits E/S por esclavo
- AS-i Safety at Work: integración de funciones de seguridad SIL 2/3

**Ventajas:**
- Instalación simple sin polaridad
- Bajo costo por punto de E/S
- Diagnóstico automático de red
- Protección IP67 para sensores en campo

**Aplicaciones:** Conexión de fotoceldas, sensores de proximidad, pulsadores, actuadores neumáticos, lámparas indicadoras.

### Categorías de Ethernet Industrial

#### Ethernet/IP

Desarrollado por ODVA (Open DeviceNet Vendors Association), utiliza TCP/IP estándar con el protocolo CIP (Common Industrial Protocol).

**Características:**
- Basado en IEEE 802.3
- Comunicación implícita (I/O en tiempo real) sobre UDP
- Comunicación explícita (configuración) sobre TCP
- Sin modificaciones al hardware Ethernet estándar
- Integración directa con infraestructura IT

**Rendimiento:**
- Tiempo de ciclo: 1-10ms típico
- Jitter: 50-500μs
- Determinismo mediante switches gestionados con QoS

#### PROFINET

Protocolo Ethernet industrial de Siemens basado en estándares IEC 61158 e IEC 61784.

**Clases de comunicación:**
- PROFINET IO: comunicación en tiempo real (RT) con prioridad VLAN
- PROFINET IRT: tiempo real isócrono con ciclos de 250μs-4ms, jitter <1μs
- PROFINET CBA: automatización basada en componentes

**Características avanzadas:**
- Topología flexible con redundancia de medios (MRP)
- Sincronización precisa de tiempo
- Diagnóstico de topología automático (LLDP)
- Integración de seguridad funcional (PROFIsafe)

#### EtherCAT

Ethernet for Control Automation Technology, desarrollado por Beckhoff.

**Características distintivas:**
- Procesamiento on-the-fly: cada nodo procesa datos mientras la trama pasa
- Topología de anillo o línea
- Ciclos de actualización: hasta 100μs
- Sincronización distribuida de relojes <1μs
- Eficiencia: hasta 90% del ancho de banda para datos útiles

#### POWERLINK

Ethernet determinista de código abierto desarrollado por B&R Automation.

**Arquitectura:**
- Ciclo dividido en fases: isócrona (E/S) y asíncrona (TCP/IP)
- Nodo Managing (maestro) coordina comunicación
- Tiempo de ciclo: 200μs-10ms
- Jitter <1μs

## 2. Exploración de Dispositivos en Universidad

### Dispositivos con Modbus

**PLC con puerto Modbus RTU:**
- Función: controlador lógico programable con comunicación serial
- Interfaz: RS-485 con conector DB9 o bornera
- Registros típicos: estados digitales, valores analógicos, parámetros de configuración
- Aplicación en laboratorio: maestro de red para adquisición de datos de sensores

**Convertidor Modbus TCP/RTU:**
- Función: gateway entre redes Ethernet y RS-485
- Puertos: RJ45 (Ethernet) + bornera (RS-485 A/B)
- Configuración: dirección IP, velocidad serial, paridad
- Aplicación: integración de dispositivos legacy a red Ethernet

### Dispositivos con AS-i

**Módulo maestro AS-i:**
- Función: coordina comunicación con esclavos AS-i
- Interfaz superior: PROFINET o EtherNet/IP
- Interfaz inferior: cable amarillo AS-i de 2 hilos
- Capacidad: gestión de hasta 62 esclavos con direccionamiento automático

**Sensores AS-i:**
- Tipo: sensores inductivos, capacitivos, fotoeléctricos con chip AS-i integrado
- Alimentación: 24V DC por cable AS-i
- Conexión: conector M12 o cable directo
- Datos transmitidos: estado binario (ON/OFF) o valores analógicos simples

### Dispositivos PROFIBUS

**Acoplador PROFIBUS DP:**
- Función: conecta módulos de E/S remotas a red PROFIBUS
- Conector: DB9 con resistencia de terminación 220Ω configurable
- Velocidad soportada: hasta 12 Mbps
- GSD file: archivo de configuración para integración en TIA Portal

**Variador de frecuencia con PROFIBUS:**
- Función: control de motores AC con comunicación PROFIBUS
- Parámetros accesibles: velocidad, corriente, estado, alarmas
- Función de perfil: PROFIdrive para aplicaciones de motion
- Diagnóstico: mensajes extendidos de falla accesibles por red

### Dispositivos PROFINET

**Switch PROFINET industrial:**
- Puertos: 4-24 puertos RJ45 con PoE opcional
- Funcionalidades: MRP (redundancia), QoS, diagnóstico de topología
- Temperatura operativa: -40°C a +75°C
- Montaje: riel DIN 35mm

**HMI con PROFINET:**
- Pantalla táctil con comunicación PROFINET IO
- Función: visualización y control de proceso
- Actualización de datos: cíclica cada 10-100ms
- Alarmas y eventos registrados con timestamp

### Dispositivos Ethernet Industrial

**Controlador PAC con EtherNet/IP:**
- Procesador: multicores con sistema operativo en tiempo real
- Puertos Ethernet: dual port con switch integrado
- Protocolos soportados: EtherNet/IP, Modbus TCP, OPC UA
- Capacidad: gestión de miles de tags de E/S

**Cámara industrial con Ethernet:**
- Interfaz: GigE Vision o Ethernet/IP
- Resolución: 1-5 megapixeles
- Frame rate: 30-120 fps
- Aplicación: inspección visual, lectura de códigos, posicionamiento

### Dispositivos RS-485

**Módulo MAX485:**
- Chip transceiver: convierte TTL/UART a señal diferencial RS-485
- Pines: DI (data input), RO (receiver output), DE/RE (control dirección)
- Alimentación: 5V DC
- Aplicación: interfaz entre microcontroladores y bus RS-485

**Medidor de energía con RS-485:**
- Función: medición de voltaje, corriente, potencia, factor de potencia
- Protocolo: Modbus RTU
- Registros: valores instantáneos y acumulados de energía
- Velocidad: 9600 bps, 8N1

## 3. IPv4 vs IPv6

### Diferencias Principales

**Tamaño de dirección:**
- IPv4: 32 bits (4,294,967,296 direcciones - aproximadamente 4.3 mil millones)
- IPv6: 128 bits (3.4×10^38 direcciones - prácticamente ilimitado)

**Formato de dirección:**
- IPv4: notación decimal con puntos (192.168.1.1)
- IPv6: notación hexadecimal con dos puntos (2001:0db8:85a3:0000:0000:8a2e:0370:7334)

**Cabecera de paquete:**
- IPv4: tamaño variable (20-60 bytes), incluye checksum
- IPv6: tamaño fijo (40 bytes), sin checksum, procesamiento más eficiente

**Configuración:**
- IPv4: manual o DHCP
- IPv6: SLAAC (autoconfiguración sin estado) o DHCPv6

**Seguridad:**
- IPv4: IPsec opcional
- IPv6: IPsec obligatorio en especificación original (luego opcional pero ampliamente implementado)

**NAT (Network Address Translation):**
- IPv4: necesario debido a escasez de direcciones
- IPv6: no necesario, conectividad end-to-end nativa

**Fragmentación:**
- IPv4: realizada por routers intermedios
- IPv6: solo realizada por el host origen

**Broadcast:**
- IPv4: soporta broadcast, multicast y unicast
- IPv6: elimina broadcast, usa multicast y anycast

**Calidad de servicio:**
- IPv4: campo TOS (Type of Service) para QoS
- IPv6: campo Flow Label para mejor manejo de tráfico en tiempo real

**Movilidad:**
- IPv4: requiere Mobile IP con túneles
- IPv6: movilidad integrada en el protocolo

### Clases de Direcciones IPv4

#### Clase A
- Rango: 1.0.0.0 a 126.0.0.0
- Máscara por defecto: 255.0.0.0 (/8)
- Primer octeto: 0-127 (bit más significativo: 0)
- Hosts por red: 16,777,214
- Redes disponibles: 126
- Uso: redes muy grandes (corporaciones, ISPs)

#### Clase B
- Rango: 128.0.0.0 a 191.255.0.0
- Máscara por defecto: 255.255.0.0 (/16)
- Primeros dos bits: 10
- Hosts por red: 65,534
- Redes disponibles: 16,384
- Uso: redes medianas (universidades, empresas grandes)

#### Clase C
- Rango: 192.0.0.0 a 223.255.255.0
- Máscara por defecto: 255.255.255.0 (/24)
- Primeros tres bits: 110
- Hosts por red: 254
- Redes disponibles: 2,097,152
- Uso: redes pequeñas (oficinas, LANs)

#### Clase D
- Rango: 224.0.0.0 a 239.255.255.255
- Primeros cuatro bits: 1110
- Uso: multicast (transmisión a grupos de hosts)
- No se asigna máscara de red
- Aplicaciones: streaming de video, protocolos de enrutamiento (OSPF, RIP)

#### Clase E
- Rango: 240.0.0.0 a 255.255.255.255
- Primeros cuatro bits: 1111
- Uso: reservado para experimentación e investigación
- No disponible para uso público
- 255.255.255.255: dirección de broadcast limitado

### Direcciones Privadas IPv4

Definidas en RFC 1918 para uso en redes locales sin enrutamiento en Internet:
- Clase A: 10.0.0.0/8
- Clase B: 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
- Clase C: 192.168.0.0/16

### Tipos de Direcciones IPv6

**Unicast global:**
- Equivalente a direcciones públicas IPv4
- Prefijo: 2000::/3
- Enrutables en Internet

**Unicast link-local:**
- Prefijo: fe80::/10
- Válidas solo en el enlace local
- Autoconfiguradas automáticamente

**Unicast unique local:**
- Prefijo: fc00::/7 (prácticamente fd00::/8)
- Equivalente a direcciones privadas IPv4

**Multicast:**
- Prefijo: ff00::/8
- Reemplaza broadcast de IPv4

**Anycast:**
- Misma dirección asignada a múltiples interfaces
- El paquete se entrega al más cercano

## Comparativa de Adopción

**Estado actual IPv6:**
- Adopción global: aproximadamente 38% de usuarios (2025)
- Países líderes: India (70%), Estados Unidos (50%), Alemania (60%)
- Sectores: ISPs móviles con mayor adopción que redes fijas

**Convivencia dual-stack:**
- Mayoría de sistemas operativos modernos soportan IPv4 e IPv6 simultáneamente
- Túneles 6to4 y Teredo para transición
- Traducción NAT64 para comunicación IPv6-only con servidores IPv4-only

## Referencias

- RFC 791: Internet Protocol (IPv4)
- RFC 2460: Internet Protocol Version 6 Specification
- Modbus Organization: Modbus Protocol Specification
- AS-International Association: AS-Interface Specification
- PROFIBUS & PROFINET International (PI)
- ODVA: EtherNet/IP Specification
- IEC 61158: Digital data communications for measurement and control - Fieldbus
- IEC 61784: Industrial communication networks profiles
