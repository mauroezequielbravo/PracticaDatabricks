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

def generar_mantenimientos(num_mantenimientos=800):
    """
    Genera datos de mantenimientos con problemas de calidad incluidos
    """
    mantenimientos = []
    tipos = ["Programado", "Emergencia", "Preventivo"]
    estados = ["Programado", "En Curso", "Completado"]
    descripciones = [
        "Revisión general del equipo",
        "Cambio de filtros",
        "Calibración de sensores",
        "Reparación de válvulas",
        "Limpieza de tuberías",
        "Reemplazo de componentes",
        "Inspección de seguridad",
        "Actualización de software"
    ]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_mantenimientos):
        # Generar datos básicos
        mantenimiento_id = f"MAN{i+1:06d}"
        equipo_id = f"EQ{random.randint(1, 500):04d}"
        empleado_id = f"EMP{random.randint(1, 150):04d}"
        tipo = random.choice(tipos)
        fecha_inicio_mant = fake.date_time_between(start_date=fecha_inicio, end_date='now')
        fecha_fin_mant = fecha_inicio_mant + timedelta(hours=random.randint(2, 48))
        descripcion = random.choice(descripciones)
        costo = random.uniform(100.0, 5000.0)
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'fecha_fin_anterior',
                'empleado_inexistente',
                'equipo_inexistente',
                'costo_negativo',
                'mantenimiento_equipo_inactivo'
            ])
            
            if problema == 'fecha_fin_anterior':
                fecha_fin_mant = fecha_inicio_mant - timedelta(hours=random.randint(1, 24))
            elif problema == 'empleado_inexistente':
                empleado_id = f"EMP{random.randint(1000, 9999):04d}"  # Empleado que no existe
            elif problema == 'equipo_inexistente':
                equipo_id = f"EQ{random.randint(1000, 9999):04d}"  # Equipo que no existe
            elif problema == 'costo_negativo':
                costo = random.uniform(-1000.0, -100.0)
            elif problema == 'mantenimiento_equipo_inactivo':
                # Simular mantenimiento en equipo inactivo
                if random.random() < 0.5:
                    estado = "En Curso"  # Estado activo en equipo inactivo
        
        mantenimientos.append({
            'mantenimiento_id': mantenimiento_id,
            'equipo_id': equipo_id,
            'empleado_id': empleado_id,
            'tipo': tipo,
            'fecha_inicio': fecha_inicio_mant,
            'fecha_fin': fecha_fin_mant,
            'descripcion': descripcion,
            'costo': round(costo, 2),
            'estado': estado
        })
    
    return pd.DataFrame(mantenimientos)

if __name__ == "__main__":
    print("Generando datos de mantenimientos...")
    df_mantenimientos = generar_mantenimientos()
    
    # Guardar archivo
    df_mantenimientos.to_csv('datos_gas/mantenimientos.csv', index=False)
    print(f"Archivo mantenimientos.csv generado con {len(df_mantenimientos)} registros")
    print("Problemas de calidad incluidos:")
    print("- Fechas de fin anteriores a fecha de inicio")
    print("- Empleados inexistentes")
    print("- Equipos inexistentes")
    print("- Costos negativos")
    print("- Mantenimientos en equipos inactivos") 