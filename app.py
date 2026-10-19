import streamlit as st
import pandas as pd

from buscador import buscar_jumbo

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

# ===================================================
# TITULO
# ===================================================

st.title("🛒 Comparador Supermercados")

st.write(
    "Busca productos reales de Jumbo y agrégalos al carrito."
)

# ===================================================
# BUSCADOR
# ===================================================

busqueda = st.text_input(
    "Buscar producto"
)

if busqueda:

    try:

        resultados = buscar_jumbo(
            busqueda
        )

        resultados = [
            x for x in resultados
            if x.get("precio")
        ]

        st.subheader(
            f"Resultados Jumbo ({len(resultados)})"
        )

        if resultados:

            opciones = []

            for producto in resultados:

                opciones.append(
                    f"{producto['nombre']} (${producto['precio'\]:,})"
                )

            seleccionado = st.radio(
                "Seleccione un producto",
                opciones
            )

            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                value=1
            )

            if st.button(
                "Agregar al carrito"
            ):

                indice = opciones.index(
                    seleccionado
                )

                producto = resultados[indice]

                st.session_state.carro.append({

                    "producto":
                        producto["nombre"],

                    "jumbo":
                        producto["precio"],

                    "cantidad":
                        cantidad

                })

                st.success(
                    "Producto agregado correctamente."
                )

        else:

            st.warning(
                "No se encontraron productos."
            )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

# ===================================================
# CARRITO
# ===================================================

st.divider()

st.subheader("🛒 Carrito")

col_a, col_b = st.columns([2, 1])

with col_b:

    if st.button("🗑 Vaciar carrito"):

        st.session_state.carro = []

        st.rerun()

if len(st.session_state.carro) == 0:

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

            subtotal = (
                item["jumbo"]
                * item["cantidad"]
            )

            st.write(
                f"**{item['producto']}**"
            )

            st.caption(
                f"${item['jumbo']:,} x {item[''cantidad']} = ${subtotal:,.0f}"
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

    st.divider()

    st.subheader(
        "📋 Resumen"
    )

    detalle = []

    total = 0

    for item in st.session_state.carro:

        subtotal = (
            item["jumbo"]
            * item["cantidad"]
        )

        total += subtotal

        detalle.append({

            "Producto":
                item["producto"],

            "Cantidad":
                item["cantidad"],

            "Precio":
                item["jumbo"],

            "Subtotal":
                subtotal
        })

    st.dataframe(
        pd.DataFrame(detalle),
        use_container_width=True
    )

    st.metric(
        "Total Jumbo",
        f"${total:,.0f}"
    )
