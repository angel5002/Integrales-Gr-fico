import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN Y ESTILOS (CORREGIDO PARA MODO OSCURO) ---
st.set_page_config(page_title="Calculadora Integral 3D", layout="wide")

st.markdown("""
<style>
    /* Estilo GLOBAL para todos los botones */
    div.stButton > button {
        width: 100%;
        height: 55px;               /* Altura fija para uniformidad */
        background-color: #262730;  /* Gris oscuro (fondo del botón) */
        color: #ffffff;             /* TEXTO BLANCO (Crucial para que se vea) */
        border: 1px solid #4c4c52;  /* Borde gris sutil */
        border-radius: 8px;         /* Bordes redondeados */
        font-size: 20px;            /* Texto grande */
        font-weight: 500;
        transition: all 0.2s;       /* Transición suave al pasar el mouse */
    }

    /* Efecto al pasar el mouse (Hover) */
    div.stButton > button:hover {
        background-color: #383a47;  /* Un poco más claro al pasar el mouse */
        border-color: #ff4b4b;      /* Borde rojo característico de Streamlit */
        color: #ff4b4b;             /* Texto rojo al pasar el mouse */
    }

    /* Estilo específico para el botón CLR (Limpiar) para que destaque */
    div.stButton > button:active {
        background-color: #ff4b4b;
        color: white;
    }
    
    /* Arreglo para inputs de texto */
    .stTextInput > div > div > input {
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librería
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'. Revisa tu requirements.txt.")
    st.stop()

# --- 2. LÓGICA DE MEMORIA (CALLBACKS) ---
if 'formula' not in st.session_state:
    st.session_state.formula = ""

def agregar(simbolo):
    st.session_state.formula += simbolo

def limpiar():
    st.session_state.formula = ""

def borrar_uno():
    st.session_state.formula = st.session_state.formula[:-1]

# --- 3. INTERFAZ GRÁFICA ---

st.markdown("### ∬ Calculadora de Integrales y Superficies")

# Columnas: Izquierda (Calculadora) | Derecha (Configuración)
col_izq, col_der = st.columns([1.5, 1], gap="large")

with col_izq:
    st.markdown("##### 1. Construye tu función")
    
    # Pantalla de visualización
    formula_input = st.text_input(
        "Fórmula:", 
        value=st.session_state.formula,
        placeholder="Usa los botones...",
        label_visibility="collapsed"
    )

    # --- BOTONERA ---
    # Fila 1
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("CLR", on_click=limpiar, use_container_width=True)
    c2.button("DEL", on_click=borrar_uno, help="Borrar último caracter", use_container_width=True)
    c3.button("+", on_click=agregar, args=(" + ",), use_container_width=True)
    c4.button("-", on_click=agregar, args=(" - ",), use_container_width=True)
    c5.button("×", on_click=agregar, args=(" * ",), use_container_width=True)
    c6.button("÷", on_click=agregar, args=(" / ",), use_container_width=True)

    # Fila 2
    c7, c8, c9, c10, c11, c12 = st.columns(6)
    c7.button("x", on_click=agregar, args=("x",), use_container_width=True)
    c8.button("y", on_click=agregar, args=("y",), use_container_width=True)
    c9.button("^", on_click=agregar, args=("**",), use_container_width=True) # Muestra ^ pero escribe **
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

    # Vista Previa
    if formula_input:
        st.markdown("**Vista matemática:**")
        try:
            tex = formula_input.replace("**", "^").replace("*", "") \
                               .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                               .replace("cos", "\\cos").replace("pi", "\\pi") \
                               .replace("log", "\\ln")
            st.latex(f"f(x, y) = {tex}")
        except:
            st.caption("...")

with col_der:
    st.markdown("##### 2. Límites de Integración")
    
    with st.container(border=True):
        st.markdown("🔹 **Variable X**")
        cx1, cx2 = st.columns(2)
        x_min = cx1.number_input("Límite Inferior (a)", value=-5.0, step=1.0)
        x_max = cx2.number_input("Límite Superior (b)", value=5.0, step=1.0)
        
        st.markdown("🔸 **Variable Y**")
        cy1, cy2 = st.columns(2)
        y_min = cy1.number_input("Límite Inferior (c)", value=-5.0, step=1.0)
        y_max = cy2.number_input("Límite Superior (d)", value=5.0, step=1.0)

    resolucion = st.slider("Resolución", 20, 100, 50)

# --- 4. GRAFICACIÓN ---
st.divider()
boton_graficar = st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True)

if boton_graficar:
    if not formula_input:
        st.warning("⚠️ Escribe una función primero.")
    else:
        try:
            x = np.linspace(x_min, x_max, resolucion)
            y = np.linspace(y_min, y_max, resolucion)
            X, Y = np.meshgrid(x, y)
            
            contexto = {
                "x": X, "y": Y,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
                "abs": np.abs, "pi": np.pi, "e": np.e
            }
            
            # Reemplazo de seguridad
            formula_py = formula_input.replace("^", "**")
            
            Z = eval(formula_py, {"__builtins__": None}, contexto)
            
            fig = go.Figure(data=[go.Surface(
                z=Z, x=X, y=Y,
                colorscale='Viridis',
                colorbar=dict(title='Z')
            )])

            fig.update_layout(
                title=f"Gráfico: {formula_input}",
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    aspectmode='cube'
                ),
                height=600,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)

        except SyntaxError:
            st.error("❌ Error de sintaxis. Revisa paréntesis y operadores.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
