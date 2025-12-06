import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN Y ESTILOS CSS ---
st.set_page_config(page_title="Calculadora Integral 3D", layout="wide")

# CSS personalizado para que los botones se vean como calculadora real
st.markdown("""
<style>
    /* Estilo para los botones de la calculadora */
    div.stButton > button {
        width: 100%;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        background-color: #f0f2f6;
        color: #31333F;
        border: 1px solid #d6d6d8;
    }
    /* Hover effect (cuando pasas el mouse) */
    div.stButton > button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    /* Estilo especial para el botón CLR (Limpiar) */
    div.stButton > button:first-child {
       /* Simula énfasis si es necesario */
    }
</style>
""", unsafe_allow_html=True)

# Verificación segura de Plotly
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Falta la librería 'plotly'. Asegúrate de tener requirements.txt")
    st.stop()

# --- 2. LÓGICA DE MEMORIA (CALLBACKS) ---
# Esto evita que la app se rompa al hacer clic
if 'formula' not in st.session_state:
    st.session_state.formula = ""

def agregar_simbolo(simbolo):
    """Función que se ejecuta INMEDIATAMENTE al pulsar un botón"""
    st.session_state.formula += simbolo

def limpiar_formula():
    st.session_state.formula = ""

def borrar_ultimo():
    """Borra solo el último caracter"""
    st.session_state.formula = st.session_state.formula[:-1]

# --- 3. INTERFAZ GRÁFICA ---

st.markdown("### ∬ Calculadora de Integrales y Superficies")

col_izq, col_der = st.columns([1.5, 1], gap="large")

with col_izq:
    st.markdown("##### 1. Construye tu función")
    
    # Pantalla de la calculadora (Input)
    # El 'value' se conecta a la memoria para actualizarse con los botones
    formula_input = st.text_input(
        "Fórmula:", 
        value=st.session_state.formula,
        placeholder="Usa el teclado numérico de abajo...",
        label_visibility="collapsed"
    )

    # --- BOTONERA INTELIGENTE ---
    # Fila 1: Operaciones Básicas y Limpieza
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("CLR", on_click=limpiar_formula, use_container_width=True)
    c2.button("⌫", on_click=borrar_ultimo, help="Borrar uno", use_container_width=True)
    c3.button("+", on_click=agregar_simbolo, args=(" + ",), use_container_width=True)
    c4.button("-", on_click=agregar_simbolo, args=(" - ",), use_container_width=True)
    c5.button("×", on_click=agregar_simbolo, args=(" * ",), use_container_width=True) # Escribe *
    c6.button("÷", on_click=agregar_simbolo, args=(" / ",), use_container_width=True)

    # Fila 2: Variables y Potencias
    c7, c8, c9, c10, c11, c12 = st.columns(6)
    c7.button("x", on_click=agregar_simbolo, args=("x",), use_container_width=True)
    c8.button("y", on_click=agregar_simbolo, args=("y",), use_container_width=True)
    c9.button("^", on_click=agregar_simbolo, args=("**",), help="Potencia", use_container_width=True)
    c10.button("√", on_click=agregar_simbolo, args=("sqrt(",), use_container_width=True)
    c11.button("(", on_click=agregar_simbolo, args=("(",), use_container_width=True)
    c12.button(")", on_click=agregar_simbolo, args=(")",), use_container_width=True)

    # Fila 3: Funciones Avanzadas
    c13, c14, c15, c16, c17, c18 = st.columns(6)
    c13.button("sin", on_click=agregar_simbolo, args=("sin(",), use_container_width=True)
    c14.button("cos", on_click=agregar_simbolo, args=("cos(",), use_container_width=True)
    c15.button("tan", on_click=agregar_simbolo, args=("tan(",), use_container_width=True)
    c16.button("ln", on_click=agregar_simbolo, args=("log(",), use_container_width=True)
    c17.button("e", on_click=agregar_simbolo, args=("e",), use_container_width=True)
    c18.button("π", on_click=agregar_simbolo, args=("pi",), use_container_width=True)

    # Vista Previa LaTeX (Matemática bonita)
    if formula_input:
        try:
            # Reemplazos visuales para que se vea bonito en LaTeX
            tex = formula_input.replace("**", "^").replace("*", "") \
                               .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                               .replace("cos", "\\cos").replace("pi", "\\pi")
            st.latex(f"f(x, y) = {tex}")
        except:
            st.caption("Escribiendo...")

with col_der:
    st.markdown("##### 2. Límites de Integración")
    
    # Contenedor con borde para que parezca el panel derecho de tu referencia
    with st.container(border=True):
        st.markdown("**Variable X**")
        c_x1, c_x2 = st.columns(2)
        # Nombres explícitos como pediste
        x_min = c_x1.number_input("Límite Inferior (a)", value=-5.0, step=1.0)
        x_max = c_x2.number_input("Límite Superior (b)", value=5.0, step=1.0)
        
        st.divider() # Línea separadora
        
        st.markdown("**Variable Y**")
        c_y1, c_y2 = st.columns(2)
        y_min = c_y1.number_input("Límite Inferior (c)", value=-5.0, step=1.0)
        y_max = c_y2.number_input("Límite Superior (d)", value=5.0, step=1.0)

    # Opciones extra
    resolucion = st.slider("Resolución del Gráfico", 20, 100, 50)

# --- 4. GRAFICACIÓN ---
st.divider()
boton_graficar = st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True)

if boton_graficar:
    # Validar que haya fórmula
    if not formula_input:
        st.warning("⚠️ Por favor escribe una función primero.")
    else:
        try:
            # 1. Malla de puntos
            x = np.linspace(x_min, x_max, resolucion)
            y = np.linspace(y_min, y_max, resolucion)
            X, Y = np.meshgrid(x, y)
            
            # 2. Diccionario traductor (Seguridad)
            contexto = {
                "x": X, "y": Y,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
                "abs": np.abs, "pi": np.pi, "e": np.e
            }
            
            # 3. Preparar string (Seguridad de potencias)
            # Reemplazamos ^ por ** porque Python no entiende ^
            formula_python = formula_input.replace("^", "**")
            
            # 4. Calcular Z
            Z = eval(formula_python, {"__builtins__": None}, contexto)
            
            # 5. Dibujar
            fig = go.Figure(data=[go.Surface(
                z=Z, x=X, y=Y,
                colorscale='Viridis', # Colores científicos agradables
                colorbar=dict(title='f(x,y)')
            )])

            fig.update_layout(
                title=f"Gráfico de Superficie: {formula_input}",
                scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title='Eje Y',
                    zaxis_title='Eje Z',
                    aspectmode='cube'
                ),
                height=600,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)

        except SyntaxError:
            st.error("❌ Error de escritura. Revisa los paréntesis.")
        except Exception as e:
            st.error(f"❌ No se pudo graficar: {e}")
            st.info("Prueba algo simple como: sin(x) + cos(y)")
