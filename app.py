import streamlit as st
import pandas as pd

# ===================================================
# CONFIG
# ===================================================

st.set_page_config(
    page_title="Comparador Supermercados",
    page_icon="🛒",
    layout="wide"
)

# ===================================================
# DEMO
# ===================================================

PRODUCTOS = {

    "leche proteina": {

        "jumbo": [
            {
                "nombre": "Leche Full Proteina Cappuccino 250ml",
                "precio": 1390
            },
            {
                "nombre": "Leche Full Proteina Chocolate 250ml",
                "precio": 1450
            }
        ],

        "lider": [
            {
                "nombre": "Leche Full Proteina Cappuccino 250ml",
                "precio": 1490
            },
            {
                "nombre": "Leche Full Proteina Chocolate 250ml",
                "precio": 1550
            }
        ]
    },

    "arroz": {

        "jumbo": [
            {
                "nombre": "Arroz Tucapel 1kg",
                "precio": 1990
            }
        ],

        "lider": [
            {
                "nombre": "Arroz Tucapel 1kg",
                "precio": 1890
            }
        ]
    },

    "aceite": {

        "jumbo": [
            {
                "nombre": "Aceite Maravilla 1L",
                "precio": 2290
            }
        ],

        "lider": [
            {
                "nombre": "Aceite Maravilla 1L",
                "precio": 2490
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

    texto = busqueda.lower().strip()

    coincidencias = []

    for clave in PRODUCTOS:

        if texto in clave:

            coincidencias.append(
                (clave, PRODUCTOS[clave])
            )

    if len(coincidencias) > 0:

        clave, datos = coincidencias[0]

        st.subheader("Selecciona productos")

        col1, col2 = st.columns(2)

        # -------------------------
        # JUMBO
        # -------------------------

        with col1:

            opciones_jumbo = [
                f"{x['nombre']} (${x['precio']:,})"
                for x in datos["jumbo"]
            ]

            jumbo_sel = st.radio(
                "Jumbo",
                opciones_jumbo
            )

        # -------------------------
        # LIDER
        # -------------------------

        with col2:

            opciones_lider = [
                f"{x['nombre']} (${x['precio']:,})"
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
                "Producto agregado correctamente."
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

if st.button("🗑 Vaciar carrito"):

    st.session_state.carro = []

    st.rerun()

if len(st.session_state.carro) > 0:

    resumen = []

    total_jumbo = 0
    total_lider = 0
    total_mixto = 0

    for item in st.session_state.carro:

        jumbo_total = (
            item["jumbo"] *
            item["cantidad"]
        )

        lider_total = (
            item["lider"] *
            item["cantidad"]
        )

        mejor = (
            "Jumbo"
            if jumbo_total < lider_total
            else "Líder"
        )

        resumen.append({

            "Producto":
                item["producto"],

            "Cantidad":
                item["cantidad"],

            "Jumbo":
                jumbo_total,

            "Líder":
                lider_total,

            "Mejor opción":
                mejor

        })

        total_jumbo += jumbo_total
        total_lider += lider_total

        total_mixto += min(
            jumbo_total,
            lider_total
        )

    st.divider()

    st.subheader(
        "📋 Detalle Comparación"
    )

    st.dataframe(
        pd.DataFrame(resumen),
        use_container_width=True
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
        f"💰 Ahorro Potencial: ${ahorro:,.0f}"
    )
