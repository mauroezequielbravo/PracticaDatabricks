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

def generar_lecturas_medidores(num_lecturas=5000):
    """
    Genera datos de lecturas de medidores con problemas de calidad incluidos
    """
    lecturas = []
    estados_medidor = ["Normal", "Error", "Mantenimiento"]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_lecturas):
        # Generar datos básicos
        lectura_id = f"LEC{i+1:06d}"
        medidor_id = f"EQ{random.randint(1, 500):04d}"
        cliente_id = f"C{random.randint(1, 1000):04d}"
        fecha_lectura = fake.date_time_between(start_date=fecha_inicio, end_date='now')
        consumo_m3 = random.uniform(0.1, 100.0)
        presion = random.uniform(1.0, 10.0)
        temperatura = random.uniform(10.0, 35.0)
        estado_medidor = random.choice(estados_medidor)
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'consumo_negativo',
                'consumo_extremo',
                'fecha_futura',
                'medidor_inexistente',
                'cliente_inexistente',
                'estado_inconsistente'
            ])
            
            if problema == 'consumo_negativo':
                consumo_m3 = random.uniform(-50.0, -0.1)
            elif problema == 'consumo_extremo':
                consumo_m3 = random.uniform(999.0, 9999.0)
            elif problema == 'fecha_futura':
                fecha_lectura = fake.date_time_between(start_date='now', end_date='+30d')
            elif problema == 'medidor_inexistente':
                medidor_id = f"EQ{random.randint(1000, 9999):04d}"  # Medidor que no existe
            elif problema == 'cliente_inexistente':
                cliente_id = f"C{random.randint(1001, 9999):04d}"  # Cliente que no existe
            elif problema == 'estado_inconsistente':
                if estado_medidor == "Error":
                    consumo_m3 = 0  # Consumo 0 cuando hay error
                elif estado_medidor == "Mantenimiento":
                    presion = 0  # Presión 0 en mantenimiento
        
        lecturas.append({
            'lectura_id': lectura_id,
            'medidor_id': medidor_id,
            'cliente_id': cliente_id,
            'fecha_lectura': fecha_lectura,
            'consumo_m3': round(consumo_m3, 2),
            'presion': round(presion, 2),
            'temperatura': round(temperatura, 1),
            'estado_medidor': estado_medidor
        })
    
    return pd.DataFrame(lecturas)

if __name__ == "__main__":
    print("Generando datos de lecturas de medidores...")
    df_lecturas = generar_lecturas_medidores()
    
    # Guardar archivo
    df_lecturas.to_csv('datos_gas/lecturas_medidores.csv', index=False)
    print(f"Archivo lecturas_medidores.csv generado con {len(df_lecturas)} registros")
    print("Problemas de calidad incluidos:")
    print("- Consumos negativos o extremadamente altos")
    print("- Fechas de lectura en el futuro")
    print("- Medidores inexistentes")
    print("- Clientes inexistentes")
    print("- Estados de medidor inconsistentes") 