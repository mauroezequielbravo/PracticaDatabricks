# Datos de Empresa Transportadora de Gas

Este documento describe los archivos de datos generados para practicar la implementación de un datalake house con modelo medallón en Databricks.

## Estructura de Archivos

### 📁 Datos Base

#### `clientes.csv`
**Descripción**: Información de clientes que consumen gas (Sistema de CRM)
**Campos**:
- `cliente_id` (PK): Identificador único del cliente
- `dni`: Documento Nacional de Identidad
- `nombre`: Nombre completo del cliente
- `email`: Dirección de correo electrónico
- `telefono`: Número de teléfono
- `direccion`: Dirección completa
- `codigo_postal`: Código postal
- `zona_id` (FK): Zona de distribución asignada
- `tipo_cliente`: Residencial, Comercial, Industrial
- `fecha_alta`: Fecha de registro del cliente
- `estado`: Activo, Inactivo, Suspendido

**Problemas de calidad incluidos**:
- DNIs duplicados o mal formateados
- Emails mal formateados: "usuario@", "@dominio.com"
- Teléfonos sin formato: "123456789", "12-34-56-78"
- Códigos postales inconsistentes: "1234", "A1234", "12-34"
- Clientes con zona_id inexistente
- Fechas de alta en el futuro
- Nombres con caracteres especiales mal codificados

#### `infraestructura.csv`
**Descripción**: Red de tuberías, estaciones y equipos
**Campos**:
- `equipo_id` (PK): Identificador único del equipo
- `tipo_equipo`: Tubería, Estación, Tanque, Medidor
- `ubicacion_id` (FK): Ubicación geográfica
- `capacidad`: Capacidad en m³
- `estado`: Activo, Mantenimiento, Inactivo
- `fecha_instalacion`: Fecha de instalación
- `ultimo_mantenimiento`: Fecha del último mantenimiento

**Problemas de calidad incluidos**:
- Capacidades negativas o extremadamente altas
- Fechas de mantenimiento posteriores a la fecha actual
- Equipos con ubicación_id inexistente
- Estados inconsistentes (equipos inactivos con mantenimientos recientes)

#### `personal.csv`
**Descripción**: Operadores y técnicos de la empresa
**Campos**:
- `empleado_id` (PK): Identificador único del empleado
- `nombre`: Nombre completo
- `cargo`: Operador, Técnico, Supervisor
- `zona_asignada_id` (FK): Zona de trabajo
- `fecha_contratacion`: Fecha de ingreso
- `especialidad`: Especialidad técnica
- `estado`: Activo, Inactivo, Vacaciones

**Problemas de calidad incluidos**:
- Empleados sin zona asignada
- Fechas de contratación en el futuro
- Nombres duplicados con diferentes IDs
- Cargos inexistentes

#### `ubicaciones.csv`
**Descripción**: Información geográfica y zonas
**Campos**:
- `ubicacion_id` (PK): Identificador único de ubicación
- `nombre`: Nombre de la ubicación
- `latitud`: Coordenada latitud
- `longitud`: Coordenada longitud
- `zona_id` (FK): Zona a la que pertenece
- `tipo`: Urbana, Rural, Industrial

**Problemas de calidad incluidos**:
- Coordenadas fuera de rango (latitud > 90, longitud > 180)
- Coordenadas como texto: "40.7128°N"
- Ubicaciones sin zona asignada
- Nombres con caracteres especiales mal codificados

### 📁 Datos Operativos

#### `lecturas_medidores.csv`
**Descripción**: Lecturas diarias de consumo de gas
**Campos**:
- `lectura_id` (PK): Identificador único de lectura
- `medidor_id` (FK): Medidor que generó la lectura
- `cliente_id` (FK): Cliente asociado al medidor
- `fecha_lectura`: Fecha y hora de la lectura
- `consumo_m3`: Consumo en metros cúbicos
- `presion`: Presión del gas
- `temperatura`: Temperatura ambiente
- `estado_medidor`: Normal, Error, Mantenimiento

**Problemas de calidad incluidos**:
- Consumos negativos o extremadamente altos
- Fechas de lectura en el futuro
- Medidores inexistentes
- Clientes inexistentes
- Estados de medidor inconsistentes

