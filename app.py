import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Comparador Supermercados",
    page_icon="🛒",
    layout="wide"
)

# ===================================================
# DEMO
# ===================================================

PRODUCTOS = {

    "leche proteina":{

        "jumbo":[
            {
                "nombre":"Leche Full Proteina Cappuccino 250ml",
                "precio":1390
            },
            {
                "nombre":"Leche Full Proteina Chocolate 250ml",
                "precio":1450
            }
        ],

        "lider":[
            {
                "nombre":"Leche Full Proteina Cappuccino 250ml",
                "precio":1490
            },
            {
                "nombre":"Leche Full Proteina Chocolate 250ml",
                "precio":1550
            }
        ]

    },

    "arroz":{

        "jumbo":[
            {
                "nombre":"Arroz Tucapel 1kg",
                "precio":1990
            }
        ],

        "lider":[
            {
                "nombre":"Arroz Tucapel 1kg",
                "precio":1890
            }
        ]

    }

}

# ===================================================
# SESSION
# ===================================================

if "carro" not in st.session_state:
    st.session_state.carro = []

# ===================================================
# TITULO
# ===================================================

st.title("🛒 Comparador Supermercados")

st.write(
    "Busca productos y arma tu carrito."
)

# ===================================================
# BUSCADOR
# ===================================================

busqueda = st.text_input(
    "Buscar producto"
)

# ===================================================
# RESULTADOS
# ===================================================

if busqueda:

    clave = busqueda.lower().strip()

    if clave in PRODUCTOS:

        datos = PRODUCTOS[clave]

        st.subheader("Selecciona productos")

        col1, col2 = st.columns(2)

        with col1:

            opciones_jumbo = [
                f"{x['nombre']} (${x['precio'\]:,})"
                for x in datos["jumbo"]
            ]

            jumbo_sel = st.radio(
                "Jumbo",
                opciones_jumbo
            )

        with col2:

            opciones_lider = [
                f"{x['nombre']} (${x['precio'\]:,})"
                for x in datos["lider"]
            ]

            lider_sel = st.radio(
                "Líder",
                opciones_lider
            )

        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            value=1
        )

        if st.button("Agregar al carrito"):

            jumbo_idx = opciones_jumbo.index(
                jumbo_sel
            )

            lider_idx = opciones_lider.index(
                lider_sel
            )

            producto = {

                "producto":
                    jumbo_sel.split(" ($")[0],

                "jumbo":
                    datos["jumbo"][jumbo_idx]["precio"],

                "lider":
                    datos["lider"][lider_idx]["precio"],

                "cantidad":
                    cantidad
            }

            st.session_state.carro.append(
                producto
            )

            st.success(
                "Producto agregado."
            )

    else:

        st.warning(
            "No se encontraron coincidencias."
        )

# ===================================================
# CARRITO
# ===================================================

st.divider()

st.subheader("🛒 Carrito")

if len(st.session_state.carro) == 0:

    st.info(
        "Carrito vacío."
    )

else:

    eliminar = None

    for i, item in enumerate(
        st.session_state.carro
    ):

        col1, col2 = st.columns([8,1])

        with col1:

            st.write(
                f"{item['producto']} "
                f"x{item['cantidad']}"
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
# COMPARACION
# ===================================================

if len(st.session_state.carro) > 0:

    total_jumbo = 0
    total_lider = 0
    total_mixto = 0

    for item in st.session_state.carro:

        jumbo_total = (
            item["jumbo"]
            * item["cantidad"]
        )

        lider_total = (
            item["lider"]
            * item["cantidad"]
        )

        total_jumbo += jumbo_total
        total_lider += lider_total

        total_mixto += min(
            jumbo_total,
            lider_total
        )

    st.divider()

    st.subheader(
        "📊 Resumen"
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
        f"Ahorro potencial: ${ahorro:,.0f}"
    )

