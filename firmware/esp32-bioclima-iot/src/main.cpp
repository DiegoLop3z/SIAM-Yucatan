#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_SHT4x.h>

#include "config.h"
#include "heat_index.h"

// ============================================================================
//  PROYECTO INTEGRADOR UNIDAD 2: SIAM-Yucatán
//  Sistema Inteligente de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática
//  Universidad Politécnica de Yucatán (UPY)
//  Docente: M.I. Javier Poot
//  Autores: Diego López Pérez (@DiegoLop3z) & Arturo Heredia Martín (@arturoherediam)
// ============================================================================

enum ModoOperacion {
    MODO_AUTO = 0,
    MODO_MANUAL = 1
};

// ---------- Instancias de Hardware ----------
Adafruit_SHT4x sht4 = Adafruit_SHT4x();
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// ---------- Estado de Sensores y Variables Bioclimáticas ----------
bool sht41Disponible = false;
bool oledDisponible = false;

float temperaturaActual = 28.5f;
float humedadActual = 65.0f;
float indiceCalorActual = 30.2f;
NivelAlertaTermica alertaActual = ALERTA_PRECAUCION;

int ldrCrudo = 0;
int ldrPorcentaje = 50;

bool presenciaActual = false;
unsigned long tiempoUltimaPresencia = 0;

// ---------- Estado de Actuadores y Control ----------
bool ventiladorEncendido = false;
ModoOperacion modoActual = MODO_AUTO;
float umbralTemperatura = UMBRAL_TEMP_DEFAULT;
float umbralHeatIndex = UMBRAL_HEAT_INDEX_DEFAULT;

// Temporizador anti-olvido (Purga manual)
unsigned long tiempoInicioManual = 0;

// ---------- Temporizadores millis() ----------
unsigned long ultimaTelemetriaMs = 0;
unsigned long ultimoCambioOledMs = 0;
unsigned long ultimoIntentoWiFiMs = 0;
unsigned long ultimoIntentoMqttMs = 0;
unsigned long ultimoParpadeoLedRedMs = 0;
unsigned long ultimoParpadeoAlertaMs = 0;

uint8_t paginaOled = 0;
bool estadoLedRed = false;
bool estadoLedAlertaPeligro = false;
bool wifiReportado = false;

// ============================================================================
//  Control de Actuadores Físicos
// ============================================================================

void aplicarVentilador(bool encender) {
    ventiladorEncendido = encender;
    // Transistor NPN Low-Side Switch: HIGH satura la base y conecta a GND
    digitalWrite(PIN_FAN_SWITCH, encender ? HIGH : LOW);

    Serial.print("[VENTILADOR] Estado físico conmutado a: ");
    Serial.println(encender ? "ON (Saturación NPN)" : "OFF (Corte NPN)");

    // Confirmación desacoplada en lazo cerrado por MQTT
    if (mqttClient.connected()) {
        mqttClient.publish(TOPIC_FAN_ESTADO, encender ? "ON" : "OFF", true);
    }
}

void establecerModo(ModoOperacion nuevoModo) {
    modoActual = nuevoModo;
    if (modoActual == MODO_MANUAL) {
        tiempoInicioManual = millis();
        Serial.println("[MODO] Cambiado a MANUAL. Temporizador de purga anti-olvido iniciado (60 s).");
    } else {
        Serial.println("[MODO] Cambiado a AUTO. Control delegado a sensores térmicos y de presencia.");
    }

    if (mqttClient.connected()) {
        mqttClient.publish(TOPIC_MODO_ESTADO, modoActual == MODO_AUTO ? "AUTO" : "MANUAL", true);
    }
}

void actualizarSemaforoRgb(NivelAlertaTermica nivel, unsigned long ahora) {
    switch (nivel) {
        case ALERTA_CONFORT:
            // Verde fijo
            digitalWrite(PIN_LED_RGB_R, LOW);
            digitalWrite(PIN_LED_RGB_G, HIGH);
            digitalWrite(PIN_LED_RGB_B, LOW);
            break;

        case ALERTA_PRECAUCION:
            // Amarillo fijo (Rojo + Verde)
            digitalWrite(PIN_LED_RGB_R, HIGH);
            digitalWrite(PIN_LED_RGB_G, HIGH);
            digitalWrite(PIN_LED_RGB_B, LOW);
            break;

        case ALERTA_PELIGRO:
            // Rojo con parpadeo preventivo de advertencia cada 500 ms
            if (ahora - ultimoParpadeoAlertaMs >= 500) {
                ultimoParpadeoAlertaMs = ahora;
                estadoLedAlertaPeligro = !estadoLedAlertaPeligro;
            }
            digitalWrite(PIN_LED_RGB_R, estadoLedAlertaPeligro ? HIGH : LOW);
            digitalWrite(PIN_LED_RGB_G, LOW);
            digitalWrite(PIN_LED_RGB_B, LOW);
            break;
    }
}

