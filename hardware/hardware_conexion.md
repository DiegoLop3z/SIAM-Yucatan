# Hardware — Guía de Conexión, Tabla de Pines y Etapa de Potencia

> **Proyecto:** SIAM-Yucatán (Sistema IoT Integrador)  
> **Universidad Politécnica de Yucatán (UPY) — Ciclo Escolar 2026**  
> **Docente:** M.I. Javier Poot  
> **Autores:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z)) & Arturo Heredia Martín ([`@arturoherediam`](https://github.com/arturoherediam))

---

## 1. Asignación General de Pines en la ESP32 DevKit V1 (30 Pines)

```text
                                ESP32 DevKit V1
                               ┌───────────────┐
                     3.3V ─────┤ 3V3       VIN ├───── +5V (Fuente USB / VIN)
                      GND ─────┤ GND       GND ├───── GND Común
                (LDR) D34 ─────┤ D34       D13 ├
                (PIR) D35 ─────┤ D35       D12 ├
                      D32 ─────┤ D32       D14 ├
                      D33 ─────┤ D33       D27 ├───── LED RGB Azul (R 220Ω)
        LED RGB Rojo  D25 ─────┤ D25       D26 ├───── LED RGB Verde (R 220Ω)
   (Diagnóstico Red)  D2  ─────┤ D2        D25 ├
                      D4  ─────┤ D4        D23 ├───── Base Transistor Ventilador (R 1kΩ)
                     TX2  ─────┤ TX2       D22 ├───── I2C SCL (SHT41 & OLED)
                     RX2  ─────┤ RX2       D21 ├───── I2C SDA (SHT41 & OLED)
                      D5  ─────┤ D5        TX0 ├
                      D18 ─────┤ D18       RX0 ├
                      D19 ─────┤ D19        EN ├
                               └───────────────┘
```

---

## 2. Detalle Teórico y Eléctrico: Etapa de Conmutación NPN (Low-Side Switch)

### 2.1 La Problemática del Accionamiento Directo
Un pin GPIO del ESP32 opera a **3.3 V** y su circuitería interna CMOS está diseñada para suministrar un máximo seguro de **12 mA** (límite destructivo absoluto: 40 mA). Por otra parte, un mini ventilador de corriente continua de 5V DC demanda entre **80 mA y 150 mA** en régimen estacionario, con picos transitorios de arranque que superan los **300 mA**.

Intentar alimentar el motor directamente desde un pin del microcontrolador ocasionaría:
1. Destrucción térmica instantánea de la etapa de salida del pin de la ESP32.
2. Caídas abruptas de voltaje (*voltage brownouts*) en el regulador interno del ESP32, provocando reinicios espontáneos cíclicos (*bootloops*).
3. Ruido electromagnético masivo conducido hacia el bus del procesador.

### 2.2 Circuito Esquemático de Conmutación

Para solventar esto de forma segura y profesional, se implementa una etapa de **conmutador por lado bajo (*Low-Side Switch*) con transistor NPN** (2N2222A o similar) en `GPIO 23`:

```text
               Línea de Alimentación +5V (VIN / USB 5V)
                           │
                           ├───[+]──────────────────────────────┐
                           │                                    │
                           ▼                                    │
                     ┌───────────┐                            ┌─┴─┐
                     │ Ventilador│ Motor de extracción        ▲   ▲ Diodo Flyback
                     │   de 5V   │ 80 - 140 mA                │   │ (1N4001 / 1N4148)
                     │ (Inductivo│                            └───┤ Cátodo a +5V,
                     └───────────┘                                │ Ánodo al Colector
                           │                                    │
                           ├───[-]──────────────────────────────┘
                           │
                        Colector (C)
                           │
                     ┌─────┴─────┐
    GPIO 23 ──[ 1 kΩ ]──┤ Base (B)  │ Transistor NPN (2N2222A)
    (3.3V)      Rb    │           │
                     └─────┬─────┘
                           │
                        Emisor (E)
                           │
                           ▼
                      GND Común (Tierra compartida ESP32 y Fuente 5V)
```

---

### 2.3 Principio de Operación Física: Corte y Saturación

#### Estado 1: Corte (Ventilador Desactivado, `GPIO 23 = LOW`, 0 V)
1. El microcontrolador establece `0 V` en el pin `GPIO 23`.
2. La diferencia de potencial base-emisor es nula ($V_{BE} = 0\,\text{V}$). La corriente de base es cero ($I_B = 0\,\mu\text{A}$).
3. La unión PN base-emisor carece de portadores de carga suficientes para vencer la barrera de potencial. El canal Colector-Emisor presenta una impedancia equivalente a un circuito abierto ($R_{CE} > 10\,\text{M}\Omega$).
4. **Comportamiento de la carga:** Aunque el terminal positivo del ventilador está a +5V, no existe una trayectoria conductora de retorno hacia tierra (GND). Por tanto, la corriente que atraviesa las bobinas es nula ($I_C = 0\,\text{mA}$) y el ventilador permanece completamente detenido.

#### Estado 2: Saturación (Ventilador Activado, `GPIO 23 = HIGH`, 3.3 V)
1. El microcontrolador establece `3.3 V` en `GPIO 23`.
2. La unión base-emisor se polariza en directa ($V_{BE} \approx 0.7\,\text{V}$).
3. Se calcula la corriente inyectada a la base mediante la Ley de Ohm a través del resistor limitador $R_b = 1000\,\Omega$:
   $$I_B = \frac{V_{\text{GPIO}} - V_{BE}}{R_b} = \frac{3.3\,\text{V} - 0.7\,\text{V}}{1000\,\Omega} = \frac{2.6\,\text{V}}{1000\,\Omega} = 2.6\,\text{mA}$$
4. El pin del ESP32 entrega únicamente **2.6 mA**, un consumo ínfimo y completamente seguro para el chip.
5. Para garantizar saturación profunda con una corriente de carga estimada $I_C \approx 130\,\text{mA}$, se evalúa la ganancia forzada en saturación:
   $$\beta_{\text{sat}} = \frac{I_C}{I_B} = \frac{130\,\text{mA}}{2.6\,\text{mA}} \approx 50$$
   Dado que el 2N2222A ofrece $\beta \ge 75$, el transistor entra de inmediato en **saturación profunda**.
6. En saturación, la tensión entre colector y emisor colapsa a su valor mínimo ($V_{CE(\text{sat})} \approx 0.1\text{–}0.2\,\text{V}$).
7. El colector queda prácticamente cortocircuitado al emisor (GND), cerrando el lazo de corriente:
   $$\text{+5V} \longrightarrow \text{Devanados Ventilador} \longrightarrow \text{Colector} \longrightarrow \text{Emisor} \longrightarrow \text{GND}$$
8. El ventilador recibe prácticamente la totalidad de los 5V ($5\,\text{V} - 0.15\,\text{V} = 4.85\,\text{V}$), girando a su máximo flujo de renovación bioclimática.

---

### 2.4 Protección Inductiva: Diodo Flyback en Antiparalelo

Los motores eléctricos son cargas altamente reactivas e inductivas (representadas como una inductancia $L$ en serie con una resistencia de devanado $R$). 

Cuando el transistor conmuta súbitamente de saturación a corte para apagar el motor, la corriente intenta cesar abruptamente ($\frac{di}{dt} \ll 0$). De acuerdo con la Ley de Inducción de Faraday-Lenz:
$$\mathcal{E} = -L \frac{di}{dt}$$
El colapso del campo magnético acumulado en el rotor genera un pulso transitorio de alta tensión positiva en el colector que puede superar fácilmente los **60 V a 100 V**. Sin protección, este pico perforaría la juntura del transistor o induciría ruido destructivo en la línea de tierra del ESP32.

**Solución aplicada:**
Se coloca un diodo rectificador rápido (1N4001 o 1N4148) **en antiparalelo** con el ventilador:
- El **Cátodo (línea plateada / negra)** se conecta a la línea de **+5V**.
- El **Ánodo** se conecta al **Colector** del transistor.
- Durante el funcionamiento normal, el diodo está polarizado en inversa y no interviene.
- Al conmutar a corte, el pico de tensión positiva fuerza la conducción directa del diodo, derivando y disipando la energía magnética almacenada en la resistencia interna de la propia bobina en un lazo cerrado seguro, protegiendo al 100% el transistor y el ESP32.

---

## 3. Tabla Exhaustiva de Conexiones Físicas

| Componente | Pin Módulo | Pin ESP32 | Voltaje Operación | Justificación Eléctrica y Funcional |
|---|---|---|---|---|
| **Sensor GY-SHT41** | `VIN`<br>`GND`<br>`SDA`<br>`SCL` | `3V3`<br>`GND`<br>`GPIO 21`<br>`GPIO 22` | 3.3 V Lógico | Bus I²C compartido a 100 kHz. Dirección física `0x44`. Pull-ups integradas en el módulo breakout. Monitoreo ambiental de alta fidelidad. |
| **Pantalla OLED SSD1306** | `VCC`<br>`GND`<br>`SDA`<br>`SCL` | `3V3`<br>`GND`<br>`GPIO 21`<br>`GPIO 22` | 3.3 V Lógico | Mismo bus I²C. Dirección física `0x3C`. Despliega in situ lecturas, dirección IP, modo y estado del actuador sin pantalla de PC. |
| **Fotocelda LDR** | Nodo Divisor | `GPIO 34` (D34) | Analógico 0–3.3 V | **Pertenece a `ADC1_CH6`**, garantizando lecturas inmunes al ruido mientras el Wi-Fi transmite datos. Divisor de tensión con resistor de 10 kΩ a GND. |
| **Sensor PIR** | `VCC`<br>`GND`<br>`OUT` | `VIN` (5V)<br>`GND`<br>`GPIO 35` (D35) | 3.3 V Lógico (salida) | Sensor piroeléctrico para presencia. La salida entrega 3.3V al detectar movimiento, conectada al pin de entrada digital exclusiva `GPIO 35`. |
| **Ventilador 5V (NPN Switch)** | Base (R 1kΩ)<br>Colector<br>Emisor | `GPIO 23` (D23)<br>Terminal Negativo<br>`GND` | Control 3.3V / Carga 5V | **Low-Side Switch NPN:** Desacopla la lógica sensible de 3.3V de los 140 mA de potencia del motor. Saturación en HIGH, corte en LOW. |
| **LED RGB - Rojo** | Ánodo R (R 220Ω) | `GPIO 25` (D25) | 3.3 V Lógico | Canal Rojo del Semáforo Bioclimático NOM-015 ($I_R \approx 5.9\,\text{mA}$). Alerta de estrés térmico crítico ($HI \ge 38^\circ\text{C}$). |
| **LED RGB - Verde** | Ánodo G (R 220Ω) | `GPIO 26` (D26) | 3.3 V Lógico | Canal Verde del Semáforo Bioclimático ($I_G \approx 1.4\,\text{mA}$). Confort ambiental ($HI < 30^\circ\text{C}$). |
| **LED RGB - Azul** | Ánodo B (R 220Ω) | `GPIO 27` (D27) | 3.3 V Lógico | Canal Azul del LED RGB ($I_B \approx 1.4\,\text{mA}$). Indicación auxiliar de diagnóstico. |
| **LED RGB - Común** | Cátodo Común (`-`) | `GND` | 0 V | Retorno común de los tres canales cromáticos a la masa del circuito. |
| **LED Azul Integrado** | Onboard ESP32 | `GPIO 2` | 3.3 V Interno | **Monitor de Enlace de Red:** Parpadea rápido (200 ms) en búsqueda de Wi-Fi/MQTT; fijo en sincronización activa con Mosquitto. |

---

## 4. Procedimiento de Verificación con Multímetro (Checklist Previo a Energizar)

1. **Prueba de Continuidad de Tierras:** Colocar el multímetro en modo continuidad (bip) y comprobar que el pin `GND` del ESP32, el emisor del transistor, el borne negativo del sensor PIR, la pantalla OLED, el sensor SHT41 y el cátodo del LED RGB estén sólidamente unidos al mismo riel de tierra.
2. **Prueba de No-Cortocircuito (3.3V vs GND):** Medir resistencia entre el pin `3V3` y `GND`. Debe marcar alta impedancia ($> 10\,\text{k}\Omega$). Si marca $0\,\Omega$, revisar de inmediato los módulos I²C antes de conectar.
3. **Prueba de No-Cortocircuito (VIN vs GND):** Medir resistencia entre `VIN` (5V) y `GND`. Debe superar varios kiloohms.
4. **Polaridad del Diodo Flyback:** Confirmar visualmente que la banda de cátodo apunte hacia el carril de +5V y la terminal de ánodo al colector del transistor NPN. Si se monta invertido, al activar el transistor se provocará un cortocircuito directo entre 5V y GND.
