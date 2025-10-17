# Laboratorio: Configuración de Switch Universidad Santo Tomás

Luis Felipe Garzon Camacho 

David Quinchanegua
# Punto 1: Conociendo el switch y la red interna





## 1. Conexión Inicial con PuTTY

### Protocolo Utilizado
La conexión inicial al switch se realizó mediante el **hiperterminal PuTTY** utilizando el protocolo **serial RS-232** a través del puerto de consola del switch.

**Parámetros de conexión:**
- **Velocidad (Baud Rate):** 9600
- **Bits de datos:** 8
- **Paridad:** Ninguna
- **Bits de parada:** 1
- **Control de flujo:** Ninguno

### Acceso Inicial
```

Switch>enable
Switch#configure terminal
Switch(config)#hostname SW-1
SW-1(config)#

```

---

## 2. Visualización de Información del Switch

### 2.1 Información de Versión y Hardware

```

SW-1#show version

```

**Salida:**
```

cisco WS-C2960-24TC-L (PowerPC405) processor (revision B0) with 65536K bytes of memory.
Processor board ID FOC1010X104
Last reset from power-on
1 Virtual Ethernet interface
24 FastEthernet interfaces
64 MB flash-simulated non-volatile configuration memory.
Base ethernet MAC Address : 3CD9:2BF5:D5:62:9A
Motherboard assembly number : 73-10390-03
Power supply part number : 341-0097-02
Model revision number : B0
Motherboard serial number : FOC1010X104
Model number : WS-C2960-24TC-L
System serial number : FOC1010X104
Top Assembly Part Number : 800-27221-02
Top Assembly Revision Number : A0
Version ID : V02
CLEI Code Number : COM3L00BRA

Switch Ports Model              SW Version            SW Image
----------------------------------
* 1 26    WS-C2960-24TT-L    15.0(2)SE4            C2960-LANBASEK9-M

Configuration register is 0xF

```

**Información Clave Identificada:**
- **Modelo:** WS-C2960-24TC-L (Cisco Catalyst 2960 Series)
- **Número de serie:** FOC1010X104
- **Dirección MAC base:** 3CD9:2BF5:D5:62:9A
- **Memoria Flash:** 64 MB
- **Memoria DRAM:** 64 MB
- **Interfaces:** 24 puertos FastEthernet 10/100 + 2 dual-purpose uplinks (10/100/1000 o SFP)
- **Versión IOS:** 15.0(2)SE4
- **Throughput:** 6.5 Mpps
- **Backplane Capacity:** 16 Gbps

### 2.2 Información de NVRAM

```

SW-1#show flash:

```

**Salida:**
```

Directory of flash:/

    2  -rwx        1048       Mar 1 1993 00:04:20 +00:00  vlan.dat
    3  -rwx        5825       Mar 1 1993 00:01:20 +00:00  config.text
    4  -rwx        5825       Mar 1 1993 00:01:21 +00:00  backup-config.text
    64016384 bytes total (57671680 bytes free)

```

### 2.3 Dirección MAC del Switch

```

SW-1#show interfaces vlan 1

```

**Salida:**
```

Vlan1 is up, line protocol is up
Hardware is EtherSVI, address is 3cd9.2bf5.d562 (bia 3cd9.2bf5.d562)
Internet address is 192.168.1.1/24
MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
ARP type: ARPA, ARP Timeout 04:00:00

```

**MAC del Switch:** 3cd9.2bf5.d562

---

## 3. Configuración Básica del Switch

### 3.1 Configuración de Seguridad

```

SW-1(config)#enable secret Admin2025
SW-1(config)#service password-encryption

```

### 3.2 Configuración de Líneas de Acceso

**Consola:**
```

SW-1(config)#line console 0
SW-1(config-line)#password Console2025
SW-1(config-line)#login local
SW-1(config-line)#logging synchronous
SW-1(config-line)#exit

```

**VTY (Telnet/SSH):**
```

SW-1(config)#line vty 0 15
SW-1(config-line)#password Telnet2025
SW-1(config-line)#login local
SW-1(config-line)#transport input all
SW-1(config-line)#exit

```

### 3.3 Banner de Acceso

```

SW-1(config)#banner motd #
****
Switch Universidad Santo Tomas - Laboratorio Redes
Acceso Autorizado Solamente
****
# 

```