void actualizarLedRed(unsigned long ahora) {
    bool redConectada = (WiFi.status() == WL_CONNECTED) && mqttClient.connected();

    if (!redConectada) {
        // Parpadeo rápido (200 ms) indicando reconexión / búsqueda de red
        if (ahora - ultimoParpadeoLedRedMs >= 200) {
            ultimoParpadeoLedRedMs = ahora;
            estadoLedRed = !estadoLedRed;
            digitalWrite(PIN_LED_NETWORK, estadoLedRed ? HIGH : LOW);
        }
    } else {
        // Enlace activo y saludable: Encendido continuo / latido sutil
        digitalWrite(PIN_LED_NETWORK, HIGH);
    }
}

// ============================================================================
//  Visualización en Pantalla OLED SSD1306 (128x32)
// ============================================================================

void actualizarPantallaOled() {
    if (!oledDisponible) return;

    display.clearDisplay();

    // Barra de encabezado fija (Modo a la izquierda, Ventilador a la derecha)
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print(modoActual == MODO_AUTO ? "M:AUTO" : "M:MAN");

    const char* txtFan = ventiladorEncendido ? "FAN:ON" : "FAN:OFF";
    int anchoFan = strlen(txtFan) * 6;
    display.setCursor(SCREEN_WIDTH - anchoFan, 0);
    display.print(txtFan);

    display.drawLine(0, 9, SCREEN_WIDTH, 9, SSD1306_WHITE);

    // Contenido dinámico rotativo
    display.setCursor(0, 14);
    switch (paginaOled) {
        case 0: // Temperatura y Humedad
            display.setTextSize(2);
            display.print(temperaturaActual, 1);
            display.setTextSize(1);
            display.print("C  ");
            display.setTextSize(2);
            display.print(humedadActual, 0);
            display.setTextSize(1);
            display.print("%");
            break;

        case 1: // Sensación Térmica (Heat Index) y NOM-015
            display.setTextSize(1);
            display.print("Heat Index: ");
            display.print(indiceCalorActual, 1);
            display.println(" C");
            display.setCursor(0, 24);
            display.print("Riesgo: [");
            display.print(obtenerNombreAlerta(alertaActual));
            display.print("]");
            break;

        case 2: // Iluminación LDR y Sensor PIR
            display.setTextSize(1);
            display.print("Luz: ");
            display.print(ldrPorcentaje);
            display.println("%");
            display.setCursor(0, 24);
            display.print("Presencia: ");
            display.print(presenciaActual ? "DETECTADA" : "DESPEJADO");
            break;

        case 3: // Estado de Red y Broker MQTT
            display.setTextSize(1);
            if (WiFi.status() == WL_CONNECTED) {
                display.print("IP: ");
                display.println(WiFi.localIP().toString());
            } else {
                display.println("Wi-Fi: DESCONECTADO");
            }
            display.setCursor(0, 24);
            display.print("MQTT: ");
            display.print(mqttClient.connected() ? "SINCRONIZADO" : "RECONECTANDO");
            break;
    }

    display.display();
}

// ============================================================================
//  Adquisición de Sensores y Algoritmo Bioclimático
// ============================================================================

void leerSensores() {
    // 1. Sensor SHT41 (I2C)
    if (sht41Disponible) {
        sensors_event_t humEvent, tempEvent;
        sht4.getEvent(&humEvent, &tempEvent);
        if (!isnan(tempEvent.temperature) && !isnan(humEvent.relative_humidity)) {
            temperaturaActual = tempEvent.temperature;
            humedadActual = humEvent.relative_humidity;
        }
    }

    // 2. Cálculo de Sensación Térmica (Heat Index NOAA) y NOM-015
    indiceCalorActual = calcularIndiceCalor(temperaturaActual, humedadActual);
    alertaActual = evaluarNivelAlerta(indiceCalorActual);

    // 3. Sensor Fotocelda LDR (ADC1_CH6)
    ldrCrudo = analogRead(PIN_LDR_ADC);
    // Divisor 3.3V -> LDR -> ADC -> 10k -> GND: mayor luz = menor resistencia LDR = mayor voltaje
    ldrPorcentaje = map(ldrCrudo, 0, 4095, 0, 100);
    ldrPorcentaje = constrain(ldrPorcentaje, 0, 100);

    // 4. Sensor PIR (Digital In)
    presenciaActual = (digitalRead(PIN_PIR_DIGITAL) == HIGH);
    if (presenciaActual) {
        tiempoUltimaPresencia = millis();
    }
}

