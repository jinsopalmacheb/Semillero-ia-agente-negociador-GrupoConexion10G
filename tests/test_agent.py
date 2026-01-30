from src.main import detectar_intencion, detectar_fecha

def test_intencion():
    assert detectar_intencion("Voy a pagar mañana") == "Promesa de pago"

def test_fecha():
    assert detectar_fecha("el 15 de febrero") is not None
