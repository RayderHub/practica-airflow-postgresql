from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "entrega_practica_ia_datos" / "analisis_comparativo_casos.pdf"
ARIAL = Path("C:/Windows/Fonts/arial.ttf")
ARIAL_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")


def register_fonts():
    if ARIAL.exists():
        pdfmetrics.registerFont(TTFont("Arial", str(ARIAL)))
    if ARIAL_BOLD.exists():
        pdfmetrics.registerFont(TTFont("Arial-Bold", str(ARIAL_BOLD)))


def styles():
    register_fonts()
    font = "Arial" if ARIAL.exists() else "Helvetica"
    bold = "Arial-Bold" if ARIAL_BOLD.exists() else "Helvetica-Bold"
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(name="TitleCustom", fontName=bold, fontSize=15, alignment=TA_CENTER, leading=18, spaceAfter=8))
    base.add(ParagraphStyle(name="SubtitleCustom", fontName=font, fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=14))
    base.add(ParagraphStyle(name="Heading1Custom", fontName=bold, fontSize=13, leading=16, spaceBefore=10, spaceAfter=6))
    base.add(ParagraphStyle(name="Heading2Custom", fontName=bold, fontSize=11, leading=14, spaceBefore=8, spaceAfter=4))
    base.add(ParagraphStyle(name="BodyCustom", fontName=font, fontSize=9.5, leading=12, spaceAfter=5))
    base.add(ParagraphStyle(name="BulletCustom", fontName=font, fontSize=9.5, leading=12, leftIndent=12, firstLineIndent=-8, spaceAfter=3))
    return base


def p(text, style):
    return Paragraph(text.replace("&", "&amp;"), style)


def bullets(items, story, style):
    for item in items:
        story.append(p(f"• {item}", style))


def table(data, story, style):
    rows = [[p(str(cell), style) for cell in row] for row in data]
    t = Table(rows, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold" if ARIAL_BOLD.exists() else "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 8))


