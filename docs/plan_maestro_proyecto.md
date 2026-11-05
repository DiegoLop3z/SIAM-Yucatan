# Plan Maestro: SIAM-Yucatán
## Sistema Inteligente de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática

> **Evaluación Unidad 2: Sistema IoT Integrador**  
> **Institución:** Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026  
> **Materia:** Internet de las Cosas (IoT)  
> **Docente Titular:** M.I. Javier Poot  
> **Integrantes y Metodología:**  
> • **Diego López Pérez** ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) — Copiloto IA: **Gemini**  
> • **Arturo Heredia Martín** ([`@arturoherediam`](https://github.com/arturoherediam)) — Copiloto IA: **Claude**  

---

## 1. Definición y Alcance del Proyecto

**SIAM-Yucatán** es una estación IoT industrial y educativa para la supervisión bioclimática, cálculo en tiempo real del estrés térmico laboral (Heat Index según la ecuación de regresión de Rothfusz de la NOAA) y mitigación forzada de calor diseñada para talleres de manufactura en Kanasín y laboratorios tecnológicos en el campus UPY (Ucú, Yucatán).

### Pilares de Ingeniería:
1. **Conformidad Normativa:** Cumplimiento de la **NOM-015-STPS-2001** (condiciones térmicas extremas) y **NOM-025-STPS-2008** (iluminancia en planos de trabajo).
2. **Desacoplo Eléctrico de Potencia:** Etapa de conmutación *Low-Side Switch* con transistor NPN (2N2222A) y diodo flyback (1N4001) para accionar un ventilador de 5V DC sin sobrecargar los GPIOs de 3.3V de la ESP32 ni generar reinicios por ruido inductivo.
3. **Automatización Inteligente Condicionada:** Mitigación térmica activa únicamente ante peligro térmico ($HI \ge 38^\circ\text{C}$ o $\text{Temp} \ge 32^\circ\text{C}$) **Y** presencia humana detectada por sensor PIR, con apagado automático tras 30 s de desocupación.
4. **Control Remoto Desacoplado y Protección Anti-Olvido:** Control bidireccional desde Node-RED Dashboard 2.0 con confirmación en lazo cerrado y retorno autónomo a modo `AUTO` tras 60 s en caso de activación manual por purga.

---

## 2. Nueva Distribución de Responsabilidades en Pareja

| Estudiante | Usuario GitHub | Herramienta IA | Rol Principal | Tareas Asignadas |
|---|---|:---:|---|---|
| **Diego López Pérez** | [`@DiegoLop3z`](https://github.com/DiegoLop3z) | **Gemini** | Líder de Hardware Físico, Ensamble en Protoboard y Pruebas de Banco | • Montaje físico del circuito en protoboard de 830 puntos (ESP32, SHT41, OLED, LDR, PIR, Transistor NPN, Diodo, Ventilador 5V, LED RGB).<br>• Verificación con multímetro de continuidad, voltajes (3.3V, 5V) y ausencia de cortos.<br>• Flasheo del firmware compilado a la ESP32 física vía cable micro-USB.<br>• Pruebas físicas de perturbación en banco.<br>• Toma de fotografías del protoboard (**Foto 1** y **Foto 2**) y subida a `docs/imagenes/`. |
| **Arturo Heredia Martín** | [`@arturoherediam`](https://github.com/arturoherediam) | **Claude** | Líder de Documentación Oficial, Broker MQTT y Dashboard Web | • Redacción, desarrollo y refinamiento del **Reporte Técnico Oficial de 16/18 secciones** (`docs/reporte_tecnico.md`) con asistencia de Claude.<br>• Configuración del broker Mosquitto y reglas de cortafuegos.<br>• Despliegue y validación interactiva del panel en Node-RED Dashboard 2.0.<br>• Captura de pantallas del dashboard (**Foto 3** y **Foto 4**) y subida a `docs/imagenes/`. |

---

## 3. Matriz de Entregables Oficiales (Rúbrica UPY - M.I. Javier Poot)

| Entregable Oficial | Descripción del Entregable | Archivo en el Repositorio | Responsable Principal | Estado |
|:---:|---|---|:---:|:---:|
| **Entregable 1** | Propuesta Formal del Proyecto | [`docs/propuesta_proyecto.md`](propuesta_proyecto.md) | Diego & Arturo | Completo (100%) |
| **Entregable 2** | Diseños (Bloques, esquemático, arquitectura y flujo) | [`docs/arquitectura_iot.md`](arquitectura_iot.md)<br>[`hardware/diagrama_conexiones.svg`](../hardware/diagrama_conexiones.svg) | Diego López | Completo (100%) |
| **Entregable 3** | Código Fuente (ESP32 C++, Node-RED flows, Mosquitto) | [`firmware/esp32-bioclima-iot/`](../firmware/esp32-bioclima-iot/)<br>[`node-red/dashboard_flows.json`](../node-red/dashboard_flows.json) | Diego (FW) / Arturo (DASH) | Completo (100%) |
| **Entregable 4** | Prototipo Físico Ensamblado y Funcionando | [`hardware/hardware_conexion.md`](../hardware/hardware_conexion.md)<br>[`docs/imagenes/protoboard_vista_general.png`](imagenes/protoboard_vista_general.png) | Diego López | En proceso físico |
| **Entregable 5** | Dashboard de Visualización y Mando Web | [`node-red/dashboard_flows.json`](../node-red/dashboard_flows.json)<br>[`docs/imagenes/dashboard_nodered_telemetria.png`](imagenes/dashboard_nodered_telemetria.png) | Arturo Heredia | Flujo listo / Pruebas en vivo |
| **Entregable 6** | Manual de Demostración en Vivo (7 Pasos) | [`docs/manual_demostracion.md`](manual_demostracion.md) | Diego & Arturo | Completo (100%) |
| **Entregable 7** | Reporte Técnico Oficial (16 Secciones UPY) | [`docs/reporte_tecnico.md`](reporte_tecnico.md) | Arturo Heredia (con Claude) | Plantilla 18 secciones lista |

---

## 4. Backlog de GitHub Issues (Reasignación Actualizada)

- **Issue #1:** `[HW] Armado Físico del Hardware en Protoboard, Pruebas de Banco y Registro Fotográfico`  
  *Asignado a:* **Diego López Pérez** (`@DiegoLop3z` / Gemini) — DoD: Circuito cableado, pruebas de multímetro superadas, Foto 1 y Foto 2 capturadas.
- **Issue #2:** `[FW] Desarrollo del Módulo de Sensores, LDR y Algoritmo de Sensación Térmica`  
  *Asignado a:* **Diego López Pérez** (`@DiegoLop3z` / Gemini) — DoD: PlatformIO C++, algoritmos NOAA y NOM-015, loop sin delays.
- **Issue #3:** `[FW] Implementación de Reglas de Automatización, Temporizador Anti-Olvido y MQTT`  
  *Asignado a:* **Diego López Pérez** (`@DiegoLop3z` / Gemini) — DoD: Máquina de estados, conmutación NPN, temporizador 60s, LWT en `/status`.
- **Issue #4:** `[DASH] Configuración de Broker Mosquitto y Flujos en Node-RED Dashboard 2.0`  
  *Asignado a:* **Arturo Heredia Martín** (`@arturoherediam` / Claude) — DoD: Mosquitto activo, dashboard desplegado, Foto 3 y Foto 4 capturadas.
- **Issue #5:** `[QA] Protocolo de Pruebas Integrales y Verificación de Demostración (7 Pasos)`  
  *Asignado a:* **Diego López Pérez & Arturo Heredia Martín** — DoD: 7 pasos del manual demostrados en vivo ante el docente.
- **Issue #6:** `[DOC] Redacción del Reporte Técnico Oficial (16 Secciones) y README Principal`  
  *Asignado a:* **Arturo Heredia Martín** (`@arturoherediam` / Claude) — DoD: 18 secciones de `docs/reporte_tecnico.md` consolidadas y pulidas.

---

## 5. Guías de Trabajo Operativas

### 5.1 Flujo para Arturo Heredia Martín (con Copiloto Claude)
1. **Clonar repositorio y abrir en VS Code:**
   ```bash
   git clone https://github.com/DiegoLop3z/Monitor_actuador.git
   cd Monitor_actuador
   code .
   ```
2. **Cargar contexto a Claude:** Subir a una conversación en Claude los archivos `docs/reporte_tecnico.md`, `node-red/guia_montaje_nodered.md` y `docs/propuesta_proyecto.md`.
3. **Ejecutar Prompt base:**
   > *"Hola Claude. Soy Arturo Heredia Martín (@arturoherediam) y trabajo en pareja con Diego López Pérez (@DiegoLop3z) en el proyecto SIAM-Yucatán (UPY, profesor Javier Poot). Mi responsabilidad es completar y pulir el Reporte Técnico Oficial en `docs/reporte_tecnico.md` con las 16 secciones requeridas, y validar el Dashboard Node-RED 2.0. Ayúdame a detallar la justificación psicrométrica NOAA, la etapa del transistor NPN, la NOM-015-STPS y los resultados de supervisión remota."*
4. **Validación de Dashboard y Capturas:** Importar `node-red/dashboard_flows.json`, probar con `python3 scripts/simular_mqtt.py`, tomar capturas y guardarlas en `docs/imagenes/dashboard_nodered_telemetria.png` y `dashboard_nodered_control.png`.
5. **Subir avances a Git:**
   ```bash
   git add docs/reporte_tecnico.md docs/imagenes/
   git commit -m "docs(reporte): completar redaccion academica y evidencias de interfaz"
   git push origin main
   ```

### 5.2 Flujo para Diego López Pérez (con Copiloto Gemini)
1. **Armado físico en protoboard:** Seguir detalladamente el diagrama en `hardware/diagrama_conexiones.png` y la guía `hardware/hardware_conexion.md`.
2. **Inspección eléctrica previa:** Verificar con multímetro que no existan cortocircuitos entre rieles de 3.3V, 5V y GND.
3. **Flasheo de Firmware:**
   ```bash
   cd firmware/esp32-bioclima-iot
   cp include/secrets.h.example include/secrets.h
   # Editar include/secrets.h con el SSID y contraseña del Hotspot / Wi-Fi
   pio run -t upload
   pio device monitor
   ```
4. **Fotografías físicas:** Tomar `docs/imagenes/protoboard_vista_general.png` (vista cenital completa) y `docs/imagenes/protoboard_actuacion_ventilador.png` (primer plano de aspas girando y LED encendido) y guardarlas en el repositorio.
5. **Subir cambios a GitHub:**
   ```bash
   git add docs/imagenes/
   git commit -m "docs(evidencias): incorporar fotografias reales del protoboard ensamblado"
   git push origin main
   ```
