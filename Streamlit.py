import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Calculadora Integral", layout="wide")

# Estilos CSS para botones visibles y grandes
st.markdown("""
<style>
    div.stButton > button {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #4c4c54 !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin: 2px !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }
    .stTextInput > div > div > input {
        font-size: 1.5rem;
        background-color: #1a1b26;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Intentar importar Plotly con manejo de error
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta la librería 'plotly'. Revisa requirements.txt")
    st.stop()

# --- 2. LÓGICA DE MEMORIA ---
# Inicializamos la variable de la ecuación
if 'user_expression' not in st.session_state:
    st.session_state.user_expression = "6 - 0.0006*x"

# Funciones para los botones
def add(val):
    st.session_state.user_expression += str(val)

def clear():
    st.session_state.user_expression = ""

def delete():
    current = st.session_state.user_expression
    if len(current) > 0:
        st.session_state.user_expression = current[:-1]

# --- 3. INTERFAZ ---
st.title("∫ Calculadora de Integrales y Sólidos")

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.subheader("1. Función f(x)")
    
    # Input vinculado directamente a la memoria
    st.text_input(
        "Ecuación:", 
        key="user_expression", 
        label_visibility="collapsed"
    )

    # --- BOTONERA ---
    # Fila 1
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.button("CLR", on_click=clear)
    b2.button("DEL", on_click=delete)
    b3.button("(", on_click=add, args=("(",))
    b4.button(")", on_click=add, args=(")",))
    b5.button("^", on_click=add, args=("**",))

    # Fila 2
    b6, b7, b8, b9, b10 = st.columns(5)
    b6.button("7", on_click=add, args=("7",))
    b7.button("8", on_click=add, args=("8",))
    b8.button("9", on_click=add, args=("9",))
    b9.button("÷", on_click=add, args=(" / ",))
    b10.button("√", on_click=add, args=("sqrt(",))

    # Fila 3
    b11, b12, b13, b14, b15 = st.columns(5)
    b11.button("4", on_click=add, args=("4",))
    b12.button("5", on_click=add, args=("5",))
    b13.button("6", on_click=add, args=("6",))
    b14.button("×", on_click=add, args=(" * ",))
    b15.button("sin", on_click=add, args=("sin(",))

    # Fila 4
    b16, b17, b18, b19, b20 = st.columns(5)
    b16.button("1", on_click=add, args=("1",))
    b17.button("2", on_click=add, args=("2",))
    b18.button("3", on_click=add, args=("3",))
    b19.button("－", on_click=add, args=(" - ",))
    b20.button("cos", on_click=add, args=("cos(",))

    # Fila 5
    b21, b22, b23, b24, b25 = st.columns(5)
    b21.button("0", on_click=add, args=("0",))
    b22.button(".", on_click=add, args=(".",))
    b23.button("x", on_click=add, args=("x",))
    b24.button("＋", on_click=add, args=(" + ",))
    b25.button("π", on_click=add, args=("pi",))

    # Vista previa LaTeX
    if st.session_state.user_expression:
        try:
            nice_tex = st.session_state.user_expression.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                  .replace("cos", "\\cos").replace("pi", "\\pi")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col2:
    st.subheader("2. Configuración")
    
    with st.container(border=True):
        st.markdown("**Límites de Integración**")
        c1, c2 = st.columns(2)
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)
    
    st.markdown("---")
    st.markdown("### 🛠️ Modo de Cálculo")
    
    # Interruptor para Sólido de Revolución
    modo_revolucion = st.toggle("Sólido de Revolución (x π)", value=False)
    
    if modo_revolucion:
        st.info("🔄 Volumen (Rotación en X)")
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 dx")
    else:
        st.info("📐 Área bajo la curva")
        st.latex(r"A = \int_{a}^{b} f(x) dx")

    st.markdown("---")
    
    # Botón Calcular
    if st.button("🚀 CALCULAR Y GRAFICAR", type="primary"):
        st.session_state.run_calc = True

# --- 4. CÁLCULO Y GRÁFICO ---
if 'run_calc' in st.session_state and st.session_state.run_calc and st.session_state.user_expression:
    st.divider()
    
    try:
        # A. Cálculo Numérico Preciso
        x_exact = np.linspace(lim_a, lim_b, 1000)
        
        ctx = {
            "x": x_exact, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }
        
        f_safe = st.session_state.user_expression.replace("^", "**")
        y_exact = eval(f_safe, {"__builtins__": None}, ctx)

        if modo_revolucion:
            resultado = np.pi * np.trapz(y_exact**2, x_exact)
            titulo = "Volumen del Sólido"
        else:
            resultado = np.trapz(y_exact, x_exact)
            titulo = "Área bajo la Curva"

        # B. Gráfico (Menos puntos para rapidez)
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 100)
        
        ctx["x"] = x_plot
        y_plot = eval(f_safe, {"__builtins__": None}, ctx)

        if modo_revolucion:
            # Sólido de Revolución
            theta = np.linspace(0, 2*np.pi, 60)
            X_mesh, Theta_mesh = np.meshgrid(x_plot, theta)
            R_mesh = np.tile(y_plot, (len(theta), 1))
            Y_mesh = R_mesh * np.cos(Theta_mesh)
            Z_mesh = R_mesh * np.sin(Theta_mesh)
            
            surface = go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Jet', opacity=0.8)
            title_plot = "Sólido de Revolución 3D"
            aspect = dict(x=2, y=1, z=1)
        else:
            # Gráfico Extruido (Sábana)
            y_fake = np.linspace(0, 10, 50)
            X_mesh, Y_mesh = np.meshgrid(x_plot, y_fake)
            Z_mesh = np.tile(y_plot, (len(y_fake), 1))
            
            surface = go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Jet', opacity=0.9)
            title_plot = "Visualización 3D Extruida"
            aspect = dict(x=1, y=1, z=1)

        # C. Mostrar
        c1, c2 = st.columns([1, 2])
        with c1:
            st.success("✅ Cálculo Exitoso")
            st.metric(titulo, f"{resultado:,.4f}")
        with c2:
            fig = go.Figure(data=[surface])
            fig.update_layout(title=title_plot, scene=dict(aspectratio=aspect), height=500)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