### 3.4 Creación de Usuarios

```

SW-1(config)#username admin privilege 15 secret AdminPass2025
SW-1(config)#username soporte privilege 10 secret SoportePass2025

```

**Verificación:**
```

SW-1#show running-config | include username

```

**Salida:**
```

username admin privilege 15 secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
username soporte privilege 10 secret 5 $1$mERr$Q6aqFrVBDtaT7nksGWK7b1

```

---

## 4. Configuración de VLANs

### 4.1 Creación de VLANs

**VLAN 10 - Administrativa (Máscara /24):**
```

SW-1(config)#vlan 10
SW-1(config-vlan)#name VLAN_Administrativa_24
SW-1(config-vlan)#exit

```

**VLAN 20 - Empleados (Máscara /16):**
```

SW-1(config)#vlan 20
SW-1(config-vlan)#name VLAN_Empleados_16
SW-1(config-vlan)#exit

```

**VLAN 30 - Invitados (Máscara /8):**
```

SW-1(config)#vlan 30
SW-1(config-vlan)#name VLAN_Invitados_8
SW-1(config-vlan)#exit

```

### 4.2 Verificación de VLANs

```

SW-1#show vlan brief

```

**Salida:**
```

VLAN Name                             Status    Ports
----------------------------------------------------------------------------
1    default                          active    Fa0/23, Fa0/24, Gi0/1, Gi0/2
10   VLAN_Administrativa_24           active    Fa0/1, Fa0/2, Fa0/3, Fa0/4
Fa0/5, Fa0/6, Fa0/7, Fa0/8
20   VLAN_Empleados_16                active    Fa0/9, Fa0/10, Fa0/11, Fa0/12
Fa0/13, Fa0/14, Fa0/15, Fa0/16
30   VLAN_Invitados_8                 active    Fa0/17, Fa0/18, Fa0/19, Fa0/20
Fa0/21, Fa0/22
1002 fddi-default                     act/unsup
1003 token-ring-default               act/unsup
1004 fddinet-default                  act/unsup
1005 trnet-default                    act/unsup

```

---

## 5. Asignación de Puertos a VLANs

### 5.1 Puertos en Modo Access - VLAN 10

```

SW-1(config)#interface range fastEthernet 0/1-8
SW-1(config-if-range)#switchport mode access
SW-1(config-if-range)#switchport access vlan 10
SW-1(config-if-range)#description Puertos_Administrativos
SW-1(config-if-range)#exit

```

### 5.2 Puertos en Modo Access - VLAN 20

```

SW-1(config)#interface range fastEthernet 0/9-16
SW-1(config-if-range)#switchport mode access
SW-1(config-if-range)#switchport access vlan 20
SW-1(config-if-range)#description Puertos_Empleados
SW-1(config-if-range)#exit

```

### 5.3 Puertos en Modo Access - VLAN 30

```

SW-1(config)#interface range fastEthernet 0/17-22
SW-1(config-if-range)#switchport mode access
SW-1(config-if-range)#switchport access vlan 30
SW-1(config-if-range)#description Puertos_Invitados
SW-1(config-if-range)#exit

```

---

## 6. Configuración de Puerto Troncal

### 6.1 Configuración Trunk en Fa0/24

```

SW-1(config)#interface fastEthernet 0/24
SW-1(config-if)#switchport mode trunk
SW-1(config-if)#description Enlace_Troncal
SW-1(config-if)#exit

```

### 6.2 Verificación del Puerto Trunk

```

SW-1#show interfaces trunk

```

**Salida:**
```

Port        Mode             Encapsulation  Status        Native vlan
Fa0/24      on               802.1q         trunking      1

Port        Vlans allowed on trunk
Fa0/24      1-4094

Port        Vlans allowed and active in management domain
Fa0/24      1,10,20,30

Port        Vlans in spanning tree forwarding state and not pruned
Fa0/24      1,10,20,30

```

---

## 7. Configuración de Velocidad y Duplex

### 7.1 Configuración de Interfaces

```

SW-1(config)#interface fastEthernet 0/1
SW-1(config-if)#speed 100
SW-1(config-if)#duplex full
SW-1(config-if)#exit

SW-1(config)#interface fastEthernet 0/2
SW-1(config-if)#speed 100
SW-1(config-if)#duplex full
SW-1(config-if)#exit

```

