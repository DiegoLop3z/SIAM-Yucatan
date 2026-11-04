# Issue #3: [FW] Implementación de Reglas de Automatización, Temporizador Anti-Olvido y MQTT

- **Asignado a:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z))
- **Copiloto IA:** Gemini
- **Etiquetas:** `firmware`, `automation`, `mqtt`, `timer-purga`, `closed-loop`

---

## Descripción del Trabajo
Desarrollar la máquina de estados local, las reglas de decisión autónoma y la integración bidireccional con el broker MQTT:

1. **Cliente MQTT (PubSubClient) con LWT:**
   - Configuración de buffer extendido a 512 bytes para dar cabida a payloads JSON.
   - Registro de Last Will and Testament en `yucatan/bioclima/status` con valor `"offline"` retenido.
   - Al conectar, publicar `"online"` retenido y suscribirse a los tópicos de mando `.../actuador/+/set` y `.../config/+`.
2. **Automatización 1: Mitigación Térmica Condicionada a Presencia:**
   - En modo `AUTO`: Si $(HI \ge 38.0^\circ\text{C} \lor \text{Temp} \ge 32.0^\circ\text{C})$ **Y** `Presencia == 1`: saturar transistor NPN (`GPIO 23 = HIGH`) activando el ventilador de 5V.
   - Apagar ventilador si el espacio permanece desocupado por más de 30 segundos continuos (ahorro de energía eléctrica).
   - Apagar ventilador por histéresis térmica si $\text{Temp} < 30.0^\circ\text{C}$ y $HI < 35.0^\circ\text{C}$.
3. **Automatización 2: Semáforo Bioclimático en LED RGB:**
   - Verde: Confort ($HI < 30^\circ\text{C}$).
   - Amarillo: Precaución ($30^\circ\text{C} \le HI < 38^\circ\text{C}$).
   - Rojo: Peligro crítico ($HI \ge 38^\circ\text{C}$) con parpadeo preventivo de advertencia cada 500 ms.
4. **Control Remoto con Temporizador Anti-Olvido:**
   - Permitir al usuario enviar `"ON"` o `"OFF"` al ventilador.
   - En modo `MANUAL`, iniciar un temporizador no bloqueante: tras 60 segundos (demostración de la purga de 30 min de campo), conmutar autónomamente de regreso a modo `AUTO` y publicar la confirmación para evitar que el ventilador quede encendido indefinidamente por descuido humano.
5. **Confirmación en Lazo Cerrado Desacoplado:**
   - Publicar el estado real confirmado en `.../ventilador/estado` y `.../modo/estado`.

---

## Criterios de Aceptación (Definition of Done - DoD)
- [ ] Publicación periódica cada 2 s en tópicos independientes y en JSON agregado `yucatan/bioclima/telemetria`.
- [ ] Ventilador enciende automáticamente por calor + presencia y se apaga tras 30 s de desocupación.
- [ ] LED RGB refleja con exactitud la categoría de riesgo NOM-015.
- [ ] Temporizador anti-olvido conmuta de regreso a `AUTO` tras 60 s y actualiza a Node-RED.
- [ ] Broker Mosquitto publica automáticamente `"offline"` si el ESP32 se desconecta físicamente.
