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

def generar_entregas_gas(num_entregas=1000):
    """
    Genera datos de entregas de gas con problemas de calidad incluidos
    """
    entregas = []
    estados = ["Completada", "En Proceso", "Cancelada"]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_entregas):
        # Generar datos básicos
        entrega_id = f"ENT{i+1:06d}"
        tanque_id = f"EQ{random.randint(1, 500):04d}"
        proveedor_id = f"PROV{random.randint(1, 50):03d}"
        fecha_entrega = fake.date_time_between(start_date=fecha_inicio, end_date='now')
        volumen_m3 = random.uniform(100.0, 5000.0)
        presion_entrada = random.uniform(5.0, 15.0)
        temperatura_gas = random.uniform(-10.0, 30.0)
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'volumen_negativo',
                'volumen_cero',
                'tanque_inexistente',
                'proveedor_inexistente',
                'fecha_futura',
                'estado_inconsistente'
            ])
            
            if problema == 'volumen_negativo':
                volumen_m3 = random.uniform(-100.0, -1.0)
            elif problema == 'volumen_cero':
                volumen_m3 = 0
            elif problema == 'tanque_inexistente':
                tanque_id = f"EQ{random.randint(1000, 9999):04d}"  # Tanque que no existe
            elif problema == 'proveedor_inexistente':
                proveedor_id = f"PROV{random.randint(100, 999):03d}"  # Proveedor que no existe
            elif problema == 'fecha_futura':
                fecha_entrega = fake.date_time_between(start_date='now', end_date='+30d')
            elif problema == 'estado_inconsistente':
                if estado == "Cancelada":
                    volumen_m3 = 0  # Volumen 0 si está cancelada
                elif estado == "En Proceso":
                    presion_entrada = 0  # Presión 0 si está en proceso
        
        entregas.append({
            'entrega_id': entrega_id,
            'tanque_id': tanque_id,
            'proveedor_id': proveedor_id,
            'fecha_entrega': fecha_entrega,
            'volumen_m3': round(volumen_m3, 2),
            'presion_entrada': round(presion_entrada, 2),
            'temperatura_gas': round(temperatura_gas, 1),
            'estado': estado
        })
    
    return pd.DataFrame(entregas)

if __name__ == "__main__":
    print("Generando datos de entregas de gas...")
    df_entregas = generar_entregas_gas()
    
    # Guardar archivo
    df_entregas.to_csv('datos_gas/entregas_gas.csv', index=False)
    print(f"Archivo entregas_gas.csv generado con {len(df_entregas)} registros")
    print("Problemas de calidad incluidos:")
    print("- Volúmenes negativos o cero")
    print("- Tanques inexistentes")
    print("- Proveedores inexistentes")
    print("- Fechas de entrega en el futuro")
    print("- Estados inconsistentes") 