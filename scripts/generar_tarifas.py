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

def generar_tarifas(num_tarifas=100):
    """
    Genera datos de tarifas con problemas de calidad incluidos
    """
    tarifas = []
    tipos_cliente = ["Residencial", "Comercial", "Industrial"]
    estados = ["Activa", "Inactiva"]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_tarifas):
        # Generar datos básicos
        tarifa_id = f"TAR{i+1:04d}"
        zona_id = f"Z{random.randint(1, 10):02d}"
        tipo_cliente = random.choice(tipos_cliente)
        tarifa_por_m3 = random.uniform(30.0, 300.0)
        fecha_inicio_vigencia = fake.date_between(start_date=fecha_inicio, end_date='now')
        fecha_fin_vigencia = fecha_inicio_vigencia + timedelta(days=random.randint(180, 365))
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'zona_inexistente',
                'fecha_fin_anterior',
                'tarifa_negativa',
                'período_superpuesto',
                'tipo_cliente_inexistente'
            ])
            
            if problema == 'zona_inexistente':
                zona_id = f"Z{random.randint(20, 30):02d}"  # Zona que no existe
            elif problema == 'fecha_fin_anterior':
                fecha_fin_vigencia = fecha_inicio_vigencia - timedelta(days=random.randint(1, 30))
            elif problema == 'tarifa_negativa':
                tarifa_por_m3 = random.uniform(-100.0, -1.0)
            elif problema == 'período_superpuesto':
                # Crear período superpuesto con otra tarifa
                fecha_fin_vigencia = fecha_inicio_vigencia + timedelta(days=random.randint(1, 30))
            elif problema == 'tipo_cliente_inexistente':
                tipo_cliente = random.choice(["Premium", "VIP", "Especial", "Otro"])
        
        tarifas.append({
            'tarifa_id': tarifa_id,
            'zona_id': zona_id,
            'tipo_cliente': tipo_cliente,
            'tarifa_por_m3': round(tarifa_por_m3, 2),
            'fecha_inicio': fecha_inicio_vigencia,
            'fecha_fin': fecha_fin_vigencia,
            'estado': estado
        })
    
    return pd.DataFrame(tarifas)

if __name__ == "__main__":
    print("Generando datos de tarifas...")
    df_tarifas = generar_tarifas()
    
    # Guardar archivo
    df_tarifas.to_csv('datos_gas/tarifas.csv', index=False)
    print(f"Archivo tarifas.csv generado con {len(df_tarifas)} registros")
    print("Problemas de calidad incluidos:")
    print("- Zonas inexistentes")
    print("- Fechas de fin anteriores a inicio")
    print("- Tarifas negativas")
    print("- Períodos de vigencia superpuestos")
    print("- Tipos de cliente inexistentes") 