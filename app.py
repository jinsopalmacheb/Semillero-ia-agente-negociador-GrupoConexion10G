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

    patron = r"(\d{1,2})\s*(?:de)?\s*(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)"
    match = re.search(patron, texto)

    if match:
        dia = match.group(1).zfill(2)
        mes = MESES[match.group(2)]
        anio = datetime.now().year
        return f"{dia}/{mes}/{anio}"

    return "No detectada"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        mensaje = request.form.get("mensaje", "")
        mensaje_norm = normalizar_texto(mensaje)

        resultado = {
            "cliente": "Sector Hogar",
            "sector": "Hogar",
            "estado": "DEUDA PENDIENTE",
            "intencion": "Promesa de pago" if "pagar" in mensaje_norm else "Sin intención clara",
            "fecha_pago": detectar_fecha(mensaje)
        }

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
