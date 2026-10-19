import streamlit as st

from buscador import (
    buscar_jumbo,
    buscar_lider
)

st.set_page_config(
    page_title="Prueba Buscador",
    page_icon="🛒"
)

st.title(
    "Prueba de búsqueda supermercados"
)

texto = st.text_input(
    "Buscar producto"
)

if st.button("Buscar"):

    st.subheader("Jumbo")

    jumbo = buscar_jumbo(texto)

    st.write(jumbo)

    st.subheader("Líder")

    lider = buscar_lider(texto)

    st.write(lider)
