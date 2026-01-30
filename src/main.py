from dateutil import parser
from datetime import datetime
from src.cartera import consultar_cartera

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

def detectar_fecha(texto):
    texto = texto.lower()
    hoy = datetime.now()

    mes_detectado = None
    for mes, num in MESES.items():
        if mes in texto:
            mes_detectado = num
            break

    try:
        fecha = parser.parse(texto, fuzzy=True, dayfirst=True, default=hoy)

        if mes_detectado:
            fecha = fecha.replace(month=mes_detectado)

        if fecha.date() < hoy.date():
            fecha = fecha.replace(year=hoy.year + 1)

        return fecha.strftime("%d/%m/%Y")
    except:
        return None


def detectar_intencion(texto):
    texto = texto.lower()
    if "pagar" in texto or "cancelar" in texto:
        return "Promesa de pago"
    return "Sin intención clara"


def generar_promesa(mensaje):
    cartera = consultar_cartera()
    intencion = detectar_intencion(mensaje)
    fecha = detectar_fecha(mensaje)

    return {
        "cliente": cartera["cliente"],
        "sector": cartera["sector"],
        "deuda": cartera["deuda"],
        "intencion": intencion,
        "fecha": fecha
    }