// ============================================================================
//  Reglas de Automatización y Control Anti-Olvido
// ============================================================================

void evaluarAutomatizaciones(unsigned long ahora) {
    if (modoActual == MODO_AUTO) {
        // Regla 1: Mitigación Térmica Forzada condicionada a Presencia Humana
        bool condicionTermicaActiva = (indiceCalorActual >= umbralHeatIndex) || 
                                     (temperaturaActual >= umbralTemperatura);

        if (condicionTermicaActiva && presenciaActual) {
            if (!ventiladorEncendido) {
                Serial.println("[AUTO] Condición de calor y presencia detectada. Activando ventilador.");
                aplicarVentilador(true);
            }
        } 
        else if (ventiladorEncendido) {
            // Condición de apagado A: Desocupación por más de TIMEOUT_DESOCUPACION_MS (30 s)
            bool tiempoDesocupadoExcedido = (!presenciaActual) && 
                                            ((ahora - tiempoUltimaPresencia) >= TIMEOUT_DESOCUPACION_MS);

            // Condición de apagado B: Histéresis térmica (ambiente refrescado)
            bool ambienteRefrescado = (temperaturaActual < (umbralTemperatura - HISTERESIS_TEMP_OFFSET)) &&
                                      (indiceCalorActual < UMBRAL_HEAT_INDEX_APAGADO);

            if (tiempoDesocupadoExcedido) {
                Serial.println("[AUTO] Espacio desocupado por > 30 s. Apagando ventilador (Ahorro energético).");
                aplicarVentilador(false);
            } else if (ambienteRefrescado) {
                Serial.println("[AUTO] Temperatura e índice de calor bajo umbral de histéresis. Apagando ventilador.");
                aplicarVentilador(false);
            }
        }
    } 
    else if (modoActual == MODO_MANUAL) {
        // Regla 3: Protección Anti-Fallo Humano por Olvido
        // Retorno autónomo a modo AUTO tras DURACION_MODO_MANUAL_MS (60 s en demo / 30 min en campo)
        if ((ahora - tiempoInicioManual) >= DURACION_MODO_MANUAL_MS) {
            Serial.println("[MANUAL] Expiró el temporizador de purga (60 s). Retorno autónomo a modo AUTO.");
            establecerModo(MODO_AUTO);
            // Al regresar a AUTO, reevaluamos de inmediato la condición ambiental
            bool condicionTermicaActiva = (indiceCalorActual >= umbralHeatIndex) || 
                                         (temperaturaActual >= umbralTemperatura);
            if (!(condicionTermicaActiva && presenciaActual)) {
                aplicarVentilador(false);
            }
        }
    }

    // Regla 2: Semáforo Bioclimático en LED RGB según estrés térmico
    actualizarSemaforoRgb(alertaActual, ahora);
}

// ============================================================================
//  Publicación de Telemetría por MQTT
// ============================================================================

void publicarTelemetria() {
    if (!mqttClient.connected()) return;

    // 1. Tópicos individuales planos para gauges y componentes rápidos de Node-RED
    mqttClient.publish(TOPIC_TEMP, String(temperaturaActual, 1).c_str());
    mqttClient.publish(TOPIC_HUM, String(humedadActual, 1).c_str());
    mqttClient.publish(TOPIC_HEAT_INDEX, String(indiceCalorActual, 1).c_str());
    mqttClient.publish(TOPIC_LUZ, String(ldrPorcentaje).c_str());
    mqttClient.publish(TOPIC_PRESENCIA, presenciaActual ? "1" : "0");
    mqttClient.publish(TOPIC_FAN_ESTADO, ventiladorEncendido ? "ON" : "OFF", true);
    mqttClient.publish(TOPIC_MODO_ESTADO, modoActual == MODO_AUTO ? "AUTO" : "MANUAL", true);

    // 2. Payload unificado en JSON para histórico, base de datos y procesamiento global
    JsonDocument doc;
    doc["temp"] = round(temperaturaActual * 10.0f) / 10.0f;
    doc["hum"] = round(humedadActual * 10.0f) / 10.0f;
    doc["hi"] = round(indiceCalorActual * 10.0f) / 10.0f;
    doc["luz"] = ldrPorcentaje;
    doc["pres"] = presenciaActual ? 1 : 0;
    doc["fan"] = ventiladorEncendido ? 1 : 0;
    doc["modo"] = (modoActual == MODO_AUTO) ? "AUTO" : "MANUAL";
    doc["alerta"] = obtenerNombreAlerta(alertaActual);

    char jsonBuffer[384];
    size_t n = serializeJson(doc, jsonBuffer, sizeof(jsonBuffer));
    mqttClient.publish(TOPIC_TELEMETRIA, (const uint8_t*)jsonBuffer, n, false);

    Serial.print("[MQTT PUB] ");
    Serial.println(jsonBuffer);
}

