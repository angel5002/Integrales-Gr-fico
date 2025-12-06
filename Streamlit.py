import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Calculadora Integral Pro", layout="wide")

# --- 2. CSS PREMIUM (ESTILO DARK TECH) ---
# Forzamos los colores y tamaños para que no se vean blancos o rotos
st.markdown("""
<style>
    /* Estilo del botón general */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;              /* Botones más altos */
        background-color: #262730 !important; /* Fondo Gris Oscuro */
        color: #ffffff !important;            /* TEXTO BLANCO PURO */
        border: 1px solid #4c4c54 !important; /* Borde sutil */
        border-radius: 10px !important;       /* Bordes redondeados */
        font-size: 22px !important;           /* Letra grande */
        font-weight: 600 !important;          /* Letra gruesa */
        margin-bottom: 8px !important;        /* Espacio entre botones */
        transition: all 0.2s ease-in-out;     /* Animación suave */
    }

    /* Efecto al pasar el mouse (Hover) */
    div.stButton > button:hover {
        border-color: #ff4b4b !important;     /* Borde Rojo Streamlit */
        color: #ff4b4b !important;            /* Texto Rojo */
        background-color: #31333F !important; /* Fondo un poco más claro */
        transform: scale(1.02);               /* Pequeño efecto zoom */
    }

    /* Estilo del Input de Texto (Pantalla) */
    .stTextInput > div > div > input {
        font-size: 1.8rem !important;         /* Texto muy grande */
        background-color: #0e1117 !important; /* Fondo negro profundo */
        color: #00ff00 !important;            /* Texto verde terminal */
        border: 1px solid #4c4c54;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librerías
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'.")
    st.stop()

# --- 3. LÓGICA DE MEMORIA (ESTABLE) ---
# Usamos el sistema nativo. key='user_expression' conecta todo automáticamente.
if 'user_expression' not in st.session_state:
    st.session_state.user_expression = "6 - 0.0006*x"

# Funciones Callback (Simples y rápidas)
def add(val):
    st.session_state.user_expression += str(val)

def clear():
    st.session_state.user_expression = ""

def delete():
    if len(st.session_state.user_expression) > 0:
        st.session_state.user_expression = st.session_state.user_expression[:-1]

# --- 4. INTERFAZ GRÁFICA ---
st.title("∫ Calculadora de Integrales y Sólidos")

# División principal: Calculadora (Izquierda) | Opciones (Derecha)
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.subheader("1. Función f(x)")
    
    # PANTALLA DE LA CALCULADORA
    st.text_input(
        "Ecuación:", 
        key="user_expression", 
        label_visibility="collapsed"
    )

    # --- BOTONERA GRID ---
    # Usamos use_container_width=True para que llenen todo el espacio
    
    # Fila 1
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("CLR", on_click=clear, use_container_width=True)
    c2.button("DEL", on_click=delete, use_container_width=True)
    c3.button("(", on_click=add, args=("(",), use_container_width=True)
    c4.button(")", on_click=add, args=(")",), use_container_width=True)
    c5.button("^", on_click=add, args=("**",), use_container_width=True)

    # Fila 2
    c6, c7, c8, c9, c10 = st.columns(5)
    c6.button("7", on_click=add, args=("7",), use_container_width=True)
    c7.button("8", on_click=add, args=("8",), use_container_width=True)
    c8.button("9", on_click=add, args=("9",), use_container_width=True)
    c9.button("÷", on_click=add, args=(" / ",), use_container_width=True)
    c10.button("√", on_click=add, args=("sqrt(",), use_container_width=True)

    # Fila 3
    c11, c12, c13, c14, c15 = st.columns(5)
    c11.button("4", on_click=add, args=("4",), use_container_width=True)
    c12.button("5", on_click=add, args=("5",), use_container_width=True)
    c13.button("6", on_click=add, args=("6",), use_container_width=True)
    c14.button("×", on_click=add, args=(" * ",), use_container_width=True)
    c15.button("sin", on_click=add, args=("sin(",), use_container_width=True)

    # Fila 4
    c16, c17, c18, c19, c20 = st.columns(5)
    c16.button("1", on_click=add, args=("1",), use_container_width=True)
    c17.button("2", on_click=add, args=("2",), use_container_width=True)
    c18.button("3", on_click=add, args=("3",), use_container_width=True)
    c19.button("－", on_click=add, args=(" - ",), use_container_width=True)
    c20.button("cos", on_click=add, args=("cos(",), use_container_width=True)

    # Fila 5
    c21, c22, c23, c24, c25 = st.columns(5)
    c21.button("0", on_click=add, args=("0",), use_container_width=True)
    c22.button(".", on_click=add, args=(".",), use_container_width=True)
    c23.button("x", on_click=add, args=("x",), use_container_width=True)
    c24.button("＋", on_click=add, args=(" + ",), use_container_width=True)
    c25.button("π", on_click=add, args=("pi",), use_container_width=True)

    # Vista previa LaTeX
    if st.session_state.user_expression:
        try:
            nice_tex = st.session_state.user_expression.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                  .replace("cos", "\\cos").replace("pi", "\\pi")
            st.info(f"Interpretación matemática:")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col2:
    st.subheader("2. Configuración")
    
    with st.container(border=True):
        st.markdown("**Límites de Integración**")
        cx, cy = st.columns(2)
        lim_a = cx.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = cy.number_input("Hasta (b)", value=6500.0, step=100.0)
    
    st.markdown("---")
    st.markdown("### 🛠️ Modo de Cálculo")
    
    modo_revolucion = st.toggle("Sólido de Revolución (x π)", value=False)
    
    if modo_revolucion:
        st.success("Modo: Volumen (Cilindro/Cono)")
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 dx")
    else:
        st.info("Modo: Área bajo la curva")
        st.latex(r"A = \int_{a}^{b} f(x) dx")

    st.markdown("---")
    
    # Botón de Acción Grande
    if st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True):
        st.session_state.run_calc = True

# --- 5. LÓGICA DE CÁLCULO ---
if 'run_calc' in st.session_state and st.session_state.run_calc and st.session_state.user_expression:
    st.divider()
    
    try:
        # A. Matemática Precisa
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
            # Volumen
            resultado = np.pi * np.trapz(y_exact**2, x_exact)
            titulo = "Volumen del Sólido"
        else:
            # Área
            resultado = np.trapz(y_exact, x_exact)
            titulo = "Área bajo la Curva"

        # B. Datos para Gráfico (Optimizados para velocidad)
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 120)
        
        ctx["x"] = x_plot
        y_plot = eval(f_safe, {"__builtins__": None}, ctx)

        # C. Construcción 3D
        if modo_revolucion:
            # Sólido Rotado
            theta = np.linspace(0, 2*np.pi, 50)
            X_mesh, Theta_mesh = np.meshgrid(x_plot, theta)
            R_mesh = np.tile(y_plot, (len(theta), 1))
            Y_mesh = R_mesh * np.cos(Theta_mesh)
            Z_mesh = R_mesh * np.sin(Theta_mesh)
            
            surface = go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Jet', opacity=0.9, colorbar=dict(title='Radio'))
            layout_title = "Sólido de Revolución 3D"
            aspect = dict(x=2.5, y=1, z=1)
        else:
            # Sábana 2D Extruida
            y_fake = np.linspace(0, 10, 50)
            X_mesh, Y_mesh = np.meshgrid(x_plot, y_fake)
            Z_mesh = np.tile(y_plot, (len(y_fake), 1))
            
            surface = go.Surface(x=X_mesh, y=Y_mesh, z=Z_mesh, colorscale='Jet', opacity=0.9, colorbar=dict(title='f(x)'))
            layout_title = "Visualización 3D Extruida"
            aspect = dict(x=1, y=1, z=1)

        # D. Resultados Finales
        res_col, plot_col = st.columns([1, 2])
        
        with res_col:
            st.balloons() # ¡Un toque festivo si funciona!
            st.success("✅ Resultado Calculado")
            st.metric(titulo, f"{resultado:,.4f}")
            st.caption(f"Intervalo: [{lim_a}, {lim_b}]")
            
        with plot_col:
            fig = go.Figure(data=[surface])
            fig.update_layout(
                title=layout_title, 
                scene=dict(
                    xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                    aspectratio=aspect
                ),
                height=500,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error Matemático: {e}")
        st.warning("Revisa tu fórmula. Recuerda usar el botón '×' para multiplicar.")
