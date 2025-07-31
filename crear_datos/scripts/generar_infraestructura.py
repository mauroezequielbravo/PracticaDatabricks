import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar Faker para datos en español
fake = Faker(['es_ES'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

def generar_infraestructura(num_equipos=500):
    """
    Genera datos de infraestructura con problemas de calidad incluidos
    """
    equipos = []
    tipos_equipo = ["Tubería", "Estación", "Tanque", "Medidor"]
    estados = ["Activo", "Mantenimiento", "Inactivo"]
    
    for i in range(num_equipos):
        # Generar datos básicos
        equipo_id = f"EQ{i+1:04d}"
        tipo_equipo = random.choice(tipos_equipo)
        ubicacion_id = f"UB{random.randint(1, 200):04d}"
        
        # Capacidad según tipo de equipo
        if tipo_equipo == "Tubería":
            capacidad = random.uniform(100, 10000)
        elif tipo_equipo == "Estación":
            capacidad = random.uniform(5000, 50000)
        elif tipo_equipo == "Tanque":
            capacidad = random.uniform(10000, 100000)
        else:  # Medidor
            capacidad = random.uniform(10, 1000)
        
        estado = random.choice(estados)
        fecha_instalacion = fake.date_between(start_date='-5y', end_date='-1y')
        ultimo_mantenimiento = fake.date_between(start_date='-1y', end_date='today')
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'capacidad_negativa',
                'capacidad_extrema',
                'fecha_mantenimiento_futura',
                'ubicacion_inexistente',
                'estado_inconsistente'
            ])
            
            if problema == 'capacidad_negativa':
                capacidad = random.uniform(-1000, -100)
            elif problema == 'capacidad_extrema':
                capacidad = random.uniform(999999, 9999999)
            elif problema == 'fecha_mantenimiento_futura':
                ultimo_mantenimiento = fake.date_between(start_date='today', end_date='+1y')
            elif problema == 'ubicacion_inexistente':
                ubicacion_id = f"UB{random.randint(1000, 9999):04d}"  # Ubicación que no existe
            elif problema == 'estado_inconsistente':
                if estado == "Inactivo":
                    ultimo_mantenimiento = fake.date_between(start_date='-1m', end_date='today')
        
        equipos.append({
            'equipo_id': equipo_id,
            'tipo_equipo': tipo_equipo,
            'ubicacion_id': ubicacion_id,
            'capacidad': round(capacidad, 2),
            'estado': estado,
            'fecha_instalacion': fecha_instalacion,
            'ultimo_mantenimiento': ultimo_mantenimiento
        })
    
    return pd.DataFrame(equipos)

if __name__ == "__main__":
    print("Generando datos de infraestructura...")
    df_infraestructura = generar_infraestructura()
    
    # Guardar archivo
    df_infraestructura.to_csv('datos_gas/infraestructura.csv', index=False)
    print(f"Archivo infraestructura.csv generado con {len(df_infraestructura)} registros")
    print("Problemas de calidad incluidos:")
    print("- Capacidades negativas o extremadamente altas")
    print("- Fechas de mantenimiento posteriores a la fecha actual")
    print("- Equipos con ubicación_id inexistente")
    print("- Estados inconsistentes (equipos inactivos con mantenimientos recientes)") 