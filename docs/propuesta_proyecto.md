# Propuesta de Proyecto: SIAM-Yucatán
## Sistema Inteligente de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática

> **Evaluación Unidad 2: Sistema IoT Integrador — Entregable 1**  
> **Institución:** Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026  
> **Materia:** Internet de las Cosas (IoT)  
> **Docente Titular:** M.I. Javier Poot  
> **Autores:**  
> • **Diego López Pérez** (GitHub: [`@DiegoLop3z`](https://github.com/DiegoLop3z))  
> • **Arturo Heredia Martín** (GitHub: [`@arturoherediam`](https://github.com/arturoherediam))  
> **Metodología de Desarrollo:** Programación en pareja asistida por IA (Diego con Gemini / Arturo con Claude)

---

## 1. Nombre del Proyecto

**SIAM-Yucatán** (*Sistema Inteligente de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática*).

---

## 2. Definición de la Problemática Real

En la zona metropolitana del estado de Yucatán —específicamente en el corredor de conurbación **Mérida – Kanasín – Ucú**— se experimenta una de las dinámicas bioclimáticas más agresivas de la República Mexicana:
1. **Condición Climática Extrema:** Durante la primavera y la temporada de canícula, la temperatura ambiente en sombra supera comúnmente los **40 °C**, acompañada de una humedad relativa sostenida entre el **65% y el 85%**. Bajo estas condiciones psicrométricas, la **sensación térmica real (*Heat Index*) calculada por la ecuación de Rothfusz de la NOAA sobrepasa rutinariamente los 48 °C a 52 °C**.
2. **Impacto en Espacios Productivos y Aulas (Kanasín y Ucú):**
   - En **Kanasín**, proliferan talleres de herrería, carpinterías, manufactura y bodegas con techos de lámina galvanizada y losas delgadas donde la temperatura superficial irradia hasta **55 °C** hacia el interior.
   - En **Ucú**, la sede del campus de la UPY y los polonos tecnológicos adyacentes albergan laboratorios de cómputo, talleres de mecatrónica y aulas donde las cargas térmicas internas (equipos electrónicos disipando calor) se suman al calor ambiental, provocando fatiga metabólica, pérdida de concentración y somnolencia en alumnos y técnicos.
3. **Peligro Biológico (NOM-015-STPS):** El cuerpo humano disipa calor principalmente mediante la evaporación del sudor. Cuando la humedad ambiental es excesiva, la tasa de evaporación se anula, acumulando calor metabólico en el núcleo corporal e induciendo deshidratación rápida, calambres, agotamiento por calor o el peligro mortal de un **golpe de calor (*heat stroke*)**.
4. **Ineficiencia Energética Regional:** La solución convencional de dejar encendidos ventiladores o sistemas de extracción de aire de manera ininterrumpida resulta económicamente insostenible ante las elevadas tarifas eléctricas de la península (CFE tarifa comercial e industrial). Se requiere una solución que ventile forzadamente **únicamente cuando el índice de calor represente un peligro real Y exista presencia humana confirmada en el espacio**.

---

## 3. Justificación Técnica y Normativa

El proyecto no constituye una maqueta escolar con reglas artificiales, sino una estación de supervisión laboral y mitigación bioclimática fundamentada en normativas vigentes:
- **NOM-015-STPS-2001 (Condiciones térmicas elevadas o abatidas):** Exige monitorear el régimen térmico en centros de trabajo cerrados y regular los tiempos de exposición, activando ventilación mecánica de renovación de aire.
- **NOM-025-STPS-2008 (Condiciones de iluminación en los centros de trabajo):** Establece niveles mínimos de iluminancia para puestos de trabajo visuales, evitando fatiga ocular y riesgos de accidentes.
- **Ecuación del Índice de Calor de Rothfusz (NOAA / National Weather Service):** Un termómetro común no refleja el peligro fisiológico. El algoritmo implementado en la ESP32 combina temperatura y humedad en tiempo real para determinar el riesgo biológico verdadero.
- **Prevención de Fallo Humano por Olvido:** En talleres o laboratorios, el supervisor suele activar manualmente la ventilación a primera hora para realizar una "purga de aire caliente estancado" previo al ingreso del personal. Un descuido común es olvidar apagarlo, consumiendo energía todo el día. SIAM-Yucatán incorpora un **temporizador de retorno automático de MANUAL a AUTO** (parametrizado a 60 s en la prueba escolar demostrable; 30 min en régimen productivo de campo).

---

## 4. Objetivos del Proyecto

### 4.1 Objetivo General
Diseñar, implementar en protoboard, calibrar y desplegar un sistema IoT integrador de monitoreo bioclimático, evaluación de sensación térmica en tiempo real y mitigación forzada mediante ventilación conmutada por transistor NPN y semáforo visual NOM-015, gobernado por un microcontrolador ESP32 y supervisado remotamente a través de MQTT (Mosquitto) y Node-RED Dashboard 2.0.

### 4.2 Objetivos Específicos
1. Integrar físicamente en protoboard 4 variables ambientales directas: temperatura (°C), humedad relativa (%), nivel de iluminación (%) y presencia humana (0/1), complementadas con el cálculo en firmware del Índice de Calor (°C).
2. Construir una etapa de conmutación de potencia desacoplada con **transistor NPN (*Low-Side Switch*)** en `GPIO 23` para accionar de forma segura un mini ventilador de 5V DC, protegiendo al ESP32 contra picos inductivos mediante un diodo flyback en antiparalelo.
3. Programar en PlatformIO un firmware modular no bloqueante (`millis()`) que ejecute dos decisiones automáticas locales:
   - **Automatización A (Mitigación Térmica):** Encender el ventilador si $HI \ge 38^\circ\text{C}$ o $\text{Temp} \ge 32^\circ\text{C}$ **y** hay presencia humana confirmada; apagar con histéresis térmica y timeout de 30 segundos por desocupación.
   - **Automatización B (Semáforo Bioclimático):** Manejar un LED RGB con código tricromático acorde a la NOM-015 (Verde < 30°C, Amarillo 30–37.9°C, Rojo $\ge 38^\circ\text{C}$ con parpadeo preventivo).
4. Implementar un monitor de enlace de red físico utilizando el LED azul integrado onboard (`GPIO 2`) que parpadee en búsqueda de Wi-Fi/MQTT y permanezca fijo en sincronización activa.
5. Diseñar un flujo en Node-RED Dashboard 2.0 que presente telemetría en tiempo real, gauges analógicos, gráfico histórico, tarjeta de alerta NOM-015 y un switch de mando remoto desacoplado en lazo cerrado para accionar el ventilador con demostración del temporizador anti-olvido.

---

## 5. Descripción de la Solución Técnica

El sistema se compone de cuatro subsistemas acoplados:

```text
┌───────────────────────────┐      ┌───────────────────────────┐
│     SENSORES FÍSICOS      │      │     ACTUADORES LOCALES    │
│ • SHT41 (I2C 0x44): T & H │      │ • Ventilador 5V (NPN D23) │
│ • LDR (ADC1 D34): Luz     │─────►│ • LED RGB Semáforo (D25-27│
│ • PIR (Digital D35): Pres │      │ • OLED 128x32 (I2C 0x3C)  │
└───────────────────────────┘      └───────────────────────────┘
              │                                  ▲
              ▼                                  │
┌──────────────────────────────────────────────────────────────┐
│        CONTROLADOR CENTRAL: ESP32 DevKit V1 (30 Pines)       │
│ • Algoritmo NOAA Heat Index • Máquina de Estados no bloqueante│
│ • Diagnóstico de Red (LED Azul D2) • FreeRTOS / PlatformIO   │
└──────────────────────────────────────────────────────────────┘
              ▲                                  │
              │ Publica telemetría/estados       │ Suscripción comandos
              ▼                                  ▼
┌──────────────────────────────────────────────────────────────┐
│             SERVICIO IOT: Mosquitto Broker Local             │
│ • Puerto 1883 • Autenticación por roles • Mecanismo LWT      │
└──────────────────────────────────────────────────────────────┘
              ▲
              │ WebSockets / MQTT
              ▼
┌──────────────────────────────────────────────────────────────┐
│       INTERFAZ DE USUARIO: Node-RED Dashboard 2.0 Web        │
│ • Gauges analógicos • Gráficas de tendencia • Switch remoto  │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. Sensores, Actuadores y Tecnologías

### 6.1 Sensores Utilizados
| Sensor | Variable Medida | Interfaz / Pin ESP32 | Justificación |
|---|---|---|---|
| **Sensirion GY-SHT41** | Temperatura (°C) y Humedad (%) | I²C (`GPIO 21` SDA / `GPIO 22` SCL) | Precisión industrial (±0.2 °C, ±1.8 % RH), bajo consumo, bus compartido a 3.3V. |
| **Fotocelda LDR** | Iluminancia en plano laboral (%) | Analógica en **`GPIO 34` (`ADC1_CH6`)** | Pertenece al bloque ADC1, permitiendo muestreo continuo y seguro mientras el Wi-Fi transmite. |
| **PIR HC-SR501** | Presencia / Ocupación humana | Digital en **`GPIO 35` (Input)** | Detección piroeléctrica con lente Fresnel para validar ocupación real antes de encender ventilación. |

### 6.2 Actuadores e Indicadores
| Actuador | Función en el Sistema | Pin ESP32 | Circuito de Potencia / Control |
|---|---|---|---|
| **Ventilador 5V DC** | Mitigación térmica y renovación forzada de aire | `GPIO 23` | **Low-Side Switch con Transistor NPN (2N2222A)**, $R_b=1\,\text{k}\Omega$, diodo flyback 1N4001 antiparalelo. |
| **LED RGB** | Semáforo visual in situ de estrés térmico NOM-015 | `GPIO 25, 26, 27` | Cátodo común con 3× resistores limitadores de $220\,\Omega$ ($I_R \approx 5.9\,\text{mA}$, $I_{G,B} \approx 1.4\,\text{mA}$). |
| **LED Azul Onboard** | Diagnóstico instantáneo de red Wi-Fi y MQTT | `GPIO 2` | LED interno del DevKit (parpadeo rápido en reconexión, fijo en enlace activo). |
| **Pantalla OLED** | Telemetría local in situ | I²C (`0x3C`, `GPIO 21/22`) | Alterna vistas de métricas, IP y estado del ventilador sin requerir PC conectada. |

### 6.3 Pila Tecnológica
- **Entorno de Firmware:** PlatformIO Core + Arduino C++ en Visual Studio Code.
- **Protocolo de Comunicación IoT:** MQTT 3.1.1 con QoS 0 y 1, mensajes retenidos y Last Will and Testament (LWT).
- **Broker Local:** Eclipse Mosquitto con listas de control de acceso (ACL).
- **Servidor y Dashboard Web:** Node-RED con el paquete oficial `@flowfuse/node-red-dashboard` (Dashboard 2.0).
- **Herramientas de Simulación y Análisis:** Python 3 (cálculo matricial psicrométrico, generación vectorial SVG y simulación de tráfico MQTT).

---

## 7. Plan de Ejecución y Asignación de Roles en Pareja

| Integrante | Rol en el Proyecto | Herramienta IA | Tareas Asignadas |
|---|---|---|---|
| **Diego López Pérez** (`@DiegoLop3z`) | Líder de Hardware Físico, Firmware y Pruebas de Banco | Gemini | Armado en protoboard (circuito transistor NPN del ventilador 5V, SHT41, OLED, LDR, PIR, LEDs), flasheo de firmware, pruebas físicas con multímetro, registro fotográfico de evidencias físicas (Fotos 1 y 2), y scripts de automatización/simulación. |
| **Arturo Heredia Martín** (`@arturoherediam`) | Líder de Documentación Oficial, Broker y Dashboard | Claude | Redacción y consolidación del Reporte Técnico Oficial (16 secciones obligatorias UPY con Claude), configuración del broker Mosquitto local, despliegue de Node-RED Dashboard 2.0, captura de evidencias web (Fotos 3 y 4) y pruebas de supervisión remota en lazo cerrado. |
