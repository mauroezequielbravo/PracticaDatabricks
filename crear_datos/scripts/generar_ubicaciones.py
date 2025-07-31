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

def generar_ubicaciones(num_ubicaciones=200):
    """
    Genera datos de ubicaciones con problemas de calidad incluidos
    """
    ubicaciones = []
    
    # Zonas predefinidas
    zonas = [
        "Zona Norte", "Zona Sur", "Zona Este", "Zona Oeste", 
        "Zona Centro", "Zona Industrial", "Zona Residencial",
        "Zona Comercial", "Zona Rural", "Zona Suburbana"
    ]
    
    tipos = ["Urbana", "Rural", "Industrial"]
    
    for i in range(num_ubicaciones):
        # Generar datos básicos
        ubicacion_id = f"UB{i+1:04d}"
        nombre = fake.company() if random.random() < 0.3 else fake.street_name()
        tipo = random.choice(tipos)
        zona_id = f"Z{random.randint(1, 10):02d}"
        
        # Generar coordenadas realistas para Argentina
        latitud = random.uniform(-55, -22)  # Argentina latitud
        longitud = random.uniform(-73, -53)  # Argentina longitud
        
        # Introducir problemas de calidad (10% de los registros)
        if random.random() < 0.1:
            problema = random.choice([
                'coordenadas_fuera_rango',
                'coordenadas_texto',
                'sin_zona',
                'nombre_mal_codificado'
            ])
            
            if problema == 'coordenadas_fuera_rango':
                latitud = random.uniform(91, 95)  # Fuera de rango
                longitud = random.uniform(181, 185)  # Fuera de rango
            elif problema == 'coordenadas_texto':
                latitud = f"{latitud:.4f}°N"
                longitud = f"{longitud:.4f}°W"
            elif problema == 'sin_zona':
                zona_id = None
            elif problema == 'nombre_mal_codificado':
                nombre = "Estación María José González"  # Con caracteres especiales
        
        ubicaciones.append({
            'ubicacion_id': ubicacion_id,
            'nombre': nombre,
            'latitud': latitud,
            'longitud': longitud,
            'zona_id': zona_id,
            'tipo': tipo
        })
    
    return pd.DataFrame(ubicaciones)

if __name__ == "__main__":
    print("Generando datos de ubicaciones...")
    df_ubicaciones = generar_ubicaciones()
    
    # Guardar archivo
    df_ubicaciones.to_csv('datos_gas/ubicaciones.csv', index=False)
    print(f"Archivo ubicaciones.csv generado con {len(df_ubicaciones)} registros")
    print("Problemas de calidad incluidos:")
    print("- Coordenadas fuera de rango")
    print("- Coordenadas como texto")
    print("- Ubicaciones sin zona asignada")
    print("- Nombres con caracteres especiales mal codificados") 