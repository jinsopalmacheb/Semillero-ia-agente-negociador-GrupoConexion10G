from flask import Flask, render_template, request
from datetime import datetime
from dateutil import parser
import os
import re

app = Flask(__name__)

# -------------------------
# FUNCIONES DEL AGENTE IA
# -------------------------

def detectar_intencion(mensaje):
    mensaje = mensaje.lower()

    if any(palabra in mensaje for palabra in ["pagar", "pago", "cancelar deuda", "voy a pagar", "puedo pagar"]):
        return "Promesa de pago"

    if any(palabra in mensaje for palabra in ["cancelar servicio", "dar de baja", "cancelar contrato"]):
        return "Cancelación"

    return "Sin intención clara"


def detectar_fecha(mensaje):
    try:
        # Buscar fechas tipo "15 de marzo", "20/03/2026", etc.
        match = re.search(r"\d{1,2}.*?(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)", mensaje.lower())
        if match:
            fecha = parser.parse(match.group(), dayfirst=True)
            return fecha.strftime("%d/%m/%Y")

        # Intentar detección automática
        fecha = parser.parse(mensaje, fuzzy=True, dayfirst=True)
        return fecha.strftime("%d/%m/%Y")

    except:
        return "No detectada"


# -------------------------
# RUTAS WEB
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        intencion = detectar_intencion(mensaje)
        fecha = detectar_fecha(mensaje)

        resultado = {
            "cliente": "Sector Hogar",
            "intencion": intencion,
            "fecha": fecha
        }

        # Guardar promesa tipo factura
        with open("factura_promesa.txt", "w", encoding="utf-8") as f:
            f.write(
                f"Cliente: Sector Hogar\n"
                f"DEUDA PENDIENTE\n"
                f"Promesa de pago: {fecha}\n"
            )

    return render_template("index.html", resultado=resultado)


# -------------------------
# CONFIGURACIÓN PARA RENDER
# -------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
