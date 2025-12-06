import streamlit as st
import numpy as np
# Intentamos importar plotly de forma segura
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Plotly no está instalado. Crea el archivo requirements.txt")
    st.stop()

st.set_page_config(page_title="Calculadora Gráfica 3D", layout="wide")

def main():
    st.title("🧮 Calculadora Gráfica 3D Inteligente")
    st.markdown("Escribe funciones matemáticas de forma natural (ej: `sin(x) + cos(y)` o `x^2`).")

    # --- BARRA LATERAL ---
    st.sidebar.header("1. Ecuación y Límites")

    # Ayuda visual para la sintaxis (Especie de "Teclado" visual)
    with st.sidebar.expander("ℹ️ Ver Guía de Sintaxis"):
        st.markdown("""
        * **Potencia:** `x^2` o `x**2`
        * **Raíz:** `sqrt(x)`
        * **Trig:** `sin(x)`, `cos(x)`, `tan(x)`
        * **Constantes:** `pi`, `e`
        * **Logaritmo:** `log(x)` (natural), `log10(x)`
        * **Absoluto:** `abs(x)`
        """)

    # 1. Entrada de la función (Texto simple)
    funcion_texto = st.sidebar.text_input(
        "f(x, y) =", 
        value="sin(x) * cos(y)",
        help="Escribe tu función aquí. No necesitas poner 'np.' antes de las funciones."
    )

    # 2. Límites
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.sidebar.markdown("**Eje X**")
        x_min = st.sidebar.number_input("Mín", value=-5.0, key="xm")
        x_max = st.sidebar.number_input("Máx", value=5.0, key="xM")
    with col2:
        st.sidebar.markdown("**Eje Y**")
        y_min = st.sidebar.number_input("Mín", value=-5.0, key="ym")
        y_max = st.sidebar.number_input("Máx", value=5.0, key="yM")

    resolucion = st.sidebar.slider("Resolución (Detalle)", 20, 150, 60)

    # --- PROCESAMIENTO MATEMÁTICO ---
    try:
        # Generar malla
        x = np.linspace(x_min, x_max, resolucion)
        y = np.linspace(y_min, y_max, resolucion)
        X
