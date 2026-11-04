# Manual de Demostración y Protocolo de Evaluación en Vivo (7 Pasos)
## Sistema IoT Integrador SIAM-Yucatán

> **Evaluación Unidad 2: Sistema IoT Integrador — Entregable 6**  
> **Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026**  
> **Docente Evaluador:** M.I. Javier Poot  
> **Autores:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))

---

## 1. Propósito de este Manual

Este documento proporciona el guion operativo exacto para llevar a cabo la demostración funcional frente al profesor M.I. Javier Poot, estructurado punto por punto con base en los **7 criterios obligatorios de demostración** indicados en el PDF de instrucciones de evaluación.

---

## 2. Preparación Previa a la Demostración

1. **Alimentación del Hardware:** Conectar la placa ESP32 a la computadora mediante cable Micro-USB de datos.
2. **Servicio MQTT:** Asegurar que Mosquitto esté activo escuchando en `0.0.0.0:1883` (`sudo systemctl status mosquitto`).
3. **Servicio Node-RED:** Iniciar Node-RED y tener abierta en el navegador la pestaña del dashboard:  
   [`http://localhost:1880/dashboard/bioclima`](http://localhost:1880/dashboard/bioclima).
4. **Terminal de Diagnóstico (Opcional):** Abrir una terminal con el comando:
   ```bash
   mosquitto_sub -h localhost -p 1883 -u dashboard -P 'UpY2026!Dash' -t 'yucatan/bioclima/#' -v
   ```

---

## 3. Guion de Evaluación en Vivo (Paso a Paso)

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   SECUENCIA DE DEMOSTRACIÓN DE 7 PASOS                           │
├────────┬────────────────────────────────────────┬────────────────────────────────┤
│ Paso 1 │ Encendido del Sistema y Diagnóstico    │ LED Azul (GPIO 2) y OLED local │
│ Paso 2 │ Lectura de Sensores Ambientales        │ SHT41, LDR y PIR coherentes    │
│ Paso 3 │ Envío de Información por MQTT          │ Tópicos planos y JSON agregado │
│ Paso 4 │ Visualización en Node-RED Dashboard    │ Gauges, gráficas y semáforo    │
│ Paso 5 │ Activación Automática de Actuadores    │ Ventilador NPN + Presencia     │
│ Paso 6 │ Control Remoto y Retorno Anti-Olvido   │ Purga manual y auto AUTO (60s) │
│ Paso 7 │ Respuesta ante Cambios Externos        │ Cubrir LDR y timeout de 30s    │
└────────┴────────────────────────────────────────┴────────────────────────────────┘
```

---

### Paso 1: Encendido del Sistema y Diagnóstico de Red
- **Acción:** Energizar el ESP32 conectándolo al puerto USB o presionar el botón de `RESET`.
- **Qué observar en el prototipo físico:**
  1. El **LED azul integrado onboard (`GPIO 2`)** comienza a parpadear rápidamente (cada 200 ms), evidenciando que el microcontrolador se encuentra buscando la red Wi-Fi y estableciendo el socket con el broker Mosquitto.
  2. La **pantalla OLED SSD1306** enciende de inmediato, mostrando el mensaje de bienvenida `SIAM - YUCATAN` e indicando la dirección IP asignada.
  3. En cuanto el cliente MQTT sincroniza la conexión y registra el mensaje LWT, el **LED azul pasa a encendido fijo continuo**, confirmando enlace saludable sin necesidad de periféricos externos.
- **Resultado Esperado:** Arranque limpio, sin bloqueos y con diagnóstico visual instantáneo en el protoboard.

---

### Paso 2: Lectura de Sensores Físicos
- **Acción:** Inspeccionar la pantalla OLED y la consola serie a 115200 baudios.
- **Qué observar:**
  1. **Sensor Sensirion GY-SHT41:** Valores de temperatura (e.g., 28.0 °C a 32.0 °C) y humedad relativa (e.g., 60% a 75%) estables y acordes a la temperatura del laboratorio.
  2. **Sensor LDR en `GPIO 34` (`ADC1`):** Nivel de iluminación reportado entre 40% y 80% bajo la luz ambiental del aula.
  3. **Sensor PIR en `GPIO 35`:** Detección de presencia confirmada al moverse frente al lente Fresnel.
- **Resultado Esperado:** Cuatro variables físicas sensadas simultáneamente sin interferencias con el módem Wi-Fi.

---

### Paso 3: Envío de Información Mediante MQTT
- **Acción:** Observar la terminal con `mosquitto_sub`.
- **Qué observar:**
  1. Cada 2000 ms (2 segundos), el ESP32 publica los valores en tópicos independientes:
     - `yucatan/bioclima/sensor/temperatura` $\rightarrow$ `"31.4"`
     - `yucatan/bioclima/sensor/humedad` $\rightarrow$ `"74.0"`
     - `yucatan/bioclima/sensor/indice_calor` $\rightarrow$ `"41.2"`
     - `yucatan/bioclima/sensor/luz` $\rightarrow$ `"65"`
     - `yucatan/bioclima/sensor/presencia` $\rightarrow$ `"1"`
  2. Publicación simultánea del payload JSON unificado en `yucatan/bioclima/telemetria`:
     ```json
     {"temp":31.4,"hum":74.0,"hi":41.2,"luz":65,"pres":1,"fan":0,"modo":"AUTO","alerta":"PELIGRO"}
     ```
- **Resultado Esperado:** Flujo continuo de publicaciones con QoS 0 y retención controlada de estados.

---

### Paso 4: Visualización en Node-RED Dashboard 2.0
- **Acción:** Abrir [`http://localhost:1880/dashboard/bioclima`](http://localhost:1880/dashboard/bioclima).
- **Qué observar:**
  1. Los cuatro **gauges semicirculares** se posicionan con fluidez en los valores transmitidos.
  2. La **gráfica de tendencia temporal** dibuja la evolución de la temperatura y la sensación térmica.
  3. La tarjeta de **Ocupación en Sala** muestra `🚶 PRESENCIA DETECTADA`.
  4. La tarjeta de **Diagnóstico Bioclimático** despliega la categoría de riesgo NOM-015 (Verde, Amarillo o Rojo).
  5. El indicador LWT confirma `🟢 NODO ESP32 CONECTADO Y TRANSMITIENDO`.
- **Resultado Esperado:** Visualización en tiempo real sin recargar la página web.

---

### Paso 5: Activación Automática de Actuadores (Mitigación Bioclimática)
- **Acción:** Demostrar la primera regla de decisión autónoma.
  1. Con el sistema en modo `AUTO`, inducir calor suavemente sobre el SHT41 (acercar un dedo tibio o soplo de aire húmedo) para elevar el Heat Index por encima de **38.0 °C** (o superar el umbral de 32 °C).
  2. Mover la mano frente al sensor PIR para confirmar ocupación humana.
- **Qué observar:**
  1. El ESP32 conmuta instantáneamente el pin `GPIO 23` a nivel `HIGH`, inyectando 2.6 mA a la base del **transistor NPN (2N2222A)**.
  2. El transistor entra en **saturación profunda**, cierra el retorno a tierra y el **ventilador de 5V comienza a girar a máxima velocidad**, disipando calor forzadamente.
  3. El **LED RGB** cambia inmediatamente a color **Rojo con parpadeo preventivo**, alertando sobre el riesgo de estrés térmico laboral in situ (NOM-015).
  4. En Node-RED, el texto de estado se actualiza automáticamente a `🌀 EN REVOLUCIÓN (Transistor Saturado / Extracción Activa)`.
- **Resultado Esperado:** Actuación física inmediata y desacoplada condicionada al peligro térmico y a la presencia humana.

---

### Paso 6: Control Remoto en Lazo Cerrado y Retorno Anti-Olvido
- **Acción:** Demostrar la comunicación bidireccional y la protección anti-fallo humano.
  1. Desde el Dashboard de Node-RED, conmutar el selector de modo a `MANUAL` y accionar el switch del ventilador a `ON` (simulando una purga matutina de calor en un taller de Kanasín o laboratorio de Ucú).
  2. Observar la confirmación: el switch de Node-RED está **desacoplado**, por lo que sólo se enciende cuando el ESP32 responde a través de `.../actuador/ventilador/estado`.
  3. El ventilador enciende inmediatamente y la interfaz muestra:  
     `⚙️ MANUAL (Purga iniciada: auto-retorno a AUTO en 60s)`.
  4. **Demostración de la Protección Anti-Olvido:** Dejar el sistema desatendido durante **60 segundos** (representación escolar de los 30 min de purga en campo).
  5. Al cumplirse el minuto, el temporizador no bloqueante en la ESP32 expira: el microcontrolador conmuta de regreso a modo `AUTO`, lo publica por MQTT y la interfaz de Node-RED actualiza el selector a `AUTO` sin intervención humana. Si no hay presencia, el ventilador se apaga automáticamente.
- **Resultado Esperado:** Demostración exitosa de mando bidireccional y erradicación del error humano por descuido del operador.

---

### Paso 7: Respuesta Dinámica ante Cambios en las Variables Externas
- **Acción:** Probar la respuesta inmediata a perturbaciones físicas del entorno.
  1. **Perturbación en LDR:** Cubrir la fotocelda LDR con el pulgar para simular oscuridad o interrupción de iluminación laboral según NOM-025. El gauge en Node-RED cae de inmediato a menos del 15%. Retirar el pulgar y constatar el restablecimiento a >65%.
  2. **Timeout de Desocupación en Modo AUTO:** Con el ventilador girando por calor, apartarse del sensor PIR y permanecer inmóvil durante **30 segundos**.
  3. Al transcurrir los 30 s sin pulsos del PIR, el ESP32 conmuta `GPIO 23` a nivel `LOW` (corte del transistor NPN), apagando el ventilador para **ahorrar energía eléctrica**, demostrando que el confort se mitiga sólo cuando hay humanos a quienes proteger.
- **Resultado Esperado:** Reacción determinística ante variaciones externas en menos de 2 segundos.

---

## 4. Lista de Chequeo Rápida para Evaluación en Aula

| Criterio Evaluado | Estado | Observación Técnica |
|---|:---:|---|
| **1. Encendido y LED Azul** | [x] | Diagnóstico instantáneo de Wi-Fi y broker Mosquitto en `GPIO 2`. |
| **2. Cuatro Variables Físicas** | [x] | Temperatura, Humedad, Luz LDR en ADC1 y Presencia PIR en digital. |
| **3. Cálculo Heat Index NOAA** | [x] | Ecuación de Rothfusz en firmware evaluando riesgo metabólico real. |
| **4. MQTT y Last Will** | [x] | Mosquitto local con tópicos independientes, JSON y LWT en `/status`. |
| **5. Dashboard 2.0 Web** | [x] | Gauges, gráfica de tendencia, tarjetas de alerta NOM-015 y switch. |
| **6. Mitigación Térmica NPN** | [x] | Transistor satura con 2.6 mA y acciona ventilador 5V (140 mA) con diodo flyback. |
| **7. Semáforo LED RGB** | [x] | Verde (<30°C), Amarillo (30-38°C) y Rojo parpadeante ($\ge 38^\circ\text{C}$). |
| **8. Control Remoto Desacoplado** | [x] | Switch en lazo cerrado: confirma estado antes de fijar posición gráfica. |
| **9. Temporizador Anti-Olvido** | [x] | Retorno autónomo a AUTO tras 60 s (emulando los 30 min de purga de campo). |
| **10. Ahorro por Desocupación** | [x] | Apagado de ventilación tras 30 s sin ocupación en sala. |
