import pandas as pd
import numpy as np
from faker import Faker
import random
import json
from datetime import datetime, timedelta

# Configurar Faker para datos en español
fake = Faker(['es_ES'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

def generar_eventos_sistema(num_eventos=2000):
    """
    Genera datos de eventos del sistema en formato JSON con problemas de calidad incluidos
    """
    eventos = []
    tipos_evento = ["Alerta", "Error", "Información"]
    severidades = ["Baja", "Media", "Alta", "Crítica"]
    
    mensajes = [
        "Presión fuera de rango normal",
        "Temperatura elevada detectada",
        "Falla en sensor de flujo",
        "Mantenimiento programado completado",
        "Alerta de seguridad activada",
        "Conexión perdida con equipo",
        "Nivel de tanque bajo",
        "Válvula de emergencia activada",
        "Calibración requerida",
        "Error de comunicación"
    ]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_eventos):
        # Generar datos básicos
        evento_id = f"EVT{i+1:08d}"
        timestamp = fake.date_time_between(start_date=fecha_inicio, end_date='now')
        tipo_evento = random.choice(tipos_evento)
        equipo_id = f"EQ{random.randint(1, 500):04d}"
        severidad = random.choice(severidades)
        mensaje = random.choice(mensajes)
        
        # Datos adicionales según tipo de evento
        datos_adicionales = {
            "valor_medido": round(random.uniform(0, 100), 2),
            "umbral": round(random.uniform(50, 80), 2),
            "unidad": random.choice(["bar", "°C", "m³/h", "psi"]),
            "ubicacion": f"Zona {random.randint(1, 10)}"
        }
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'timestamp_inconsistente',
                'tipo_evento_inexistente',
                'severidad_invalida',
                'json_mal_formateado',
                'equipo_inexistente'
            ])
            
            if problema == 'timestamp_inconsistente':
                # Formato inconsistente de timestamp
                timestamp = random.choice([
                    "2024-13-45 25:70:00",  # Fecha inválida
                    "01/32/2024 14:30",     # Formato diferente
                    "2024-12-25T14:30:00Z", # Formato ISO
                    "25-12-2024 14:30"      # Formato europeo
                ])
            elif problema == 'tipo_evento_inexistente':
                tipo_evento = random.choice(["Warning", "Debug", "Fatal", "Info"])
            elif problema == 'severidad_invalida':
                severidad = random.choice(["Muy Baja", "Extrema", "Normal", "Urgente"])
            elif problema == 'json_mal_formateado':
                datos_adicionales = "datos mal formateados"  # No es JSON válido
            elif problema == 'equipo_inexistente':
                equipo_id = f"EQ{random.randint(1000, 9999):04d}"  # Equipo que no existe
        
        evento = {
            'evento_id': evento_id,
            'timestamp': timestamp,
            'tipo_evento': tipo_evento,
            'equipo_id': equipo_id,
            'severidad': severidad,
            'mensaje': mensaje,
            'datos_adicionales': datos_adicionales
        }
        
        eventos.append(evento)
    
    return eventos

if __name__ == "__main__":
    print("Generando datos de eventos del sistema...")
    eventos = generar_eventos_sistema()
    
    # Crear directorio si no existe
    import os
    os.makedirs('datos_gas', exist_ok=True)
    
    # Guardar archivo JSON
    with open('datos_gas/eventos_sistema.json', 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Archivo eventos_sistema.json generado con {len(eventos)} registros")
    print("Problemas de calidad incluidos:")
    print("- Timestamps en formato inconsistente")
    print("- Tipos de evento inexistentes")
    print("- Severidades no válidas")
    print("- JSON mal formateado")
    print("- Equipos inexistentes") 