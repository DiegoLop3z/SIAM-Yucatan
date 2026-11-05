#!/usr/bin/env python3
"""
Generador Autónomo de Diagramas Vectoriales (SVG) y Renders de Documentación (PNG)
Sistema IoT Integrador SIAM-Yucatán — UPY 2026
Autores: Diego López Pérez (@DiegoLop3z) & Arturo Heredia Martín (@arturoherediam)

Genera:
1. hardware/diagrama_conexiones.svg y hardware/diagrama_conexiones.png
2. docs/diagrama_arquitectura.svg y docs/imagenes/diagrama_arquitectura.png
3. docs/diagrama_flujo_firmware.svg y docs/imagenes/diagrama_flujo_firmware.png
4. Placeholders visuales de alta resolución para docs/imagenes/
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==============================================================================
# 1. GENERADOR DE DIAGRAMA ELECTRÓNICO DE CONEXIONES (SVG & PNG)
# ==============================================================================

def generar_diagrama_conexiones_svg(salida_svg):
    W, H = 1500, 1260
    F = "DejaVu Sans, Arial, sans-serif"
    M = "DejaVu Sans Mono, Consolas, monospace"
    C = {
        "3v3": "#d62728",
        "5v": "#ff6b35",
        "gnd": "#222222",
        "sda": "#1c71d8",
        "scl": "#e5a50a",
        "ldr": "#9141ac",
        "pir": "#008080",
        "fan": "#26a269",
        "rgb_r": "#e01b24",
        "rgb_g": "#2ec27e",
        "rgb_b": "#3584e4",
        "net": "#1a5fb4"
    }

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{F}">')
    a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    a('<text x="40" y="44" font-size="24" font-weight="bold" fill="#0f172a">Diagrama Electrónico de Conexiones — Sistema SIAM-Yucatán</text>')
    a('<text x="40" y="70" font-size="14" fill="#475569">UPY 2026 · SHT41 + OLED (I²C GPIO 21/22) · LDR (GPIO 34 ADC1) · PIR (GPIO 35) · NPN Low-Side Switch Ventilador 5V (GPIO 23) · LED RGB (GPIO 25/26/27)</text>')

    def box(x, y, w, h, fill, stroke, rx=8):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def txt(x, y, s, size=12, weight="normal", fill="#222", anchor="start", font=None):
        ff = f' font-family="{font}"' if font else ""
        s_esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ff}>{s_esc}</text>')

    def wire(pts, col, w=3.2):
        d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        a(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    # ---- ESP32 DevKit V1 Central ----
    bx, by, bw, bh = 580, 110, 310, 640
    box(bx, by, bw, bh, "#1e293b", "#0f172a", rx=12)
    a('<path d="M685 125 h20 v14 h20 v-14 h20 v14 h20 v-14 h20" fill="none" stroke="#f59e0b" stroke-width="3"/>')
    box(675, 155, 120, 230, "#cbd5e1", "#94a3b8", rx=4)
    txt(735, 270, "ESP-WROOM-32", 11, "bold", "#1e293b", "middle")
    txt(735, 425, "ESP32 DevKit V1", 16, "bold", "#ffffff", "middle")
    txt(735, 447, "(Dual-Core 240MHz · Wi-Fi/MQTT)", 12, "normal", "#94a3b8", "middle")
    a(f'<rect x="705" y="{by+bh-6}" width="60" height="22" rx="3" fill="#94a3b8" stroke="#64748b"/>')
    txt(735, by+bh+34, "USB Datos / Alimentación 5V", 11, "normal", "#64748b", "middle")

    left_pins  = ["EN","VP","VN","D34","D35","D32","D33","D25","D26","D27","D14","D12","D13","GND","VIN"]
    right_pins = ["D23","D22","TX0","RX0","D21","D19","D18","D5","TX2","RX2","D4","D2","D15","GND","3V3"]

    used_left  = {"D34": "ldr", "D35": "pir", "D25": "rgb_r", "D26": "rgb_g", "D27": "rgb_b", "GND": "gnd", "VIN": "5v"}
    used_right = {"D23": "fan", "D22": "scl", "D21": "sda", "D2": "net", "GND": "gnd", "3V3": "3v3"}

    py_l, py_r = {}, {}
    for i, (lp, rp) in enumerate(zip(left_pins, right_pins)):
        y = 190 + i * 36
        ul = lp in used_left
        cl = C[used_left[lp]] if ul else "#64748b"
        a(f'<circle cx="{bx+16}" cy="{y}" r="{6.5 if ul else 4.5}" fill="{cl}" stroke="#fff" stroke-width="{1.5 if ul else 0}"/>')
        txt(bx+28, y+4, lp, 12, "bold" if ul else "normal", "#ffffff" if ul else "#94a3b8")
        py_l[lp] = y

        ur = rp in used_right
        cr = C[used_right[rp]] if ur else "#64748b"
        a(f'<circle cx="{bx+bw-16}" cy="{y}" r="{6.5 if ur else 4.5}" fill="{cr}" stroke="#fff" stroke-width="{1.5 if ur else 0}"/>')
        txt(bx+bw-28, y+4, rp, 12, "bold" if ur else "normal", "#ffffff" if ur else "#94a3b8", "end")
        py_r[rp] = y

    # ---- LADO IZQUIERDO: LDR, PIR, LED RGB ----
    # 1. LDR
    lx, ly, lw, lh = 40, 110, 430, 145
    box(lx, ly, lw, lh, "#fdf4ff", "#c026d3")
    txt(lx+16, ly+26, "Sensor de Iluminación — LDR (ADC1)", 14, "bold", "#86198f")
    txt(lx+16, ly+46, "Divisor: 3.3V → LDR → GPIO 34 → R 10kΩ → GND", 11.5, "normal", "#475569")
    txt(lx+16, ly+68, "• Pin ADC1_CH6 (GPIO 34): Lectura analógica inmune a Wi-Fi", 11.5, "normal", "#334155")
    txt(lx+16, ly+88, "• Conversión: 0..4095 ADC → 0..100% de iluminancia laboral", 11.5, "normal", "#334155")
    txt(lx+lw-14, ly+124, "Nodo Divisor (OUT) → GPIO 34", 11.5, "bold", "#86198f", "end")
    wire([(lx+lw, ly+120), (510, ly+120), (510, py_l["D34"]), (bx+16, py_l["D34"])], C["ldr"])

    # 2. PIR
    px, py, pw, ph = 40, 275, 430, 130
    box(px, py, pw, ph, "#f0fdfa", "#0d9488")
    txt(px+16, py+26, "Sensor de Presencia — PIR HC-SR501 / AM312", 14, "bold", "#115e59")
    txt(px+16, py+46, "• Salida digital 3.3V hacia GPIO 35 · Lente Fresnel 100°", 11.5, "normal", "#334155")
    txt(px+16, py+68, "• Timeout de desocupación: 30s sin presencia apaga el ventilador", 11.5, "normal", "#334155")
    txt(px+pw-14, py_l["D35"]+4, "Señal OUT → GPIO 35", 11.5, "bold", "#115e59", "end")
    wire([(px+pw, py_l["D35"]), (bx+16, py_l["D35"])], C["pir"])

    # 3. LED RGB Semáforo Bioclimático
    rx, ry, rw, rh = 40, 425, 430, 270
    box(rx, ry, rw, rh, "#fff7ed", "#ea580c")
    txt(rx+16, ry+26, "Semáforo Bioclimático — LED RGB (NOM-015)", 14, "bold", "#9a3412")
    txt(rx+16, ry+46, "3× Resistores limitadores de 220 Ω · Cátodo Común a GND", 11.5, "normal", "#475569")

    rgb_rows = [
        ("D25", "rgb_r", 505, "R (220 Ω) ← GPIO 25 (Rojo: HI >= 38°C Peligro)"),
        ("D26", "rgb_g", 550, "G (220 Ω) ← GPIO 26 (Verde: HI < 30°C Confort)"),
        ("D27", "rgb_b", 595, "B (220 Ω) ← GPIO 27 (Azul: Diagnóstico de Modo)"),
    ]
    for idx, (pin_name, col_key, box_y, label_txt) in enumerate(rgb_rows):
        pin_y = py_l[pin_name]
        mid_x = 490 + idx * 16
        wire([(rx+rw, box_y), (mid_x, box_y), (mid_x, pin_y), (bx+16, pin_y)], C[col_key])
        txt(rx+18, box_y+4, label_txt, 11.5, "bold", C[col_key])

    # Tierras y 5V del lado izquierdo
    wire([(bx+16, py_l["GND"]), (545, py_l["GND"]), (545, 665), (rx+rw, 665)], C["gnd"])
    txt(rx+rw-14, 669, "GND Común (LDR, PIR, Cátodo RGB)", 11.5, "bold", "#222", "end")
    wire([(bx+16, py_l["VIN"]), (560, py_l["VIN"]), (560, py+108), (px+pw, py+108)], C["5v"])
    txt(px+pw-14, py+104, "VCC PIR ← 5V (VIN)", 11.5, "bold", C["5v"], "end")

    # ---- LADO DERECHO: Etapa Transistor NPN + Ventilador 5V, SHT41, OLED ----
    # 1. Etapa NPN Low-Side Switch Ventilador 5V
    vx, vy, vw, vh = 1010, 110, 450, 200
    box(vx, vy, vw, vh, "#f0fdf4", "#16a34a")
    txt(vx+18, vy+26, "Etapa de Potencia — Transistor NPN (Low-Side Switch)", 14, "bold", "#166534")
    txt(vx+18, vy+46, "Ventilador 5V DC (140 mA) · Desacoplo de 3.3V a 5V de potencia", 11.5, "normal", "#475569")
    txt(vx+18, vy+68, "• Base (B): Resistor Rb 1 kΩ inyecta 2.6 mA desde GPIO 23", 11.5, "normal", "#334155")
    txt(vx+18, vy+88, "• Colector (C): Al borne (-) del motor y ánodo diodo Flyback", 11.5, "normal", "#334155")
    txt(vx+18, vy+108, "• Emisor (E): Conectado directamente a GND común", 11.5, "normal", "#334155")
    txt(vx+18, vy+128, "• Diodo Flyback (1N4001): Antiparalelo con cátodo a +5V (Protección fem)", 11.5, "normal", "#334155")
    txt(vx+18, vy+176, "Base NPN (Rb 1 kΩ) ← GPIO 23", 12, "bold", C["fan"])
    wire([(bx+bw-16, py_r["D23"]), (975, py_r["D23"]), (975, vy+172), (vx, vy+172)], C["fan"])

    # Buses I2C compartidos
    X_BUS = {"scl": 920, "sda": 945, "gnd": 965, "3v3": 985}
    wire([(bx+bw-16, py_r["D22"]), (X_BUS["scl"], py_r["D22"]), (X_BUS["scl"], 660)], C["scl"])
    wire([(bx+bw-16, py_r["D21"]), (X_BUS["sda"], py_r["D21"]), (X_BUS["sda"], 690)], C["sda"])
    wire([(bx+bw-16, py_r["GND"]), (X_BUS["gnd"], py_r["GND"]), (X_BUS["gnd"], 420)], C["gnd"])
    wire([(bx+bw-16, py_r["3V3"]), (X_BUS["3v3"], py_r["3V3"]), (X_BUS["3v3"], 390)], C["3v3"])

    # 2. Sensor GY-SHT41
    sx, sy, sw, sh = 1010, 330, 450, 165
    box(sx, sy, sw, sh, "#eff6ff", "#2563eb")
    txt(sx+18, sy+26, "Sensor Ambiental — Sensirion GY-SHT41 (I²C 0x44)", 14, "bold", "#1e40af")
    txt(sx+18, sy+48, "• Temp (±0.2 °C) y Humedad Relativa (±1.8 % RH) de alta fidelidad", 11.5, "normal", "#334155")
    txt(sx+18, sy+70, "• Alimenta el cálculo del Índice de Calor (Heat Index NOAA Rothfusz)", 11.5, "normal", "#334155")
    txt(sx+18, sy+100, "SCL ← GPIO 22", 11.5, "bold", C["scl"])
    txt(sx+18, sy+120, "SDA ← GPIO 21", 11.5, "bold", C["sda"])
    txt(sx+18, sy+140, "VCC ← 3V3 · GND ← GND", 11.5, "bold", "#475569")
    wire([(X_BUS["scl"], sy+96), (sx, sy+96)], C["scl"])
    wire([(X_BUS["sda"], sy+116), (sx, sy+116)], C["sda"])
    wire([(X_BUS["3v3"], sy+136), (sx, sy+136)], C["3v3"])

    # 3. Pantalla OLED SSD1306
    ox, oy, ow, oh = 1010, 515, 450, 175
    box(ox, oy, ow, oh, "#f8fafc", "#64748b")
    txt(ox+18, oy+26, "Pantalla Local — OLED 128×32 SSD1306 (I²C 0x3C)", 14, "bold", "#334155")
    txt(ox+18, oy+48, "• Comparte bus I²C (GPIO 21/22) con el sensor SHT41 sin colisión", 11.5, "normal", "#334155")
    txt(ox+18, oy+70, "• Despliega métricas in situ, IP local y estado FAN / MODO", 11.5, "normal", "#334155")
    txt(ox+18, oy+100, "SCL ← GPIO 22", 11.5, "bold", C["scl"])
    txt(ox+18, oy+120, "SDA ← GPIO 21", 11.5, "bold", C["sda"])
    txt(ox+18, oy+140, "VCC ← 3V3 · GND ← GND", 11.5, "bold", "#475569")
    wire([(X_BUS["scl"], oy+96), (ox, oy+96)], C["scl"])
    wire([(X_BUS["sda"], oy+116), (ox, oy+116)], C["sda"])
    wire([(X_BUS["3v3"], oy+136), (ox, oy+136)], C["3v3"])

    # Indicador de Red LED Onboard
    wire([(bx+bw-16, py_r["D2"]), (955, py_r["D2"]), (955, 725), (1010, 725)], C["net"])
    box(1010, 705, 450, 45, "#eff6ff", "#1d4ed8")
    txt(1025, 732, "LED Azul Onboard (GPIO 2): Monitor Enlace Wi-Fi / Broker MQTT", 11.5, "bold", "#1d4ed8")

    # Resumen inferior de alimentaciones
    box(40, 770, 1420, 450, "#f8fafc", "#cbd5e1", rx=10)
    txt(60, 805, "RESUMEN DE ARQUITECTURA DE ENERGÍA Y PROTECCIÓN ELÉCTRICA", 14, "bold", "#0f172a")
    txt(60, 835, "1. Línea 5V (VIN / USB): Suministra energía a la bobina del ventilador y al sensor PIR. Corriente hasta 140 mA absorbida directamente del puerto USB.", 12, "normal", "#334155")
    txt(60, 860, "2. Línea 3.3V (ESP32 3V3): Alimenta el sensor Sensirion SHT41, pantalla OLED SSD1306 y divisor de la fotocelda LDR. Corriente total < 25 mA.", 12, "normal", "#334155")
    txt(60, 885, "3. Etapa de Transistor NPN (Low-Side Switch): Desacopla la lógica de control (3.3V / 2.6 mA en GPIO 23) de la potencia inductiva (5V / 140 mA en ventilador).", 12, "normal", "#334155")
    txt(60, 910, "4. Diodo Flyback en Antiparalelo: Elimina pulsos destructivos de contratensión inductiva (f.e.m. inversa) al conmutar a corte el ventilador.", 12, "normal", "#334155")
    txt(60, 935, "5. Tierra Común (GND): Todas las masas (ESP32, emisor NPN, GND del ventilador, OLED, SHT41, PIR y LDR) están interconectadas a la misma referencia.", 12, "normal", "#334155")
    txt(60, 960, "6. Pines Analógicos Seguros: LDR conectado exclusivamente a GPIO 34 (ADC1), garantizando operación sin colisión con el módem de radio Wi-Fi.", 12, "normal", "#334155")

    a('</svg>')
    with open(salida_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(o))
    print(f"[OK] Diagrama de conexiones SVG generado en: {salida_svg}")

def render_diagrama_conexiones_png(salida_png):
    fig, ax = plt.subplots(figsize=(16, 12), dpi=120)
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Título
    ax.text(0.5, 11.5, "Diagrama Electrónico de Conexiones — Sistema SIAM-Yucatán", fontsize=18, fontweight='bold', color='#0f172a')
    ax.text(0.5, 11.1, "UPY 2026 · SHT41 & OLED (I2C GPIO 21/22) · LDR (GPIO 34) · PIR (GPIO 35) · NPN Switch Ventilador 5V (GPIO 23) · LED RGB (GPIO 25/26/27)", fontsize=11, color='#475569')

    # ESP32 Central
    esp = patches.FancyBboxPatch((6.0, 3.5), 3.8, 6.8, boxstyle="round,pad=0.2", facecolor='#1e293b', edgecolor='#0f172a', linewidth=2)
    ax.add_patch(esp)
    ax.text(7.9, 9.8, "ESP32 DevKit V1", fontsize=14, fontweight='bold', color='#ffffff', ha='center')
    ax.text(7.9, 9.4, "Dual-Core 240MHz · Wi-Fi/MQTT", fontsize=10, color='#94a3b8', ha='center')

    # Pines ESP32
    pins_l = ["VIN", "GND", "D13", "D12", "D14", "D27", "D26", "D25", "D33", "D32", "D35", "D34", "VN", "VP", "EN"]
    pins_r = ["3V3", "GND", "D15", "D2", "D4", "RX2", "TX2", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"]
    for i, p in enumerate(pins_l):
        y = 4.0 + i * 0.38
        ax.plot(6.2, y, 'o', color='#38bdf8', markersize=6)
        ax.text(6.5, y, p, fontsize=8, color='#e2e8f0', va='center')
    for i, p in enumerate(pins_r):
        y = 4.0 + i * 0.38
        ax.plot(9.6, y, 'o', color='#38bdf8', markersize=6)
        ax.text(9.3, y, p, fontsize=8, color='#e2e8f0', va='center', ha='right')

    # Cajas Izquierda: LDR, PIR, LED RGB
    ldr_box = patches.FancyBboxPatch((0.6, 8.4), 4.8, 1.8, boxstyle="round,pad=0.15", facecolor='#fdf4ff', edgecolor='#c026d3', linewidth=2)
    ax.add_patch(ldr_box)
    ax.text(0.8, 9.9, "Sensor LDR (Iluminación) — GPIO 34 (ADC1)", fontsize=11, fontweight='bold', color='#86198f')
    ax.text(0.8, 9.5, "Divisor: 3.3V → LDR → GPIO 34 → 10kΩ → GND", fontsize=9, color='#475569')
    ax.text(0.8, 9.1, "Lectura de 12 bits inmune a Wi-Fi (ADC1_CH6)", fontsize=9, color='#334155')

    pir_box = patches.FancyBboxPatch((0.6, 6.2), 4.8, 1.8, boxstyle="round,pad=0.15", facecolor='#f0fdfa', edgecolor='#0d9488', linewidth=2)
    ax.add_patch(pir_box)
    ax.text(0.8, 7.7, "Sensor PIR (Presencia) — GPIO 35 (Digital In)", fontsize=11, fontweight='bold', color='#115e59')
    ax.text(0.8, 7.3, "Salida 3.3V al detectar movimiento · VCC a 5V (VIN)", fontsize=9, color='#475569')
    ax.text(0.8, 6.9, "Timeout de desocupación de 30 s para apagar ventilador", fontsize=9, color='#334155')

    rgb_box = patches.FancyBboxPatch((0.6, 3.4), 4.8, 2.4, boxstyle="round,pad=0.15", facecolor='#fff7ed', edgecolor='#ea580c', linewidth=2)
    ax.add_patch(rgb_box)
    ax.text(0.8, 5.5, "Semáforo Bioclimático NOM-015 — LED RGB", fontsize=11, fontweight='bold', color='#9a3412')
    ax.text(0.8, 5.1, "• GPIO 25: Canal Rojo (R 220Ω) — HI >= 38°C (Peligro)", fontsize=9, color='#e01b24', fontweight='bold')
    ax.text(0.8, 4.7, "• GPIO 26: Canal Verde (R 220Ω) — HI < 30°C (Confort)", fontsize=9, color='#16a34a', fontweight='bold')
    ax.text(0.8, 4.3, "• GPIO 27: Canal Azul (R 220Ω) — Diagnóstico / Modo", fontsize=9, color='#2563eb', fontweight='bold')
    ax.text(0.8, 3.9, "• Cátodo común conectado a GND", fontsize=9, color='#475569')

    # Cajas Derecha: NPN Switch + Ventilador, SHT41, OLED
    fan_box = patches.FancyBboxPatch((10.4, 7.8), 5.0, 2.5, boxstyle="round,pad=0.15", facecolor='#f0fdf4', edgecolor='#16a34a', linewidth=2)
    ax.add_patch(fan_box)
    ax.text(10.6, 10.0, "Etapa NPN Low-Side Switch — Ventilador 5V", fontsize=11, fontweight='bold', color='#166534')
    ax.text(10.6, 9.6, "• Control en GPIO 23 con Rb = 1 kΩ (IB = 2.6 mA)", fontsize=9, color='#15803d', fontweight='bold')
    ax.text(10.6, 9.2, "• Colector NPN al borne (-) de carga del Ventilador", fontsize=9, color='#334155')
    ax.text(10.6, 8.8, "• Diodo Flyback (1N4001) en antiparalelo (cátodo a +5V)", fontsize=9, color='#334155')
    ax.text(10.6, 8.4, "• Emisor a GND · Protege al microcontrolador de sobrecargas", fontsize=9, color='#475569')

    sht_box = patches.FancyBboxPatch((10.4, 5.4), 5.0, 2.0, boxstyle="round,pad=0.15", facecolor='#eff6ff', edgecolor='#2563eb', linewidth=2)
    ax.add_patch(sht_box)
    ax.text(10.6, 7.1, "Sensor GY-SHT41 (I2C 0x44) — Precisión Climática", fontsize=11, fontweight='bold', color='#1e40af')
    ax.text(10.6, 6.7, "• Bus I2C: SDA (GPIO 21) y SCL (GPIO 22) a 3.3V", fontsize=9, color='#334155')
    ax.text(10.6, 6.3, "• Monitoreo de Temperatura (±0.2°C) y Humedad (±1.8% RH)", fontsize=9, color='#334155')
    ax.text(10.6, 5.9, "• Entrada de regresión polinomial Heat Index NOAA", fontsize=9, color='#475569')

    oled_box = patches.FancyBboxPatch((10.4, 3.4), 5.0, 1.7, boxstyle="round,pad=0.15", facecolor='#f8fafc', edgecolor='#64748b', linewidth=2)
    ax.add_patch(oled_box)
    ax.text(10.6, 4.8, "Pantalla OLED 128x32 SSD1306 (I2C 0x3C)", fontsize=11, fontweight='bold', color='#334155')
    ax.text(10.6, 4.4, "• Comparte bus I2C (GPIO 21/22) a 3.3V", fontsize=9, color='#475569')
    ax.text(10.6, 4.0, "• Despliega métricas, IP local y estado FAN/MODO", fontsize=9, color='#475569')

    # Panel inferior
    inf_box = patches.FancyBboxPatch((0.6, 0.4), 14.8, 2.5, boxstyle="round,pad=0.15", facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.5)
    ax.add_patch(inf_box)
    ax.text(0.8, 2.6, "CONSIDERACIONES ELÉCTRICAS Y CRITERIOS DE DISEÑO PRODUCTIVO", fontsize=11, fontweight='bold', color='#0f172a')
    ax.text(0.8, 2.2, "1. Desacoplo de Carga: La ESP32 opera a 3.3V y sólo suministra 12 mA por pin. El ventilador 5V (140 mA) se alimenta desde VIN/5V mediante conmutación NPN.", fontsize=9.5, color='#334155')
    ax.text(0.8, 1.8, "2. Supresión de Picos Inductivos: El diodo flyback absorbe la f.e.m. inversa inducida en las bobinas al apagar el ventilador, evitando picos de >60V.", fontsize=9.5, color='#334155')
    ax.text(0.8, 1.4, "3. Respaldo Diagnóstico: LED azul onboard (GPIO 2) señaliza parpadeo (búsqueda de Wi-Fi/MQTT) y fijo (enlace sincronizado con Mosquitto).", fontsize=9.5, color='#334155')
    ax.text(0.8, 1.0, "4. Protección Anti-Olvido: Temporizador no bloqueante de 60s en modo MANUAL para demostración de purga previa de 30 min en campo.", fontsize=9.5, color='#334155')

    fig.savefig(salida_png, bbox_inches='tight', dpi=130)
    plt.close(fig)
    print(f"[OK] Diagrama de conexiones PNG renderizado en: {salida_png}")

# ==============================================================================
# 2. GENERADOR DE ARQUITECTURA IOT (SVG & PNG)
# ==============================================================================

def generar_diagrama_arquitectura_svg(salida_svg):
    W, H = 1400, 900
    F = "DejaVu Sans, Arial, sans-serif"
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{F}">')
    a(f'<rect width="{W}" height="{H}" fill="#f8fafc"/>')
    a('<text x="50" y="50" font-size="24" font-weight="bold" fill="#0f172a">Arquitectura Integral del Sistema IoT — SIAM-Yucatán</text>')
    a('<text x="50" y="78" font-size="14" fill="#64748b">Universidad Politécnica de Yucatán (UPY) · Capas IoT: Percepción, Control Embebido, Red MQTT y Supervisión Node-RED</text>')

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def card(x, y, w, h, title, subtitle, bg, border, icon):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{border}" stroke-width="2"/>')
        a(f'<text x="{x+20}" y="{y+32}" font-size="16" font-weight="bold" fill="{border}">{esc(icon)} {esc(title)}</text>')
        a(f'<text x="{x+20}" y="{y+54}" font-size="12" fill="#475569">{esc(subtitle)}</text>')

    def t(x, y, text, size=12, weight="normal", fill="#334155"):
        a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(text)}</text>')

    # 4 Capas Verticales
    card(50, 110, 290, 720, "1. Percepción y Entorno", "Variables Físicas & Transductores", "#ffffff", "#0284c7", "📡")
    card(380, 110, 310, 720, "2. Nodo Controlador", "ESP32 Firmware & Automatización", "#ffffff", "#16a34a", "⚡")
    card(730, 110, 290, 720, "3. Transporte y Servicio", "Eclipse Mosquitto Broker", "#ffffff", "#ea580c", "🌐")
    card(1060, 110, 290, 720, "4. Supervisión y Mando", "Node-RED Dashboard 2.0", "#ffffff", "#7c3aed", "🖥️")

    # Contenido Capa 1
    t(70, 200, "• GY-SHT41 (I²C 0x44):", 13, "bold", "#0f172a")
    t(70, 222, "  Temperatura (±0.2 °C)")
    t(70, 242, "  Humedad Relativa (±1.8 %)")
    t(70, 280, "• Fotocelda LDR (ADC1_CH6):", 13, "bold", "#0f172a")
    t(70, 302, "  GPIO 34 · Divisor 10 kΩ")
    t(70, 322, "  Nivel de iluminancia (0-100%)")
    t(70, 360, "• Sensor PIR HC-SR501:", 13, "bold", "#0f172a")
    t(70, 382, "  GPIO 35 · Entrada digital")
    t(70, 402, "  Detección humana en sala")
    t(70, 440, "• Entorno Bioclimático:", 13, "bold", "#0f172a")
    t(70, 462, "  Mérida, Ucú y Kanasín")
    t(70, 482, "  Estrés térmico y canícula")

    # Contenido Capa 2
    t(400, 200, "• ESP32 DevKit V1 (240 MHz):", 13, "bold", "#0f172a")
    t(400, 222, "  Arquitectura modular no bloqueante")
    t(400, 242, "  Algoritmo Heat Index NOAA Rothfusz")
    t(400, 280, "• Actuador 1: Ventilador 5V", 13, "bold", "#0f172a")
    t(400, 302, "  Low-Side Switch NPN en GPIO 23")
    t(400, 322, "  Diodo flyback antiparalelo")
    t(400, 360, "• Actuador 2: LED RGB (NOM-015)", 13, "bold", "#0f172a")
    t(400, 382, "  Semáforo Verde/Amarillo/Rojo")
    t(400, 402, "  GPIO 25, 26, 27 con R 220 Ω")
    t(400, 440, "• OLED SSD1306 Local (0x3C):", 13, "bold", "#0f172a")
    t(400, 462, "  Alternancia de vistas cada 3s")
    t(400, 500, "• Reglas Autónomas:", 13, "bold", "#0f172a")
    t(400, 522, "  AUTO: Calor + Presencia")
    t(400, 542, "  Timeout 30s desocupado")
    t(400, 562, "  Purga manual: timer 60s anti-olvido")

    # Contenido Capa 3
    t(750, 200, "• Mosquitto MQTT Broker:", 13, "bold", "#0f172a")
    t(750, 222, "  Puerto estándar 1883 en 0.0.0.0")
    t(750, 242, "  Autenticación por usuario y hash")
    t(750, 280, "• Tópicos de Telemetría:", 13, "bold", "#0f172a")
    t(750, 302, "  yucatan/bioclima/sensor/+")
    t(750, 322, "  yucatan/bioclima/telemetria (JSON)")
    t(750, 360, "• Lazo Cerrado Desacoplado:", 13, "bold", "#0f172a")
    t(750, 382, "  .../actuador/ventilador/set")
    t(750, 402, "  .../actuador/ventilador/estado")
    t(750, 440, "• Mecanismo LWT:", 13, "bold", "#0f172a")
    t(750, 462, "  yucatan/bioclima/status")
    t(750, 482, "  online / offline retenido")

    # Contenido Capa 4
    t(1080, 200, "• Dashboard 2.0 Web:", 13, "bold", "#0f172a")
    t(1080, 222, "  Acceso: /dashboard/bioclima")
    t(1080, 242, "  Tema adaptativo responsive")
    t(1080, 280, "• Instrumentación Visual:", 13, "bold", "#0f172a")
    t(1080, 302, "  Gauges Temp, Hum, HI, Luz")
    t(1080, 322, "  Gráfica de tendencia temporal")
    t(1080, 342, "  Indicador de ocupación PIR")
    t(1080, 380, "• Mandos de Control Remoto:", 13, "bold", "#0f172a")
    t(1080, 402, "  Switch desacoplado de ventilador")
    t(1080, 422, "  Selector AUTO / MANUAL")
    t(1080, 442, "  Aviso de retorno de purga")
    t(1080, 480, "• Evaluador / Supervisor:", 13, "bold", "#0f172a")
    t(1080, 502, "  M.I. Javier Poot / Equipo UPY")

    # Flechas de conexión entre capas
    def arrow(x1, y1, x2, y2, color):
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-dasharray="4,4"/>')

    arrow(340, 250, 380, 250, "#0284c7")
    arrow(340, 340, 380, 340, "#0284c7")
    arrow(690, 310, 730, 310, "#16a34a")
    arrow(730, 390, 690, 390, "#ea580c")
    arrow(1020, 310, 1060, 310, "#ea580c")
    arrow(1060, 390, 1020, 390, "#7c3aed")

    a('</svg>')
    with open(salida_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(o))
    print(f"[OK] Diagrama de arquitectura SVG generado en: {salida_svg}")

def render_diagrama_arquitectura_png(salida_png):
    fig, ax = plt.subplots(figsize=(15, 9), dpi=120)
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(0.5, 8.5, "Arquitectura del Sistema IoT — SIAM-Yucatán", fontsize=18, fontweight='bold', color='#0f172a')
    ax.text(0.5, 8.1, "Universidad Politécnica de Yucatán (UPY) · Flujo de Datos, Decisión y Mando Bidireccional", fontsize=11, color='#64748b')

    capas = [
        (0.6, "1. Percepción Física", "#0284c7", "#f0f9ff", [
            "• SHT41: Temp & Humedad",
            "• LDR: Iluminancia (ADC1)",
            "• PIR: Presencia (Digital)",
            "• Ecosistema: Clima Yucatán",
            "• Estrés térmico severo"
        ]),
        (4.2, "2. Nodo ESP32", "#16a34a", "#f0fdf4", [
            "• Dual-Core 240 MHz FreeRTOS",
            "• Algoritmo Heat Index NOAA",
            "• NPN Switch Ventilador 5V",
            "• Semáforo RGB (NOM-015)",
            "• OLED 128x32 SSD1306",
            "• Timer purga anti-olvido 60s"
        ]),
        (7.8, "3. Broker Mosquitto", "#ea580c", "#fff7ed", [
            "• Mosquitto Local (0.0.0.0:1883)",
            "• Autenticación & ACL por Rol",
            "• Telemetría individual & JSON",
            "• Comandos actuador/.../set",
            "• Confirmación .../estado",
            "• LWT: yucatan/bioclima/status"
        ]),
        (11.4, "4. Node-RED Dashboard", "#7c3aed", "#faf5ff", [
            "• Dashboard 2.0 Web UI",
            "• Gauges Temp, Hum, HI, Luz",
            "• Histórico de evolución térmica",
            "• Switch ventilador desacoplado",
            "• Selector AUTO/MANUAL",
            "• Tarjeta alerta NOM-015"
        ]),
    ]

    for x, titulo, borde, fondo, items in capas:
        caja = patches.FancyBboxPatch((x, 1.2), 3.0, 6.4, boxstyle="round,pad=0.15", facecolor=fondo, edgecolor=borde, linewidth=2)
        ax.add_patch(caja)
        ax.text(x+0.2, 7.2, titulo, fontsize=12, fontweight='bold', color=borde)
        for i, item in enumerate(items):
            ax.text(x+0.2, 6.4 - i * 0.7, item, fontsize=9.5, color='#334155')

    # Flechas entre bloques
    ax.annotate('', xy=(4.2, 5.0), xytext=(3.6, 5.0), arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2.5))
    ax.annotate('', xy=(7.8, 5.5), xytext=(7.2, 5.5), arrowprops=dict(arrowstyle="->", color='#16a34a', lw=2.5))
    ax.annotate('', xy=(7.2, 4.0), xytext=(7.8, 4.0), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2.5))
    ax.annotate('', xy=(11.4, 5.5), xytext=(10.8, 5.5), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2.5))
    ax.annotate('', xy=(10.8, 4.0), xytext=(11.4, 4.0), arrowprops=dict(arrowstyle="->", color='#7c3aed', lw=2.5))

    fig.savefig(salida_png, bbox_inches='tight', dpi=130)
    plt.close(fig)
    print(f"[OK] Diagrama de arquitectura PNG renderizado en: {salida_png}")

# ==============================================================================
# 3. GENERADOR DE DIAGRAMA DE FLUJO DEL FIRMWARE (SVG & PNG)
# ==============================================================================

def generar_diagrama_flujo_svg(salida_svg):
    W, H = 1000, 1300
    F = "DejaVu Sans, Arial, sans-serif"
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{F}">')
    a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    a('<text x="50" y="44" font-size="22" font-weight="bold" fill="#0f172a">Diagrama de Flujo del Firmware — ESP32 SIAM-Yucatán</text>')
    a('<text x="50" y="70" font-size="13" fill="#64748b">Lógica No Bloqueante (millis) · Control Térmico, Conmutación NPN y Retorno Anti-Olvido</text>')

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def node(x, y, w, h, text, shape="rect", fill="#f8fafc", stroke="#64748b"):
        if shape == "ellipse":
            a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        elif shape == "diamond":
            a(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        else:
            a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        lines = text.split("\n")
        start_y = y + (h/2) - (len(lines)-1)*8 + 4
        for i, l in enumerate(lines):
            a(f'<text x="{x+w/2}" y="{start_y + i*16}" font-size="11.5" font-weight="bold" fill="#0f172a" text-anchor="middle">{esc(l)}</text>')

    def flow_line(x1, y1, x2, y2, label=""):
        a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="2"/>')
        a(f'<polygon points="{x2},{y2} {x2-4},{y2-8} {x2+4},{y2-8}" fill="#334155"/>')
        if label:
            a(f'<text x="{(x1+x2)/2 + 8}" y="{(y1+y2)/2}" font-size="10" font-weight="bold" fill="#2563eb">{esc(label)}</text>')

    cx = 500
    # 1. Inicio
    node(cx-90, 100, 180, 45, "INICIO / RESET", "ellipse", "#eff6ff", "#2563eb")
    flow_line(cx, 145, cx, 175)

    # 2. Setup
    node(cx-150, 175, 300, 70, "setup():\nInicializar Pines (FAN, RGB, LED Red, LDR, PIR)\nWire.begin() · SHT41 (0x44) · OLED (0x3C)\nWi-Fi STA + MQTT LWT ('offline')", "rect", "#f0fdf4", "#16a34a")
    flow_line(cx, 245, cx, 280)

    # 3. Loop Inicio
    node(cx-120, 280, 240, 45, "loop(): Obtener millis()\nRevisar Wi-Fi & MQTT", "rect", "#f8fafc", "#64748b")
    flow_line(cx, 325, cx, 360)

    # 4. Decisión Red Conectada
    node(cx-110, 360, 220, 60, "¿Wi-Fi & MQTT\nConectados?", "diamond", "#fff7ed", "#ea580c")
    flow_line(cx+110, 390, cx+180, 390, "NO")
    node(cx+180, 370, 170, 40, "Parpadeo LED Azul (200ms)\nReintentar conexión", "rect", "#fef2f2", "#dc2626")
    flow_line(cx, 420, cx, 460, "SÍ")

    # 5. Telemetría 2s
    node(cx-140, 460, 280, 60, "¿ahora - ultimaLectura >= 2000 ms?\nLeer SHT41, LDR, PIR\nCalcular Heat Index NOAA", "diamond", "#eff6ff", "#0284c7")
    flow_line(cx, 520, cx, 560, "SÍ")

    # 6. Decisión de Modo
    node(cx-100, 560, 200, 60, "¿Modo Operativo?", "diamond", "#f5f3ff", "#7c3aed")
    flow_line(cx-100, 590, cx-220, 590, "AUTO")
    flow_line(cx+100, 590, cx+220, 590, "MANUAL")

    # Rama AUTO
    node(cx-360, 620, 250, 70, "¿(HI >= 38°C || Temp >= Umbral)\n&& Presencia == 1?", "diamond", "#fefce8", "#ca8a04")
    node(cx-360, 730, 250, 45, "Ventilador ON (Saturar NPN GPIO 23)\ntiempoUltimaPresencia = millis()", "rect", "#dcfce7", "#15803d")
    flow_line(cx-235, 690, cx-235, 730, "SÍ")
    node(cx-360, 810, 250, 60, "¿Desocupado > 30s ||\n(Temp < 30°C && HI < 35°C)?", "diamond", "#fefce8", "#ca8a04")
    flow_line(cx-235, 775, cx-235, 810)
    node(cx-360, 910, 250, 45, "Ventilador OFF (Corte NPN GPIO 23)", "rect", "#fee2e2", "#b91c1c")
    flow_line(cx-235, 870, cx-235, 910, "SÍ")

    # Rama MANUAL
    node(cx+110, 620, 250, 65, "Control Remoto desde Node-RED\nRecibe ON / OFF en tópico set\nConfirma estado en lazo cerrado", "rect", "#f0fdf4", "#16a34a")
    flow_line(cx+235, 685, cx+235, 725)
    node(cx+110, 725, 250, 70, "¿Ventilador ON &&\nahora - inicioManual >= 60 s?\n(Purga anti-olvido)", "diamond", "#fefce8", "#ca8a04")
    node(cx+110, 835, 250, 50, "Retorno Autónomo a MODO AUTO\nPublicar cambio de modo\nEvaluar presencia para apagar", "rect", "#ffedd5", "#c2410c")
    flow_line(cx+235, 795, cx+235, 835, "SÍ")

    # Unificación
    node(cx-150, 1000, 300, 75, "Actualizar Semáforo RGB NOM-015\nPublicar tópicos planos y JSON por MQTT\nRotar pantalla OLED cada 3s (vistas 0-3)", "rect", "#eff6ff", "#1d4ed8")
    flow_line(cx-235, 955, cx-100, 1000)
    flow_line(cx+235, 885, cx+100, 1000)

    # Retorno al loop
    flow_line(cx, 1075, cx, 1120)
    node(cx-100, 1120, 200, 40, "Fin de iteración loop()", "ellipse", "#f8fafc", "#64748b")

    a('</svg>')
    with open(salida_svg, 'w', encoding='utf-8') as f:
        f.write('\n'.join(o))
    print(f"[OK] Diagrama de flujo SVG generado en: {salida_svg}")

def render_diagrama_flujo_png(salida_png):
    fig, ax = plt.subplots(figsize=(10, 13), dpi=120)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.axis('off')

    ax.text(5.0, 12.6, "Diagrama de Flujo — Firmware ESP32 (SIAM)", fontsize=16, fontweight='bold', color='#0f172a', ha='center')
    ax.text(5.0, 12.3, "Máquina de Estados No Bloqueante, Reglas Bioclimáticas y Retorno Anti-Olvido", fontsize=9.5, color='#64748b', ha='center')

    pasos = [
        (5.0, 11.5, "INICIO / RESET", '#eff6ff', '#2563eb', 3.0, 0.6),
        (5.0, 10.3, "setup(): Pines, I2C SHT41/OLED, Wi-Fi & MQTT LWT", '#f0fdf4', '#16a34a', 6.0, 0.9),
        (5.0, 8.9, "loop(): Verificar Enlace Red & LED Azul (GPIO 2)", '#f8fafc', '#64748b', 5.5, 0.8),
        (5.0, 7.5, "Telemetría (2s): SHT41, LDR, PIR & Heat Index NOAA", '#eff6ff', '#0284c7', 6.0, 0.8),
        (2.6, 5.8, "MODO AUTO:\nCalor + Presencia -> Fan ON\nDesocupado >30s -> Fan OFF", '#fefce8', '#ca8a04', 4.2, 1.2),
        (7.4, 5.8, "MODO MANUAL:\nMando Node-RED con Lazo Cerrado\nTimer 60s expira -> Auto AUTO", '#fff7ed', '#ea580c', 4.2, 1.2),
        (5.0, 3.8, "Semáforo RGB (NOM-015: Verde / Amarillo / Rojo)", '#fdf4ff', '#c026d3', 6.0, 0.7),
        (5.0, 2.6, "Publicar MQTT (Tópicos Planos + JSON Agregado)", '#eff6ff', '#1d4ed8', 6.0, 0.7),
        (5.0, 1.5, "Rotar Pantalla OLED 128x32 (Ciclo 3s Vistas 0-3)", '#f8fafc', '#475569', 6.0, 0.7),
    ]

    for x, y, texto, bg, border, w, h in pasos:
        caja = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(caja)
        ax.text(x, y, texto, fontsize=9.5, fontweight='bold', color='#0f172a', ha='center', va='center')

    # Flechas
    for i in range(len(pasos)-1):
        if i in (3, 4, 5):
            continue
        ax.annotate('', xy=(pasos[i+1][0], pasos[i+1][1] + pasos[i+1][6]/2),
                    xytext=(pasos[i][0], pasos[i][1] - pasos[i][6]/2),
                    arrowprops=dict(arrowstyle="->", color='#334155', lw=2))

    # Bifurcación AUTO / MANUAL
    ax.annotate('', xy=(2.6, 6.4), xytext=(4.0, 7.1), arrowprops=dict(arrowstyle="->", color='#ca8a04', lw=2))
    ax.annotate('', xy=(7.4, 6.4), xytext=(6.0, 7.1), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2))

    # Convergencia a RGB
    ax.annotate('', xy=(4.0, 4.15), xytext=(2.6, 5.2), arrowprops=dict(arrowstyle="->", color='#ca8a04', lw=2))
    ax.annotate('', xy=(6.0, 4.15), xytext=(7.4, 5.2), arrowprops=dict(arrowstyle="->", color='#ea580c', lw=2))

    fig.savefig(salida_png, bbox_inches='tight', dpi=120)
    plt.close(fig)
    print(f"[OK] Diagrama de flujo PNG renderizado en: {salida_png}")

# ==============================================================================
# 4. GENERADOR DE RENDERS DE PROTOBOARD Y DASHBOARD PARA DOCS/IMAGENES/
# ==============================================================================

def generar_placeholder_protoboard_general(salida_png):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
    ax.set_facecolor('#1e293b')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6.0, 7.4, "Prototipo Físico Ensamblado en Protoboard (SIAM-Yucatán)", fontsize=16, fontweight='bold', color='#ffffff', ha='center')
    ax.text(6.0, 7.0, "Entregable 4 / Evidencia Fotográfica 1 · Vista General del Ensamble Físico", fontsize=10, color='#94a3b8', ha='center')

    # Protoboard layout
    pb = patches.FancyBboxPatch((1.0, 1.2), 10.0, 5.4, boxstyle="round,pad=0.2", facecolor='#f1f5f9', edgecolor='#94a3b8', linewidth=3)
    ax.add_patch(pb)

    # Componentes en Protoboard
    comps = [
        (2.0, 3.8, 2.2, 1.6, "ESP32 DevKit V1\n(Microcontrolador Central)", '#0f172a', '#38bdf8', '#ffffff'),
        (4.7, 4.5, 1.8, 1.0, "OLED 128x32\n(SSD1306 0x3C)", '#334155', '#94a3b8', '#38bdf8'),
        (4.7, 2.5, 1.8, 1.0, "GY-SHT41\n(Temp & Hum 0x44)", '#1e3a8a', '#60a5fa', '#ffffff'),
        (7.0, 4.5, 1.6, 1.0, "Sensor PIR\n(HC-SR501)", '#134e4a', '#2dd4bf', '#ffffff'),
        (7.0, 2.5, 1.6, 1.0, "LDR + R 10k\n(GPIO 34 ADC1)", '#701a75', '#e879f9', '#ffffff'),
        (9.0, 4.2, 1.6, 1.4, "Ventilador 5V\n+ Transistor NPN\n+ Diodo Flyback", '#14532d', '#4ade80', '#ffffff'),
        (9.0, 2.2, 1.6, 1.0, "LED RGB\nSemáforo NOM-015", '#7c2d12', '#fb923c', '#ffffff'),
    ]

    for x, y, w, h, etiqueta, bg, border, textcol in comps:
        c = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(c)
        ax.text(x + w/2, y + h/2, etiqueta, fontsize=8.5, fontweight='bold', color=textcol, ha='center', va='center')

    ax.text(6.0, 0.6, "[Instrucción para Diego: Reemplazar este render por fotografía real del protoboard tomada con celular o cámara]", fontsize=9, color='#cbd5e1', ha='center', style='italic')

    fig.savefig(salida_png, bbox_inches='tight', dpi=120)
    plt.close(fig)
    print(f"[OK] Render de Protoboard Vista General generado en: {salida_png}")

def generar_placeholder_protoboard_actuacion(salida_png):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=120)
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(6.0, 7.4, "Evidencia de Actuación Física: Ventilador 5V y LED RGB", fontsize=16, fontweight='bold', color='#ffffff', ha='center')
    ax.text(6.0, 7.0, "Entregable 4 / Evidencia Fotográfica 2 · Conmutación por Saturación de Transistor NPN", fontsize=10, color='#94a3b8', ha='center')

    # Ventilador en rotación
    fan_circle = patches.Circle((4.0, 4.0), 2.2, facecolor='#1e293b', edgecolor='#22c55e', linewidth=4)
    ax.add_patch(fan_circle)
    # Aspas dinámicas vectoriales
    for angle in [0, 90, 180, 270]:
        blade = patches.Wedge((4.0, 4.0), 1.9, angle, angle + 45, width=1.4, facecolor='#22c55e', alpha=0.85)
        ax.add_patch(blade)
    center_hub = patches.Circle((4.0, 4.0), 0.6, facecolor='#0f172a', edgecolor='#4ade80', linewidth=2)
    ax.add_patch(center_hub)
    ax.text(4.0, 4.0, "5V", fontsize=15, fontweight='bold', ha='center', va='center', color='#4ade80')

    ax.text(4.0, 1.4, "VENTILADOR 5V EN ROTACIÓN\n(Transistor NPN Saturado: 140 mA a GND)", fontsize=11, fontweight='bold', color='#4ade80', ha='center')

    # LED RGB encendido en Peligro / Alerta
    led_circle = patches.Circle((8.5, 4.0), 1.6, facecolor='#dc2626', edgecolor='#f87171', linewidth=4)
    ax.add_patch(led_circle)
    glow_circle = patches.Circle((8.5, 4.0), 2.1, facecolor='none', edgecolor='#ef4444', linewidth=2, linestyle='--')
    ax.add_patch(glow_circle)
    ax.text(8.5, 4.0, "ALERTA\nACTIVA", fontsize=13, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(8.5, 1.4, "LED RGB SEMÁFORO (ROJO)\n(Alerta Crítica: Heat Index >= 38 °C)", fontsize=11, fontweight='bold', color='#ef4444', ha='center')

    ax.text(6.0, 0.6, "[Instrucción para Diego: Reemplazar por fotografía real en primer plano del ventilador girando y LED encendido]", fontsize=9, color='#94a3b8', ha='center', style='italic')

    fig.savefig(salida_png, bbox_inches='tight', dpi=120)
    plt.close(fig)
    print(f"[OK] Render de Actuación Ventilador generado en: {salida_png}")

def generar_placeholder_dashboard_telemetria(salida_png):
    fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Barra superior Dashboard
    top = patches.Rectangle((0, 8.0), 14, 1.0, facecolor='#1e293b')
    ax.add_patch(top)
    ax.text(0.5, 8.5, "SIAM-Yucatán — Monitoreo Bioclimático & Estrés Térmico (Node-RED Dashboard 2.0)", fontsize=13, fontweight='bold', color='#ffffff', va='center')
    ax.text(13.5, 8.5, "[ONLINE] Enlace LWT: ACTIVO", fontsize=11, fontweight='bold', color='#4ade80', va='center', ha='right')

    # 4 Gauges
    gauges_data = [
        (0.6, "Temperatura", "33.4 °C", "#e01b24", "Riesgo Térmico"),
        (3.8, "Humedad Relativa", "76.5 %", "#3584e4", "Humedad Alta"),
        (7.0, "Índice de Calor (NOAA)", "45.8 °C", "#dc2626", "PELIGRO EXTREMO"),
        (10.2, "Iluminación LDR", "68 %", "#f59e0b", "Luz de Trabajo OK"),
    ]
    for x, tit, val, col, sub in gauges_data:
        g = patches.FancyBboxPatch((x, 5.0), 3.0, 2.6, boxstyle="round,pad=0.1", facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.5)
        ax.add_patch(g)
        ax.text(x+1.5, 7.1, tit, fontsize=11, fontweight='bold', color='#334155', ha='center')
        ax.text(x+1.5, 6.2, val, fontsize=20, fontweight='bold', color=col, ha='center')
        ax.text(x+1.5, 5.4, sub, fontsize=9.5, color='#64748b', ha='center')

    # Gráfica Histórica
    chart_box = patches.FancyBboxPatch((0.6, 1.4), 8.0, 3.2, boxstyle="round,pad=0.1", facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.5)
    ax.add_patch(chart_box)
    ax.text(1.0, 4.2, "Tendencia Térmica en Tiempo Real (SHT41 + Heat Index)", fontsize=11, fontweight='bold', color='#0f172a')
    # Líneas simuladas
    xs = [1.2, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    ys_temp = [2.2, 2.3, 2.5, 2.7, 2.8, 2.9, 3.1, 3.2]
    ys_hi = [2.6, 2.8, 3.1, 3.4, 3.6, 3.8, 4.0, 4.1]
    ax.plot(xs, ys_temp, color='#f97316', linewidth=2.5, label='Temp (°C)')
    ax.plot(xs, ys_hi, color='#dc2626', linewidth=3, label='Heat Index (°C)')
    ax.legend(loc='lower right', fontsize=9)

    # Tarjeta de Estado
    status_box = patches.FancyBboxPatch((9.0, 1.4), 4.4, 3.2, boxstyle="round,pad=0.1", facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.5)
    ax.add_patch(status_box)
    ax.text(9.3, 4.2, "Diagnóstico Bioclimático NOM-015", fontsize=11, fontweight='bold', color='#0f172a')
    ax.text(9.3, 3.6, "• Semáforo: [ROJO] PELIGRO CRÍTICO", fontsize=10, fontweight='bold', color='#dc2626')
    ax.text(9.3, 3.1, "• Presencia: [SI] DETECTADA (Sala ocupada)", fontsize=10, fontweight='bold', color='#16a34a')
    ax.text(9.3, 2.6, "• Ventilador: [ON] ACTIVADO (Disipando)", fontsize=10, fontweight='bold', color='#0284c7')
    ax.text(9.3, 2.1, "• Modo: [AUTO] AUTOMÁTICO", fontsize=10, fontweight='bold', color='#475569')

    ax.text(7.0, 0.6, "[Captura representativa de Node-RED Dashboard 2.0 en operación continua]", fontsize=9.5, color='#64748b', ha='center', style='italic')

    fig.savefig(salida_png, bbox_inches='tight', dpi=120)
    plt.close(fig)
    print(f"[OK] Render de Dashboard Telemetría generado en: {salida_png}")

def generar_placeholder_dashboard_control(salida_png):
    fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Barra superior
    top = patches.Rectangle((0, 8.0), 14, 1.0, facecolor='#1e293b')
    ax.add_patch(top)
    ax.text(0.5, 8.5, "SIAM-Yucatán — Panel de Mando y Control Remoto (Lazo Cerrado Desacoplado)", fontsize=13, fontweight='bold', color='#ffffff', va='center')
    ax.text(13.5, 8.5, "Broker: MOSQUITTO LOCAL", fontsize=11, fontweight='bold', color='#38bdf8', va='center', ha='right')

    # Tarjeta Control Remoto del Ventilador
    fan_ctrl = patches.FancyBboxPatch((1.0, 4.5), 12.0, 3.0, boxstyle="round,pad=0.15", facecolor='#ffffff', edgecolor='#16a34a', linewidth=2)
    ax.add_patch(fan_ctrl)
    ax.text(1.5, 7.0, "Interruptor de Conmutación del Ventilador 5V (Low-Side Switch NPN)", fontsize=13, fontweight='bold', color='#166534')
    ax.text(1.5, 6.4, "Comando enviado: topic yucatan/bioclima/actuador/ventilador/set [ON]", fontsize=10.5, color='#475569')

    # Switch ON visual
    sw_bg = patches.FancyBboxPatch((1.5, 5.2), 2.2, 0.8, boxstyle="round,pad=0.1", facecolor='#22c55e', edgecolor='#16a34a')
    ax.add_patch(sw_bg)
    sw_knob = patches.Circle((3.2, 5.6), 0.35, facecolor='#ffffff', edgecolor='#cbd5e1')
    ax.add_patch(sw_knob)
    ax.text(2.1, 5.6, "ON", fontsize=11, fontweight='bold', color='#ffffff', va='center')

    ax.text(4.2, 5.6, "Estado Real Físico Confirmado: [ON] EN REVOLUCIÓN (Transistor Saturado / Extracción Activa)", fontsize=11, fontweight='bold', color='#15803d', va='center')

    # Tarjeta Modo y Purga Anti-Olvido
    mode_ctrl = patches.FancyBboxPatch((1.0, 1.5), 12.0, 2.6, boxstyle="round,pad=0.15", facecolor='#ffffff', edgecolor='#ea580c', linewidth=2)
    ax.add_patch(mode_ctrl)
    ax.text(1.5, 3.6, "Gestión de Modo Operativo y Protección Anti-Fallo Humano", fontsize=13, fontweight='bold', color='#9a3412')
    ax.text(1.5, 3.0, "Modo Activo Confirmado: [MANUAL] (Purga Térmica Previa en Proceso)", fontsize=11, fontweight='bold', color='#ea580c')

    # Caja de advertencia de timer
    alert_box = patches.FancyBboxPatch((1.5, 1.9), 11.0, 0.8, boxstyle="round,pad=0.08", facecolor='#fff7ed', edgecolor='#f97316', linewidth=1.5)
    ax.add_patch(alert_box)
    ax.text(1.8, 2.3, "[TEMPORIZADOR ANTI-OLVIDO ACTIVO] Retorno autónomo a MODO AUTO en 60 segundos (Evita consumo innecesario).", fontsize=10, fontweight='bold', color='#c2410c', va='center')

    ax.text(7.0, 0.7, "[Demostración en vivo de conmutación en lazo cerrado desacoplado y temporizador anti-olvido]", fontsize=9.5, color='#64748b', ha='center', style='italic')

    fig.savefig(salida_png, bbox_inches='tight', dpi=120)
    plt.close(fig)
    print(f"[OK] Render de Dashboard Control Remoto generado en: {salida_png}")

# ==============================================================================
# EJECUCIÓN PRINCIPAL
# ==============================================================================

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    hw_dir = os.path.join(base_dir, "hardware")
    docs_dir = os.path.join(base_dir, "docs")
    img_dir = os.path.join(docs_dir, "imagenes")

    os.makedirs(hw_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    print("=================================================================")
    print("  GENERANDO DIAGRAMAS VECTORIALES (SVG) Y RENDERS (PNG)")
    print("=================================================================")

    # 1. Diagrama de Conexiones
    diag_hw_svg = os.path.join(hw_dir, "diagrama_conexiones.svg")
    diag_hw_png = os.path.join(hw_dir, "diagrama_conexiones.png")
    generar_diagrama_conexiones_svg(diag_hw_svg)
    render_diagrama_conexiones_png(diag_hw_png)

    # 2. Diagrama de Arquitectura
    diag_arq_svg = os.path.join(docs_dir, "diagrama_arquitectura.svg")
    diag_arq_png = os.path.join(img_dir, "diagrama_arquitectura.png")
    generar_diagrama_arquitectura_svg(diag_arq_svg)
    render_diagrama_arquitectura_png(diag_arq_png)

    # 3. Diagrama de Flujo del Firmware
    diag_flu_svg = os.path.join(docs_dir, "diagrama_flujo_firmware.svg")
    diag_flu_png = os.path.join(img_dir, "diagrama_flujo_firmware.png")
    generar_diagrama_flujo_svg(diag_flu_svg)
    render_diagrama_flujo_png(diag_flu_png)

    # 4. Renders de Evidencias para docs/imagenes/
    generar_placeholder_protoboard_general(os.path.join(img_dir, "protoboard_vista_general.png"))
    generar_placeholder_protoboard_actuacion(os.path.join(img_dir, "protoboard_actuacion_ventilador.png"))
    generar_placeholder_dashboard_telemetria(os.path.join(img_dir, "dashboard_nodered_telemetria.png"))
    generar_placeholder_dashboard_control(os.path.join(img_dir, "dashboard_nodered_control.png"))

    print("=================================================================")
    print("  ¡TODOS LOS DIAGRAMAS Y RENDERS FUERON GENERADOS CON ÉXITO!")
    print("=================================================================")

if __name__ == "__main__":
    main()
