Practica 2 - Fase 1: Configuracion de Infraestructura e Ingesta Automatizada de Datos

Se implemento un pipeline ETL usando Docker, Apache Airflow, PostgreSQL y Python.

El proyecto contiene:
- docker-compose.yml: levanta los contenedores de Airflow y PostgreSQL.
- dags/elt_pipeline.py: define el DAG elt_ecommerce_pipeline.
- scripts/ingestion.py: lee data/data.csv, limpia datos y carga la tabla stg_ecommerce_sales.
- data/data.csv: dataset de e-commerce usado en la practica.
- prueba.png: evidencia de ejecucion.

Resultado:
La tarea Extract_and_Load se ejecuto correctamente en Airflow y se validaron 541909 registros cargados en PostgreSQL.

Comando de ejecucion:
docker compose up -d

Airflow:
http://localhost:8080

Base de datos:
Host: localhost
Puerto: 5432
Base: dw_analytics
Usuario: uteq_user
Password: uteq_password
Tabla: stg_ecommerce_sales

Repositorio GitHub:
https://github.com/RayderHub/practica-airflow-postgresql
