import streamlit as st
import numpy as np

# Intentamos importar plotly. Si falla, mostramos un mensaje amigable en lugar del error rojo.
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Plotly no está instalado.")
    st.markdown("Por favor, asegúrate de crear un archivo `requirements.txt` que incluya la palabra `plotly`.")
    st.stop()

# Configuración de la página
st.set_page_config(page_title="Visualizador de Integrales 3D", layout="wide")

def main():
    st.title("🧮 Visualizador Interactivo de Funciones en 3D")
    
    # --- BARRA LATERAL ---
    st.sidebar.header("⚙️ Configuración")
    
    # Entrada de función
    funcion_input = st.sidebar.text_input(
        "Función f(x, y):", 
        value="np.sin(x) * np.cos(y)",
        help="Usa sintaxis Python: np.sin(x), x**2, etc."
    )

    # Límites
    col1, col2 = st.sidebar.columns(2)
    with col1:
        x_min = st.number_input("X Min", value=-5.0)
        x_max = st.number_input("X Max", value=5.0)
    with col2:
        y_min = st.number_input("Y Min", value=-5.0)
        y_max = st.number_input("Y Max", value=5.0)

    resolucion = st.sidebar.slider("Resolución", 20, 100, 50)

    # --- LÓGICA ---
    try:
        x = np.linspace(x_min, x_max, resolucion)
        y = np.linspace(y_min, y_max, resolucion)
        X, Y = np.meshgrid(x, y)
        
        local_dict = {"x": X, "y": Y, "np": np}
        Z = eval(funcion_input, {"__builtins__": None}, local_dict)

        # --- GRÁFICO ---
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            colorscale='Viridis', # Cambié a Viridis que es muy claro científicamente
            colorbar=dict(title='Z'),
        )])

        fig.update_layout(
            title=f'Gráfico de {funcion_input}',
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            margin=dict(l=0, r=0, b=0, t=40),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error en la función: {e}")

if __name__ == "__main__":
    main()
