# Issue #1: [HW] Armado Físico del Hardware en Protoboard, Pruebas de Banco y Registro Fotográfico

- **Asignado a:** Diego López Pérez ([`@DiegoLop3z`](https://github.com/DiegoLop3z))
- **Copiloto IA:** Gemini
- **Etiquetas:** `hardware`, `protoboard`, `etapa-npn`, `evidencias`, `banco-pruebas`

---

## Descripción del Trabajo
Armar, cablear y verificar exhaustivamente el circuito en la protoboard de 830 puntos, asegurando el cumplimiento estricto del diagrama electrónico y el mapa de conexiones (`hardware/hardware_conexion.md`), así como realizar las pruebas de banco y captura de fotografías físicas reales:

### Puntos Específicos de Inspección:
1. **Bus I²C Compartido (3.3V):** Confirmar que el sensor SHT41 (`0x44`) y la pantalla OLED SSD1306 (`0x3C`) compartan `GPIO 21` (SDA) y `GPIO 22` (SCL) sin interferencias.
2. **Entradas Analógica y Digital:** Confirmar que la fotocelda LDR esté conectada a `GPIO 34` (`ADC1_CH6`) con su divisor resistivo de 10 kΩ a tierra, y que el sensor PIR entregue su pulso digital en `GPIO 35` alimentado a 5V (VIN).
3. **Etapa de Potencia NPN (Ventilador 5V):**
   - Base del transistor NPN (2N2222A) conectada a `GPIO 23` a través de un resistor de $1\,\text{k}\Omega$.
   - Colector conectado al borne negativo del mini ventilador y al ánodo del diodo flyback (1N4001).
   - Emisor conectado firmemente a la línea de tierra común (GND).
   - Borne positivo del ventilador y cátodo del diodo flyback conectados a +5V (VIN).
4. **Semáforo Bioclimático LED RGB:** Pines `GPIO 25, 26, 27` conectados a los ánodos R, G, B con 3 resistores limitadores de $220\,\Omega$ y cátodo común a GND.

---

## Criterios de Aceptación (Definition of Done - DoD)
- [ ] Prueba de continuidad con multímetro: línea de tierra común verificada en todos los módulos.
- [ ] Prueba de no-cortocircuito entre 3.3V/5V y GND superada satisfactoriamente.
- [ ] Escáner I²C confirma detección de direcciones `0x3C` (OLED) y `0x44` (SHT41).
- [ ] Prueba de conmutación: al aplicar nivel `HIGH` en `GPIO 23`, el transistor satura y el ventilador enciende con fuerza.
- [ ] Fotografía 1 tomada y guardada en `docs/imagenes/protoboard_vista_general.png` (ensamble completo etiquetado).
- [ ] Fotografía 2 tomada y guardada en `docs/imagenes/protoboard_actuacion_ventilador.png` (ventilador girando y LED RGB encendido).