// ============================================================================
//  Callback MQTT (Recepción de Comandos desde Node-RED)
// ============================================================================

void callbackMqtt(char* topic, byte* payload, unsigned int length) {
    char mensaje[32];
    unsigned int len = length < sizeof(mensaje) - 1 ? length : sizeof(mensaje) - 1;
    for (unsigned int i = 0; i < len; i++) {
        mensaje[i] = toupper((char)payload[i]);
    }
    mensaje[len] = '\0';

    // Limpieza de espacios y retornos
    while (len > 0 && isspace((unsigned char)mensaje[len - 1])) {
        mensaje[--len] = '\0';
    }

    Serial.print("[MQTT SUB] [");
    Serial.print(topic);
    Serial.print("] Recibido: ");
    Serial.println(mensaje);

    // Comando 1: Control Remoto del Ventilador
    if (strcmp(topic, TOPIC_FAN_SET) == 0) {
        if (strcmp(mensaje, "ON") == 0) {
            // Si el usuario fuerza ON desde Node-RED, conmutamos a MANUAL con timer
            if (modoActual == MODO_AUTO) {
                establecerModo(MODO_MANUAL);
            } else {
                tiempoInicioManual = millis(); // reinicia timer de purga
            }
            aplicarVentilador(true);
        } else if (strcmp(mensaje, "OFF") == 0) {
            aplicarVentilador(false);
        }
    }
    // Comando 2: Cambio de Modo (AUTO / MANUAL)
    else if (strcmp(topic, TOPIC_MODO_SET) == 0) {
        if (strcmp(mensaje, "AUTO") == 0) {
            establecerModo(MODO_AUTO);
        } else if (strcmp(mensaje, "MANUAL") == 0) {
            establecerModo(MODO_MANUAL);
        }
    }
    // Comando 3: Reconfiguración Dinámica de Umbral de Temperatura
    else if (strcmp(topic, TOPIC_CONFIG_UMBRAL) == 0) {
        float nuevoUmbral = atof(mensaje);
        if (nuevoUmbral >= 20.0f && nuevoUmbral <= 45.0f) {
            umbralTemperatura = nuevoUmbral;
            Serial.print("[CONFIG] Nuevo umbral de temperatura configurado: ");
            Serial.print(umbralTemperatura);
            Serial.println(" °C");
        }
    }
}

// ============================================================================
//  Gestión de Red y Conectividad MQTT no bloqueante
// ============================================================================

bool conectarMqtt() {
    Serial.print("[MQTT] Conectando a broker Mosquitto en ");
    Serial.print(MQTT_SERVER);
    Serial.print(":");
    Serial.print(MQTT_PORT);
    Serial.print("...");

    // Configuración LWT: En caso de apagón o pérdida de enlace, el broker publica 'offline'
    bool ok = mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD,
                                 TOPIC_STATUS, 0, true, "offline");

    if (ok) {
        Serial.println(" ¡Conectado con éxito!");
        // Anunciar estado activo retained
        mqttClient.publish(TOPIC_STATUS, "online", true);

        // Publicar estados iniciales
        mqttClient.publish(TOPIC_FAN_ESTADO, ventiladorEncendido ? "ON" : "OFF", true);
        mqttClient.publish(TOPIC_MODO_ESTADO, modoActual == MODO_AUTO ? "AUTO" : "MANUAL", true);

        // Suscribirse a los tópicos de mando remoto y configuración
        mqttClient.subscribe(TOPIC_FAN_SET, 1);
        mqttClient.subscribe(TOPIC_MODO_SET, 1);
        mqttClient.subscribe(TOPIC_CONFIG_UMBRAL, 1);
        return true;
    } else {
        Serial.print(" Error de conexión, rc=");
        Serial.println(mqttClient.state());
        return false;
    }
}

