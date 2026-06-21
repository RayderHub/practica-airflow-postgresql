import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "data.csv"
OUTPUT_DIR = ROOT / "entrega_practica_ia_datos"
RANDOM_STATE = 42
SAMPLES_PER_CLASS = 10000
TRAIN_RATIO = 0.8


def clean_description(value):
    if pd.isna(value):
        return "SIN_DESCRIPTION"
    value = str(value).upper()
    value = re.sub(r"[^A-Z0-9\s\-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or "SIN_DESCRIPTION"


def clean_country(value):
    if pd.isna(value):
        return "SIN_PAIS"
    value = str(value).upper()
    value = re.sub(r"[^A-Z\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or "SIN_PAIS"


def valid_invoice(value):
    invoice = str(value).strip()
    return invoice if re.match(r"^C?\d{6}$", invoice) else "INVALID_INVOICE"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATASET_PATH, encoding="ISO-8859-1")
    raw_rows = len(df)
    raw_missing_customer = int(df["CustomerID"].isna().sum())
    raw_cancelled = int(df["InvoiceNo"].astype(str).str.startswith("C").sum())

    df["Description"] = df["Description"].apply(clean_description)
    df["Country"] = df["Country"].apply(clean_country)
    df["InvoiceNo"] = df["InvoiceNo"].apply(valid_invoice)
    df["CustomerID"] = df["CustomerID"].fillna("SIN_CLIENTE").astype(str).str.replace(r"\.0$", "", regex=True)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["importe_linea"] = df["Quantity"] * df["UnitPrice"]

    analytic = df[
        (df["InvoiceDate"].notna())
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
        & (df["InvoiceNo"] != "INVALID_INVOICE")
    ].copy()

    threshold = float(analytic["importe_linea"].median())
    analytic["alto_valor_transaccion"] = (analytic["importe_linea"] >= threshold).astype(int)
    analytic["mes_compra"] = analytic["InvoiceDate"].dt.month
    analytic["dia_semana"] = analytic["InvoiceDate"].dt.dayofweek

    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "importe_linea",
        "CustomerID",
        "Country",
        "mes_compra",
        "dia_semana",
        "alto_valor_transaccion",
    ]
    analytic = analytic[columns]

    balanced = (
        analytic.groupby("alto_valor_transaccion", group_keys=False)
        .sample(n=SAMPLES_PER_CLASS, random_state=RANDOM_STATE)
        .sample(frac=1, random_state=RANDOM_STATE)
        .reset_index(drop=True)
    )

    train_parts = []
    test_parts = []
    for _, group in balanced.groupby("alto_valor_transaccion"):
        group = group.sample(frac=1, random_state=RANDOM_STATE)
        split_index = int(len(group) * TRAIN_RATIO)
        train_parts.append(group.iloc[:split_index])
        test_parts.append(group.iloc[split_index:])

    train = pd.concat(train_parts).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    test = pd.concat(test_parts).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    train_path = OUTPUT_DIR / "train_ecommerce_balanced.csv"
    test_path = OUTPUT_DIR / "test_ecommerce_balanced.csv"
    notebook_path = OUTPUT_DIR / "notebook_particionamiento.txt"

    train.to_csv(train_path, index=False, encoding="utf-8")
    test.to_csv(test_path, index=False, encoding="utf-8")

    train_dist = train["alto_valor_transaccion"].value_counts(normalize=True).sort_index() * 100
    test_dist = test["alto_valor_transaccion"].value_counts(normalize=True).sort_index() * 100

    notebook_path.write_text(
        "EVIDENCIA TIPO JUPYTER - PARTICIONAMIENTO TRAIN/TEST\n"
        "======================================================\n\n"
        "Dataset usado: data/data.csv\n"
        "Contexto: transacciones de e-commerce cargadas previamente por el pipeline ETL.\n\n"
        "1. Diagnostico inicial\n"
        f"Filas crudas: {raw_rows}\n"
        f"Clientes faltantes: {raw_missing_customer}\n"
        f"Facturas canceladas detectadas por prefijo C: {raw_cancelled}\n"
        f"Filas analiticas despues de filtros: {len(analytic)}\n\n"
        "2. Variable objetivo\n"
        "alto_valor_transaccion = 1 si importe_linea >= mediana de importes positivos; 0 en caso contrario.\n"
        f"Umbral de mediana usado: {threshold:.2f}\n\n"
        "3. Codigo base del particionamiento estratificado\n"
        "balanced = analytic.groupby('alto_valor_transaccion').sample(n=10000, random_state=42)\n"
        "train = 80% de cada clase\n"
        "test = 20% de cada clase\n\n"
        "4. Resultado del particionamiento\n"
        f"Train filas: {len(train)}\n"
        f"Test filas: {len(test)}\n"
        f"Train clase 0: {train_dist.get(0, 0):.2f}%\n"
        f"Train clase 1: {train_dist.get(1, 0):.2f}%\n"
        f"Test clase 0: {test_dist.get(0, 0):.2f}%\n"
        f"Test clase 1: {test_dist.get(1, 0):.2f}%\n\n"
        "5. Archivos exportados\n"
        "train_ecommerce_balanced.csv\n"
        "test_ecommerce_balanced.csv\n",
        encoding="utf-8",
    )

    print(f"Train: {train_path} ({len(train)} filas)")
    print(f"Test: {test_path} ({len(test)} filas)")
    print(f"Evidencia: {notebook_path}")
    print(f"Distribucion train: {train['alto_valor_transaccion'].value_counts().sort_index().to_dict()}")
    print(f"Distribucion test: {test['alto_valor_transaccion'].value_counts().sort_index().to_dict()}")


if __name__ == "__main__":
    main()
