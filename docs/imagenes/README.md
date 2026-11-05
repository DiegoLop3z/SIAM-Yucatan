# Registro de Evidencias Fotográficas y Diagramas Visuales
## Sistema IoT Integrador SIAM-Yucatán

> **Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026**  
> **Docente Titular:** M.I. Javier Poot  
> **Autores:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))

---

## 1. Inventario de Imágenes del Repositorio

Este directorio aloja las evidencias gráficas oficiales requeridas por la rúbrica de evaluación de la Unidad 2:

| Archivo | Tipo de Evidencia | Responsable de Captura | Estado / Uso |
|---|---|---|---|
| `protoboard_vista_general.png` | Fotografía física del ensamble completo en protoboard | Diego López Pérez | Entregable 4 (Prototipo físico ensamblado) y Reporte Técnico |
| `protoboard_actuacion_ventilador.png` | Fotografía de detalle en conmutación de ventilador y LED RGB | Diego López Pérez | Entregable 4 / 6 (Demostración de actuación física en vivo) |
| `dashboard_nodered_telemetria.png` | Captura de pantalla de Node-RED Dashboard 2.0 en operación | Arturo Heredia Martín | Entregable 5 (Dashboard web con métricas y gauges en vivo) |
| `dashboard_nodered_control.png` | Captura de mando remoto, lazo cerrado y retorno anti-olvido | Arturo Heredia Martín | Entregable 5 / 7 (Control bidireccional y temporizador de 60s) |
| `diagrama_arquitectura.png` | Diagrama de bloques y capas IoT del sistema integral | Diego López Pérez | Entregable 2 (Arquitectura IoT) y README general |
| `diagrama_flujo_firmware.png` | Diagrama de flujo de la máquina de estados del firmware ESP32 | Diego López Pérez | Entregable 2 (Diseño lógico del sistema) |

---

## 2. Pautas Técnicas para las Fotografías del Hardware Físico

Para garantizar que el docente M.I. Javier Poot aprecie la calidad técnica del montaje:

### 2.1 Foto 1: `protoboard_vista_general.png`
- **Encuadre:** Plano cenital (desde arriba) o en ángulo de 45° con iluminación uniforme y sin sombras duras.
- **Elementos visibles obligatorios:**
  1. Microcontrolador ESP32 DevKit V1 conectado a la protoboard.
  2. Sensor SHT41 montado en el bus I²C.
  3. Pantalla OLED 128×32 encendida mostrando métricas.
  4. Fotocelda LDR con su resistor de 10 kΩ a tierra.
  5. Sensor PIR con lente Fresnel visible.
  6. Etapa del transistor NPN (2N2222) con su resistor de 1 kΩ en la base y diodo flyback.
  7. Ventilador de 5V DC colocado junto al disipador o área de prueba.
  8. LED RGB de 5 mm con sus 3 resistores de 220 Ω.
  9. Cable USB suministrando alimentación.

### 2.2 Foto 2: `protoboard_actuacion_ventilador.png`
- **Encuadre:** Primer plano enfocado en el ventilador de 5V y el LED RGB durante un evento de activación (por ejemplo, induciendo calor o forzándolo desde Node-RED).
- **Detalle clave:** Las aspas del ventilador deben apreciarse en rotación (efecto de movimiento o desenfoque dinámico) y el LED RGB encendido en Amarillo o Rojo, evidenciando la conmutación real de potencia mediante el transistor NPN.

---

## 3. Pautas Técnicas para las Capturas del Dashboard

### 3.1 Foto 3: `dashboard_nodered_telemetria.png`
- Capturar la vista completa del navegador en [`http://localhost:1880/dashboard/bioclima`](http://localhost:1880/dashboard/bioclima).
- Deben apreciarse los 4 gauges (Temperatura, Humedad, Heat Index y Luz) con valores coherentes, la gráfica temporal con líneas continuas y la tarjeta de ocupación en sala.

### 3.2 Foto 4: `dashboard_nodered_control.png`
- Captura de pantalla tomada inmediatamente después de accionar el ventilador en modo MANUAL:
  - El interruptor debe reflejar la posición `ON`.
  - El texto de estado debe confirmar: `🌀 EN REVOLUCIÓN (Transistor Saturado / Extracción Activa)`.
  - El modo debe mostrar: `⚙️ MANUAL (Purga iniciada: auto-retorno a AUTO en 60s)`.
  - El diagnóstico de red LWT debe mostrar: `🟢 NODO ESP32 CONECTADO Y TRANSMITIENDO`.

---

## 4. Reemplazo de Archivos
Una vez capturadas las fotografías y capturas reales con la cámara o herramienta de captura de pantalla, simplemente guardarlas con estos mismos nombres en este directorio para actualizar automáticamente todos los documentos técnicos del proyecto.
