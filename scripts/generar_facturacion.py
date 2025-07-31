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

def generar_facturacion(num_facturas=3000):
    """
    Genera datos de facturación con problemas de calidad incluidos
    Sistema separado que usa DNI en lugar de cliente_id
    """
    facturas = []
    estados = ["Emitida", "Pagada", "Vencida"]
    
    # Generar algunos DNIs para problemas de unificación
    dnis_problema = [generar_dni() for _ in range(10)]
    
    # Generar fechas para los últimos 2 años
    fecha_inicio = datetime.now() - timedelta(days=730)
    
    for i in range(num_facturas):
        # Generar datos básicos
        factura_id = f"FAC{i+1:08d}"
        dni_cliente = generar_dni()
        nombre_cliente = fake.name()
        fecha_emision = fake.date_between(start_date=fecha_inicio, end_date='now')
        fecha_vencimiento = fecha_emision + timedelta(days=random.randint(15, 30))
        consumo_facturado = random.uniform(10.0, 500.0)
        tarifa_por_m3 = random.uniform(50.0, 200.0)
        subtotal = consumo_facturado * tarifa_por_m3
        impuestos = subtotal * 0.21  # 21% IVA
        total = subtotal + impuestos
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'dni_inexistente',
                'nombre_diferente',
                'fecha_vencimiento_anterior',
                'consumo_negativo',
                'tarifa_negativa',
                'total_incorrecto',
                'estado_inconsistente'
            ])
            
            if problema == 'dni_inexistente':
                dni_cliente = f"{random.randint(100000000, 999999999)}"  # DNI que no existe en CRM
            elif problema == 'nombre_diferente':
                # Nombre ligeramente diferente al del CRM
                nombre_cliente = random.choice([
                    "Juan Carlos Pérez",  # vs "Juan Pérez"
                    "María José González",  # vs "María González"
                    "José Luis Rodríguez",  # vs "José Rodríguez"
                    "Ana María López"  # vs "Ana López"
                ])
            elif problema == 'fecha_vencimiento_anterior':
                fecha_vencimiento = fecha_emision - timedelta(days=random.randint(1, 10))
            elif problema == 'consumo_negativo':
                consumo_facturado = random.uniform(-100.0, -1.0)
            elif problema == 'tarifa_negativa':
                tarifa_por_m3 = random.uniform(-50.0, -1.0)
            elif problema == 'total_incorrecto':
                total = subtotal + impuestos + random.uniform(100, 500)  # Total incorrecto
            elif problema == 'estado_inconsistente':
                if estado == "Pagada":
                    fecha_vencimiento = fecha_emision + timedelta(days=random.randint(1, 10))  # Pagada antes de vencimiento
        
        facturas.append({
            'factura_id': factura_id,
            'dni_cliente': dni_cliente,
            'nombre_cliente': nombre_cliente,
            'fecha_emision': fecha_emision,
            'fecha_vencimiento': fecha_vencimiento,
            'consumo_facturado': round(consumo_facturado, 2),
            'tarifa_por_m3': round(tarifa_por_m3, 2),
            'subtotal': round(subtotal, 2),
            'impuestos': round(impuestos, 2),
            'total': round(total, 2),
            'estado': estado
        })
    
    return pd.DataFrame(facturas)

if __name__ == "__main__":
    print("Generando datos de facturación...")
    df_facturacion = generar_facturacion()
    
    # Guardar archivo
    df_facturacion.to_csv('datos_gas/facturacion.csv', index=False)
    print(f"Archivo facturacion.csv generado con {len(df_facturacion)} registros")
    print("Problemas de calidad incluidos:")
    print("- DNIs que no existen en el sistema de clientes")
    print("- Nombres de cliente diferentes al CRM")
    print("- Fechas de vencimiento anteriores a emisión")
    print("- Consumos negativos")
    print("- Tarifas negativas o cero")
    print("- Totales que no coinciden con subtotal + impuestos")
    print("- Estados inconsistentes") 