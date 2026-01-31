from flask import Flask, render_template, request
import re
import unicodedata
from datetime import datetime
import os

app = Flask(__name__)

MESES = {
    "enero": "01", "febrero": "02", "marzo": "03",
    "abril": "04", "mayo": "05", "junio": "06",
    "julio": "07", "agosto": "08", "septiembre": "09",
    "octubre": "10", "noviembre": "11", "diciembre": "12"
}

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def detectar_fecha(texto):
    texto = normalizar_texto(texto)
    patron = r"(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)"
    match = re.search(patron, texto)

    if match:
        dia = match.group(1).zfill(2)
        mes = MESES[match.group(2)]
        anio = datetime.now().year
        return f"{dia}/{mes}/{anio}"

    return ""

def generar_factura(fecha):
    with open("factura_promesa.txt", "w", encoding="utf-8") as f:
        f.write(
            f"FACTURA DE PROMESA DE PAGO\n\n"
            f"Cliente: Sector Hogar\n"
            f"Estado: Deuda Pendiente\n"
            f"Fecha de pago: {fecha}\n"
        )

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}

    if request.method == "POST":
        mensaje = request.form.get("mensaje", "")
        fecha = detectar_fecha(mensaje)

        if fecha:
            generar_factura(fecha)

        resultado = {
            "cliente": "Sector Hogar",
            "sector": "Hogar",
            "estado": "Deuda Pendiente",
            "intencion": "Promesa de pago",
            "fecha": fecha
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
