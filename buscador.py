import requests
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def buscar_jumbo(texto):

    url = f"https://www.jumbo.cl/busqueda?ft={texto}"

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    html = r.text

    encontrados = re.findall(
        r'"name":"([^"]+)".{0,500}?"price":"?(\d+)',
        html,
        flags=re.DOTALL
    )

    productos = []

    vistos = set()

    for nombre, precio in encontrados:

        clave = (nombre, precio)

        if clave in vistos:
            continue

        vistos.add(clave)

        productos.append({
            "nombre": nombre,
            "precio": int(precio)
        })

    return productos


def buscar_lider(texto):

    url = f"https://super.lider.cl/v/{texto}"

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    html = r.text

    encontrados = re.findall(
        r'"name":"([^"]+)".{0,500}?"price":"?(\d+)',
        html,
        flags=re.DOTALL
    )

    productos = []

    vistos = set()

    for nombre, precio in encontrados:

        clave = (nombre, precio)

        if clave in vistos:
            continue

        vistos.add(clave)

        productos.append({
            "nombre": nombre,
            "precio": int(precio)
        })

    return productos
