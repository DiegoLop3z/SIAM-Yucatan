# Guía de Contribución — Proyecto SIAM-Yucatán

¡Bienvenidos al repositorio del **Sistema Inteligente de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática (SIAM-Yucatán)**! Este proyecto corresponde a la evaluación integradora de la **Unidad 2: Sistema IoT Integrador** de la **Universidad Politécnica de Yucatán (UPY)**, evaluada por el profesor **M.I. Javier Poot**.

---

## 1. Equipo de Desarrollo y Metodología en Pareja con IA

El desarrollo se realiza mediante la metodología de **programación en parejas asistida por IA (AI Pair Programming)**:

| Desarrollador | Usuario GitHub | Rol Principal | Herramienta IA Copiloto |
|---|---|---|---|
| **Diego López Pérez** | [`@DiegoLop3z`](https://github.com/DiegoLop3z) | Arquitectura de Firmware PlatformIO, Algoritmos bioclimáticos, Scripts y Reporte Técnico | Gemini |
| **Arturo Heredia Martín** | [`@arturoherediam`](https://github.com/arturoherediam) | Ensamble y Validación de Hardware, Broker Mosquitto local, Node-RED Dashboard 2.0 y QA | Claude |

---

## 2. Flujo de Trabajo con Git y Convenciones

### 2.1 Ramas de Trabajo
- Rama principal de producción: `main`.
- Para cambios específicos, crear ramas descriptivas:
  - `feature/firmware-telemetria`
  - `feature/dashboard-nodered`
  - `docs/reporte-tecnico`
  - `fix/calibracion-ldr`

### 2.2 Mensajes de Commit (Conventional Commits)
Se deben estructurar los commits con prefijos claros:
- `feat(fw):` Nuevas funcionalidades de firmware en ESP32.
- `feat(ui):` Nuevos componentes o flujos en Node-RED Dashboard.
- `hw:` Cambios o documentación de conexiones electrónicas.
- `docs:` Modificaciones a documentación técnica, entregables o README.
- `fix:` Corrección de errores en código, calibraciones o suscripciones MQTT.
- `test:` Scripts de prueba o verificación de hardware/red.

Ejemplo:
```bash
git commit -m "feat(fw): implementar temporizador no bloqueante de retorno a modo AUTO tras 60s"
```

---

## 3. Estándares de Código y Hardware

### 3.1 Firmware ESP32 (PlatformIO / C++)
1. **Cero retrasos bloqueantes:** Queda estrictamente prohibido el uso de `delay()` en el bucle principal `loop()`. Todo temporizado debe realizarse mediante variables de tiempo y `millis()`.
2. **Reconexión no bloqueante:** La pérdida temporal de Wi-Fi o del broker MQTT **no debe bloquear** la lectura de sensores, la actualización de la pantalla OLED ni el control autónomo local.
3. **Manejo de tópicos MQTT:**
   - Publicación en tópicos independientes para telemetría plana y en JSON agregado para persistencia.
   - Todo comando (`.../set`) debe procesarse y responderse con una publicación de confirmación en el tópico de estado (`.../estado`).
4. **Protección de periféricos:** Los pines analógicos deben pertenecer al bloque `ADC1` (e.g., `GPIO 34`) para evitar conflictos de multiplexado con el módem Wi-Fi.

### 3.2 Montaje Físico y Buenas Prácticas
1. **Verificación de polaridad:** Antes de conectar el ESP32 al puerto USB, verificar siempre la ausencia de cortocircuitos entre las líneas de 3.3V, 5V (VIN) y GND usando multímetro en modo continuidad.
2. **Etapa de Potencia:** El ventilador de 5V DC **nunca** debe conectarse directamente a un pin del ESP32. Debe controlarse mediante el transistor NPN en configuración *Low-Side Switch* con su resistencia de base de 1 kΩ y su diodo flyback en antiparalelo.
3. **GND Común:** Todas las tierras (fuente externa de 5V, ventilador, sensores y ESP32) deben compartir una referencia de masa común (*common ground*).

---

## 4. Gestión del Backlog y Tareas (GitHub Issues)

El proyecto se gestiona mediante los 6 issues detallados en la carpeta [`github_issues/`](github_issues/):
- **Issue #1:** `[HW] Verificación Física del Protoboard y Registro Fotográfico de Evidencias` (Arturo Heredia / Claude)
- **Issue #2:** `[FW] Desarrollo del Módulo de Sensores, LDR y Algoritmo de Sensación Térmica` (Diego López / Gemini)
- **Issue #3:** `[FW] Implementación de Reglas de Automatización, Temporizador Anti-Olvido y MQTT` (Diego López / Gemini)
- **Issue #4:** `[DASH] Configuración de Broker Mosquitto y Flujos en Node-RED Dashboard 2.0` (Arturo Heredia / Claude)
- **Issue #5:** `[QA] Protocolo de Pruebas Integrales y Verificación de Demostración (7 Pasos)` (Ambos colaboradores)
- **Issue #6:** `[DOC] Redacción del Reporte Técnico Oficial (16 Secciones) y README Principal` (Diego López / Gemini)

---

## 5. Licencia

Al contribuir a este repositorio, aceptas que tus contribuciones se licencien bajo los términos de la [Licencia MIT](LICENSE).
