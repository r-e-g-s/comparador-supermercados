import streamlit as st
import requests
import re

st.title("Diagnóstico Jumbo 2")

url = "https://www.jumbo.cl/busqueda?ft=leche"

r = requests.get(
    url,
    headers={
        "User-Agent": (
            "Mozilla/5.0 "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/125.0 Safari/537.36"
        )
    }
)

texto = r.text

st.write("Status:", r.status_code)

coincidencias = []

for patron in [

    "__NEXT_DATA__",

    "price",

    "sellingPrice",

    "products",

    '"name"',

    '"offers"'

\]:

    if patron in texto:

        coincidencias.append(patron)

st.write("Patrones encontrados:")

st.write(coincidencias)
