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

def generar_personal(num_empleados=150):
    """
    Genera datos de personal con problemas de calidad incluidos
    """
    empleados = []
    cargos = ["Operador", "Técnico", "Supervisor"]
    especialidades = [
        "Mantenimiento", "Operaciones", "Seguridad", "Calidad", 
        "Instrumentación", "Electricidad", "Mecánica", "Control"
    ]
    estados = ["Activo", "Inactivo", "Vacaciones"]
    
    # Generar algunos nombres para problemas de duplicación
    nombres_problema = [fake.name() for _ in range(3)]
    
    for i in range(num_empleados):
        # Generar datos básicos
        empleado_id = f"EMP{i+1:04d}"
        nombre = fake.name()
        cargo = random.choice(cargos)
        zona_asignada_id = f"Z{random.randint(1, 10):02d}"
        fecha_contratacion = fake.date_between(start_date='-10y', end_date='-1y')
        especialidad = random.choice(especialidades)
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (8% de los registros)
        if random.random() < 0.08:
            problema = random.choice([
                'sin_zona_asignada',
                'fecha_contratacion_futura',
                'nombre_duplicado',
                'cargo_inexistente'
            ])
            
            if problema == 'sin_zona_asignada':
                zona_asignada_id = None
            elif problema == 'fecha_contratacion_futura':
                fecha_contratacion = fake.date_between(start_date='today', end_date='+1y')
            elif problema == 'nombre_duplicado':
                nombre = random.choice(nombres_problema)  # Usar nombre ya generado
            elif problema == 'cargo_inexistente':
                cargo = random.choice(["Gerente", "Director", "Asistente", "Auxiliar"])
        
        empleados.append({
            'empleado_id': empleado_id,
            'nombre': nombre,
            'cargo': cargo,
            'zona_asignada_id': zona_asignada_id,
            'fecha_contratacion': fecha_contratacion,
            'especialidad': especialidad,
            'estado': estado
        })
    
    return pd.DataFrame(empleados)

if __name__ == "__main__":
    print("Generando datos de personal...")
    df_personal = generar_personal()
    
    # Guardar archivo
    df_personal.to_csv('datos_gas/personal.csv', index=False)
    print(f"Archivo personal.csv generado con {len(df_personal)} registros")
    print("Problemas de calidad incluidos:")
    print("- Empleados sin zona asignada")
    print("- Fechas de contratación en el futuro")
    print("- Nombres duplicados con diferentes IDs")
    print("- Cargos inexistentes") 