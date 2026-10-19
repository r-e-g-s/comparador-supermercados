import requests
import re

def buscar_jumbo(texto):

    url = (
        f"https://www.jumbo.cl/busqueda?ft={texto}"
    )

    r = requests.get(
        url,
        headers={
            "User-Agent":"Mozilla/5.0"
        }
    )

    html = r.text

    encontrados = re.findall(
        r'"name":"([^"]+)".{0,500}?"price":"?(\d+)',
        html,
        flags=re.DOTALL
    )

    productos = []

    for nombre, precio in encontrados:

        productos.append({
            "nombre": nombre,
            "precio": int(precio)
        })

    return productos
