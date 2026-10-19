import requests
import re

from difflib import SequenceMatcher

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def limpiar(texto):

    texto = str(texto).lower()

    texto = re.sub(
        r"[^a-z0-9áéíóúñ ]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def puntaje(busqueda, nombre):

    busqueda_limpia = limpiar(busqueda)
    nombre_limpio = limpiar(nombre)

    palabras_busqueda = set(
        busqueda_limpia.split()
    )

    palabras_producto = set(
        nombre_limpio.split()
    )

    coincidencias = len(
        palabras_busqueda.intersection(
            palabras_producto
        )
    )

    score_texto = SequenceMatcher(
        None,
        busqueda_limpia,
        nombre_limpio
    ).ratio()

    return (
        coincidencias * 1000
        + score_texto
    )


def ordenar_productos(
    productos,
    busqueda
):

    for producto in productos:

        producto["score"] = puntaje(
            busqueda,
            producto["nombre"]
        )

    productos.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return productos


def buscar_jumbo(texto):

    url = (
        f"https://www.jumbo.cl/busqueda?ft={texto}"
    )

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

        clave = (
            nombre.lower().strip(),
            precio
        )

        if clave in vistos:
            continue

        vistos.add(clave)

        productos.append({
            "nombre": nombre,
            "precio": int(precio)
        })

    return ordenar_productos(
        productos,
        texto
    )


def buscar_lider(texto):

    busqueda_url = texto.replace(
        " ",
        "%20"
    )

    url = (
        f"https://super.lider.cl/v/{busqueda_url}"
    )

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

        clave = (
            nombre.lower().strip(),
            precio
        )

        if clave in vistos:
            continue

        vistos.add(clave)

        productos.append({
            "nombre": nombre,
            "precio": int(precio)
        })

    return ordenar_productos(
        productos,
        texto
    )