void mantenerConexiones(unsigned long ahora) {
    // 1. Verificación de Wi-Fi
    if (WiFi.status() != WL_CONNECTED) {
        wifiReportado = false;
        if (ahora - ultimoIntentoWiFiMs >= INTERVALO_REINTENTO_WIFI_MS) {
            ultimoIntentoWiFiMs = ahora;
            Serial.println("[WIFI] Reconectando a punto de acceso...");
            WiFi.disconnect();
            WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        }
        return; // Sin Wi-Fi no es posible intentar MQTT
    }

    if (!wifiReportado) {
        wifiReportado = true;
        Serial.println("[WIFI] Conexión establecida.");
        Serial.print("[WIFI] Dirección IP local: ");
        Serial.println(WiFi.localIP());
    }

    // 2. Verificación de MQTT
    if (!mqttClient.connected()) {
        if (ahora - ultimoIntentoMqttMs >= INTERVALO_REINTENTO_MQTT_MS) {
            ultimoIntentoMqttMs = ahora;
            conectarMqtt();
        }
    } else {
        mqttClient.loop();
    }
}

// ============================================================================
//  Setup y Bucle Principal Loop
// ============================================================================

void setup() {
    Serial.begin(115200);
    delay(200);

    Serial.println("\n========================================================");
    Serial.println("  SIAM-Yucatán — Sistema IoT Integrador (Unidad 2)");
    Serial.println("  Autores: Diego López Pérez & Arturo Heredia Martín");
    Serial.println("  Docente: M.I. Javier Poot — UPY 2026");
    Serial.println("========================================================");

    // Inicialización de Pines
    pinMode(PIN_FAN_SWITCH, OUTPUT);
    digitalWrite(PIN_FAN_SWITCH, LOW);

    pinMode(PIN_LED_RGB_R, OUTPUT);
    pinMode(PIN_LED_RGB_G, OUTPUT);
    pinMode(PIN_LED_RGB_B, OUTPUT);
    digitalWrite(PIN_LED_RGB_R, LOW);
    digitalWrite(PIN_LED_RGB_G, LOW);
    digitalWrite(PIN_LED_RGB_B, LOW);

    pinMode(PIN_LED_NETWORK, OUTPUT);
    digitalWrite(PIN_LED_NETWORK, LOW);

    pinMode(PIN_LDR_ADC, INPUT);
    pinMode(PIN_PIR_DIGITAL, INPUT);

    // Inicialización I2C
    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);

    // Inicialización OLED SSD1306 (0x3C)
    if (display.begin(SSD1306_SWITCHCAPVCC, OLED_I2C_ADDR)) {
        oledDisponible = true;
        display.clearDisplay();
        display.setTextColor(SSD1306_WHITE);
        display.setTextSize(1);
        display.setCursor(10, 8);
        display.println("SIAM - YUCATAN");
        display.setCursor(10, 20);
        display.println("Iniciando...");
        display.display();
        Serial.println("[I2C] Pantalla OLED SSD1306 detectada en 0x3C.");
    } else {
        Serial.println("[WARN] No se detectó la pantalla OLED SSD1306 en 0x3C.");
    }

    // Inicialización SHT41 (0x44)
    if (sht4.begin(&Wire)) {
        sht41Disponible = true;
        sht4.setPrecision(SHT4X_HIGH_PRECISION);
        sht4.setHeater(SHT4X_NO_HEATER);
        Serial.println("[I2C] Sensor Sensirion SHT41 detectado en 0x44.");
    } else {
        Serial.println("[WARN] Sensor SHT41 no detectado en 0x44. Modo de simulación/prueba activo.");
    }

    // Configuración Wi-Fi
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("[WIFI] Intentando conectar a: ");
    Serial.println(WIFI_SSID);

    // Configuración MQTT
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
    mqttClient.setCallback(callbackMqtt);
    mqttClient.setBufferSize(512);

    tiempoUltimaPresencia = millis();
}

void loop() {
    unsigned long ahora = millis();

    // 1. Mantenimiento de Conexiones de Red y Señalización Bioclimática
    mantenerConexiones(ahora);
    actualizarLedRed(ahora);
    actualizarSemaforoRgb(alertaActual, ahora);

    // 2. Ciclo de Lectura, Automatización y Telemetría cada 2000 ms
    if (ahora - ultimaTelemetriaMs >= INTERVALO_TELEMETRIA_MS) {
        ultimaTelemetriaMs = ahora;
        leerSensores();
        evaluarAutomatizaciones(ahora);
        publicarTelemetria();
    }

    // 3. Rotación de Pantallas en OLED cada 3000 ms
    if (ahora - ultimoCambioOledMs >= INTERVALO_OLED_ROTACION_MS) {
        ultimoCambioOledMs = ahora;
        paginaOled = (paginaOled + 1) % 4;
        actualizarPantallaOled();
    }
}
