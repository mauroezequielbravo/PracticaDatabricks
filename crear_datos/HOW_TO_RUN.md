# 🚀 Guía de Ejecución - Generación de Datos Gas

## 📋 Prerrequisitos

Antes de ejecutar los scripts, asegúrate de tener Python 3.7+ instalado y las dependencias necesarias.

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Ejecución Rápida

Para generar todos los datos de una vez, ejecuta:

```bash
python crear_datos/scripts/generar_todos_datos.py
```

Este comando:
- ✅ Crea la carpeta `datos_gas/` automáticamente
- ✅ Genera todos los archivos CSV y JSON
- ✅ Muestra el progreso en tiempo real
- ✅ Proporciona un resumen final

## 📁 Estructura de Archivos Generados

Después de la ejecución, tendrás:

```
datos_gas/
├── ubicaciones.csv
├── clientes.csv
├── infraestructura.csv
├── personal.csv
├── lecturas_medidores.csv
├── entregas_gas.csv
├── mantenimientos.csv
├── eventos_sistema.json
├── facturacion.csv
├── pagos.csv
└── tarifas.csv
```

## 🔧 Ejecución Individual

Si quieres generar archivos específicos, puedes ejecutar cada script por separado:

```bash
# Generar ubicaciones y zonas
python crear_datos/scripts/generar_ubicaciones.py

# Generar clientes (CRM)
python crear_datos/scripts/generar_clientes.py

# Generar infraestructura
python crear_datos/scripts/generar_infraestructura.py

# Generar personal
python crear_datos/scripts/generar_personal.py

# Generar lecturas de medidores
python crear_datos/scripts/generar_lecturas_medidores.py

# Generar entregas de gas
python crear_datos/scripts/generar_entregas_gas.py

# Generar mantenimientos
python crear_datos/scripts/generar_mantenimientos.py

# Generar eventos del sistema
python crear_datos/scripts/generar_eventos_sistema.py

# Generar facturación (Sistema de Billing)
python crear_datos/scripts/generar_facturacion.py

# Generar pagos (Sistema de Cobranzas)
python crear_datos/scripts/generar_pagos.py

# Generar tarifas
python crear_datos/scripts/generar_tarifas.py
```

## 📊 Datos Generados

### Volumen de Datos
- **Ubicaciones**: 200 registros
- **Clientes**: 1,000 registros (CRM)
- **Infraestructura**: 500 registros
- **Personal**: 150 registros
- **Lecturas**: 5,000 registros
- **Entregas**: 800 registros
- **Mantenimientos**: 300 registros
- **Eventos**: 2,000 registros (JSON)
- **Facturación**: 3,000 registros (Billing)
- **Pagos**: 2,500 registros (Cobranzas)
- **Tarifas**: 100 registros

### Problemas de Calidad Incluidos
Cada archivo incluye aproximadamente 8-10% de registros con problemas de calidad para practicar:
- ✅ Datos faltantes
- ✅ Valores duplicados
- ✅ Formatos incorrectos
- ✅ Referencias rotas
- ✅ Datos inconsistentes
- ✅ Valores extremos
- ✅ Problemas de codificación

## 🔗 Relaciones entre Sistemas

### Sistemas Simulados
1. **CRM** (`clientes.csv`) - Sistema de gestión de clientes
2. **Billing** (`facturacion.csv`) - Sistema de facturación
3. **Payments** (`pagos.csv`) - Sistema de cobranzas

### Unificación por DNI
Los sistemas no están conectados por `cliente_id` sino por `dni`, requiriendo:
- 🔄 Unificación en la capa Silver del Data Lakehouse
- 🔍 Resolución de inconsistencias entre sistemas
- 🎯 Creación de vista maestra de clientes

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install pandas numpy faker
```

### Error: "Permission denied"
```bash
# En Windows
python -m pip install --user -r requirements.txt

# En Linux/Mac
sudo pip install -r requirements.txt
```

### Error: "No such file or directory"
Asegúrate de estar en el directorio raíz del proyecto:
```bash
cd /ruta/a/PracticaDatabricks
```

## 📈 Próximos Pasos

Una vez generados los datos:

1. **Cargar en Databricks** - Subir archivos a DBFS
2. **Capa Bronze** - Cargar datos raw sin transformaciones
3. **Capa Silver** - Limpiar y normalizar datos
4. **Capa Gold** - Aplicar lógica de negocio y denormalizar
5. **Unificación** - Resolver inconsistencias entre sistemas por DNI

## 📝 Notas Importantes

- Los datos incluyen problemas de calidad intencionales para práctica
- Los sistemas CRM, Billing y Payments están desacoplados
- La unificación por DNI es una tarea clave en la capa Silver
- Todos los archivos se generan en formato UTF-8
- Los timestamps están en formato ISO 8601

---

¡Listo para practicar con tu Data Lakehouse en Databricks! 🎉 