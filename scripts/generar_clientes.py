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

def generar_clientes(num_clientes=1000):
    """
    Genera datos de clientes con problemas de calidad incluidos
    """
    clientes = []
    tipos_cliente = ["Residencial", "Comercial", "Industrial"]
    estados = ["Activo", "Inactivo", "Suspendido"]
    
    # Generar algunos DNIs para problemas de duplicación
    dnis_problema = [generar_dni() for _ in range(5)]
    
    for i in range(num_clientes):
        # Generar datos básicos
        cliente_id = f"C{i+1:04d}"
        dni = generar_dni()
        nombre = fake.name()
        email = fake.email()
        telefono = fake.phone_number()
        direccion = fake.address()
        codigo_postal = fake.postcode()
        zona_id = f"Z{random.randint(1, 10):02d}"
        tipo_cliente = random.choice(tipos_cliente)
        fecha_alta = fake.date_between(start_date='-2y', end_date='today')
        estado = random.choice(estados)
        
        # Introducir problemas de calidad (8% de los registros)
        if random.random() < 0.08:
            problema = random.choice([
                'dni_duplicado',
                'email_mal_formateado',
                'telefono_sin_formato',
                'codigo_postal_inconsistente',
                'zona_inexistente',
                'fecha_futura',
                'nombre_mal_codificado'
            ])
            
            if problema == 'dni_duplicado':
                dni = random.choice(dnis_problema)  # Usar DNI ya generado
            elif problema == 'email_mal_formateado':
                email = random.choice(["usuario@", "@dominio.com", "usuario", "dominio.com"])
            elif problema == 'telefono_sin_formato':
                telefono = random.choice(["123456789", "12-34-56-78", "1234567890"])
            elif problema == 'codigo_postal_inconsistente':
                codigo_postal = random.choice(["1234", "A1234", "12-34", "ABC123"])
            elif problema == 'zona_inexistente':
                zona_id = f"Z{random.randint(20, 30):02d}"  # Zona que no existe
            elif problema == 'fecha_futura':
                fecha_alta = fake.date_between(start_date='today', end_date='+1y')
            elif problema == 'nombre_mal_codificado':
                nombre = "José María González"  # Con caracteres especiales
        
        clientes.append({
            'cliente_id': cliente_id,
            'dni': dni,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'direccion': direccion,
            'codigo_postal': codigo_postal,
            'zona_id': zona_id,
            'tipo_cliente': tipo_cliente,
            'fecha_alta': fecha_alta,
            'estado': estado
        })
    
    return pd.DataFrame(clientes)

if __name__ == "__main__":
    print("Generando datos de clientes...")
    df_clientes = generar_clientes()
    
    # Guardar archivo
    df_clientes.to_csv('datos_gas/clientes.csv', index=False)
    print(f"Archivo clientes.csv generado con {len(df_clientes)} registros")
    print("Problemas de calidad incluidos:")
    print("- DNIs duplicados o mal formateados")
    print("- Emails mal formateados")
    print("- Teléfonos sin formato")
    print("- Códigos postales inconsistentes")
    print("- Clientes con zona_id inexistente")
    print("- Fechas de alta en el futuro")
    print("- Nombres con caracteres especiales mal codificados") 