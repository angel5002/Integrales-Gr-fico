import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN Y ESTILOS FORZADOS ---
st.set_page_config(page_title="Calculadora Integral 3D", layout="wide")

st.markdown("""
<style>
    /* FORZAR estilo de botones para que no sean blancos ni invisibles */
    div.stButton > button {
        background-color: #2b2d42 !important; /* Fondo Azul Oscuro/Gris */
        color: #ffffff !important;             /* Texto BLANCO puro */
        border: 1px solid #8d99ae !important;  /* Borde gris claro */
        border-radius: 8px !important;
        height: 60px !important;               /* Altura fija para todos */
        font-size: 22px !important;            /* Texto grande y legible */
        font-weight: bold !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        
        /* Centrado perfecto del texto */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Efecto al pasar el mouse */
    div.stButton > button:hover {
        background-color: #ef233c !important; /* Rojo al pasar el mouse */
        border-color: #ffffff !important;
        color: white !important;
    }
    
    /* Input de texto más grande */
    .stTextInput > div > div > input {
        font-size: 1.5rem;
        background-color: #1a1b26;
        color: white;
    }
    
    /* Ajuste específico para botón DEL para que no se descuadre */
    button[data-testid="baseButton-secondary"] {
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librería
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'. Revisa requirements.txt.")
    st.stop()

# --- 2. LÓGICA DE MEMORIA ---
if 'formula' not in st.session_state:
    st.session_state.formula = ""

def agregar(simbolo):
    st.session_state.formula += simbolo

def limpiar():
    st.session_state.formula = ""

def borrar_uno():
    # Borra el último caracter de forma segura
    if len(st.session_state.formula) > 0:
        st.session_state.formula = st.session_state.formula[:-1]

# --- 3. INTERFAZ GRÁFICA ---

st.title("∬ Calculadora de Integrales Definidas")

col_izq, col_der = st.columns([1.5, 1], gap="large")

with col_izq:
    st.subheader("1. Función a Integrar")
    
    # Input principal
    formula_input = st.text_input(
        "f(x, y) =", 
        value=st.session_state.formula,
        placeholder="Usa el teclado...",
        label_visibility="collapsed"
    )

    # --- BOTONERA (GRILLA 6x3) ---
    # Usamos contenedores para asegurar alineación perfecta
    
    # Fila 1
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("CLR", on_click=limpiar, use_container_width=True)
    # Usamos un caracter Unicode grueso para el menos y el mas
    c2.button("DEL", on_click=borrar_uno, use_container_width=True) 
    c3.button("＋", on_click=agregar, args=(" + ",), use_container_width=True) # Símbolo Fullwidth Plus
    c4.button("－", on_click=agregar, args=(" - ",), use_container_width=True) # Símbolo Fullwidth Minus
    c5.button("×", on_click=agregar, args=(" * ",), use_container_width=True)
    c6.button("÷", on_click=agregar, args=(" / ",), use_container_width=True)

    # Fila 2
    c7, c8, c9, c10, c11, c12 = st.columns(6)
    c7.button("x", on_click=agregar, args=("x",), use_container_width=True)
    c8.button("y", on_click=agregar, args=("y",), use_container_width=True)
    c9.button("^", on_click=agregar, args=("**",), use_container_width=True)
    c10.button("√", on_click=agregar, args=("sqrt(",), use_container_width=True)
    c11.button("(", on_click=agregar, args=("(",), use_container_width=True)
    c12.button(")", on_click=agregar, args=(")",), use_container_width=True)

    # Fila 3
    c13, c14, c15, c16, c17, c18 = st.columns(6)
    c13.button("sin", on_click=agregar, args=("sin(",), use_container_width=True)
    c14.button("cos", on_click=agregar, args=("cos(",), use_container_width=True)
    c15.button("tan", on_click=agregar, args=("tan(",), use_container_width=True)
    c16.button("ln", on_click=agregar, args=("log(",), use_container_width=True)
    c17.button("e", on_click=agregar, args=("e",), use_container_width=True)
    c18.button("π", on_click=agregar, args=("pi",), use_container_width=True)

    # Renderizado LaTeX
    if formula_input:
        st.markdown("---")
        st.info("Vista Matemática:")
        try:
            tex = formula_input.replace("**", "^").replace("*", "") \
                               .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                               .replace("cos", "\\cos").replace("pi", "\\pi") \
                               .replace("log", "\\ln")
            st.latex(f"\\int \\int {tex} \\, dx dy")
        except:
            pass

with col_der:
    st.subheader("2. Configuración")
    
    # --- SEPARACIÓN CLARA: MATEMÁTICAS ---
    st.markdown("#### 📐 Límites de Integración (Matemáticos)")
    st.caption("Estos valores definen el volumen a calcular.")
    
    with st.container(border=True):
        st.markdown("**Dominio en X** $\int_a^b$")
        cx1, cx2 = st.columns(2)
        x_min = cx1.number_input("a (Inferior)", value=-5.0, step=1.0)
        x_max = cx2.number_input("b (Superior)", value=5.0, step=1.0)
        
        st.markdown("**Dominio en Y** $\int_c^d$")
        cy1, cy2 = st.columns(2)
        y_min = cy1.number_input("c (Inferior)", value=-5.0, step=1.0)
        y_max = cy2.number_input("d (Superior)", value=5.0, step=1.0)

    # --- SEPARACIÓN CLARA: VISUALIZACIÓN ---
    st.markdown("#### 🎨 Ajustes del Gráfico")
    st.caption("Solo afecta cómo se ve la imagen.")
    
    with st.container(border=True):
        resolucion = st.slider("Resolución (Detalle de la malla)", 20, 100, 50)
        colors = st.selectbox("Paleta de Color", ["Viridis", "Jet", "Plasma", "Inferno"])

# --- 4. GRAFICACIÓN ---
st.divider()
boton_graficar = st.button("🚀 CALCULAR INTEGRAL Y GRAFICAR 3D", type="primary", use_container_width=True)

if boton_graficar:
    if not formula_input:
        st.warning("⚠️ Escribe una función primero.")
    else:
        try:
            # 1. Malla basada estrictamente en los límites matemáticos
            x = np.linspace(x_min, x_max, resolucion)
            y = np.linspace(y_min, y_max, resolucion)
            X, Y = np.meshgrid(x, y)
            
            # 2. Contexto
            contexto = {
                "x": X, "y": Y,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
                "abs": np.abs, "pi": np.pi, "e": np.e
            }
            
            # 3. Evaluar
            formula_py = formula_input.replace("^", "**")
            Z = eval(formula_py, {"__builtins__": None}, contexto)
            
            # 4. Graficar
            fig = go.Figure(data=[go.Surface(
                z=Z, x=X, y=Y,
                colorscale=colors,
                colorbar=dict(title='f(x,y)')
            )])

            fig.update_layout(
                title=f"Sólido sobre la región [{x_min},{x_max}] x [{y_min},{y_max}]",
                scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title='Eje Y',
                    zaxis_title='Eje Z',
                ),
                height=700,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 5. Cálculo Numérico (Integral aproximada)
            dx = (x_max - x_min) / (resolucion - 1)
            dy = (y_max - y_min) / (resolucion - 1)
            volumen = np.sum(Z) * dx * dy
            
            st.success(f"✅ **Resultado Aproximado del Volumen:** {volumen:.4f} u³")

        except Exception as e:
            st.error(f"❌ Error: {e}")
