import streamlit as st
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Calculadora Integral Pro", layout="wide")

# --- 2. CSS PREMIUM (ESTILO DARK TECH) ---
st.markdown("""
<style>
    /* Estilo del botón general */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4c4c54 !important;
        border-radius: 10px !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
        background-color: #31333F !important;
        transform: scale(1.02);
    }
    /* Estilo del Input de Texto */
    .stTextInput > div > div > input {
        font-size: 1.8rem !important;
        background-color: #0e1117 !important;
        color: #00ff00 !important;
        border: 1px solid #4c4c54;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'.")
    st.stop()

# --- 3. LÓGICA DE MEMORIA ---
if 'user_expression' not in st.session_state:
    st.session_state.user_expression = "x^(3/2)" 

# Variables de estado
if 'result_ready' not in st.session_state:
    st.session_state.result_ready = False
if 'fig_storage' not in st.session_state:
    st.session_state.fig_storage = None
if 'text_result_storage' not in st.session_state:
    st.session_state.text_result_storage = ""
if 'pi_result_storage' not in st.session_state:
    st.session_state.pi_result_storage = ""

# Callbacks
def add(val):
    st.session_state.user_expression += str(val)

def clear():
    st.session_state.user_expression = ""

def delete():
    if len(st.session_state.user_expression) > 0:
        st.session_state.user_expression = st.session_state.user_expression[:-1]

# --- FUNCIÓN MAESTRA DE CÁLCULO ---
def realizar_calculo(formula, a, b, es_volumen):
    try:
        # 1. Rango matemático (Alta precisión)
        x_math = np.linspace(a, b, 2000)
        
        # 2. Contexto matemático
        ctx = {
            "x": x_math, "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp, "pi": np.pi, "e": np.e, "abs": np.abs
        }
        
        # 3. TRADUCCIÓN Y LIMPIEZA DE ERRORES
        f_clean = formula.replace("^", "**")
        
        # Evaluamos f(x)
        y_raw = eval(f_clean, {"__builtins__": None}, ctx)
        
        # --- CORRECCIÓN CRÍTICA ---
        # Convertimos NaNs (errores de raíz negativa) y números complejos a 0.0
        # Esto evita que la app se rompa con x^(3/2) en negativos.
        if np.iscomplexobj(y_raw):
            y_math = np.nan_to_num(y_raw.real, nan=0.0)
        else:
            y_math = np.nan_to_num(y_raw, nan=0.0)
            
        # 4. Cálculos
        if es_volumen:
            # Volumen: pi * integral(y^2)
            integral_base = np.trapz(y_math**2, x_math)
            volumen_total = integral_base * np.pi
            
            txt_res = f"{volumen_total:,.4f} u³"
            txt_pi = f"{integral_base:,.4f} π u³"
            
            # --- GRÁFICO SÓLIDO ---
            x_plot = np.linspace(a, b, 80)
            ctx["x"] = x_plot
            y_plot_raw = eval(f_clean, {"__builtins__": None}, ctx)
            
            # Limpieza para gráfico
            if np.iscomplexobj(y_plot_raw): y_plot = np.nan_to_num(y_plot_raw.real, nan=0.0)
            else: y_plot = np.nan_to_num(y_plot_raw, nan=0.0)
            
            theta = np.linspace(0, 2*np.pi, 60)
            X_m, T_m = np.meshgrid(x_plot, theta)
            R_m = np.tile(y_plot, (len(theta), 1))
            Y_m = R_m * np.cos(T_m)
            Z_m = R_m * np.sin(T_m)
            
            surface = go.Surface(x=X_m, y=Y_m, z=Z_m, colorscale='Jet', opacity=0.8, name='Sólido')
            
            # Eje X visual
            margin = (b - a) * 0.2 if (b-a) != 0 else 1
            x_line = np.linspace(a - margin, b + margin, 10)
            linea_eje = go.Scatter3d(x=x_line, y=x_line*0, z=x_line*0, mode='lines', line=dict(color='white', width=4), name='Eje X')

            fig = go.Figure(data=[surface, linea_eje])
            fig.update_layout(
                title="Sólido de Revolución 3D", 
                scene=dict(
                    xaxis=dict(title='Eje X', range=[a-margin, b+margin]),
                    yaxis=dict(title='Y'), zaxis=dict(title='Z'),
                    aspectmode='data'
                ), 
                height=600, margin=dict(l=0, r=0, b=0, t=40)
            )
            
        else:
            # Área: integral(y)
            area_total = np.trapz(y_math, x_math)
            txt_res = f"{area_total:,.4f} u²"
            txt_pi = ""
            
            # --- GRÁFICO ÁREA ---
            x_plot = np.linspace(a, b, 100)
            ctx["x"] = x_plot
            y_plot_raw = eval(f_clean, {"__builtins__": None}, ctx)
            
            if np.iscomplexobj(y_plot_raw): y_plot = np.nan_to_num(y_plot_raw.real, nan=0.0)
            else: y_plot = np.nan_to_num(y_plot_raw, nan=0.0)
            
            y_fake = np.linspace(0, 4, 20)
            X_m, Y_m = np.meshgrid(x_plot, y_fake)
            Z_m = np.tile(y_plot, (len(y_fake), 1))
            
            surface = go.Surface(x=X_m, y=Y_m, z=Z_m, colorscale='Viridis', opacity=0.9, name='Área')
            
            # Línea de función
            margin = (b - a) * 0.2 if (b-a) != 0 else 1
            x_line = np.linspace(a - margin, b + margin, 150)
            ctx["x"] = x_line
            y_line_raw = eval(f_clean, {"__builtins__": None}, ctx)
            
            if np.iscomplexobj(y_line_raw): y_line = np.nan_to_num(y_line_raw.real, nan=0.0)
            else: y_line = np.nan_to_num(y_line_raw, nan=0.0)
            
            line_trace = go.Scatter3d(x=x_line, y=np.zeros_like(x_line), z=y_line, mode='lines', line=dict(color='white', width=5), name='Función f(x)')
            
            fig = go.Figure(data=[surface, line_trace])
            fig.update_layout(
                title="Área bajo la curva (3D)", 
                scene=dict(xaxis=dict(range=[a-margin, b+margin]), aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.5)), 
                height=600, margin=dict(l=0, r=0, b=0, t=40)
            )

        st.session_state.text_result_storage = txt_res
        st.session_state.pi_result_storage = txt_pi
        st.session_state.fig_storage = fig
        st.session_state.result_ready = True

    except Exception as e:
        st.error(f"Error Matemático: {e}")
        st.warning("Revisa que los paréntesis estén cerrados. Ej: x^(3/2)")
        st.session_state.result_ready = False

# --- 4. INTERFAZ GRÁFICA ---
st.title("∫ Calculadora de Integrales y Sólidos")



[Image of volume of revolution formula]


col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.subheader("1. Función f(x)")
    st.text_input("Ecuación:", key="user_expression", label_visibility="collapsed")

    # Botonera
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("CLR", on_click=clear, use_container_width=True)
    c2.button("DEL", on_click=delete, use_container_width=True)
    c3.button("(", on_click=add, args=("(",), use_container_width=True)
    c4.button(")", on_click=add, args=(")",), use_container_width=True)
    c5.button("^", on_click=add, args=("^",), use_container_width=True)

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.button("7", on_click=add, args=("7",), use_container_width=True)
    c7.button("8", on_click=add, args=("8",), use_container_width=True)
    c8.button("9", on_click=add, args=("9",), use_container_width=True)
    c9.button("÷", on_click=add, args=(" / ",), use_container_width=True)
    c10.button("√", on_click=add, args=("sqrt(",), use_container_width=True)

    c11, c12, c13, c14, c15 = st.columns(5)
    c11.button("4", on_click=add, args=("4",), use_container_width=True)
    c12.button("5", on_click=add, args=("5",), use_container_width=True)
    c13.button("6", on_click=add, args=("6",), use_container_width=True)
    c14.button("×", on_click=add, args=(" * ",), use_container_width=True)
    c15.button("sin", on_click=add, args=("sin(",), use_container_width=True)

    c16, c17, c18, c19, c20 = st.columns(5)
    c16.button("1", on_click=add, args=("1",), use_container_width=True)
    c17.button("2", on_click=add, args=("2",), use_container_width=True)
    c18.button("3", on_click=add, args=("3",), use_container_width=True)
    c19.button("－", on_click=add, args=(" - ",), use_container_width=True)
    c20.button("cos", on_click=add, args=("cos(",), use_container_width=True)

    c21, c22, c23, c24, c25 = st.columns(5)
    c21.button("0", on_click=add, args=("0",), use_container_width=True)
    c22.button(".", on_click=add, args=(".",), use_container_width=True)
    c23.button("x", on_click=add, args=("x",), use_container_width=True)
    c24.button("＋", on_click=add, args=(" + ",), use_container_width=True)
    c25.button("π", on_click=add, args=("pi",), use_container_width=True)

    if st.session_state.user_expression:
        try:
            nice_tex = st.session_state.user_expression.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                                  .replace("cos", "\\cos").replace("pi", "\\pi")
            st.info("Interpretación:")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col2:
    st.subheader("2. Configuración")
    with st.container(border=True):
        st.markdown("**Límites**")
        cx, cy = st.columns(2)
        lim_a = cx.number_input("Desde (a)", value=0.0, step=1.0)
        lim_b = cy.number_input("Hasta (b)", value=4.0, step=1.0)
    
    st.markdown("---")
    modo_revolucion = st.toggle("Sólido de Revolución (x π)", value=False)
    
    if modo_revolucion:
        st.success("Modo: Volumen (Cilindro/Cono)")
        st.latex(r"V = \pi \int_{a}^{b} [f(x)]^2 dx")
    else:
        st.info("Modo: Área")
        st.latex(r"A = \int_{a}^{b} f(x) dx")

    st.markdown("---")
    
    if st.button("🚀 CALCULAR Y GRAFICAR", type="primary", use_container_width=True):
        realizar_calculo(st.session_state.user_expression, lim_a, lim_b, modo_revolucion)

# --- 5. RESULTADOS ---
if st.session_state.result_ready:
    st.divider()
    r1, r2 = st.columns([1, 2])
    
    with r1:
        st.success("✅ Resultado:")
        st.metric("Valor Total", st.session_state.text_result_storage)
        
        if st.session_state.pi_result_storage:
            st.markdown("---")
            st.info("**En función de π:**")
            st.latex(f"V \\approx {st.session_state.pi_result_storage}")
        
    with r2:
        if st.session_state.fig_storage:
            st.plotly_chart(st.session_state.fig_storage, use_container_width=True)
