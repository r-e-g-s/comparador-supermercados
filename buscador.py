import requests
import json
import re

from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote


session = requests.Session()

session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    ),
    "Accept-Language": "es-CL,es;q=0.9"
})


def precio_clp(valor):

    if valor is None:
        return None

    texto = str(valor).replace("$", "").strip()

    texto = texto.replace(".", "")

    if texto.isdigit():
        return int(texto)

    return None


def buscar_jumbo(texto):

    url = (
        "https://www.jumbo.cl/busqueda?"
        + urlencode({"ft": texto})
    )

    try:

        r = session.get(
            url,
            timeout=20
        )

        soup = BeautifulSoup(
            r.text,
            "lxml"
        )

        resultados = []

        for script in soup.select(
            'script[type="application/ld+json"]'
        ):

            try:

                data = json.loads(
                    script.string
                )

                if isinstance(data, list):

                    for item in data:

                        if (
                            isinstance(item, dict)
                            and item.get("@type") == "Product"
                        ):

                            precio = None

                            ofertas = item.get(
                                "offers",
                                {}
                            )

                            if isinstance(
                                ofertas,
                                dict
                            ):
                                precio = ofertas.get(
                                    "price"
                                )

                            resultados.append({
                                "nombre": item.get(
                                    "name"
                                ),
                                "precio": precio_clp(
                                    precio
                                )
                            })

            except:
                pass

        return resultados[:20]

    except Exception as e:

        return [
            {
                "nombre": f"ERROR JUMBO: {e}",
                "precio": None
            }
        ]


def buscar_lider(texto):

    slug = re.sub(
        r"\s+",
        "-",
        texto.lower()
    )

    url = (
        f"https://super.lider.cl/v/{quote(slug)}"
    )

    try:

        r = session.get(
            url,
            timeout=20
        )

        return [
            {
                "nombre":
                    f"HTTP {r.status_code}",
                "precio":
                    None
            }
        ]

    except Exception as e:

        return [
            {
                "nombre":
                    f"ERROR LIDER: {e}",
                "precio":
                    None
            }
        ]