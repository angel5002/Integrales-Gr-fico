import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Calculadora Integral Pro", layout="wide")

st.markdown("""
<style>
    /* Estilo de Botones Oscuros */
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
        background-color: #1a1b26;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Intentamos importar Plotly, si falla no rompemos todo, solo avisamos
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error crítico: Falta la librería 'plotly'.")
    st.info("Asegúrate de que tu archivo requirements.txt contenga: streamlit, numpy, plotly")
    st.stop()

# --- 2. LÓGICA DE MEMORIA SIMPLE (ESTABLE) ---
# Usamos el sistema nativo de Streamlit.
# La clave 'user_expression' vinculará automáticamente el Input y los Botones.
if 'user_expression' not in st.session_state:
    st.session_state.user_expression = "6 - 0.0006*x"

def add(val):
    """Añade valor al final de la expresión actual"""
    st.session_state.user_expression += str(val)

def clear():
    """Borra todo"""
    st.session_state.user_expression = ""

def delete():
    """Borra el último caracter"""
    current = st.session_state.user_expression
    if len(current) > 0:
        st.session_state.user_expression = current[:-1]

# --- 3. INTERFAZ GRÁFICA ---
st.title("∫ Calculadora de Integrales y Sólidos")

col_calc, col_opts = st.columns([1.5, 1], gap="large")

with col_calc:
    st.subheader("1. Función f(x)")
    
    # INPUT VINCULADO
    # Al poner key="user_expression", cualquier cambio aquí actualiza la memoria
    # y cualquier cambio en la memoria (botones) actualiza esto. ¡Sin bucles!
    st.text_input(
        "Ecuación:", 
        key="user_expression",
        label_visibility="collapsed"
    )

    # --- BOTONERA ---
    # Fila 1
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.button("CLR", on_click=clear, use_container_width=True)
    b2.button("DEL", on_click=delete, use_container_width=True)
    b3.button("(", on_click=add, args=("(",), use_container_width=True)
    b4.button(")", on_click=add, args=(")",), use_container_width=True)
    b5.button("^", on_click=add, args=("**",), use_container_width=True)

    # Fila 2
    b6, b7, b8, b9, b10 = st.columns(5)
    b6.button("7", on_click=add, args=("7",), use_container_width=True)
    b7.button("8", on_click=add, args=("8",), use_container_width=True)
    b8.button("9", on_click=add, args=("9",), use_container_width=True)
    b9.button("÷", on_click=add, args=(" / ",), use_container_width=True)
    b10.button("√", on_click=add, args=("sqrt(",), use_container_width=True)

    # Fila 3
    b11, b12, b13, b14, b15 = st.columns(5)
    b11.button("4", on_click=add, args=("4",), use_container_width=True)
    b12.button("5", on_click=add, args=("5",), use_container_width=True)
    b13.button("6", on_click=add, args=("6",), use_container_width=True)
    b14.button("×", on_click=add, args=(" * ",), use_container_width=True)
    b15.button("sin", on_click=add, args=("sin(",), use_container_width=True)

    # Fila 4
    b16, b17, b18, b19, b20 = st.columns(5)
    b16.button("1", on_click=add, args=("1",), use_container_width=True)
    b17.button("2", on_click=add, args=("2",), use_container_width=True)
    b18.button("3", on_click=add, args=("3",), use_container_width=True)
    b19.button("－", on_click=add, args=(" - ",), use_container_width=True)
    b20.button("cos", on_click=add, args=("cos(",), use_container_width=True)

    # Fila 5
    b21, b22, b23, b24, b25 = st.columns(5)
    b21.button("0", on_click=add, args=("0",), use_container_width=True)
    b22.button(".", on_click=add, args=("."), use_container_width=True)
    b23.button("x", on_click=add, args=("x",), use_container_width=True)
    b24.button("＋", on_click=add, args=(" + ",), use_container_width=True)
    b25.button("π", on_click=add, args=("pi",), use_container_width=True)

    # Vista previa LaTeX (Visual)
    if st.session_state.user_expression:
        try:
            nice_tex = st.session_state.user_expression.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                  .replace("cos", "\\cos")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col_opts:
    st.subheader("2. Configuración")
    
    with st.container(border=True):
        st.markdown("**Límites de Integración**")
        c1, c2 = st.columns(2)
        # Valores por defecto de tu ejemplo
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)
    
    st.markdown("---")
    st.markdown("### 🛠️ Modo de Cálculo")
    
    # Interruptor para Área vs Volumen (Sólido de Revolución)
    modo_revolucion = st.toggle("Sólido de Revolución (x π)", value=False)
    
    if modo_revolucion:
        st.info("🔄 Calculando Volumen (Rotación en X)")
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 dx")
    else:
        st.info("📐 Calculando Área bajo la curva")
        st.latex(r"A = \int_{a}^{b} f(x) dx")

    st.markdown("---")
    
    # Botón principal
    if st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True):
        calc_active = True
    else:
        calc_active = False

# --- 4. CÁLCULO Y VISUALIZACIÓN ---
if calc_active and st.session_state.user_expression:
    st.divider()
    
    try:
        # A. CÁLCULO NUMÉRICO DE ALTA PRECISIÓN
        # Usamos 1000 puntos exactos entre a y b para la integral
        x_exact = np.linspace(lim_a, lim_b, 1000)
        
        ctx = {
            "x": x_exact, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }
        
        # Preparar fórmula (Python usa ** para potencia)
        f_safe = st.session_state.user_expression.replace("^", "**")
        
        # Evaluar f(x)
        y_exact = eval(f_safe, {"__builtins__": None}, ctx)

        # Decidir qué fórmula usar
        if modo_revolucion:
            # Volumen = pi * integral(f(x)^2)
            resultado = np.pi * np.trapz(y_exact**2, x_exact)
            titulo_res = "Volumen del Sólido"
        else:
            # Área = integral(f(x))
            resultado = np.trapz(y_exact, x_exact)
            titulo_res = "Área bajo la Curva"

        # B. GENERACIÓN DEL GRÁFICO (VISUALIZACIÓN)
        # Usamos menos puntos para el gráfico para que sea rápido y ligero
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 100)
        
        # Re-evaluamos f(x) para los puntos del gráfico
        ctx["x"] = x_plot
        y_plot = eval(f_safe, {"__builtins__": None}, ctx) # Esto es el Radio

        # Configuración del gráfico 3D
        if modo_revolucion:
            # --- MODO REVOLUCIÓN (Cilindro/Cono) ---
            theta = np.linspace(0, 2*np.pi, 50) # Ángulos de 0 a 360
            X_mesh, Theta_mesh = np.meshgrid(x_plot, theta)
            R_mesh = np.tile(y_plot, (len(theta), 1))
            
            # Coordenadas polares a cartesianas
            Y_mesh = R_mesh * np.cos(Theta_mesh)
            Z_mesh = R_mesh * np.sin(Theta_mesh)
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.8,
                colorbar=dict(title='Radio')
            )
            layout_title = "Sólido de Revolución 3D"
            aspecto = dict(x=2, y=1, z=1) # Estiramos un poco en X

        else:
            # --- MODO NORMAL (Sábana Extruida) ---
            y_fake = np.linspace(0, 10, 50) # Profundidad decorativa
            X_mesh, Y_mesh = np.meshgrid(x_plot, y_fake)
            Z_mesh = np.tile(y_plot, (len(y_fake), 1)) # Repetimos la altura
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.9,
                colorbar=dict(title='f(x)')
            )
            layout_title = "Visualización Extruida 3D"
            aspecto = dict(x=1, y=1, z=1)

        # C. MOSTRAR RESULTADOS
        c_txt, c_plot = st.columns([1, 2])
        
        with c_txt:
            st.success("✅ Cálculo Exitoso")
            st.metric(titulo_res, f"{resultado:,.4f}")
            st.info(f"Intervalo: [{lim_a}, {lim_b}]")
            
        with c_plot:
            fig = go.Figure(data=[surface])
            fig.update_layout(
                title=layout_title,
                scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    aspectmode='manual',
                    aspectratio=aspecto
                ),
                height=500,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error Matemático: {e}")
        st.warning("Consejo: Usa el asterisco para multiplicar (ej: 6 - 0.0006 * x)")
