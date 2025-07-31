


# Creacion de capas

Creacion de Bronze, Silver y Gold.



## Carpetas dentro de la capa

/bronze/
   ├── fuente_1/  (ej: "sales_api", "erp_db")
   │   ├── raw/               # Datos sin procesar (originales)
   │   ├── ingested/          # Datos ya ingeridos en Delta
   │   ├── _checkpoints/      # Metadata de Spark para streaming
   │   └── _schema_log/       # Histórico de schemas (opcional)
   └── fuente_2/


**Ejemplo para datos batch**: 
```bash
/bronze/sales_api/raw/sales_20230701.json
/bronze/sales_api/raw/sales_20230702.json
```

**Para streaming**:
```bash
/bronze/iot_stream/raw/device_events_ts=20230701120000.parquet
```

**Reglas clave**:
- Incluir fecha/hora en el nombre (`YYYYMMDD` o timestamp).
- Usar formatos splitteables (Parquet, JSON, CSV).
- Evitar espacios y caracteres especiales.




























