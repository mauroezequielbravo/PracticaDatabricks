#!/usr/bin/env python3
"""
Script principal para generar todos los datos de la empresa transportadora de gas
Ejecuta todos los generadores de datos en el orden correcto
"""

import os
import sys
from datetime import datetime

def crear_directorio():
    """Crea el directorio datos_gas si no existe"""
    if not os.path.exists('datos_gas'):
        os.makedirs('datos_gas')
        print("✅ Directorio 'datos_gas' creado")

def ejecutar_generador(script_name, descripcion):
    """Ejecuta un script generador específico"""
    print(f"\n🔄 Ejecutando {script_name}...")
    print(f"📝 {descripcion}")
    
    try:
        # Importar y ejecutar el módulo
        module_name = script_name.replace('.py', '')
        module = __import__(module_name)
        
        # Ejecutar la función principal si existe
        if hasattr(module, 'generar_ubicaciones'):
            df = module.generar_ubicaciones()
            df.to_csv('datos_gas/ubicaciones.csv', index=False)
        elif hasattr(module, 'generar_clientes'):
            df = module.generar_clientes()
            df.to_csv('datos_gas/clientes.csv', index=False)
        elif hasattr(module, 'generar_infraestructura'):
            df = module.generar_infraestructura()
            df.to_csv('datos_gas/infraestructura.csv', index=False)
        elif hasattr(module, 'generar_personal'):
            df = module.generar_personal()
            df.to_csv('datos_gas/personal.csv', index=False)
        elif hasattr(module, 'generar_lecturas_medidores'):
            df = module.generar_lecturas_medidores()
            df.to_csv('datos_gas/lecturas_medidores.csv', index=False)
        elif hasattr(module, 'generar_entregas_gas'):
            df = module.generar_entregas_gas()
            df.to_csv('datos_gas/entregas_gas.csv', index=False)
        elif hasattr(module, 'generar_mantenimientos'):
            df = module.generar_mantenimientos()
            df.to_csv('datos_gas/mantenimientos.csv', index=False)
        elif hasattr(module, 'generar_eventos_sistema'):
            eventos = module.generar_eventos_sistema()
            import json
            with open('datos_gas/eventos_sistema.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, ensure_ascii=False, indent=2, default=str)
        elif hasattr(module, 'generar_facturacion'):
            df = module.generar_facturacion()
            df.to_csv('datos_gas/facturacion.csv', index=False)
        elif hasattr(module, 'generar_pagos'):
            df = module.generar_pagos()
            df.to_csv('datos_gas/pagos.csv', index=False)
        elif hasattr(module, 'generar_tarifas'):
            df = module.generar_tarifas()
            df.to_csv('datos_gas/tarifas.csv', index=False)
        
        print(f"✅ {script_name} completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {str(e)}")
        return False

def main():
    """Función principal que ejecuta todos los generadores"""
    print("🚀 Iniciando generación de datos para empresa transportadora de gas")
    print("=" * 70)
    
    # Crear directorio
    crear_directorio()
    
    # Lista de generadores en orden de ejecución
    generadores = [
        ("generar_ubicaciones.py", "Generando datos de ubicaciones y zonas geográficas"),
        ("generar_clientes.py", "Generando datos de clientes (Sistema CRM)"),
        ("generar_infraestructura.py", "Generando datos de infraestructura y equipos"),
        ("generar_personal.py", "Generando datos de personal operativo"),
        ("generar_lecturas_medidores.py", "Generando lecturas de medidores"),
        ("generar_entregas_gas.py", "Generando datos de entregas de gas"),
        ("generar_mantenimientos.py", "Generando datos de mantenimientos"),
        ("generar_eventos_sistema.py", "Generando eventos del sistema (JSON)"),
        ("generar_facturacion.py", "Generando datos de facturación (Sistema separado)"),
        ("generar_pagos.py", "Generando datos de pagos (Sistema separado)"),
        ("generar_tarifas.py", "Generando datos de tarifas")
    ]
    
    exitos = 0
    total = len(generadores)
    
    for script, descripcion in generadores:
        if ejecutar_generador(script, descripcion):
            exitos += 1
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE GENERACIÓN")
    print("=" * 70)
    print(f"✅ Scripts exitosos: {exitos}/{total}")
    print(f"❌ Scripts fallidos: {total - exitos}/{total}")
    
    if exitos == total:
        print("\n🎉 ¡Todos los datos han sido generados exitosamente!")
        print("\n📁 Archivos generados en el directorio 'datos_gas/':")
        
        archivos = [
            "ubicaciones.csv",
            "clientes.csv", 
            "infraestructura.csv",
            "personal.csv",
            "lecturas_medidores.csv",
            "entregas_gas.csv",
            "mantenimientos.csv",
            "eventos_sistema.json",
            "facturacion.csv",
            "pagos.csv",
            "tarifas.csv"
        ]
        
        for archivo in archivos:
            if os.path.exists(f'datos_gas/{archivo}'):
                size = os.path.getsize(f'datos_gas/{archivo}')
                print(f"   📄 {archivo} ({size:,} bytes)")
        
        print("\n🔧 Problemas de calidad incluidos:")
        print("   • DNIs duplicados y mal formateados")
        print("   • Emails y teléfonos sin formato")
        print("   • Fechas futuras donde no corresponde")
        print("   • Valores negativos en campos numéricos")
        print("   • Claves foráneas rotas")
        print("   • Estados inconsistentes")
        print("   • Datos de diferentes sistemas no unificados")
        
        print("\n📚 Uso para práctica:")
        print("   • Bronze Layer: Ingestión de datos crudos")
        print("   • Silver Layer: Limpieza y normalización")
        print("   • Gold Layer: Desnormalización y métricas")
        
    else:
        print(f"\n⚠️  {total - exitos} script(s) fallaron. Revisa los errores arriba.")
    
    print(f"\n⏰ Generación completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 