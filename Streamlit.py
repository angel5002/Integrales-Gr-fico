import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Calculadora Integral Pro", layout="wide")

# CSS para forzar botones oscuros y visibles
st.markdown("""
<style>
    div.stButton > button {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #4c4c54 !important;
        border-radius: 8px !important;
        height: 60px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin: 2px !important;
    }
    div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }
    /* Input de texto grande */
    .stTextInput > div > div > input {
        font-size: 1.5rem;
        background-color: #1a1b26;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librerías
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'. Crea el archivo requirements.txt")
    st.stop()

# --- 2. LÓGICA DE MEMORIA (ESTABLE) ---
# Usamos el sistema nativo de key binding.
# Esto conecta los botones y el teclado sin causar bucles infinitos.
if 'user_expression' not in st.session_state:
    st.session_state.user_expression = "6 - 0.0006*x"

def add_char(char):
    """Callback para añadir caracteres al final"""
    st.session_state.user_expression += str(char)

def clear_all():
    """Callback para borrar todo"""
    st.session_state.user_expression = ""

def delete_last():
    """Callback para borrar el último caracter"""
    current = st.session_state.user_expression
    if len(current) > 0:
        st.session_state.user_expression = current[:-1]

# --- 3. DISEÑO DE LA INTERFAZ ---
st.title("∫ Calculadora de Integrales y Sólidos")
st.markdown("Calcula integrales definidas y visualiza sólidos de revolución.")



[Image of solid of revolution calculus]


col_calc, col_opts = st.columns([1.5, 1], gap="large")

with col_calc:
    st.subheader("1. Función f(x)")
    
    # LA CLAVE DEL ÉXITO: key="user_expression"
    # Esto vincula automáticamente el input con la memoria.
    st.text_input(
        "Ecuación:", 
        key="user_expression", 
        label_visibility="collapsed"
    )

    # --- BOTONERA ---
    # Fila 1
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.button("CLR", on_click=clear_all, use_container_width=True)
    b2.button("DEL", on_click=delete_last, use_container_width=True)
    b3.button("(", on_click=add_char, args=("(",), use_container_width=True)
    b4.button(")", on_click=add_char, args=(")",), use_container_width=True)
    b5.button("^", on_click=add_char, args=("**",), use_container_width=True)

    # Fila 2
    b6, b7, b8, b9, b10 = st.columns(5)
    b6.button("7", on_click=add_char, args=("7",), use_container_width=True)
    b7.button("8", on_click=add_char, args=("8",), use_container_width=True)
    b8.button("9", on_click=add_char, args=("9",), use_container_width=True)
    b9.button("÷", on_click=add_char, args=(" / ",), use_container_width=True)
    b10.button("√", on_click=add_char, args=("sqrt(",), use_container_width=True)

    # Fila 3
    b11, b12, b13, b14, b15 = st.columns(5)
    b11.button("4", on_click=add_char, args=("4",), use_container_width=True)
    b12.button("5", on_click=add_char, args=("5",), use_container_width=True)
    b13.button("6", on_click=add_char, args=("6",), use_container_width=True)
    b14.button("×", on_click=add_char, args=(" * ",), use_container_width=True)
    b15.button("sin", on_click=add_char, args=("sin(",), use_container_width=True)

    # Fila 4
    b16, b17, b18, b19, b20 = st.columns(5)
    b16.button("1", on_click=add_char, args=("1",), use_container_width=True)
    b17.button("2", on_click=add_char, args=("2",), use_container_width=True)
    b18.button("3", on_click=add_char, args=("3",), use_container_width=True)
    b19.button("－", on_click=add_char, args=(" - ",), use_container_width=True)
    b20.button("cos", on_click=add_char, args=("cos(",), use_container_width=True)

    # Fila 5
    b21, b22, b23, b24, b25 = st.columns(5)
    b21.button("0", on_click=add_char, args=("0",), use_container_width=True)
    b22.button(".", on_click=add_char, args=("."), use_container_width=True)
    b23.button("x", on_click=add_char, args=("x",), use_container_width=True)
    b24.button("＋", on_click=add_char, args=(" + ",), use_container_width=True)
    b25.button("π", on_click=add_char, args=("pi",), use_container_width=True)

    # Vista previa LaTeX
    if st.session_state.user_expression:
        try:
            # Limpieza visual para mostrarlo bonito
            nice_tex = st.session_state.user_expression.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                  .replace("cos", "\\cos").replace("pi", "\\pi")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col_opts:
    st.subheader("2. Configuración")
    
    with st.container(border=True):
        st.markdown("**Límites de Integración**")
        c1, c2 = st.columns(2)
        # Valores por defecto de tu ejemplo (4000 a 6500)
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)

    st.markdown("---")
    st.markdown("### 🛠️ Tipo de Gráfico")
    
    # Interruptor: Área vs Volumen
    modo_revolucion = st.toggle("Sólido de Revolución (x π)", value=False)

    if modo_revolucion:
        st.info("🔄 Volumen (Rotación en X)")
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 dx")
    else:
        st.info("📐 Área bajo la curva")
        st.latex(r"A = \int_{a}^{b} f(x) dx")

    st.markdown("---")
    
    # Botón de calcular
    # Usamos session_state para saber si se presionó, evitando recargas falsas
    if st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True):
        st.session_state.calcular = True
    
# --- 4. CÁLCULO Y VISUALIZACIÓN ---
# Verificamos si existe la bandera 'calcular' en memoria
if 'calcular' in st.session_state and st.session_state.calcular and st.session_state.user_expression:
    st.divider()
    
    try:
        # A. CALCULO MATEMÁTICO PRECISO (1000 puntos)
        x_exact = np.linspace(lim_a, lim_b, 1000)
        
        ctx = {
            "x": x_exact, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }
        
        # Preparamos la fórmula (seguridad)
        f_safe = st.session_state.user_expression.replace("^", "**")
        
        # Evaluamos f(x)
        y_exact = eval(f_safe, {"__builtins__": None}, ctx)

        # B. INTEGRAL (Área o Volumen)
        if modo_revolucion:
            # Volumen = pi * integral(y^2)
            resultado = np.pi * np.trapz(y_exact**2, x_exact)
            titulo_res = "Volumen del Sólido"
        else:
            # Área = integral(y)
            resultado = np.trapz(y_exact, x_exact)
            titulo_res = "Área bajo la Curva"

        # C. DATOS PARA EL GRÁFICO (Menos puntos para rapidez)
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1.0
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 150)
        
        # Re-evaluamos para el gráfico
        ctx["x"] = x_plot
        y_plot = eval(f_safe, {"__builtins__": None}, ctx) # Esto es el radio/altura

        # D. GENERACIÓN VISUAL
        if modo_revolucion:
            # --- CILINDRO / CONO (Rotación) ---
            theta = np.linspace(0, 2*np.pi, 60) # 0 a 360 grados
            X_mesh, Theta_mesh = np.meshgrid(x_plot, theta)
            R_mesh = np.tile(y_plot, (len(theta), 1))
            
            # Polares a Cartesianas
            Y_mesh = R_mesh * np.cos(Theta_mesh)
            Z_mesh = R_mesh * np.sin(Theta_mesh)
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.8,
                colorbar=dict(title='Radio')
            )
            layout_title = "Sólido de Revolución 3D"
            aspecto = dict(x=2, y=1, z=1) # Estirado en X para ver mejor

        else:
            # --- SÁBANA EXTRUIDA (Estilo 3D simple) ---
            y_fake = np.linspace(0, 10, 50) # Profundidad decorativa
            X_mesh, Y_mesh = np.meshgrid(x_plot, y_fake)
            Z_mesh = np.tile(y_plot, (len(y_fake), 1))
            
            surface = go.Surface(
                x=X_mesh, y=Y_mesh, z=Z_mesh,
                colorscale='Jet', opacity=0.9,
                colorbar=dict(title='f(x)')
            )
            layout_title = "Visualización 3D Extruida"
            aspecto = dict(x=1, y=1, z=1)

        # E. RESULTADOS
        c_txt, c_plot = st.columns([1, 2])
        
        with c_txt:
            st.success("✅ Cálculo Exitoso")
            st.metric(titulo_res, f"{resultado:,.4f}")
            st.info(f"Intervalo de integración:\n[{lim_a}, {lim_b}]")
            
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
        st.error(f"❌ Error en el cálculo: {e}")
        st.warning("Revisa que la fórmula sea válida (ej: usa asterisco '*' para multiplicar).")
