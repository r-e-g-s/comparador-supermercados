import streamlit as st
import requests
import re

st.title("Extractor Líder")

texto = st.text_input(
    "Buscar",
    value="leche"
)

if st.button("Buscar"):

    url = (
        f"https://super.lider.cl/v/{texto}"
    )

    r = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )

    html = r.text

    encontrados = re.findall(
        r'"name":"([^"]+)".{0,500}?"price":"?(\d+)',
        html,
        flags=re.DOTALL
    )

    st.write(
        f"Coincidencias encontradas: {len(encontrados)}"
    )

    for nombre, precio in encontrados[:20\]:

        st.write({
            "nombre": nombre,
            "precio": precio
        })