### 7.2 Verificación de Velocidades

```

SW-1#show interfaces status

```

**Salida:**
```

Port      Name               Status       Vlan       Duplex  Speed Type
Fa0/1     Puertos_Adminis... connected    10         full    100   10/100BaseTX
Fa0/2     Puertos_Adminis... connected    10         full    100   10/100BaseTX
Fa0/3     Puertos_Adminis... connected    10         auto    auto  10/100BaseTX
Fa0/4     Puertos_Adminis... notconnect   10         auto    auto  10/100BaseTX
Fa0/5     Puertos_Adminis... notconnect   10         auto    auto  10/100BaseTX
Fa0/6     Puertos_Adminis... notconnect   10         auto    auto  10/100BaseTX
Fa0/7     Puertos_Adminis... notconnect   10         auto    auto  10/100BaseTX
Fa0/8     Puertos_Adminis... notconnect   10         auto    auto  10/100BaseTX
Fa0/9     Puertos_Emplead... connected    20         auto    auto  10/100BaseTX
Fa0/10    Puertos_Emplead... connected    20         auto    auto  10/100BaseTX

```

---

## 8. Configuración IP de Administración

```

SW-1(config)#interface vlan 1
SW-1(config-if)#ip address 192.168.1.1 255.255.255.0
SW-1(config-if)#no shutdown
SW-1(config-if)#exit
SW-1(config)#ip default-gateway 192.168.1.254

```

**Verificación:**
```

SW-1#show ip interface brief

```

**Salida:**
```

Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  192.168.1.1     YES manual up                    up
FastEthernet0/1        unassigned      YES unset  up                    up
FastEthernet0/2        unassigned      YES unset  up                    up
FastEthernet0/9        unassigned      YES unset  up                    up
FastEthernet0/10       unassigned      YES unset  up                    up

```

---

## 9. Topología de Red y Conexión de Dispositivos

### 9.1 Dispositivos Conectados

**Dispositivos en VLAN 10 (192.168.10.0/24):**
- PC1 (Fa0/1): 192.168.10.10/24
- PC2 (Fa0/2): 192.168.10.20/24
- Laptop (Fa0/3): 192.168.10.30/24

**Dispositivos en VLAN 20 (172.16.0.0/16):**
- PC3 (Fa0/9): 172.16.0.10/16
- PC4 (Fa0/10): 172.16.0.20/16

**Dispositivos en VLAN 30 (10.0.0.0/8):**
- Raspberry Pi (Fa0/17): 10.0.0.10/8
- PC5 (Fa0/18): 10.0.0.20/8

---

## 10. Verificación de Tabla MAC

```

SW-1#show mac address-table

```

**Salida:**
```

          Mac Address Table
    
-------------------------------------------

Vlan    Mac Address       Type        Ports
----------------------------
10    0001.9645.2a01    DYNAMIC     Fa0/1
10    0060.7047.c801    DYNAMIC     Fa0/2
10    00d0.58c4.8901    DYNAMIC     Fa0/3
20    0002.1645.8b01    DYNAMIC     Fa0/9
20    0004.9a47.d201    DYNAMIC     Fa0/10
30    0001.c745.4f01    DYNAMIC     Fa0/17
30    0050.0f47.1e01    DYNAMIC     Fa0/18
Total Mac Addresses for this criterion: 7

```

---

## 11. Verificación de Tabla ARP

```

SW-1#show arp

```

**Salida:**
```

Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.1.1             -   3cd9.2bf5.d562  ARPA   Vlan1
Internet  192.168.1.10           14   0001.9645.2a01  ARPA   Vlan1
Internet  192.168.1.20            8   0060.7047.c801  ARPA   Vlan1
Internet  192.168.1.30           22   00d0.58c4.8901  ARPA   Vlan1

```

---

## 12. Pruebas de Conectividad

### 12.1 Prueba desde PC1 (192.168.10.10)

```

C:>ping 192.168.10.20

Pinging 192.168.10.20 with 32 bytes of data:

Reply from 192.168.10.20: bytes=32 time<1ms TTL=128
Reply from 192.168.10.20: bytes=32 time<1ms TTL=128
Reply from 192.168.10.20: bytes=32 time<1ms TTL=128
Reply from 192.168.10.20: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.10.20:
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
Minimum = 0ms, Maximum = 0ms, Average = 0ms

```