def build_pdf():
    s = styles()
    story = []
    story.append(p("Analisis comparativo de IA, Machine Learning, Data Mining y Big Data", s["TitleCustom"]))
    story.append(p("Casos de estudio y aplicacion a la practica ETL", s["SubtitleCustom"]))
    story.append(p("Alumno: Rayder", s["BodyCustom"]))
    story.append(p("Repositorio de apoyo: https://github.com/RayderHub/practica-airflow-postgresql", s["BodyCustom"]))

    story.append(p("1. Analisis comparativo", s["Heading1Custom"]))
    story.append(p("La inteligencia artificial, machine learning, data mining y big data se relacionan, pero no son lo mismo. La IA es el campo mas amplio; machine learning aprende de datos; data mining descubre patrones; y big data permite manejar informacion masiva o compleja.", s["BodyCustom"]))
    table(
        [
            ["Concepto", "Caracteristicas", "Beneficios", "Retos", "Aplicaciones", "Herramientas"],
            ["IA", "Sistemas que simulan capacidades humanas como razonar o decidir.", "Automatiza y mejora decisiones.", "Datos, sesgos y explicabilidad.", "Chatbots, fraude, recomendaciones.", "Python, TensorFlow, PyTorch."],
            ["Machine learning", "Modelos que aprenden patrones desde datos.", "Predice y clasifica comportamientos.", "Sobreajuste y calidad de variables.", "Churn, ventas, spam.", "Scikit-learn, XGBoost, Jupyter."],
            ["Data mining", "Busca patrones y relaciones en datos historicos.", "Convierte datos en conocimiento util.", "Interpretar bien correlaciones.", "Segmentacion, canasta de mercado.", "SQL, Python, Weka, Power BI."],
            ["Big data", "Procesa volumen, velocidad y variedad de datos.", "Analisis masivo y casi en tiempo real.", "Costo, infraestructura y gobierno de datos.", "Logs, sensores, redes sociales.", "Spark, Hadoop, Kafka, BigQuery."],
        ],
        story,
        s["BodyCustom"],
    )

    story.append(p("2. Caso de estudio 1: Electro-Hogar S.A.", s["Heading1Custom"]))
    story.append(p("Objetivo y alcance", s["Heading2Custom"]))
    story.append(p("El objetivo es analizar el comportamiento historico de los clientes para identificar factores asociados al abandono, mejorar la retencion y aumentar el valor de vida del cliente. El alcance incluye ventas, clientes, productos, promociones, canales, ubicacion y servicio postventa.", s["BodyCustom"]))
    bullets(["Identificar clientes que no realizan segunda compra.", "Segmentar por recencia, frecuencia y monto.", "Detectar variables relacionadas con abandono.", "Proponer acciones de retencion basadas en datos."], story, s["BulletCustom"])
    story.append(p("Metodologia", s["Heading2Custom"]))
    story.append(p("La metodologia recomendada es CRISP-DM, porque permite iniciar con el entendimiento del negocio y de los datos antes de pasar a modelos. Tambien se propone analisis RFM para clasificar clientes por recencia, frecuencia y valor monetario.", s["BodyCustom"]))
    table(
        [
            ["Etapa", "Actividad"],
            ["Negocio", "Definir abandono e indicadores como recompra, ticket promedio y valor de vida."],
            ["Datos", "Revisar fuentes, faltantes, duplicados y formatos."],
            ["Preparacion", "Integrar ventas y clientes; crear variables utiles."],
            ["Exploracion", "Comparar clientes retenidos y no retenidos."],
            ["Segmentacion", "Aplicar RFM y clustering."],
            ["Modelado", "Preparar variable objetivo y particion train/test."],
            ["Acciones", "Proponer campanas, promociones y fidelizacion."],
        ],
        story,
        s["BodyCustom"],
    )

    story.append(p("3. Caso de estudio 2: Practica ETL", s["Heading1Custom"]))
    story.append(p("El dataset usado corresponde a ventas de e-commerce. Aunque la instruccion menciona contrataciones, se adapta el analisis al contexto real de la practica ETL realizada con Airflow, PostgreSQL y Python.", s["BodyCustom"]))
    story.append(p("Diagnostico inicial", s["Heading2Custom"]))
    bullets(["Filas crudas: 541,909.", "Clientes faltantes: 135,080.", "Descripciones faltantes: 1,454.", "Facturas canceladas: 9,288.", "Registros duplicados: 5,268.", "Cantidades negativas: 10,624.", "Precios unitarios menores o iguales a cero: 2,517."], story, s["BulletCustom"])
    story.append(p("Grano de la tabla de hechos", s["Heading2Custom"]))
    story.append(p("El grano seleccionado es una linea de producto dentro de una factura de venta. Este nivel conserva el detalle necesario para analizar ventas por producto, cliente, pais, fecha y factura.", s["BodyCustom"]))
    story.append(p("Esquema de data warehouse", s["Heading2Custom"]))
    table(
        [
            ["Tabla", "Tipo", "Contenido"],
            ["fact_venta_linea", "Hechos", "fecha, cliente, producto, pais, factura, cantidad, precio, importe y variable objetivo."],
            ["dim_fecha", "Dimension", "Dia, mes, anio, trimestre y dia de semana."],
            ["dim_cliente", "Dimension", "Cliente original, segmento y bandera de cliente identificado."],
            ["dim_producto", "Dimension", "Codigo, descripcion limpia y categoria estimada."],
            ["dim_pais", "Dimension", "Pais limpio y region."],
            ["dim_factura", "Dimension", "Factura, tipo y cancelacion."],
        ],
        story,
        s["BodyCustom"],
    )
    story.append(p("Limpieza y expresiones regulares", s["Heading2Custom"]))
    table(
        [
            ["Objetivo", "Regex", "Uso"],
            ["Limpiar descripciones", r"[^A-Z0-9\s\-]", "Quita simbolos y caracteres corruptos."],
            ["Normalizar espacios", r"\s+", "Convierte varios espacios en uno."],
            ["Validar facturas", r"^C?\d{6}$", "Acepta facturas y cancelaciones."],
            ["Variantes corporativas", r"\b(SA DE CV|SAPI DE CV|SRL|SC|AC)\b", "Homologa proveedores si el dataset fuera de contrataciones."],
        ],
        story,
        s["BodyCustom"],
    )
    story.append(p("Variable objetivo y particionamiento", s["Heading2Custom"]))
    story.append(p("Se creo la variable binaria alto_valor_transaccion. Vale 1 cuando el importe de la linea es igual o mayor a la mediana de importes positivos, y 0 cuando es menor. Se exportaron archivos balanceados para la fase de mineria de datos.", s["BodyCustom"]))
    table(
        [
            ["Archivo", "Registros", "Clase 0", "Clase 1"],
            ["train_ecommerce_balanced.csv", "16,000", "8,000", "8,000"],
            ["test_ecommerce_balanced.csv", "4,000", "2,000", "2,000"],
        ],
        story,
        s["BodyCustom"],
    )

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch, topMargin=0.65 * inch, bottomMargin=0.65 * inch)
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
