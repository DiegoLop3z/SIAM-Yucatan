# Issue #4: [DASH] Configuración de Broker Mosquitto y Flujos en Node-RED Dashboard 2.0

- **Asignado a:** Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))
- **Copiloto IA:** Claude
- **Etiquetas:** `node-red`, `dashboard-2.0`, `mosquitto`, `mqtt-broker`

---

## Descripción del Trabajo
Poner a punto la infraestructura de comunicaciones MQTT en la laptop y desplegar el panel de supervisión web en Node-RED Dashboard 2.0:

1. **Configuración del Broker Mosquitto:**
   - Asegurar que Mosquitto escuche en el puerto `1883` en todas las interfaces (`0.0.0.0`) para admitir la conexión del ESP32 a través del Hotspot Wi-Fi.
   - Configurar credenciales seguras para los usuarios `esp32_user` y `dashboard` conforme a `node-red/configuracion_mosquitto.md`.
   - Ajustar reglas de cortafuegos en Linux (`sudo ufw allow 1883/tcp`).
2. **Importación y Ajuste de Node-RED Dashboard 2.0:**
   - Instalar el paquete `@flowfuse/node-red-dashboard` en `~/.node-red`.
   - Importar el archivo `node-red/dashboard_flows.json`.
   - Configurar las credenciales en el nodo de conexión `Mosquitto Local UPY`.
   - Desplegar (*Deploy*) y abrir el dashboard en `http://localhost:1880/dashboard/bioclima`.
3. **Validación de Widgets e Interactividad:**
   - Verificar la respuesta en tiempo real de los 4 gauges (Temperatura, Humedad, Heat Index y Luz).
   - Validar que el switch del ventilador esté **desacoplado (`decouple: true`)**: sólo debe cambiar de posición al recibir la confirmación de lazo cerrado desde `.../ventilador/estado`.
   - Comprobar que el selector de modo refleje la conmutación automática de regreso a `AUTO` tras los 60 segundos de purga.
4. **Registro de Capturas de Pantalla:**
   - Guardar `docs/imagenes/dashboard_nodered_telemetria.png` (gauges y gráficas con datos activos).
   - Guardar `docs/imagenes/dashboard_nodered_control.png` (switch en ON, estado confirmado y mensaje del temporizador de retorno a AUTO).

---

## Criterios de Aceptación (Definition of Done - DoD)
- [ ] Broker Mosquitto acepta conexiones de red local y distribuye mensajes sin pérdidas.
- [ ] Dashboard 2.0 accesible y responsivo en computadoras y teléfonos móviles.
- [ ] Switch desacoplado responde exclusivamente a la confirmación de estado del actuador físico.
- [ ] 2 capturas de pantalla tomadas y alojadas en `docs/imagenes/`.
