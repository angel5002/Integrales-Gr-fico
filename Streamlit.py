import streamlit as st
import numpy as np

# Intentamos importar plotly. Si falla, mostramos mensaje claro.
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error Crítico: Plotly no está instalado.")
    st.info("Por favor, asegúrate de que el archivo requirements.txt existe y contiene la palabra 'plotly'.")
    st.stop()

st.set_page_config(page_title="Calculadora Gráfica 3D", layout="wide")

def main():
    st.title("🧮 Calculadora Gráfica 3D Inteligente")
    st.markdown("Escribe tu función abajo (ej: `sin(x) + cos(y)`).")

    # --- BARRA LATERAL ---
    st.sidebar.header("Configuración")
    
    # Guía rápida
    with st.sidebar.expander("ℹ️ Ayuda de Sintaxis"):
        st.markdown("""
        * `x^2` (Potencia)
        * `sin(x)`, `cos(x)`
        * `sqrt(x)` (Raíz cuadrada)
        * `pi`, `e`
        """)

    # Entradas
    funcion_texto = st.sidebar.text_input("f(x, y) =", value="sin(x)*cos(y)")
    
    c1, c2 = st.sidebar.columns(2)
    x_lim = c1.number_input("Límite X (+/-)", value=5.0)
    y_lim = c2.number_input("Límite Y (+/-)", value=5.0)
    
    resolucion = st.sidebar.slider("Resolución", 20, 100, 50)

    # --- LÓGICA ---
    # Usamos un solo bloque try/except grande para capturar cualquier error
    try:
        # 1. Crear los datos
        x = np.linspace(-x_lim, x_lim, resolucion)
        y = np.linspace(-y_lim, y_lim, resolucion)
        X, Y = np.meshgrid(x, y)

        # 2. Preparar la ecuación (cambiar ^ por **)
        ecuacion = funcion_texto.replace("^", "**")

        # 3. Diccionario matemático seguro
        contexto = {
            "x": X, "y": Y,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e, "abs": np.abs
        }

        # 4. Calcular Z
        Z = eval(ecuacion, {"__builtins__": None}, contexto)

        # 5. Graficar
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            colorscale='Spectral',
            colorbar=dict(title='f(x,y)')
        )])

        fig.update_layout(
            title=f"Gráfico: {funcion_texto}",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            height=600,
            margin=dict(l=0, r=0, b=0, t=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        # Aquí capturamos el error si escriben mal la fórmula
        st.error(f"❌ Error en la fórmula: {e}")
        st.markdown("Revisa que no falten paréntesis o que las funciones estén bien escritas (ej: `sin` en lugar de `sen`).")

if __name__ == "__main__":
    main()
