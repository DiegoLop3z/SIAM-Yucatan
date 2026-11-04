# Guía Práctica de Montaje y Validación de Node-RED Dashboard 2.0
## Especial para Arturo Heredia Martín (con Copiloto Claude)

> **Proyecto Integrador:** SIAM-Yucatán — Unidad 2  
> **Universidad Politécnica de Yucatán (UPY)**  
> **Docente:** M.I. Javier Poot  
> **Integrantes:** Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam)) & Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z))

---

## 1. Objetivo de esta Guía

Arturo, esta guía te permite poner en marcha de manera rápida y sin fricción la interfaz de supervisión y mando en tu computadora con Node-RED Dashboard 2.0. Puedes compartir este archivo directamente con Claude si requieres asistencia interactiva durante la configuración.

---

## 2. Requisitos Previos e Instalación

### 2.1 Verificar Node.js y Node-RED
Asegúrate de contar con Node.js (v18 o v20 LTS) y Node-RED instalados globalmente:

```bash
# Verificar versiones
node -v
npm -v
node-red --version
```

Si no los tienes instalados:
```bash
# Instalación recomendada en Ubuntu / Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt update && sudo apt install -y nodejs
sudo npm install -g --unsafe-perm node-red
```

### 2.2 Instalar el paquete de Dashboard 2.0
Node-RED Dashboard 2.0 es la nueva generación oficial de paneles web. Se instala en el directorio de usuario de Node-RED (`~/.node-red`):

```bash
cd ~/.node-red
npm install @flowfuse/node-red-dashboard
```

---

## 3. Puesta en Marcha e Importación del Flujo

1. **Iniciar el servicio de Node-RED:**
   ```bash
   node-red
   ```
2. **Abrir el editor visual:**  
   Navega en tu navegador a: [`http://localhost:1880`](http://localhost:1880)
3. **Importar el flujo del proyecto:**
   - Haz clic en el menú hamburguesa (esquina superior derecha, icono de tres líneas horizontales) $\rightarrow$ **Import**.
   - Haz clic en **select a file to import** y selecciona:
     `Monitor_actuador/node-red/dashboard_flows.json`
   - O bien, abre dicho archivo en un editor de texto, copia todo el contenido JSON y pégalo directamente en la caja de texto.
   - Selecciona la opción **Import into: new flow** y haz clic en el botón rojo **Import**.

---

## 4. Configuración del Broker MQTT en el Flujo

Por motivos de seguridad, los archivos exportados de Node-RED no incluyen contraseñas. Debes capturar las credenciales una sola vez:

1. En el lienzo de Node-RED, localiza cualquier nodo MQTT (por ejemplo, `MQTT Temp (°C)`).
2. Haz doble clic sobre él para abrir sus propiedades.
3. En el campo **Server**, verás seleccionado `Mosquitto Local UPY`. Haz clic en el icono del **lápiz** (✏️) al lado del nombre.
4. En la pestaña **Connection**:
   - **Server:** `localhost` (o la IP local de tu máquina).
   - **Port:** `1883`.
5. Ve a la pestaña **Security**:
   - **Username:** `dashboard`
   - **Password:** `UpY2026!Dash` (o la configurada según `node-red/configuracion_mosquitto.md`).
6. Haz clic en **Update** y luego en **Done**.
7. Haz clic en el botón rojo **Deploy** (esquina superior derecha).

---

## 5. Acceso al Dashboard y Validación Visual

Abre en tu navegador la URL pública del dashboard:
$$\text{\textbf{URL del Dashboard:}}\quad \text{\url{http://localhost:1880/dashboard/bioclima}}$$

### Componentes que deben verse en pantalla:
1. **Fila de Gauges:**
   - **Temperatura (°C):** Aguja semicircular (Azul / Verde / Rojo).
   - **Humedad (%):** Aguja semicircular (Amarillo / Verde / Azul).
   - **Índice de Calor NOAA (°C):** Categorización psicrométrica.
   - **Iluminación LDR (%):** Rango de 0% a 100%.
2. **Monitores de Estado:**
   - **Ocupación en Sala:** Muestra `🚶 PRESENCIA DETECTADA` o `⚪ ESPACIO DESPEJADO`.
   - **Semáforo Bioclimático NOM-015:** Muestra tarjeta con nivel Verde, Amarillo o Rojo.
3. **Gráfico Histórico:** Curva de evolución de temperatura y sensación térmica en vivo.
4. **Mando de Control:**
   - **Switch Ventilador NPN:** Interruptor desacoplado.
   - **Selector de Modo:** Alterna entre `AUTO` y `MANUAL`.
   - **Texto Confirmado:** Reporta el estado real del transistor (`🌀 EN REVOLUCIÓN` o `⏹ DETENIDO`).
   - **Diagnóstico LWT:** Indicador de enlace de la ESP32.

---

## 6. Validación Inmediata con el Simulador Python (Sin conectar ESP32 aún)

Antes de energizar el circuito físico, puedes verificar que todo tu dashboard funcione al 100% corriendo nuestro script simulador:

```bash
# Desde la raíz del repositorio Monitor_actuador:
python3 scripts/simular_mqtt.py
```

### ¿Qué hace el simulador?
- Genera variaciones sinusoidales realistas de temperatura (26 °C a 36 °C) y humedad (60% a 85%).
- Calcula dinámicamente el Heat Index.
- Simula detección de personas con el PIR.
- Escucha los comandos del switch del ventilador y responde con confirmación en lazo cerrado (`ON`/`OFF`).
- Simula la expiración del temporizador de 60 segundos en modo MANUAL y publica el retorno autónomo a `AUTO`.

---

## 7. Registro de Evidencias Fotográficas Requeridas

Cuando el dashboard esté operando fluidamente (con la ESP32 conectada o durante la simulación de pruebas), captura las 2 pantallas requeridas para la entrega:

1. **Captura 1:** `docs/imagenes/dashboard_nodered_telemetria.png`  
   - Encuadre completo mostrando los 4 gauges con valores en movimiento, la gráfica histórica con curvas y el semáforo en Verde o Amarillo.
2. **Captura 2:** `docs/imagenes/dashboard_nodered_control.png`  
   - Encuadre enfocado en la sección de control: activa el ventilador en modo MANUAL para mostrar el switch en ON, la confirmación de estado del ventilador y el mensaje de retorno a AUTO.
