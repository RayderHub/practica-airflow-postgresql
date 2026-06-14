# Practica 2 - Fase 1: Airflow y PostgreSQL

Proyecto ETL para cargar el dataset `data.csv` en PostgreSQL usando Apache Airflow.

## Estructura

```text
.
├── docker-compose.yml
├── dags/
│   └── elt_pipeline.py
├── scripts/
│   └── ingestion.py
├── data/
│   └── data.csv
├── logs/
└── plugins/
```

## Uso

1. Descarga el dataset de Kaggle y colocalo en `data/data.csv`.
2. Levanta la infraestructura:

```bash
docker compose up -d
```

3. Abre Airflow en `http://localhost:8080`.
4. Activa el DAG `elt_ecommerce_pipeline`.
5. Ejecuta la tarea `Extract_and_Load`.

## Base de datos

- Host desde Docker: `postgres-db`
- Host desde tu computadora: `localhost`
- Puerto: `5432`
- Base de datos: `dw_analytics`
- Usuario: `uteq_user`
- Password: `uteq_password`
- Tabla generada: `stg_ecommerce_sales`

## Validacion

Puedes revisar la carga con esta consulta:

```sql
SELECT COUNT(*) FROM stg_ecommerce_sales;
```
