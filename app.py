import streamlit as st
import requests

st.title("Diagnóstico Jumbo")

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

st.write("Status:", r.status_code)

st.write("Primeros 5000 caracteres")

st.text(r.text[:5000])
