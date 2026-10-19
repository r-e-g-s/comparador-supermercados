import streamlit as st
import pandas as pd

from buscador import (
    buscar_jumbo,
    buscar_lider
)

from difflib import SequenceMatcher

def encontrar_equivalentes(
    producto_jumbo,
    productos_lider
):

    palabras_jumbo = set(
        producto_jumbo["nombre"]
        .lower()
        .split()
    )

    ranking = []

    for producto in productos_lider:

        nombre_lider = producto["nombre"].lower()

        palabras_lider = set(
            nombre_lider.split()
        )

        comunes = len(
            palabras_jumbo.intersection(
                palabras_lider
            )
        )

        similitud = SequenceMatcher(
            None,
            producto_jumbo["nombre"].lower(),
            nombre_lider
        ).ratio()

        score = (
            comunes * 1000
            + similitud * 100
        )

        ranking.append(
            (score, producto)
        )

    ranking.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        x[1]
        for x in ranking[:3]
    ]

# ===================================================
# CONFIG
# ===================================================

st.set_page_config(
    page_title="Comparador Supermercados",
    page_icon="🛒",
    layout="wide"
)

# ===================================================
# SESSION
# ===================================================

if "carro" not in st.session_state:
    st.session_state.carro = []

# Limpia registros antiguos
st.session_state.carro = [
    item
    for item in st.session_state.carro
    if "lider" in item
]

# ===================================================
# TITULO
# ===================================================

st.title("🛒 Comparador Supermercados")

st.write(
    "Busca productos y compara Jumbo vs Líder."
)

# ===================================================
# BUSCADOR
# ===================================================

texto = st.text_input(
    "Buscar producto"
)

if texto:

    try:

        jumbo = buscar_jumbo(texto)
        lider = buscar_lider(texto)

        st.subheader(
            f"Jumbo ({len(jumbo)})"
        )

        opciones_jumbo = [
            f"{x['nombre']} (${x['precio'\]:,})"
            for x in jumbo[:20]
        ]

        jumbo_sel = st.radio(
            "Seleccione producto",
            opciones_jumbo
        )

        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            value=1
        )

        idx_jumbo = opciones_jumbo.index(
            jumbo_sel
        )

        producto_jumbo = jumbo[idx_jumbo]

        # TOP 3 equivalencias en Lider
        equivalentes = encontrar_equivalentes(
            producto_jumbo,
            lider
        )

        if len(equivalentes) == 0:

            st.warning(
                "No se encontraron equivalencias en Líder."
            )

            st.stop()

        opciones_lider = [
            f"{x['nombre']} (${x['precio'\]:,})"
            for x in equivalentes
        ]

        st.subheader(
            "Posibles equivalencias en Líder"
        )

        lider_sel = st.radio(
            "Seleccione el equivalente correcto",
            opciones_lider
        )

        idx_lider = opciones_lider.index(
            lider_sel
        )

        producto_lider = equivalentes[
            idx_lider
        ]

        st.divider()

        st.subheader(
            "Comparación"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("### Jumbo")

            st.write(
                producto_jumbo["nombre"]
            )

            st.metric(
                "Precio",
                f"${producto_jumbo['precio'\]:,}"
            )

        with col2:

            st.write("### Líder")

            st.write(
                producto_lider["nombre"]
            )

            st.metric(
                "Precio",
                f"${producto_lider['precio'\]:,}"
            )

        diferencia = (
            producto_jumbo["precio"]
            - producto_lider["precio"]
        )

        if diferencia > 0:

            st.success(
                f"✅ Líder es ${abs(diferencia):,} más barato"
            )

        elif diferencia < 0:

         t.success(
                f"✅ Jumbo es ${abs(diferencia):,} más barato"
            )

        else:

            st.info(
                "✅ Ambos tienen el mismo precio"
            )

        if st.button(
            "Agregar al carrito"
        ):

            st.session_state.carro.append({

                "producto_jumbo":
                    producto_jumbo["nombre"],

                "producto_lider":
                    producto_lider["nombre"],

                "jumbo":
                    producto_jumbo["precio"],

                "lider":
                    producto_lider["precio"],

                "cantidad":
                    cantidad

            })

            st.success(
                "Producto agregado al carrito."
            )

    except Exception as e:

        st.error(
            f"Error en búsqueda: {e}"
        )


# ===================================================
# CARRITO
# ===================================================

st.divider()

st.subheader("🛒 Carrito")

if st.button("🗑 Vaciar carrito"):

    st.session_state.carro = []

    st.rerun()

if len(st.session_state.carro) == 0:

    st.info("Carrito vacío.")

else:

    eliminar = None

    for i, item in enumerate(
        st.session_state.carro
    ):

        col1, col2 = st.columns([8, 1])

        with col1:

            st.write(
                f"**Jumbo:** {item['producto_jumbo']}"
            )

            st.write(
                f"**Líder:** {item['producto_lider']}"
            )

            st.write(
                f"Cantidad: {item['cantidad']}"
            )

            mejor = (
                "Jumbo"
                if item["jumbo"] < item["lider"]
                else "Líder"
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

# ===================================================
# RESUMEN
# ===================================================

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

        mejor = (
            "Jumbo"
            if jumbo_total < lider_total
            else "Líder"
        )

        total_jumbo += jumbo_total
        total_lider += lider_total
        total_mixto += mixto

        detalle.append({

            "Producto Jumbo":
                item["producto_jumbo"],

            "Producto Líder":
                item["producto_lider"],

            "Cantidad":
                item["cantidad"],

            "Total Jumbo":
                jumbo_total,

            "Total Líder":
                lider_total,

            "Mejor":
                mejor

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
        max(total_jumbo, total_lider)
        - total_mixto
    )

    st.success(
        f"💰 Ahorro potencial: ${ahorro:,.0f}"
    )
