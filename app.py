from flask import Flask, render_template, request, send_file
from src.main import generar_promesa
from src.config.settings import AGENT_NAME, COMPANY_NAME
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        mensaje = request.form["mensaje"]
        resultado = generar_promesa(mensaje)

    return render_template(
        "index.html",
        resultado=resultado,
        agent_name=AGENT_NAME,
        company_name=COMPANY_NAME
    )


@app.route("/factura")
def factura():
    contenido = """FACTURA DE PROMESA DE PAGO

Cliente: Sector Hogar
Empresa: Netlife

Estado: Deuda Pendiente
Fecha de compromiso: 20/03/2026

Gracias por su compromiso.
"""

    ruta = "factura_promesa.txt"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

    return send_file(ruta, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
