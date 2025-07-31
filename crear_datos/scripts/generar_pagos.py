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

def generar_dni():
    """Genera un DNI argentino válido"""
    return f"{random.randint(10000000, 99999999)}"

def generar_pagos(num_pagos=2500):
    """
    Genera datos de pagos con problemas de calidad incluidos
    Sistema separado que usa DNI en lugar de cliente_id
    """
    pagos = []
    metodos_pago = ["Efectivo", "Tarjeta", "Transferencia"]
    estados = ["Completado", "Pendiente", "Rechazado"]
    
    # Generar algunos DNIs para problemas de unificación
    dnis_problema = [generar_dni() for _ in range(8)]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_pagos):
        # Generar datos básicos
        pago_id = f"PAG{i+1:08d}"
        factura_id = f"FAC{random.randint(1, 3000):08d}"
        dni_cliente = generar_dni()
        fecha_pago = fake.date_between(start_date=fecha_inicio, end_date='now')
        monto = random.uniform(100.0, 5000.0)
        metodo_pago = random.choice(metodos_pago)
        estado = random.choice(estados)
        referencia = f"REF{random.randint(100000, 999999)}"
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'dni_inexistente',
                'factura_inexistente',
                'monto_negativo',
                'monto_cero',
                'fecha_futura',
                'metodo_inexistente',
                'pago_duplicado'
            ])
            
            if problema == 'dni_inexistente':
                dni_cliente = f"{random.randint(100000000, 999999999)}"  # DNI que no existe
            elif problema == 'factura_inexistente':
                factura_id = f"FAC{random.randint(10000, 99999):08d}"  # Factura que no existe
            elif problema == 'monto_negativo':
                monto = random.uniform(-1000.0, -100.0)
            elif problema == 'monto_cero':
                monto = 0
            elif problema == 'fecha_futura':
                fecha_pago = fake.date_between(start_date='today', end_date='+30d')
            elif problema == 'metodo_inexistente':
                metodo_pago = random.choice(["Cheque", "Cripto", "Billetera", "Otro"])
            elif problema == 'pago_duplicado':
                # Usar datos de un pago ya generado
                dni_cliente = random.choice(dnis_problema)
                factura_id = f"FAC{random.randint(1, 100):08d}"
        
        pagos.append({
            'pago_id': pago_id,
            'factura_id': factura_id,
            'dni_cliente': dni_cliente,
            'fecha_pago': fecha_pago,
            'monto': round(monto, 2),
            'metodo_pago': metodo_pago,
            'estado': estado,
            'referencia': referencia
        })
    
    return pd.DataFrame(pagos)

if __name__ == "__main__":
    print("Generando datos de pagos...")
    df_pagos = generar_pagos()
    
    # Guardar archivo
    df_pagos.to_csv('datos_gas/pagos.csv', index=False)
    print(f"Archivo pagos.csv generado con {len(df_pagos)} registros")
    print("Problemas de calidad incluidos:")
    print("- DNIs que no coinciden con facturación ni clientes")
    print("- Facturas inexistentes")
    print("- Montos negativos o cero")
    print("- Fechas de pago en el futuro")
    print("- Métodos de pago inexistentes")
    print("- Pagos duplicados") 