from flask import Flask, render_template, request
import re
from datetime import datetime

app = Flask(__name__)

# ==============================
# DICCIONARIO DE MESES
# ==============================
MESES = {
    "enero": "01", "febrero": "02", "marzo": "03",
    "abril": "04", "mayo": "05", "junio": "06",
    "julio": "07", "agosto": "08", "septiembre": "09",
    "octubre": "10", "noviembre": "11", "diciembre": "12"
}

# ==============================
# FUNCIÓN DETECTAR FECHA
# ==============================
def detectar_fecha_texto(mensaje):
    mensaje = mensaje.lower()

    # Formato numérico: 20/03/2026 o 20-03-2026
    match_numerico = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", mensaje)
    if match_numerico:
        dia, mes, anio = match_numerico.groups()
        return f"{dia.zfill(2)}/{mes.zfill(2)}/{anio}"

    # Formato texto: 20 de marzo
    match_texto = re.search(r"(\d{1,2})\s+de\s+([a-záéíóú]+)", mensaje)
    if match_texto:
        dia, mes_texto = match_texto.groups()
        mes_texto = mes_texto.lower()

        if mes_texto in MESES:
            mes = MESES[mes_texto]
            anio = datetime.now().year
            return f"{dia.zfill(2)}/{mes}/{anio}"

    return "No detectada"

# ==============================
# RUTA PRINCIPAL
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        mensaje_usuario = request.form.get("mensaje", "")

        # Lógica del agente
        cliente = "Sector Hogar"
        sector = ""
        estado = "Deuda Pendiente"

        if "pagar" in mensaje_usuario.lower():
            intencion = "Promesa de pago"
        else:
            intencion = "Sin intención clara"

        fecha_pago = detectar_fecha_texto(mensaje_usuario)

        resultado = {
            "cliente": cliente,
            "sector": sector,
            "estado": estado,
            "intencion": intencion,
            "fecha_pago": fecha_pago
        }

    return render_template("index.html", resultado=resultado)

# ==============================
# EJECUCIÓN (RENDER)
# ==============================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