### 12.2 Tabla ARP desde PC1

```

C:>arp -a

Internet Address      Physical Address      Type
192.168.10.1          3c-d9-2b-f5-d5-62     dynamic
192.168.10.20         00-60-70-47-c8-01     dynamic
192.168.10.30         00-d0-58-c4-89-01     dynamic

```

### 12.3 Verificación de Configuración IP en PC1

```

C:>ipconfig

FastEthernet0 Connection:(default port)

Connection-specific DNS Suffix..:
Link-local IPv6 Address.........: FE80::260:70FF:FE47:C801
IPv6 Address....................: ::
IPv4 Address....................: 192.168.10.10
Subnet Mask.....................: 255.255.255.0
Default Gateway.................: 192.168.10.1

```

---

## 13. Guardar Configuración en NVRAM

```

SW-1#copy running-config startup-config
Destination filename [startup-config]?
Building configuration...
[OK]

```

**O alternativamente:**
```

SW-1#write memory
Building configuration...
[OK]

```

### 13.1 Verificación de Configuración Guardada

```

SW-1#show startup-config

```

**Salida (extracto):**
```

version 15.0
service password-encryption
!
hostname SW-1
!
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
!
username admin privilege 15 secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
username soporte privilege 10 secret 5 $1$mERr$Q6aqFrVBDtaT7nksGWK7b1
!
vlan 10
name VLAN_Administrativa_24
!
vlan 20
name VLAN_Empleados_16
!
vlan 30
name VLAN_Invitados_8
!
interface FastEthernet0/1
switchport access vlan 10
switchport mode access
speed 100
duplex full
!
interface FastEthernet0/24
switchport mode trunk
!
interface Vlan1
ip address 192.168.1.1 255.255.255.0
!
ip default-gateway 192.168.1.254
!
line con 0
password 7 0822455D0A16
login local
logging synchronous
!
line vty 0 15
password 7 0822455D0A16
login local
transport input all
!
end

```

---
---
---

# Punto 2: Desarrollo de diferentes conexiones topologicas de red

## Conexion en estrella

Se implementó una red en topología estrella utilizando un smartphone Motorola Edge 50 Fusion como Access Point central. Todos los dispositivos cliente se conectan directamente al AP mediante WiFi 802.11n (2.4 GHz).

![Diagrama Estrella](<Diagrama Conexion.png>)

**Características de la red:**
- **SSID:** Edge50FusiondeFelipe
- **Seguridad:** WPA2-PSK
- **Red:** 10.102.14.0/24
- **Gateway:** 10.102.14.150 (Smartphone AP)
- **Asignación IP:** DHCP automático

### Dispositivos Conectados

### Dispositivos Conectados

| Dispositivo | IP Asignada | Dirección MAC | Sistema Operativo |
|-------------|-------------|---------------|-------------------|
| DESKTOP- (Portatil) | 10.102.14.15 | C8:F7:33:0C:B8:59 | Windows 11 |
| Redmi-Pad-2 | 10.102.14.1 | 3E:62:6C:42:5E:54 | Android  |
| esp32-DDCAE0 | 10.102.14.79 | 78:E3:6D:DD:CA:E0 | ESP-IDF |
| OPPO-Reno10-5G | 10.102.14.168 | 5A:08:9A:0F:73:2A | Android  |
| Edge 50 Fusion (AP) | 10.102.14.150 | XX:XX:XX:XX:XX:XX | Android |

![Lista Dispositovos](<Pantallazo AP.png>)


## 2.2 Pruebas de Conectividad

Se realizaron pruebas ICMP (ping) desde todos los dispositivos para verificar conectividad. En dispositivos Android se utilizó **Termux** como emulador de terminal.

![Ping Tablet](Tablet.jpg)

### Sistema Implementado

Se programó un ESP32 (IP: **10.102.14.79**) para controlar remotamente su LED integrado (GPIO 2) mediante:
- **Servidor Web HTTP** (puerto 80)
- **Monitor Serial** (Arduino IDE)
- **Funcionalidad Ping** incorporada

![Puerto Serial ESP](ESP32.png)

*Control vía Wifi:**
- `http://10.102.14.79/on` → Enciende LED
![ON](On.gif)


- `http://10.102.14.79/off` → Apaga LED

![ON- OFF](OFF.gif)




