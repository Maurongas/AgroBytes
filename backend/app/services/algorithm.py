def calculate_crop_recommendation(avg_temp: float, rainfall_mm: float, humedad_suelo_pct: float, soil_type: str, cultivo_actual: str, disponibilidad_agua: str, prioridad_agricultor: str):
    
    # Cálculo simulado de Machine Learning / Incertidumbre basado en datos de entrada
    incertidumbre_base = 15 if humedad_suelo_pct < 30 else 5
    confianza = 100 - incertidumbre_base

    estrategia_1 = {
        "estrategia": "Rotación Actual (Línea Base)",
        "cultivo": cultivo_actual,
        "justificacion": f"Evaluación del {cultivo_actual} frente a estrés hídrico y térmico actual.",
        "beneficios": "Cero curva de aprendizaje. Infraestructura existente.",
        "riesgos": "Alta vulnerabilidad si la humedad del suelo cae por debajo de los umbrales críticos.",
        "tradeoff": "Tradeoff: Mantienes tu mercado seguro, pero arriesgas pérdida total por anomalías climáticas."
    }

    cultivo_2 = "Leguminosas (Frijol/Lenteja)" if prioridad_agricultor == "mejorar_suelo" else "Sorgo/Mijo"
    estrategia_2 = {
        "estrategia": "Optimización DSS (Apoyo a la Decisión)",
        "cultivo": cultivo_2,
        "justificacion": f"Modelo predictivo sugiere este cultivo al priorizar '{prioridad_agricultor.replace('_', ' ')}' con humedad del suelo al {humedad_suelo_pct}%.",
        "beneficios": "Alta eficiencia en el uso de agua subsuperficial y mejora de nutrientes.",
        "riesgos": "Posible variabilidad en precios de mercado locales.",
        "tradeoff": "Tradeoff: Sacrificas rendimiento bruto a corto plazo a cambio de estabilidad ante sequías."
    }

    estrategia_3 = {
        "estrategia": "Resiliencia Extrema (Proyección SI)",
        "cultivo": "Cultivo de Cobertura (Centeno/Trébol)",
        "justificacion": "Datos de satélite proyectan degradación del suelo. Cobertura requerida para restaurar biomasa.",
        "beneficios": "Reduce evaporación, fija nitrógeno y combate la erosión.",
        "riesgos": "Inversión neta sin retorno económico en la temporada actual.",
        "tradeoff": "Tradeoff: Pierdes ingresos esta temporada, pero garantizas fertilidad para las próximas décadas."
    }

    return {
        "status": "success",
        "confianza_modelo_ml": f"{confianza}%",
        "margen_incertidumbre": f"±{incertidumbre_base}% (Basado en volatilidad de humedad/lluvia)",
        "datos_analizados": {
            "temperatura": avg_temp,
            "lluvia": rainfall_mm,
            "humedad_suelo": humedad_suelo_pct,
            "suelo": soil_type,
            "cultivo": cultivo_actual,
            "agua": disponibilidad_agua,
            "prioridad": prioridad_agricultor
        },
        "recomendaciones": [estrategia_1, estrategia_2, estrategia_3]
    }