import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN INICIAL Y ESTILOS ---
st.set_page_config(page_title="Visualizador Matemático 3D", layout="wide")

# Inyectamos un poco de CSS para que los botones se vean más "app científica"
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librería Plotly
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error Crítico: Falta 'plotly'. Revisa tu requirements.txt.")
    st.stop()

# --- 2. GESTIÓN DE MEMORIA ---
if 'formula' not in st.session_state:
    st.session_state.formula = "sin(x) * cos(y)"

def agregar(texto):
    st.session_state.formula += str(texto)

def borrar():
    st.session_state.formula = ""

# --- 3. INTERFAZ MAQUETADA ---

st.title("∬ Visualizador de Superficies y Volúmenes")
st.markdown("---")

# Estructura principal: 2 Columnas (70% Calculadora | 30% Configuración)
col_calc, col_conf = st.columns([2, 1], gap="medium")

with col_calc:
    # --- ZONA DE CALCULADORA ---
    st.subheader("1. Definir Función $f(x, y)$")
    
    # Caja de texto principal
    formula_input = st.text_input(
        "Ecuación:", 
        key="formula", 
        placeholder="Ej: x^2 + y^2",
        label_visibility="collapsed"
    )

    # Vista previa matemática inmediata
    try:
        if formula_input:
            latex_show = formula_input.replace("**", "^").replace("*", "") \
                                      .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                      .replace("cos", "\\cos").replace("pi", "\\pi")
            st.latex(f"f(x,y) = {latex_show}")
        else:
            st.info("👆 Usa los botones o el teclado para escribir.")
    except:
        st.text("...")

    # Botonera Estética
    with st.container(border=True):
        # Fila 1
        b1, b2, b3, b4, b5, b6 = st.columns(6)
        if b1.button("LIMPIAR", type="primary"): borrar()
        if b2.button("("): agregar("(")
        if b3.button(")"): agregar(")")
        if b4.button("x"): agregar("x")
        if b5.button("y"): agregar("y")
        if b6.button("^"): agregar("**") # Python usa **
        
        # Fila 2
        b7, b8, b9, b10, b11, b12 = st.columns(6)
        if b7.button("sin"): agregar("sin(")
        if b8.button("cos"): agregar("cos(")
        if b9.button("√"): agregar("sqrt(")
        if b10.button("+"): agregar(" + ")
        if b11.button("-"): agregar(" - ")
        if b12.button("÷"): agregar(" / ")

        # Fila 3
        b13, b14, b15, b16, b17, b18 = st.columns(6)
        if b13.button("tan"): agregar("tan(")
        if b14.button("log"): agregar("log(")
        if b15.button("e"): agregar("e")
        if b16.button("π"): agregar("pi")
        if b17.button("×"): agregar(" * ")
        if b18.button("ABS"): agregar("abs(")

with col_conf:
    # --- ZONA DE CONFIGURACIÓN Y LÍMITES ---
    st.subheader("2. Dominio y Ajustes")
    
    # Aquí diferenciamos claramente "Definición Matemática" de "Visualización"
    with st.container(border=True):
        st.markdown("📐 **Dominio de Integración**")
        st.caption("Define el área cuadrada donde existe la función.")
        
        st.markdown("**Intervalo Eje X**")
        c1, c2 = st.columns(2)
        x_a = c1.number_input("Desde (a)", value=-5.0, step=1.0)
        x_b = c2.number_input("Hasta (b)", value=5.0, step=1.0)
        
        st.markdown("**Intervalo Eje Y**")
        c3, c4 = st.columns(2)
        y_c = c3.number_input("Desde (c)", value=-5.0, step=1.0)
        y_d = c4.number_input("Hasta (d)", value=5.0, step=1.0)

    with st.container(border=True):
        st.markdown("🎨 **Apariencia**")
        resolucion = st.slider("Resolución de Malla", 20, 100, 60, help="Más alto = Gráfico más suave")
        color_map = st.selectbox("Mapa de Color", ["Jet", "Viridis", "Plasma", "Surface"], index=0)

# --- 4. ÁREA DE RESULTADOS (Full Width) ---
st.divider()

if st.button("🚀 GENERAR GRÁFICO 3D", type="primary", use_container_width=True):
    try:
        # 1. Crear el Dominio (Meshgrid)
        # Usamos los límites definidos en el panel derecho
        x = np.linspace(x_a, x_b, resolucion)
        y = np.linspace(y_c, y_d, resolucion)
        X, Y = np.meshgrid(x, y)

        # 2. Contexto matemático seguro
        # Esto permite que el usuario escriba sin, cos, etc.
        contexto = {
            "x": X, "y": Y,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "abs": np.abs, "pi": np.pi, "e": np.e
        }
        
        # 3. Procesar la fórmula
        ecuacion_final = formula_input.replace("^", "**") # Reemplazo de seguridad
        Z = eval(ecuacion_final, {"__builtins__": None}, contexto)

        # 4. Graficar
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            colorscale=color_map,
            colorbar=dict(title='Altura Z')
        )])

        # Diseño del gráfico limpio
        fig.update_layout(
            title=f"Superficie: {formula_input}",
            scene=dict(
                xaxis_title='Eje X',
                yaxis_title='Eje Y',
                zaxis_title='Eje Z',
                aspectmode='cube' # Mantiene proporciones reales
            ),
            height=700,
            margin=dict(l=0, r=0, b=0, t=40)
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # --- BONUS: RESULTADO NUMÉRICO (APROX) ---
        # Si estamos hablando de integrales, mostrar el volumen aproximado es útil
        volumen = np.sum(Z) * ((x_b - x_a)/resolucion) * ((y_d - y_c)/resolucion)
        st.metric(label="Volumen Aproximado (Suma de Riemann)", value=f"{volumen:.4f} u³")

    except SyntaxError:
        st.error("❌ Error de sintaxis. ¿Quizás falta un paréntesis?")
    except NameError as e:
        st.error(f"❌ Función desconocida: {e}. Usa los botones de la calculadora.")
    except Exception as e:
        st.error(f"❌ Error matemático: {e}")
