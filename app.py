import streamlit as st
import pandas as pd

from buscador import (
    buscar_jumbo,
    buscar_lider
)

st.set_page_config(
    page_title="Comparador Supermercados",
    page_icon="🛒",
    layout="wide"
)

if "carro" not in st.session_state:
    st.session_state.carro = []

st.title("🛒 Comparador Supermercados")

texto = st.text_input(
    "Buscar producto"
)

if texto:

    jumbo = buscar_jumbo(texto)

    lider = buscar_lider(texto)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            f"Jumbo ({len(jumbo)})"
        )

        opciones_jumbo = [
            f"{x['nombre']} (${x['precio']:,})"
            for x in jumbo[:20]
        ]

        jumbo_sel = st.radio(
            "Producto Jumbo",
            opciones_jumbo
        )

    with col2:

        st.subheader(
            f"Líder ({len(lider)})"
        )

        opciones_lider = [
            f"{x['nombre']} (${x['precio']:,})"
            for x in lider[:20]
        ]

        lider_sel = st.radio(
            "Producto Líder",
            opciones_lider
        )

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        value=1
    )

    if st.button(
        "Agregar al carrito"
    ):

        idx_jumbo = opciones_jumbo.index(
            jumbo_sel
        )

        idx_lider = opciones_lider.index(
            lider_sel
        )

        producto = {

            "producto":
                jumbo[idx_jumbo]["nombre"],

            "jumbo":
                jumbo[idx_jumbo]["precio"],

            "lider":
                lider[idx_lider]["precio"],

            "cantidad":
                cantidad

        }

        st.session_state.carro.append(
            producto
        )

        st.success(
            "Producto agregado."
        )

st.divider()

st.subheader("🛒 Carrito")

if st.button(
    "🗑 Vaciar carrito"
):

    st.session_state.carro = []

    st.rerun()

if len(.session_state.carro) == 0:

    st.info(
        "Carrito vacío."
    )

else:

    eliminar = None

    for i, item in enumerate(
        st.session_state.carro
    ):

        col1, col2 = st.columns([8, 1])

        with col1:

            mejor = (
                "Jumbo"
                if item["jumbo"] < item["lider"]
                else "Líder"
            )

            st.write(
                f"**{item['producto']}** "
                f"x {item['cantidad']}"
            )

            st.caption(
                f"Jumbo: ${item['jumbo']:,} | "
                f"Líder: ${item['lider']:,} | "
                f"Conviene: {mejor}"
            )

        with col2:

            if st.button(
                "❌",
                key=f"del_{i}"
            ):
                eliminar = i

    if eliminar is not None:

        st.session_state.carro.pop(
            eliminar
        )

        st.rerun()

if len(st.session_state.carro) > 0:

    total_jumbo = 0
    total_lider = 0
    total_mixto = 0

    detalle = []

    for item in st.session_state.carro:

        jumbo_total = (
            item["jumbo"]
            * item["cantidad"]
        )

        lider_total = (
            item["lider"]
            * item["cantidad"]
        )

        mixto = min(
            jumbo_total,
            lider_total
        )

        total_jumbo += jumbo_total
        total_lider += lider_total
        total_mixto += mixto

        detalle.append({

            "Producto":
                item["producto"],

            "Cantidad":
                item["cantidad"],

            "Jumbo":
                jumbo_total,

            "Líder":
                lider_total,

            "Mejor":
                (
                    "Jumbo"
                    if jumbo_total < lider_total
                    else "Líder"
                )
        })

    st.divider()

    st.subheader(
        "📋 Comparación"
    )

    st.dataframe(
        pd.DataFrame(detalle),
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Jumbo",
        f"${total_jumbo:,.0f}"
    )

    c2.metric(
        "Total Líder",
        f"${total_lider:,.0f}"
    )

    c3.metric(
        "Compra Mixta",
        f"${total_mixto:,.0f}"
    )

    ahorro = (
        max(
            total_jumbo,
            total_lider
        ) - total_mixto
    )

    st.success(
        f"💰 Ahorro potencial: ${ahorro:,.0f}"
    )
