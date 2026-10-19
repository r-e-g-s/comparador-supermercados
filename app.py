import streamlit as st
import requests

st.title("Diagnóstico Líder")

url = "https://super.lider.cl/v/leche"

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

st.write("Status:", r.status_code)

texto = r.text

patrones = []

for patron in [

    "__NEXT_DATA__",

    "price",

    "products",

    '"name"',

    '"offers"',

    "itemOffered",

    "productName",

    "seller"

]:

    if patron in texto:

        patrones.append(patron)

st.write("Patrones encontrados:")

st.write(patrones)

st.divider()

st.write("Primeros 5000 caracteres:")

st.text(texto[:5000])
