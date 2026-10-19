import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Comparador Supermercados",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# PRODUCTOS DEMO
# ==========================================

PRODUCTOS = [

    {
        "producto": "Leche Full Proteina Cappuccino 250ml",
        "jumbo": 1390,
        "lider": 1490
    },

    {
        "producto": "Arroz Tucapel 1kg",
        "jumbo": 1990,
        "lider": 1890
    },

    {
        "producto": "Aceite Maravilla 1L",
        "jumbo": 2290,
        "lider": 2490
    },

    {
        "producto": "Nescafe 170g",
        "jumbo": 4990,
        "lider": 5290
    }

]

df = pd.DataFrame(PRODUCTOS)

# ==========================================
# SESSION
# ==========================================

if "carro" not in st.session_state:
    st.session_state.carro = []

# ==========================================
# TITULO
# ==========================================

st.title("🛒 Comparador Supermercados")

st.write(
    "Agrega productos y descubre dónde conviene comprar."
)

# ==========================================
# BUSCADOR
# ==========================================

busqueda = st.text_input(
    "Buscar producto"
)

if busqueda:

    filtro = df[
        df["producto"]
        .str.lower()
        .str.contains(
            busqueda.lower()
        )
    ]

else:

    filtro = df.copy()

# ==========================================
# RESULTADOS
# ==========================================

st.subheader("Resultados")

for _, row in filtro.iterrows():

    col1, col2, col3 = st.columns([5,2,2])

    with col1:

        st.write(
            row["producto"]
        )

    with col2:

        st.write(
            f"Jumbo: ${row['jumbo']:,,}"
        )

    with col3:

        if st.button(
            f"Agregar {row['producto']}"
        ):

            st.session_state.carro.append(
                row.to_dict()
            )

# ==========================================
# CARRITO
# ==========================================

st.divider()

st.subheader("🛒 Mi carrito")

if len(st.session_state.carro) == 0:

    st.info(
        "No hay productos agregados."
    )

else:

    carro_df = pd.DataFrame(
        st.session_state.carro
    )

    st.dataframe(
        carro_df,
        use_container_width=True
    )

# ==========================================
# COMPARAR
# ==========================================

if len(st.session_state.carro) > 0:

    total_jumbo = carro_df["jumbo"].sum()

    total_lider = carro_df["lider"].sum()

    total_mixto = carro_df[
        ["jumbo", "lider"]
    ].min(axis=1).sum()

    st.divider()

    st.subheader(
        "Comparación"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Jumbo",
        f"${total_jumbo:,.0f}"
    )

    col2.metric(
        "Total Líder",
        f"${total_lider:,.0f}"
    )

    col3.metric(
        "Compra Mixta",
        f"${total_mixto:,.0f}"
    )

    ahorro = max(
        total_jumbo,
        total_lider
    ) - total_mixto

    st.success(
        f"Ahorro potencial: ${ahorro:,.0f}"
    )
