import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Visualizador de Integrales 3D", layout="wide")

def main():
    st.title("🧮 Visualizador Interactivo de Funciones en 3D")
    st.markdown("""
    Esta aplicación permite graficar funciones de dos variables $f(x, y)$ en un espacio tridimensional.
    Es útil para visualizar volúmenes y superficies antes de calcular integrales dobles.
    """)

    # --- BARRA LATERAL (Entradas del usuario) ---
    st.sidebar.header("⚙️ Configuración de la Integral")

    # 1. Entrada de la función
    st.sidebar.subheader("1. Define la función f(x, y)")
    funcion_input = st.sidebar.text_input(
        "Escribe tu función (usa 'np' para funciones complejas):", 
        value="np.sin(x) * np.cos(y)",
        help="Ejemplos: x**2 + y**2, np.sin(x), np.sqrt(x*y)"
    )

    # 2. Límites de integración
    st.sidebar.subheader("2. Límites de Integración")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        x_min = st.number_input("X Mínimo", value=-5.0, step=0.5)
        x_max = st.number_input("X Máximo", value=5.0, step=0.5)
    with col2:
        y_min = st.number_input("Y Mínimo", value=-5.0, step=0.5)
        y_max = st.number_input("Y Máximo", value=5.0, step=0.5)

    # 3. Resolución (Calidad del gráfico)
    resolucion = st.sidebar.slider(
        "Resolución de la malla (puntos por eje)", 
        min_value=20, max_value=100, value=50,
        help="Más puntos = gráfico más suave pero más lento."
    )

    # --- LÓGICA DE CÁLCULO ---
    try:
        # Generar los datos de los ejes X e Y
        x = np.linspace(x_min, x_max, resolucion)
        y = np.linspace(y_min, y_max, resolucion)
        
        # Crear la malla (grid) bidimensional
        X, Y = np.meshgrid(x, y)
        
        # Evaluar la función de forma segura
        # Creamos un diccionario local para que 'eval' entienda 'np', 'x' e 'y'
        local_dict = {"x": X, "y": Y, "np": np}
        
        # Calculamos Z (la altura)
        Z = eval(funcion_input, {"__builtins__": None}, local_dict)

        # --- GRAFICACIÓN ---
        st.subheader(f"Gráfico de: $f(x, y) = {funcion_input}$")
        
        # Crear la figura 3D con Plotly
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            colorscale='Jet',  # Colores notorios y brillantes
            colorbar=dict(title='Valor Z'),
            opacity=0.9
        )])

        # Ajustes visuales del gráfico
        fig.update_layout(
            title='Superficie 3D Interactiva',
            scene=dict(
                xaxis_title='Eje X',
                yaxis_title='Eje Y',
                zaxis_title='Eje Z (Altura)',
                aspectmode='cube' # Mantiene proporciones cúbicas
            ),
            width=800,
            height=700,
            margin=dict(l=0, r=0, b=0, t=40)
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Cálculo aproximado del volumen (Suma de Riemann simple)
        # Volumen ≈ Área base (dx * dy) * Altura promedio
        dx = (x_max - x_min) / resolucion
        dy = (y_max - y_min) / resolucion
        volumen_aprox = np.sum(Z) * dx * dy
        
        st.info(f"📊 **Volumen aproximado bajo la curva:** {volumen_aprox:.4f} unidades cúbicas (Calculado vía Suma de Riemann)")

    except Exception as e:
        st.error(f"❌ Ocurrió un error al procesar la función. Revisa la sintaxis.")
        st.warning(f"Detalle del error: {e}")
        st.markdown("""
        **Consejos:**
        * Usa `np.sin()` en lugar de `sin()`.
        * Usa `**` para potencias (ej: `x**2` para $x^2$).
        * Asegúrate de que las variables sean `x` e `y`.
        """)

if __name__ == "__main__":
    main()
