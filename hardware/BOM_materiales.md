# Lista de Materiales (Bill of Materials - BOM)
## Sistema IoT Integrador SIAM-Yucatán

> **Evaluación Unidad 2: Sistema IoT Integrador**  
> **Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026**  
> **Docente Titular:** M.I. Javier Poot  
> **Autores:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))

---

## 1. Tabla General de Componentes Físicos y Costos Estimados (MXN)

| Ítem | Componente | Modelo / Especificación | Cantidad | Costo Unitario (MXN) | Subtotal (MXN) | Función en el Sistema |
|:---:|---|---|:---:|:---:|:---:|---|
| **1** | **Microcontrolador Principal** | ESP32 DevKit V1 (30 pines, ESP-WROOM-32, Wi-Fi b/g/n, BLE, Dual-Core 240 MHz) | 1 | $145.00 | $145.00 | Controlador central, cliente MQTT, cálculo de Heat Index NOAA y control autónomo no bloqueante. |
| **2** | **Sensor de Temperatura y Humedad** | Sensirion GY-SHT41 (Precisión ±0.2 °C, ±1.8 % RH, interfaz I²C dirección `0x44`) | 1 | $95.00 | $95.00 | Adquisición ambiental de alta precisión para el monitoreo de estrés térmico laboral. |
| **3** | **Pantalla de Telemetría Local** | Pantalla OLED 0.91" 128×32 SSD1306 (I²C dirección `0x3C`, 3.3V) | 1 | $65.00 | $65.00 | Despliegue de métricas in situ, IP de red y estado físico del ventilador y modo. |
| **4** | **Sensor de Presencia y Ocupación** | Sensor Piroeléctrico PIR HC-SR501 / AM312 (Ángulo 100°, alcance 3-5 m, salida 3.3V) | 1 | $38.00 | $38.00 | Detección humana para condicionar el encendido del ventilador y timeout de 30 s. |
| **5** | **Sensor de Radiación e Iluminación** | Fotocelda LDR GL5528 (5-10 kΩ en luz, 1 MΩ en oscuridad) + Resistor de 10 kΩ 1/4W | 1 + 1 | $12.00 | $12.00 | Monitoreo del plano de iluminación de trabajo según NOM-025-STPS en `GPIO 34` (`ADC1`). |
| **6** | **Actuador 1: Disipación Térmica** | Mini Ventilador 5V DC (30×30×10 mm o 40×40×10 mm, 0.15 A, 5500 RPM) | 1 | $45.00 | $45.00 | Renovación de aire forzado ante calor extremo ($HI \ge 38^\circ\text{C}$). |
| **7** | **Etapa de Potencia para Ventilador** | Transistor NPN 2N2222A (o BC547 / TIP120) en TO-92 + Resistor Base 1 kΩ 1/4W | 1 + 1 | $8.00 | $8.00 | *Low-side switch* para desacoplar la lógica de 3.3V del motor de 5V y saturar en `GPIO 23`. |
| **8** | **Protección Inductiva** | Diodo Flyback de Conmutación 1N4001 o 1N4148 (DO-41, 1A / 100V) | 1 | $3.00 | $3.00 | Supresión de fuerza contraelectromotriz inversa producida por las bobinas del motor. |
| **9** | **Actuador 2: Semáforo Bioclimático** | LED RGB Difuso 5 mm Cátodo Común + 3× Resistores 220 Ω 1/4W | 1 + 3 | $14.00 | $14.00 | Indicación visual tricromática de seguridad según categorías NOM-015 (`GPIO 25, 26, 27`). |
| **10** | **Indicador de Diagnóstico de Red** | LED Azul Integrado onboard en el DevKit (`GPIO 2`) | 1 | $0.00 | $0.00 | Señalización de estado Wi-Fi y broker MQTT (parpadeo en búsqueda, fijo en enlace activo). |
| **11** | **Base de Prototipado** | Protoboard estándar de 830 puntos con pistas de alimentación duales | 1 | $75.00 | $75.00 | Ensamble modular sin soldaduras para verificación y pruebas en aula. |
| **12** | **Interconexión y Cableado** | Cables jumper Dupont (Macho-Macho y Macho-Hembra de 20 cm) | 1 paquete | $35.00 | $35.00 | Líneas de buses I²C, divisor resistivo, base del transistor y alimentación. |
| **13** | **Alimentación y Programación** | Cable Micro-USB blindado de alta corriente (5V / 2A) | 1 | $40.00 | $40.00 | Enlace serial a 115200 baudios y suministro eléctrico estable para el microcontrolador y motor. |
| **TOTAL** | **Costo Total del Prototipo Físico** | — | — | — | **$570.00 MXN** | Proyecto de alta fidelidad industrial y costo escolar accesible (< $30 USD). |

---

## 2. Especificaciones Eléctricas de los Componentes Clave

### 2.1 Microcontrolador ESP32 DevKit V1
- **Voltaje de Operación Lógica:** 3.3 V DC.
- **Voltaje de Entrada VIN (USB):** 5.0 V DC.
- **Corriente Máxima por GPIO:** 12 mA (recomendada), 40 mA (límite absoluto).
- **Consumo Promedio con Wi-Fi Activo:** 80 mA a 160 mA.
- **ADC Recomendado:** `ADC1` (`GPIO 32–39`), ya que `ADC2` se bloquea al activar el módem de radiofrecuencia Wi-Fi.

### 2.2 Sensor Sensirion GY-SHT41
- **Voltaje de Alimentación:** 3.3 V (mediante regulador integrado en el breakout).
- **Interfaz:** I²C en modo estándar (100 kHz) o fast-mode (400 kHz). Dirección predeterminada: `0x44`.
- **Rango de Medición:** -40 °C a +125 °C (±0.2 °C) y 0 % a 100 % RH (±1.8 % RH).
- **Consumo:** 0.08 µA (idle), 3.2 µA (durante medición periódica).

### 2.3 Ventilador 5V DC y Etapa NPN
- **Tensión Nominal del Motor:** 5.0 V DC (tomados de la línea `VIN` / 5V USB).
- **Corriente Nominal de Trabajo:** 80 mA a 140 mA (dependiendo de la contrapresión).
- **Potencia Disipada por el Motor:** $P = 5\,\text{V} \times 0.12\,\text{A} = 0.6\,\text{W}$.
- **Transistor NPN (2N2222A):**
  - $V_{CEO(\max)} = 40\,\text{V}$ (muy superior a los 5V de trabajo).
  - $I_{C(\max)} = 800\,\text{mA}$ (holgura del 500% sobre los 140 mA del ventilador).
  - $h_{FE(\min)} \approx 75$ a saturación.
  - $V_{CE(\text{sat})} \le 0.3\,\text{V}$.
