import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Calculadora Integral Pro", layout="wide")

st.markdown("""
<style>
    /* Estilo botones Dark Tech */
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4c4c54 !important;
        border-radius: 6px !important;
        height: 55px !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin: 2px !important;
    }
    div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        background-color: #31333F !important;
    }
    div.stButton > button:active {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    .stTextInput > div > div > input {
        font-size: 1.4rem;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Falta 'plotly'. Revisa requirements.txt")
    st.stop()

# --- 2. LÓGICA DE MEMORIA SINCRONIZADA ---
if 'formula_state' not in st.session_state:
    st.session_state.formula_state = "6 - 0.0006*x"

def update_from_input():
    """Sincroniza lo que el usuario escribe manualmente con la memoria"""
    st.session_state.formula_state = st.session_state.widget_input

def btn_click(val):
    """Añade símbolo al final (Limitación de Streamlit: no detecta posición del cursor)"""
    st.session_state.formula_state += str(val)

def btn_clear():
    st.session_state.formula_state = ""

def btn_delete():
    st.session_state.formula_state = st.session_state.formula_state[:-1]

# --- 3. INTERFAZ ---
st.title("∫ Calculadora de Integrales y Sólidos")

col_calc, col_opts = st.columns([1.5, 1], gap="large")

with col_calc:
    st.subheader("1. Función f(x)")
    
    # Input vinculado con callback on_change para no perder escritura manual
    st.text_input(
        "Ecuación:", 
        key="widget_input",
        value=st.session_state.formula_state,
        on_change=update_from_input,
        label_visibility="collapsed"
    )
    # Forzamos actualización visual si se apretó un botón
    if st.session_state.widget_input != st.session_state.formula_state:
        st.rerun()

    # --- BOTONERA ---
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.button("CLR", on_click=btn_clear, use_container_width=True)
    b2.button("DEL", on_click=btn_delete, use_container_width=True)
    b3.button("(", on_click=btn_click, args=("(",), use_container_width=True)
    b4.button(")", on_click=btn_click, args=(")",), use_container_width=True)
    b5.button("^", on_click=btn_click, args=("**",), use_container_width=True)

    b6, b7, b8, b9, b10 = st.columns(5)
    b6.button("7", on_click=btn_click, args=("7",), use_container_width=True)
    b7.button("8", on_click=btn_click, args=("8",), use_container_width=True)
    b8.button("9", on_click=btn_click, args=("9",), use_container_width=True)
    b9.button("÷", on_click=btn_click, args=(" / ",), use_container_width=True)
    b10.button("√", on_click=btn_click, args=("sqrt(",), use_container_width=True)

    b11, b12, b13, b14, b15 = st.columns(5)
    b11.button("4", on_click=btn_click, args=("4",), use_container_width=True)
    b12.button("5", on_click=btn_click, args=("5",), use_container_width=True)
    b13.button("6", on_click=btn_click, args=("6",), use_container_width=True)
    b14.button("×", on_click=btn_click, args=(" * ",), use_container_width=True)
    b15.button("sin", on_click=btn_click, args=("sin(",), use_container_width=True)

    b16, b17, b18, b19, b20 = st.columns(5)
    b16.button("1", on_click=btn_click, args=("1",), use_container_width=True)
    b17.button("2", on_click=btn_click, args=("2",), use_container_width=True)
    b18.button("3", on_click=btn_click, args=("3",), use_container_width=True)
    b19.button("－", on_click=btn_click, args=(" - ",), use_container_width=True)
    b20.button("cos", on_click=btn_click, args=("cos(",), use_container_width=True)

    b21, b22, b23, b24, b25 = st.columns(5)
    b21.button("0", on_click=btn_click, args=("0",), use_container_width=True)
    b22.button(".", on_click=btn_click, args=("."), use_container_width=True)
    b23.button("x", on_click=btn_click, args=("x",), use_container_width=True)
    b24.button("＋", on_click=btn_click, args=(" + ",), use_container_width=True)
    b25.button("π", on_click=btn_click, args=("pi",), use_container_width=True)

    # Vista previa LaTeX
    if st.session_state.formula_state:
        try:
            nice_tex = st.session_state.formula_state.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col_opts:
    st.subheader("2. Configuración")
    
    with st.container(border=True):
        st.markdown("**Límites de Integración**")
        c1, c2 = st.columns(2)
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)
    
    st.markdown("### 🛠️ Tipo de Cálculo")
    # AQUÍ ESTÁ LA SOLUCIÓN AL PROBLEMA DE PI
    modo_revolucion = st.toggle("Sólido de Revolución (Volumen)", value=False)
    
    if modo_revolucion:
        st.info("Calculando Volumen: $V = \pi \int [f(x)]^2 dx$")
    else:
        st.info("Calculando Área: $A = \int f(x) dx$")

    st.markdown("---")
    
    if st.button("🚀 CALCULAR Y VISUALIZAR", type="primary", use_container_width=True):
        calc_active = True
    else:
        calc_active = False

# --- 4. CÁLCULO Y LÓGICA GRÁFICA ---
if calc_active and st.session_state.formula_state:
    st.divider()
    
    try:
        # --- A. DATOS MATEMÁTICOS PRECISOS ---
        x_integ = np.linspace(lim_a, lim_b, 1000)
        
        ctx = {
            "x": x_integ, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }
        f_safe = st.session_state.formula_state.replace("^", "**")
        
        # Evaluar f(x)
        y_integ = eval(f_safe, {"__builtins__": None}, ctx)

        # --- B. LÓGICA DE CÁLCULO (ÁREA vs VOLUMEN) ---
        if modo_revolucion:
            # Volumen: pi * integral(y^2)
            integral_val = np.pi * np.trapz(y_integ**2, x_integ)
            label_res = "Volumen del Sólido"
        else:
            # Área: integral(y)
            integral_val = np.trapz(y_integ, x_integ)
            label_res = "Área bajo la Curva"

        # --- C. GENERACIÓN DE GRÁFICOS (VISUALIZACIÓN) ---
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 150)
        
        # Re-evaluar para gráfico con márgenes
        ctx["x"] = x_plot
        z_plot = eval(f_safe, {"__builtins__": None}, ctx) # Esto es el Radio en revolución

        # CONFIGURACIÓN DE LA FIGURA 3D
        if modo_revolucion:
            # --- MODO REVOLUCIÓN: CILINDRO/SOLIDO ---
            # Creamos una malla angular (theta) para rotar la función
            theta = np.linspace(0, 2*np.pi, 60)
            X_mesh, Theta_mesh = np.meshgrid(x_plot, theta)
            
            # Como Z_plot es f(x), ese es nuestro RADIO
            # Para hacer coincidir dimensiones, repetimos z_plot para cada ángulo
            R_mesh = np.tile(z_plot, (len(theta), 1))
            
            # Coordenadas cilíndricas a cartesianas
            # Eje X se mantiene. Y y Z giran.
            Y_mesh = R_mesh * np.cos(Theta_mesh)
            Z_mesh = R_mesh * np.sin(Theta_mesh)
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.9,
                colorbar=dict(title='Radio f(x)')
            )
            layout_title = "Sólido de Revolución (Rotación en X)"
            y_title = "Eje Y"
            z_title = "Eje Z"

        else:
            # --- MODO NORMAL: SÁBANA EXTRUIDA (TU GRÁFICO FAVORITO) ---
            # Profundidad decorativa
            y_vals = np.linspace(0, 10, 50) 
            X_mesh, Y_mesh = np.meshgrid(x_plot, y_vals)
            Z_mesh = np.tile(z_plot, (len(y_vals), 1))
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.9,
                colorbar=dict(title='f(x)')
            )
            layout_title = "Visualización 3D Extruida"
            y_title = "Profundidad (Decorativa)"
            z_title = "Altura f(x)"

        # --- D. MOSTRAR RESULTADOS ---
        col_res_txt, col_res_graph = st.columns([1, 2])
        
        with col_res_txt:
            st.success("✅ Cálculo Exitoso")
            st.metric(label_res, f"{integral_val:,.4f}")
            if modo_revolucion:
                st.caption("La función ha girado 360° sobre el eje X.")

        with col_res_graph:
            fig = go.Figure(data=[surface])
            fig.update_layout(
                title=layout_title,
                scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title=y_title,
                    zaxis_title=z_title,
                    aspectmode='data' # Proporción real para ver bien el sólido
                ),
                height=550,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.warning("Verifica paréntesis y multiplicaciones (ej: 0.0006 * x)")