#### `entregas_gas.csv`
**Descripción**: Entregas de gas a tanques de almacenamiento
**Campos**:
- `entrega_id` (PK): Identificador único de entrega
- `tanque_id` (FK): Tanque receptor
- `proveedor_id` (FK): Proveedor de gas
- `fecha_entrega`: Fecha y hora de entrega
- `volumen_m3`: Volumen entregado
- `presion_entrada`: Presión de entrada
- `temperatura_gas`: Temperatura del gas
- `estado`: Completada, En Proceso, Cancelada

**Problemas de calidad incluidos**:
- Volúmenes negativos o cero
- Tanques inexistentes
- Proveedores inexistentes
- Fechas de entrega en el futuro
- Estados inconsistentes

#### `mantenimientos.csv`
**Descripción**: Mantenimientos programados y de emergencia
**Campos**:
- `mantenimiento_id` (PK): Identificador único
- `equipo_id` (FK): Equipo a mantener
- `empleado_id` (FK): Empleado asignado
- `tipo`: Programado, Emergencia, Preventivo
- `fecha_inicio`: Fecha de inicio
- `fecha_fin`: Fecha de finalización
- `descripcion`: Descripción del trabajo
- `costo`: Costo del mantenimiento
- `estado`: Programado, En Curso, Completado

**Problemas de calidad incluidos**:
- Fechas de fin anteriores a fecha de inicio
- Empleados inexistentes
- Equipos inexistentes
- Costos negativos
- Mantenimientos en equipos inactivos

#### `eventos_sistema.json`
**Descripción**: Eventos y alertas del sistema (formato JSON)
**Campos**:
- `evento_id`: Identificador único
- `timestamp`: Fecha y hora del evento
- `tipo_evento`: Alerta, Error, Información
- `equipo_id`: Equipo relacionado
- `severidad`: Baja, Media, Alta, Crítica
- `mensaje`: Descripción del evento
- `datos_adicionales`: JSON con datos extra

**Problemas de calidad incluidos**:
- Timestamps en formato inconsistente
- Tipos de evento inexistentes
- Severidades no válidas
- JSON mal formateado
- Equipos inexistentes

### 📁 Datos Financieros

#### `facturacion.csv`
**Descripción**: Facturas mensuales a clientes (Sistema de Facturación)
**Campos**:
- `factura_id` (PK): Identificador único de factura
- `dni_cliente`: DNI del cliente facturado (NO es FK)
- `nombre_cliente`: Nombre del cliente (puede diferir del CRM)
- `fecha_emision`: Fecha de emisión
- `fecha_vencimiento`: Fecha de vencimiento
- `consumo_facturado`: Consumo facturado en m³
- `tarifa_por_m3`: Tarifa aplicada
- `subtotal`: Subtotal de la factura
- `impuestos`: Impuestos aplicados
- `total`: Total a pagar
- `estado`: Emitida, Pagada, Vencida

**Problemas de calidad incluidos**:
- DNIs que no existen en el sistema de clientes
- Nombres de cliente diferentes al CRM
- Fechas de vencimiento anteriores a emisión
- Consumos negativos
- Tarifas negativas o cero
- Totales que no coinciden con subtotal + impuestos
- Estados inconsistentes

#### `pagos.csv`
**Descripción**: Pagos realizados por los clientes (Sistema de Cobranzas)
**Campos**:
- `pago_id` (PK): Identificador único de pago
- `factura_id` (FK): Factura pagada
- `dni_cliente`: DNI del cliente que realizó el pago
- `fecha_pago`: Fecha del pago
- `monto`: Monto pagado
- `metodo_pago`: Efectivo, Tarjeta, Transferencia
- `estado`: Completado, Pendiente, Rechazado
- `referencia`: Número de referencia

**Problemas de calidad incluidos**:
- DNIs que no coinciden con facturación ni clientes
- Facturas inexistentes
- Montos negativos o cero
- Fechas de pago en el futuro
- Métodos de pago inexistentes
- Pagos duplicados

