#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ============================================================================
//  Configuración General del Proyecto SIAM-Yucatán
//  Sistema IoT de Monitoreo Ambiental, Estrés Térmico y Mitigación Bioclimática
//  Autores: Diego López Pérez (@DiegoLop3z) & Arturo Heredia Martín (@arturoherediam)
//  Institución: Universidad Politécnica de Yucatán (UPY)
// ============================================================================

// ---------- Asignación de Pines Físicos ----------
// Bus I2C Compartido
#define PIN_I2C_SDA             21
#define PIN_I2C_SCL             22
#define SHT41_I2C_ADDR          0x44
#define OLED_I2C_ADDR           0x3C
#define SCREEN_WIDTH            128
#define SCREEN_HEIGHT           32

// Entradas Analógicas y Digitales
#define PIN_LDR_ADC             34    // ADC1_CH6 (Seguro con Wi-Fi activo)
#define PIN_PIR_DIGITAL         35    // Entrada digital exclusiva de presencia

// Actuadores e Indicadores
#define PIN_FAN_SWITCH          23    // Salida para etapa Low-Side Switch transistor NPN
#define PIN_LED_RGB_R           25    // LED RGB Cátodo común - Canal Rojo
#define PIN_LED_RGB_G           26    // LED RGB Cátodo común - Canal Verde
#define PIN_LED_RGB_B           27    // LED RGB Cátodo común - Canal Azul
#define PIN_LED_NETWORK         2     // LED azul integrado en placa ESP32 (Diagnóstico de red)

// ---------- Parámetros de Red y Broker MQTT ----------
// Las credenciales viven solo en include/secrets.h (ignorado por git).
// Sin ese archivo la compilación se detiene con un mensaje claro, en lugar de
// flashear credenciales de ejemplo que nunca conectarían.
#if __has_include("secrets.h")
    #include "secrets.h"
#else
    #error "Falta el archivo include/secrets.h; configure las credenciales mediante el entorno de compilación."
#endif

#ifndef MQTT_PORT
    #define MQTT_PORT           1883
#endif

#define MQTT_CLIENT_ID          "esp32-bioclima-siam"
#define MQTT_KEEPALIVE_S        15

// ---------- Tópicos MQTT (Jerarquía yucatan/bioclima/...) ----------
// Publicación (ESP32 -> Broker / Node-RED)
#define TOPIC_TELEMETRIA        "yucatan/bioclima/telemetria"
#define TOPIC_TEMP              "yucatan/bioclima/sensor/temperatura"
#define TOPIC_HUM               "yucatan/bioclima/sensor/humedad"
#define TOPIC_HEAT_INDEX        "yucatan/bioclima/sensor/indice_calor"
#define TOPIC_LUZ               "yucatan/bioclima/sensor/luz"
#define TOPIC_PRESENCIA         "yucatan/bioclima/sensor/presencia"
#define TOPIC_FAN_ESTADO        "yucatan/bioclima/actuador/ventilador/estado"
#define TOPIC_MODO_ESTADO       "yucatan/bioclima/actuador/modo/estado"
#define TOPIC_STATUS            "yucatan/bioclima/status" // LWT (online / offline)

// Suscripción (Node-RED -> ESP32)
#define TOPIC_FAN_SET           "yucatan/bioclima/actuador/ventilador/set"
#define TOPIC_MODO_SET          "yucatan/bioclima/actuador/modo/set"
#define TOPIC_CONFIG_UMBRAL     "yucatan/bioclima/config/umbral_temp"

// ---------- Intervalos de Tiempo y Automatización (Milisegundos) ----------
#define INTERVALO_TELEMETRIA_MS      2000    // Lectura y publicación cada 2 segundos
#define INTERVALO_OLED_ROTACION_MS   3000    // Ciclo de vistas en pantalla OLED cada 3 segundos
#define INTERVALO_REINTENTO_WIFI_MS  5000    // Reintento no bloqueante de conexión Wi-Fi
#define INTERVALO_REINTENTO_MQTT_MS  3000    // Reintento no bloqueante de conexión MQTT

// Reglas de automatización y protección anti-olvido
#define TIMEOUT_DESOCUPACION_MS      30000   // 30 s sin ocupación -> apagar ventilador en AUTO
#define DURACION_MODO_MANUAL_MS      60000   // 60 s de purga escolar -> retorno autónomo a AUTO
#define UMBRAL_TEMP_DEFAULT          32.0f   // °C
#define UMBRAL_HEAT_INDEX_DEFAULT    38.0f   // °C (Estrés térmico severo según NOM-015 / NOAA)
#define HISTERESIS_TEMP_OFFSET       2.0f    // °C para evitar oscilación (chattering)
#define UMBRAL_HEAT_INDEX_APAGADO    35.0f   // °C límite seguro inferior

#endif // CONFIG_H
