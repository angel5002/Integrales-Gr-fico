import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Calculadora Integral 3D", layout="wide")

# Verificación de librería Plotly
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'. Revisa tu requirements.txt.")
    st.stop()

# --- 2. GESTIÓN DE MEMORIA (Session State) ---
# Esto permite que los botones escriban en la caja de texto
if 'formula' not in st.session_state:
    st.session_state.formula = "sin(x) * cos(y)"

def agregar_texto(texto):
    """Función que añade texto a la fórmula actual"""
    st.session_state.formula += str(texto)

def borrar_todo():
    """Función para limpiar la caja"""
    st.session_state.formula = ""

# --- 3. INTERFAZ PRINCIPAL (MAQUETADO) ---

st.markdown("## ∬ Calculadora de Superficies y Volúmenes")

# Dividimos la pantalla: Izquierda (Calculadora) | Derecha (Opciones/Límites)
col_izq, col_der = st.columns([2, 1], gap="large")

with col_izq:
    st.markdown("### Escribe la función:")
    
    # --- BOTONERA TIPO CALCULADORA ---
    # Fila 1 de botones
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    if b1.button("CLR", type="primary"): borrar_todo()
    if b2.button("+"): agregar_texto(" + ")
    if b3.button("-"): agregar_texto(" - ")
    if b4.button("×"): agregar_texto(" * ")
    if b5.button("÷"): agregar_texto(" / ")
    if b6.button("^"): agregar_texto("**")
    
    # Fila 2 de botones
    b7, b8, b9, b10, b11, b12 = st.columns(6)
    if b7.button("√"): agregar_texto("sqrt(")
    if b8.button("sin"): agregar_texto("sin(")
    if b9.button("cos"): agregar_texto("cos(")
    if b10.button("π"): agregar_texto("pi")
    if b11.button("("): agregar_texto("(")
    if b12.button(")"): agregar_texto(")")
    
    # Caja de texto principal (vinculada a la memoria)
    formula_input = st.text_input(
        "Fórmula:", 
        key="formula", # Esto vincula el input con st.session_state.formula
        help="Usa los botones o escribe manualmente."
    )

    # --- VISTA PREVIA MATEMÁTICA ---
    st.markdown("##### Esto será calculado:")
    try:
        # Intentamos mostrar la fórmula en formato matemático bonito (LaTeX)
        latex_str = formula_input.replace("**", "^").replace("sqrt", "\\sqrt").replace("sin", "\\sin").replace("cos", "\\cos").replace("*", "")
        st.latex(f"f(x, y) = {latex_str}")
    except:
        st.text("Escribiendo...")

with col_der:
    # --- PANEL DE OPCIONES (Lado derecho de tu imagen) ---
    st.info("🛠️ Opciones de Integración")
    
    tab1, tab2 = st.tabs(["Límites", "Configuración"])
    
    with tab1:
        st.markdown("**Límites de X**")
        c_x1, c_x2 = st.columns(2)
        x_min = c_x1.number_input("Desde X", value=-5.0)
        x_max = c_x2.number_input("Hasta X", value=5.0)
        
        st.markdown("**Límites de Y**")
        c_y1, c_y2 = st.columns(2)
        y_min = c_y1.number_input("Desde Y", value=-5.0)
        y_max = c_y2.number_input("Hasta Y", value=5.0)
    
    with tab2:
        resolucion = st.slider("Resolución (Detalle)", 20, 100, 50)
        color_scheme = st.selectbox("Color del Gráfico", ["Jet", "Viridis", "Plasma", "Inferno"])

# --- BOTÓN DE ACCIÓN GRANDE ---
st.divider()
boton_calcular = st.button("🚀 GRAFICAR FUNCIÓN 3D", type="primary", use_container_width=True)

# --- 4. LÓGICA DE CÁLCULO Y GRÁFICO ---
if boton_calcular or formula_input:
    try:
        # Preparar datos
        x = np.linspace(x_min, x_max, resolucion)
        y = np.linspace(y_min, y_max, resolucion)
        X, Y = np.meshgrid(x, y)
        
        # Diccionario seguro
        contexto = {
            "x": X, "y": Y,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e, "abs": np.abs
        }
        
        # Limpieza manual por si escribieron "x^2" en vez de usar el botón
        ecuacion_final = formula_input.replace("^", "**")
        
        # Evaluar
        Z = eval(ecuacion_final, {"__builtins__": None}, contexto)
        
        # Graficar
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            colorscale=color_scheme,
            colorbar=dict(title='f(x,y)')
        )])

        fig.update_layout(
            title="Visualización 3D",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            margin=dict(l=0, r=0, b=0, t=30),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ No se pudo graficar: {e}")
        st.warning("Revisa la sintaxis. Ejemplo: 'sin(x) * y'")
