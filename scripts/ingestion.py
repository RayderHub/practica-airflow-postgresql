import os
import re

import pandas as pd
from sqlalchemy import create_engine


def clean_special_chars(text):
    if pd.isna(text):
        return "SIN_DESCRIPTION"
    return re.sub(r"[^a-zA-Z0-9\s\-]", "", str(text))


def normalize_spacing(text):
    if pd.isna(text):
        return text
    return re.sub(r"\s+", " ", str(text)).strip()


def validate_invoice_format(invoice):
    invoice_text = str(invoice).strip()
    if re.match(r"^C?\d{6}$", invoice_text):
        return invoice_text
    return "INVALID_INVOICE"


def build_connection_string():
    db_user = os.getenv("DB_USER", "uteq_user")
    db_password = os.getenv("DB_PASSWORD", "uteq_password")
    db_host = os.getenv("DB_HOST", "postgres-db")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "dw_analytics")
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def run_ingestion():
    csv_path = "/opt/airflow/data/data.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"No se encontro el dataset en {csv_path}. "
            "Coloca el archivo data.csv dentro de la carpeta data/."
        )

    print("Iniciando lectura del dataset transaccional...")
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    print("Aplicando reglas de limpieza tipografica en memoria...")
    if "Description" in df.columns:
        df["Description"] = df["Description"].apply(clean_special_chars)
        df["Description"] = df["Description"].apply(normalize_spacing)

    if "CustomerID" in df.columns:
        df["CustomerID"] = df["CustomerID"].astype(str).str.strip()

    if "InvoiceNo" in df.columns:
        df["InvoiceNo"] = df["InvoiceNo"].apply(validate_invoice_format)

    engine = create_engine(build_connection_string())

    print("Cargando informacion al esquema de transicion (staging)...")
    df.to_sql(
        name="stg_ecommerce_sales",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi",
    )

    print("El proceso de ingesta ha finalizado con exito.")


if __name__ == "__main__":
    run_ingestion()