#### `tarifas.csv`
**Descripción**: Tarifas por zona y tipo de cliente
**Campos**:
- `tarifa_id` (PK): Identificador único
- `zona_id` (FK): Zona aplicable
- `tipo_cliente`: Residencial, Comercial, Industrial
- `tarifa_por_m3`: Precio por metro cúbico
- `fecha_inicio`: Fecha de inicio de vigencia
- `fecha_fin`: Fecha de fin de vigencia
- `estado`: Activa, Inactiva

**Problemas de calidad incluidos**:
- Zonas inexistentes
- Fechas de fin anteriores a inicio
- Tarifas negativas
- Períodos de vigencia superpuestos
- Tipos de cliente inexistentes

## Relaciones entre Archivos

### Claves Primarias (PK)
- `clientes.cliente_id`
- `infraestructura.equipo_id`
- `personal.empleado_id`
- `ubicaciones.ubicacion_id`
- `lecturas_medidores.lectura_id`
- `entregas_gas.entrega_id`
- `mantenimientos.mantenimiento_id`
- `facturacion.factura_id`
- `pagos.pago_id`
- `tarifas.tarifa_id`

### Claves Foráneas (FK)
- `clientes.zona_id` → `ubicaciones.zona_id`
- `infraestructura.ubicacion_id` → `ubicaciones.ubicacion_id`
- `personal.zona_asignada_id` → `ubicaciones.zona_id`
- `lecturas_medidores.medidor_id` → `infraestructura.equipo_id`
- `lecturas_medidores.cliente_id` → `clientes.cliente_id`
- `entregas_gas.tanque_id` → `infraestructura.equipo_id`
- `mantenimientos.equipo_id` → `infraestructura.equipo_id`
- `mantenimientos.empleado_id` → `personal.empleado_id`
- `pagos.factura_id` → `facturacion.factura_id`
- `tarifas.zona_id` → `ubicaciones.zona_id`

### **NO hay FK entre**:
- `facturacion.dni_cliente` ↔ `clientes.dni`
- `pagos.dni_cliente` ↔ `clientes.dni`

## Tipos de Problemas de Calidad Incluidos

### 1. **Problemas de Integridad Referencial**
- Claves foráneas que apuntan a registros inexistentes
- Registros huérfanos (sin padre)
- Ciclos de referencias

### 2. **Problemas de Formato**
- Fechas en formatos inconsistentes
- Números como texto
- Emails mal formateados
- Códigos postales sin estandarizar

### 3. **Problemas de Lógica de Negocio**
- Consumos negativos
- Fechas futuras donde no corresponde
- Estados inconsistentes
- Cálculos matemáticos incorrectos

### 4. **Problemas de Datos**
- Valores NULL en campos obligatorios
- Registros duplicados
- Caracteres especiales mal codificados
- Espacios extra en texto

### 5. **Problemas de Consistencia**
- Datos que no coinciden entre tablas relacionadas
- Estados inconsistentes entre tablas
- Fechas que no tienen sentido lógico

### 6. **Problemas de Unificación**
- **DNIs duplicados**: Mismo DNI con diferentes datos
- **Nombres diferentes**: "Juan Pérez" vs "Juan Carlos Pérez"
- **Datos faltantes**: Cliente en facturación pero no en CRM
- **Formatos inconsistentes**: DNI con/sin guiones, espacios
- **Errores de tipeo**: DNIs con dígitos incorrectos

## Tareas de Unificación en DLH

### **Bronze Layer**:
- Ingestión de datos crudos de diferentes sistemas
- Preservación de la estructura original

### **Silver Layer**:
- **Unificación por DNI**: Crear tabla maestra de clientes
- **Resolución de conflictos**: Nombres diferentes, datos faltantes
- **Validación de integridad**: DNIs válidos, datos consistentes

### **Gold Layer**:
- **Vista unificada**: Cliente con toda su información
- **Métricas de negocio**: Consumo por cliente, facturación, pagos
- **Análisis de calidad**: Detección de inconsistencias entre sistemas

## Uso para Práctica

Estos datos están diseñados para practicar:

1. **Bronze Layer**: Ingestión de datos crudos con problemas
2. **Silver Layer**: Limpieza, validación y normalización
3. **Gold Layer**: Desnormalización y creación de métricas de negocio

Los problemas de calidad están distribuidos de manera realista (5-10% de los registros) para simular un entorno de producción real. 