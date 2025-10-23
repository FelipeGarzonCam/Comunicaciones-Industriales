# Qz Practico
# SIMATIC S7-1200 - Sistema de Control Programable

## Descripción General

El SIMATIC S7-1200 es un controlador lógico programable (PLC) compacto y modular de Siemens, diseñado para soluciones de automatización industrial de pequeña a mediana escala. Este sistema combina un diseño escalable con capacidades de comunicación industrial avanzadas, siendo ideal para aplicaciones en control de máquinas, líneas de producción y procesos industriales discretos.
![WhatsApp Image 2025-10-22 at 8 38 45 PM](https://github.com/user-attachments/assets/29ce8c5e-4fb5-40c6-84bd-60eabea9af75)

## Características Técnicas

### Especificaciones de la CPU

El sistema S7-1200 está disponible en diferentes variantes de CPU, cada una con capacidades específicas:

| Modelo | Memoria de Trabajo | E/S Integradas | Interfaces de Comunicación | Módulos Adicionales |
|--------|-------------------|----------------|---------------------------|---------------------|
| CPU 1211C | 25 KB | 6 DI / 4 DO | 1x Ethernet | Hasta 2 |
| CPU 1212C | 50 KB | 8 DI / 6 DO | 1x Ethernet | Hasta 3 |
| CPU 1214C | 100 KB | 14 DI / 10 DO | 1x Ethernet, 1x RS-485 | Hasta 8 |
| CPU 1215C | 125 KB | 14 DI / 10 DO | 2x Ethernet, 1x RS-485 | Hasta 8 |
| CPU 1217C | 125 KB | 14 DI / 10 DO | 2x Ethernet, 1x RS-485 | Hasta 8 |

### Características del Sistema

**Procesamiento:**
- Procesador de alto rendimiento para ejecución rápida de programa
- Tiempo de ejecución optimizado para instrucciones booleanas
- Soporte para operaciones matemáticas de punto flotante
- Capacidad de procesamiento de hasta 32 bits

**Memoria:**
- Memoria de trabajo: 25 KB a 150 KB según modelo
- Memoria de carga: 2 MB a 4 MB
- Memoria retentiva con respaldo de batería opcional
- Tarjeta de memoria SD para almacenamiento de programas y datos

**Alimentación:**
- Tensión nominal: 85-264 VAC o 24 VDC según versión
- Consumo típico: 40-80 mA a 120/240 VAC
- Fuente de alimentación integrada en la CPU
- Protección contra cortocircuitos y sobretensiones

## Componentes del Sistema

### 1. Unidad Central de Procesamiento (CPU)

La CPU es el núcleo del sistema S7-1200 e integra:

- Procesador principal para ejecución del programa de usuario
- Interfaces de comunicación Ethernet/PROFINET integradas
- Entradas y salidas digitales incorporadas
- Conectores para módulos de expansión
- LED de diagnóstico y estado operacional
- Ranura para tarjeta de memoria SIMATIC

### 2. Módulos de Señales (Signal Modules)

Los módulos de señales se conectan al lado derecho de la CPU para expandir las capacidades de E/S:

**Módulos de Entradas Digitales:**
- 8, 16 o 32 entradas digitales
- Tensiones de 24 VDC o 120/230 VAC
- Filtros de entrada configurables
- Detección de frente de subida/bajada

**Módulos de Salidas Digitales:**
- 8, 16 o 32 salidas digitales
- Salidas de relé, transistor o MOSFET
- Corriente por canal: hasta 2A (relé) o 0.5A (transistor)
- Protección contra cortocircuitos

**Módulos de Entradas Analógicas:**
- 2, 4 u 8 entradas analógicas
- Tipos de señal: tensión (±10V), corriente (0-20mA, 4-20mA)
- Sensores de temperatura: PT100, PT1000, termopares tipo J, K
- Resolución: 12-16 bits según modelo

**Módulos de Salidas Analógicas:**
- 2 o 4 salidas analógicas
- Señales de tensión (±10V) o corriente (0-20mA, 4-20mA)
- Resolución: 12-15 bits
- Tiempo de conversión optimizado

### 3. Tarjetas de Señales (Signal Boards)

Las Signal Boards se conectan directamente a la CPU sin aumentar el tamaño físico del sistema:

- 2-4 entradas/salidas digitales adicionales
- 1-2 entradas/salidas analógicas
- Expansión compacta para aplicaciones con limitaciones de espacio

### 4. Módulos de Comunicación (Communication Modules)

Se conectan al lado izquierdo de la CPU (hasta 3 módulos):

**CM 1241 RS-232:**
- Interfaz serial RS-232
- Velocidad: hasta 115.2 kbps
- Comunicación punto a punto
- Protocolos: Freeport, USS, Modbus RTU

**CM 1241 RS-485:**
- Interfaz serial RS-485
- Comunicación multipunto
- Distancia: hasta 1200 metros
- Protocolos: USS, Modbus RTU, Freeport

**CM 1243-1 (Ethernet):**
- Puerto Ethernet adicional RJ45
- Velocidad: 10/100 Mbps
- Protocolos TCP/IP, ISO-on-TCP

**CM 1243-5 (PROFIBUS):**
- Interfaz PROFIBUS DP
- Velocidad: hasta 12 Mbps
- Comunicación con dispositivos PROFIBUS

### 5. Panel HMI (Human-Machine Interface)

**SIMATIC HMI KTP700 Touch:**
- Pantalla táctil TFT de 7 pulgadas
- Resolución: 800x480 píxeles
- 65,536 colores
- Interface táctil resistiva
- Comunicación integrada vía PROFINET
- Memoria: 10 MB para proyecto, 512 KB para recetas
- Retroiluminación LED de larga duración
- Teclas de función programables

### 6. Panel de Conexiones E/S

El sistema incluye paneles de conexión personalizados para:

**Entradas Digitales:**
- Borneras extraíbles para cableado
- Indicadores LED de estado
- Protección contra inversión de polaridad

**Salidas Digitales:**
- Contactos de relé o salidas de transistor
- LED indicadores por canal
- Fusibles de protección individual

**Entradas/Salidas Analógicas:**
- Conexión de 2, 3 o 4 hilos
- Calibración en campo
- Filtros digitales configurables

## Funciones Tecnológicas Integradas

### Contadores de Alta Velocidad (HSC)

- 6 contadores integrados (3x 100 kHz, 3x 30 kHz)
- Modos: contador simple, contador de cuadratura, A/B con fase Z
- Interrupciones por eventos de conteo
- Preajuste y captura de valores
- Aplicaciones: encoders incrementales, medición de frecuencia

### Salidas de Pulsos

**Salidas PTO (Pulse Train Output):**
- 2 salidas de tren de pulsos hasta 100 kHz
- Factor de trabajo del 50%
- Control de motores paso a paso y servomotores
- Perfiles de movimiento: posicionamiento, velocidad, home

**Salidas PWM (Pulse Width Modulation):**
- 4 salidas moduladas por ancho de pulso
- Frecuencia y ciclo de trabajo configurables
- Control de velocidad de motores DC
- Regulación de temperatura en sistemas de calefacción

### Control de Movimiento

- Bloques de función para control de ejes
- Posicionamiento absoluto y relativo
- Control de velocidad variable
- Rampa de aceleración/desaceleración configurable
- Homing automático
- Sincronización de movimientos

### Regulación PID

- Bloques PID integrados en firmware
- Autoajuste de parámetros
- Control de temperatura, presión, nivel y caudal
- Monitorización de valores de proceso
- Alarmas y límites configurables

## Protocolos de Comunicación

### PROFINET

**Descripción:**
PROFINET es el estándar de comunicación industrial de Siemens basado en Ethernet, diseñado para aplicaciones de automatización en tiempo real.

**Características:**
- Estándar abierto basado en IEEE 802.3 (Ethernet)
- Comunicación determinista en tiempo real
- Topologías: línea, estrella, árbol o mixta
- Velocidad: 100 Mbps (Fast Ethernet)
- Distancia máxima entre nodos: 100 metros (cobre)
- Hot-swapping de dispositivos con switch integrado

**Funcionalidades:**
- PROFINET IO: comunicación entre controlador y dispositivos de campo
- PROFINET CBA: arquitectura basada en componentes
- Diagnóstico integrado y detección de errores
- Sincronización de reloj para aplicaciones de control de movimiento
- Seguridad funcional mediante PROFIsafe

**Aplicaciones en S7-1200:**
- Programación y diagnóstico con TIA Portal
- Comunicación con HMI y paneles de operador
- Intercambio de datos entre PLCs (comunicación S7)
- Conexión de módulos de E/S distribuidas

### TCP/IP (Transmission Control Protocol/Internet Protocol)

**Descripción:**
Suite de protocolos estándar de Internet para comunicación confiable en redes IP.

**Características:**
- Protocolo orientado a conexión
- Garantía de entrega de datos
- Control de flujo y reordenamiento de paquetes
- Compatibilidad universal con dispositivos IP

**Servicios en S7-1200:**
- T-Send/T-Receive para envío/recepción de datos
- TCP Client/Server para conexiones activas/pasivas
- Hasta 8 conexiones TCP simultáneas
- Buffer de datos configurable (hasta 8 KB)

**Aplicaciones:**
- Comunicación con sistemas SCADA
- Intercambio de datos con bases de datos
- Integración con sistemas MES/ERP
- Conexión con dispositivos de terceros

### ISO-on-TCP (RFC 1006)

**Descripción:**
Protocolo que encapsula servicios ISO/OSI sobre TCP/IP, permitiendo comunicación industrial estándar.

**Características:**
- Transporte de servicios ISO 8073 sobre TCP/IP
- Puerto estándar: 102
- Compatible con comunicación S7
- Conexiones punto a punto

**Funcionalidades:**
- Lectura/escritura de áreas de memoria
- Acceso a datos de proceso
- Control remoto de CPU
- Transferencia de archivos

### Modbus TCP

**Descripción:**
Protocolo de comunicación industrial abierto basado en arquitectura maestro-esclavo, ampliamente utilizado en automatización.

**Características:**
- Protocolo de capa de aplicación sobre TCP/IP
- Puerto estándar: 502
- Formato de trama simple y eficiente
- Compatibilidad con múltiples fabricantes

**Funcionalidades en S7-1200:**
- Cliente Modbus: lectura/escritura de registros remotos
- Servidor Modbus: exposición de datos del PLC
- Funciones soportadas: FC1, FC2, FC3, FC4, FC5, FC6, FC15, FC16
- Hasta 8 conexiones simultáneas

**Aplicaciones:**
- Integración con variadores de frecuencia
- Lectura de medidores inteligentes
- Comunicación con sistemas de terceros

### Modbus RTU

**Descripción:**
Versión serial del protocolo Modbus, utilizada en redes RS-485/RS-232.

**Características:**
- Comunicación serial asíncrona
- Velocidades: 300 bps a 115.2 kbps
- Formato de datos: RTU binario
- Hasta 247 dispositivos en red RS-485

**Configuración:**
- Bits de datos: 8
- Paridad: par, impar o ninguna
- Bits de parada: 1 o 2
- Tiempo de espera (timeout) configurable

**Aplicaciones:**
- Conexión con instrumentación de campo
- Redes de sensores y actuadores inteligentes
- Comunicación con sistemas legacy

### USS (Universal Serial Interface Protocol)

**Descripción:**
Protocolo propietario de Siemens para comunicación con variadores de frecuencia SINAMICS.

**Características:**
- Comunicación serial RS-485
- Velocidad: 1200 a 115200 bps
- Arquitectura maestro-esclavo
- Hasta 31 esclavos por red

**Funcionalidades:**
- Control de velocidad y arranque/paro
- Lectura de parámetros del variador
- Configuración remota
- Monitorización de estado y alarmas

### S7 Communication

**Descripción:**
Protocolo propietario de Siemens para comunicación entre dispositivos SIMATIC.

**Características:**
- Comunicación optimizada entre PLCs Siemens
- Operaciones GET/PUT para lectura/escritura
- Acceso directo a áreas de memoria
- Alto rendimiento y baja latencia

**Funcionalidades:**
- Comunicación CPU a CPU
- Intercambio de datos de proceso
- Sincronización de programas
- Diagnóstico remoto

**Tipos de conexión:**
- Conexión S7 unilateral: una CPU inicia comunicación
- Conexión S7 bilateral: ambas CPUs pueden iniciar
- Datos consistentes y sincronizados

## Software de Programación

### TIA Portal (Totally Integrated Automation)

**Descripción:**
Plataforma unificada de ingeniería de Siemens para programación, configuración y diagnóstico.

**Características:**
- STEP 7 Basic V14 o superior para S7-1200
- Entorno de programación integrado
- Simulador de CPU (S7-PLCSIM)
- Biblioteca de bloques de función

**Lenguajes de Programación Soportados:**
- LAD (Ladder Diagram): diagrama de contactos
- FBD (Function Block Diagram): diagrama de bloques funcionales
- STL (Statement List): lista de instrucciones
- SCL (Structured Control Language): lenguaje estructurado similar a Pascal
- GRAPH: programación de secuencias

## Diagnóstico y Mantenimiento

### Herramientas de Diagnóstico

**LED de Estado:**
- RUN (verde): CPU en modo ejecución
- STOP (amarillo): CPU detenida
- ERROR (rojo): error de sistema o hardware

**Diagnóstico en Línea:**
- Monitorización de variables en tiempo real
- Tabla de estado de forzado
- Buffer de diagnóstico con historial de eventos
- Visualización de carga de CPU

**Funciones Avanzadas:**
- Trace: captura de señales para análisis
- Watchdog: supervisión de tiempo de ciclo
- Alarmas de proceso y sistema
- Registro de eventos con marca temporal

### Mantenimiento Preventivo

**Recomendaciones:**
- Verificación periódica de conexiones de cable
- Limpieza de polvo en ventilación
- Inspección visual de LED indicadores
- Respaldo de programa en tarjeta de memoria
- Actualización de firmware según recomendaciones del fabricante

## Aplicaciones Típicas

- Automatización de máquinas empaquetadoras
- Control de líneas de ensamblaje
- Sistemas de transporte y logística
- Control de procesos en plantas de tratamiento
- Automatización de edificios e infraestructura
- Células de manufactura flexible
- Sistemas de dosificación y mezcla
- Control de HVAC industrial

## Ventajas del Sistema

- Diseño compacto que optimiza espacio en tableros
- Escalabilidad mediante módulos de expansión
- Comunicación industrial estándar integrada
- Programación intuitiva con TIA Portal
- Diagnóstico avanzado integrado
- Robustez para entornos industriales exigentes
- Bajo costo de propiedad
- Amplia comunidad de usuarios y soporte técnico
- Compatibilidad con ecosistema SIMATIC de Siemens

## Referencias Técnicas

- Manual del sistema SIMATIC S7-1200 (Siemens)
- TIA Portal V14 o superior
- Documentación de protocolos PROFINET y Modbus
- Estándares IEEE 802.3 para Ethernet Industrial
- Normas IEC 61131-3 para programación de PLC

## Consideraciones de Seguridad

- El sistema debe instalarse según las normativas eléctricas locales
- Conexión a tierra adecuada es obligatoria
- Protección mediante fusibles en alimentación
- Paro de emergencia independiente del PLC
- Acceso restringido a personal capacitado
- Respaldo periódico del programa de usuario
