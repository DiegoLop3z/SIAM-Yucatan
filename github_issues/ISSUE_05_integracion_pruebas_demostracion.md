# Issue #5: [QA] Protocolo de Pruebas Integrales y Verificación de Demostración (7 Pasos)

- **Asignado a:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))
- **Copiloto IA:** Gemini (Hardware & Firmware) + Claude (Dashboard & Reporte)
- **Etiquetas:** `qa`, `testing`, `demostracion`, `rubrica`

---

## Descripción del Trabajo
Ejecutar en conjunto la secuencia de pruebas funcionales de extremo a extremo conforme a la lista de chequeo de 7 pasos establecida en `docs/manual_demostracion.md`, asegurando que el prototipo físico y la plataforma web respondan sin fallas durante la evaluación con el docente M.I. Javier Poot.
- **Diego López Pérez:** A cargo de la manipulación física del banco de pruebas (excitación de calor al SHT41, oclusión del LDR, movimiento frente al PIR, verificación del ventilador 5V y semáforo RGB).
- **Arturo Heredia Martín:** A cargo de la operación del panel web Node-RED Dashboard 2.0, broker Mosquitto, temporizador anti-olvido y cotejo con el reporte técnico oficial.

### Secuencia de Verificación:
1. **Paso 1: Encendido y Diagnóstico de Red:** Comprobar que el LED azul onboard (`GPIO 2`) parpadee al buscar Wi-Fi/MQTT y se quede fijo al conectar, y que la pantalla OLED muestre la bienvenida y la IP local.
2. **Paso 2: Lectura de Sensores:** Validar que los valores de SHT41, LDR y PIR sean congruentes con el entorno físico.
3. **Paso 3: Envío por MQTT:** Verificar mediante `mosquitto_sub` la llegada de tópicos planos y el JSON agregado cada 2 s.
4. **Paso 4: Visualización en Dashboard:** Constatar que los gauges, tendencias históricas y tarjetas de ocupación en Node-RED Dashboard 2.0 se actualicen fluidamente.
5. **Paso 5: Activación Automática por Calor y Presencia:** Inducir calor en el SHT41 ($HI \ge 38^\circ\text{C}$) con presencia frente al PIR; corroborar que el transistor NPN satura, el ventilador de 5V gira y el LED RGB pasa a Rojo parpadeante.
6. **Paso 6: Control Remoto y Retorno Anti-Olvido:** Conmutar a modo `MANUAL` y encender el ventilador desde Node-RED; esperar 60 segundos y corroborar que el ESP32 regresa de forma autónoma a modo `AUTO` y lo notifica al dashboard.
7. **Paso 7: Respuesta ante Variaciones Externas:** Cubrir la fotocelda LDR (el gauge de luz cae a <20%); permanecer quieto 30 segundos (el ventilador se apaga por desocupación).

---

## Criterios de Aceptación (Definition of Done - DoD)
- [ ] Los 7 pasos de demostración ejecutados y aprobados al 100%.
- [ ] Cero retrasos perceptibles o caídas de conexión durante la sesión de prueba continua de 15 minutos.
- [ ] Lista de chequeo en `docs/manual_demostracion.md` completamente marcada y validada.
