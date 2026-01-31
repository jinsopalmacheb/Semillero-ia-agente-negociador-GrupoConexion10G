from flask import Flask, render_template, request
import re
import unicodedata
from datetime import datetime

app = Flask(__name__)

# -------------------------
# Diccionario de meses
# -------------------------
MESES = {
    "enero": "01", "febrero": "02", "marzo": "03",
    "abril": "04", "mayo": "05", "junio": "06",
    "julio": "07", "agosto": "08", "septiembre": "09",
    "octubre": "10", "noviembre": "11", "diciembre": "12"
}

# -------------------------
# Normalizar texto
# -------------------------
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

# -------------------------
# Detectar fecha tipo:
# "20 de marzo" -> "20/03/2026"
# -------------------------
def detectar_fecha(texto):
    texto = normalizar_texto(texto)

    patron = r"(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)"
    match = re.search(patron, texto)

    if match:
        dia = match.group(1).zfill(2)
        mes = MESES[match.group(2)]
        anio = datetime.now().year
        return f"{dia}/{mes}/{anio}"

    return "No detectada"

# -------------------------
# Ruta principal
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        mensaje = request.form.get("mensaje", "")
        mensaje_norm = normalizar_texto(mensaje)

        # Lógica del agente
        fecha_pago = detectar_fecha(mensaje)
        intencion = "Promesa de pago" if "pagar" in mensaje_norm else "Sin intención clara"

        # Datos fijos para la demo
        resultado = {
            "cliente": "Sector Hogar",
            "sector": "Hogar",
            "estado": "DEUDA PENDIENTE",
            "intencion": intencion,
            "fecha_pago": fecha_pago
        }

    return render_template("index.html", resultado=resultado)

# -------------------------
# Inicio de la app
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
