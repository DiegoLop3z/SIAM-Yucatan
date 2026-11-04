# Configuración del Broker MQTT Mosquitto
## Sistema IoT Integrador SIAM-Yucatán

> **Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026**  
> **Docente:** M.I. Javier Poot  
> **Autores:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))

---

## 1. Arquitectura de Seguridad y Roles MQTT

El broker Mosquitto actúa como el núcleo de intercambio de mensajes publish/subscribe entre el microcontrolador ESP32 y la interfaz de usuario en Node-RED. Para garantizar robustez y seguridad en redes locales y hotspots:

```text
┌─────────────────────────┐               ┌─────────────────────────┐
│     ESP32 DevKit V1     │               │   Node-RED Dashboard    │
│  (Usuario: esp32_user)  │               │   (Usuario: dashboard)  │
└───────────┬─────────────┘               └────────────┬────────────┘
            │ Publica telemetría/estado                │ Publica comandos
            │ Se suscribe a comandos                   │ Se suscribe a telemetría
            ▼                                          ▼
     ┌───────────────────────────────────────────────────────┐
     │           Eclipse Mosquitto Broker (Laptop)           │
     │                 Puerto: 0.0.0.0:1883                  │
     │      Control de Acceso: mosquitto.passwd + ACL        │
     └───────────────────────────────────────────────────────┘
```

---

## 2. Archivo de Configuración Principal (`mosquitto.conf`)

En la computadora de desarrollo (Linux / Ubuntu / Debian), editar el archivo `/etc/mosquitto/conf.d/bioclima.conf` o `/etc/mosquitto/mosquitto.conf`:

```conf
# ==============================================================================
# Configuración Mosquitto - SIAM Yucatán (UPY 2026)
# ==============================================================================

# Escucha en todas las interfaces de red (Localhost y Hotspot Wi-Fi)
listener 1883 0.0.0.0

# Deshabilitar accesos anónimos para cumplimiento de seguridad
allow_anonymous false

# Archivo de contraseñas hasheadas
password_file /etc/mosquitto/passwd

# Archivo de Lista de Control de Acceso (ACL)
acl_file /etc/mosquitto/acl

# Persistencia de mensajes Retained (LWT y estados)
persistence true
persistence_location /var/lib/mosquitto/

# Registro de eventos
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
```

---

## 3. Creación de Usuarios y Contraseñas

Ejecutar en la terminal de la máquina host para registrar a los dos clientes:

```bash
# 1. Crear el archivo de contraseñas y agregar el usuario del ESP32
sudo mosquitto_passwd -c /etc/mosquitto/passwd esp32_user
# Ingresar contraseña: UpY2026!

# 2. Agregar el usuario de Node-RED (sin flag -c para no sobreescribir)
sudo mosquitto_passwd /etc/mosquitto/passwd dashboard
# Ingresar contraseña: UpY2026!Dash
```

---

## 4. Política de Control de Acceso por Rol (`mosquitto.acl`)

Crear `/etc/mosquitto/acl` para restringir el alcance de cada usuario:

```text
# ------------------------------------------------------------------------------
# ACL: Usuario del ESP32 (Hardware de Campo)
# ------------------------------------------------------------------------------
user esp32_user
# Puede publicar telemetría, estados de actuadores y su LWT
topic write yucatan/bioclima/telemetria
topic write yucatan/bioclima/sensor/#
topic write yucatan/bioclima/actuador/+/estado
topic write yucatan/bioclima/status
# Puede leer comandos y cambios de configuración
topic read yucatan/bioclima/actuador/+/set
topic read yucatan/bioclima/config/#

# ------------------------------------------------------------------------------
# ACL: Usuario de Node-RED (Interfaz de Monitoreo y Mando)
# ------------------------------------------------------------------------------
user dashboard
# Puede leer toda la telemetría, estados y presencia
topic read yucatan/bioclima/#
# Puede enviar comandos y configuraciones
topic write yucatan/bioclima/actuador/+/set
topic write yucatan/bioclima/config/#
```

---

## 5. Ajustes de Red y Firewall (UFW)

Para permitir que el ESP32 conectado al Hotspot Wi-Fi alcance el broker en el puerto 1883:

```bash
# Habilitar puerto MQTT en el cortafuegos
sudo ufw allow 1883/tcp

# Reiniciar y aplicar cambios en Mosquitto
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

---

## 6. Comprobación y Pruebas con Clientes CLI

### Probar suscripción (escuchar todo el tráfico del sistema):
```bash
mosquitto_sub -h localhost -p 1883 -u dashboard -P 'UpY2026!Dash' -t 'yucatan/bioclima/#' -v
```

### Probar comando de encendido del ventilador:
```bash
mosquitto_pub -h localhost -p 1883 -u dashboard -P 'UpY2026!Dash' -t 'yucatan/bioclima/actuador/ventilador/set' -m 'ON' -q 1 -r
```

### Probar cambio de modo a MANUAL:
```bash
mosquitto_pub -h localhost -p 1883 -u dashboard -P 'UpY2026!Dash' -t 'yucatan/bioclima/actuador/modo/set' -m 'MANUAL' -q 1 -r
```
