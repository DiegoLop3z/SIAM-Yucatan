#ifndef HEAT_INDEX_H
#define HEAT_INDEX_H

#include <Arduino.h>
#include <math.h>

// ============================================================================
//  Cálculo de Sensación Térmica / Índice de Calor (Heat Index)
//  Basado en la ecuación de regresión de Rothfusz (NOAA / National Weather Service)
//  y alineado con la NOM-015-STPS-2001 (Condiciones térmicas extremas laborales)
// ============================================================================

enum NivelAlertaTermica {
    ALERTA_CONFORT,     // < 30.0 °C -> Verde: Seguro / Trabajo normal
    ALERTA_PRECAUCION,   // 30.0 °C a 37.9 °C -> Amarillo: Fatiga térmica, hidratación
    ALERTA_PELIGRO      // >= 38.0 °C -> Rojo: Riesgo inminente de golpe de calor
};

/**
 * Calcula el Índice de Calor (Heat Index) en grados Celsius.
 * @param tempC Temperatura ambiental medida en °C
 * @param humRel Humedad relativa medida en % (0 a 100)
 * @return Sensación térmica estimada en °C
 */
inline float calcularIndiceCalor(float tempC, float humRel) {
    // Si la temperatura es baja (< 20 °C), el índice de calor no presenta
    // efecto acumulativo sobre el estrés metabólico humano; se reporta temp ambiental.
    if (tempC < 20.0f) {
        return tempC;
    }

    // Conversión a grados Fahrenheit requerida por el modelo matemático de Rothfusz
    float tf = (tempC * 1.8f) + 32.0f;
    float rh = humRel;

    // Aproximación inicial de Steadman
    float hi = 0.5f * (tf + 61.0f + ((tf - 68.0f) * 1.2f) + (rh * 0.094f));

    // Si la sensación preliminar alcanza o supera los 80 °F (~26.7 °C), se ejecuta
    // la regresión polinomial multivariable completa de Rothfusz (NOAA)
    if (hi >= 80.0f) {
        hi = -42.379f 
             + 2.04901523f * tf 
             + 10.14333127f * rh 
             - 0.22475541f * tf * rh 
             - 0.00683783f * tf * tf 
             - 0.05481717f * rh * rh 
             + 0.00122874f * tf * tf * rh 
             + 0.00085282f * tf * rh * rh 
             - 0.00000199f * tf * tf * rh * rh;

        // Factor de ajuste para humedades relativas bajas (< 13%)
        if (rh < 13.0f && tf >= 80.0f && tf <= 112.0f) {
            float adj = ((13.0f - rh) / 4.0f) * sqrtf((17.0f - fabsf(tf - 95.0f)) / 17.0f);
            hi -= adj;
        }
        // Factor de ajuste para humedades relativas altas (> 85%)
        else if (rh > 85.0f && tf >= 80.0f && tf <= 87.0f) {
            float adj = ((rh - 85.0f) / 10.0f) * ((87.0f - tf) / 5.0f);
            hi += adj;
        }
    }

    // Conversión de retorno a grados Celsius
    float hiC = (hi - 32.0f) / 1.8f;
    return hiC;
}

/**
 * Determina el nivel de alerta bioclimática según la sensación térmica resultante.
 */
inline NivelAlertaTermica evaluarNivelAlerta(float heatIndexC) {
    if (heatIndexC < 30.0f) {
        return ALERTA_CONFORT;
    } else if (heatIndexC < 38.0f) {
        return ALERTA_PRECAUCION;
    } else {
        return ALERTA_PELIGRO;
    }
}

/**
 * Devuelve la cadena descriptiva de la alerta para telemetría y dashboard.
 */
inline const char* obtenerNombreAlerta(NivelAlertaTermica nivel) {
    switch (nivel) {
        case ALERTA_CONFORT:    return "CONFORT";
        case ALERTA_PRECAUCION:  return "PRECAUCION";
        case ALERTA_PELIGRO:    return "PELIGRO";
        default:                return "NORMAL";
    }
}

#endif // HEAT_INDEX_H
