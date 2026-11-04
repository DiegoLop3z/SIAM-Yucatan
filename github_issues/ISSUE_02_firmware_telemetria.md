# Issue #2: [FW] Desarrollo del Módulo de Sensores, LDR y Algoritmo de Sensación Térmica

- **Asignado a:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z))
- **Copiloto IA:** Gemini
- **Etiquetas:** `firmware`, `platformio`, `sensors`, `heat-index`

---

## Descripción del Trabajo
Implementar en el proyecto PlatformIO (`firmware/esp32-bioclima-iot/`) el subsistema de adquisición periódica de sensores y el algoritmo matemático de sensación térmica:

1. **Adquisición No Bloqueante (Cadencia 2000 ms):**
   - Lectura de temperatura y humedad mediante la librería `Adafruit_SHT4x`.
   - Lectura analógica de 12 bits de la fotocelda LDR en `GPIO 34` (`ADC1_CH6`) y mapeo a porcentaje de iluminancia laboral (0 a 100%).
   - Muestreo digital del sensor piroeléctrico PIR en `GPIO 35`.
2. **Cálculo de Sensación Térmica (Heat Index NOAA):**
   - Crear cabecera `include/heat_index.h` con la regresión multivariable polinomial de Rothfusz oficial del National Weather Service de Estados Unidos.
   - Categorización del estrés bioclimático conforme a los límites de seguridad de la NOM-015-STPS (Confort <30°C, Precaución 30-38°C, Peligro $\ge 38^\circ\text{C}$).
3. **Monitor de Diagnóstico de Red en LED Azul Onboard (`GPIO 2`):**
   - Rutina no bloqueante de parpadeo rápido (200 ms) mientras se adquiere IP o se conecta al broker.
   - Encendido fijo / latido continuo cuando el enlace MQTT y Wi-Fi se encuentran sincronizados.
4. **Pantalla OLED SSD1306 (128x32):**
   - Rotación periódica cada 3000 ms entre 4 pantallas de visualización in situ (Métricas ambientales, Heat Index NOM-015, Luz/Presencia, y Estado de Red/IP local).

---

## Criterios de Aceptación (Definition of Done - DoD)
- [ ] Compilación en PlatformIO libre de advertencias o errores de sintaxis.
- [ ] Bucle principal `loop()` opera con cero retrasos bloqueantes (`delay()`).
- [ ] Valores devueltos por el algoritmo de Heat Index coinciden con la tabla psicrométrica de la NOAA.
- [ ] LED azul onboard (`GPIO 2`) señaliza fidedignamente el estado de conectividad.
- [ ] Pantalla OLED cicla vistas de telemetría sin congelar la ejecución.
