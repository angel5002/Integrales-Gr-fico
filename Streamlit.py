import streamlit as st
import numpy as np
import pandas as pd

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Calculadora de Integrales 3D", layout="wide")

st.markdown("""
<style>
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

# --- 2. LÓGICA DE MEMORIA ---
if 'formula_state' not in st.session_state:
    st.session_state.formula_state = "6 - 0.0006*x"

def btn_click(val):
    st.session_state.formula_state += str(val)

def btn_clear():
    st.session_state.formula_state = ""

def btn_delete():
    st.session_state.formula_state = st.session_state.formula_state[:-1]

# --- 3. INTERFAZ ---
st.title("∫ Calculadora de Integrales (Visualización 3D)")

col_calc, col_opts = st.columns([1.5, 1], gap="large")

with col_calc:
    st.subheader("1. Función f(x)")
    
    formula_txt = st.text_input(
        "Ecuación:", 
        key="formula_state", 
        label_visibility="collapsed"
    )

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

    if formula_txt:
        try:
            nice_tex = formula_txt.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col_opts:
    st.subheader("2. Límites de Integración")
    
    with st.container(border=True):
        st.markdown("**Intervalo en el Eje X**")
        c1, c2 = st.columns(2)
        # Valores por defecto corregidos para tu ejemplo
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)

    st.markdown("---")
    
    if st.button("🚀 CALCULAR E INTEGRAR", type="primary", use_container_width=True):
        calc_active = True
    else:
        calc_active = False

# --- 4. CÁLCULO Y GRÁFICO 3D ---
if calc_active and formula_txt:
    st.divider()
    
    try:
        # --- PASO 1: CÁLCULO MATEMÁTICO PRECISO ---
        # Creamos un array que va EXACTAMENTE de 'a' a 'b' con alta resolución
        # Esto garantiza que el cálculo numérico sea preciso (dará 7125)
        x_integ = np.linspace(lim_a, lim_b, 1000)
        
        ctx = {
            "x": x_integ, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }
        f_safe = formula_txt.replace("^", "**")
        
        # Evaluamos para el cálculo del área
        y_integ = eval(f_safe, {"__builtins__": None}, ctx)
        area_val = np.trapz(y_integ, x_integ) # Integral numérica precisa

        # --- PASO 2: VISUALIZACIÓN 3D (Con márgenes) ---
        # Ahora generamos datos aparte para que el gráfico se vea bonito con márgenes
        margin = (lim_b - lim_a) * 0.1 
        if margin == 0: margin = 1
        
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 100)
        
        # Evaluamos de nuevo pero para los puntos del gráfico
        ctx["x"] = x_plot
        z_plot = eval(f_safe, {"__builtins__": None}, ctx)

        # Truco 3D: Crear profundidad falsa (Eje Y)
        y_vals = np.linspace(0, 10, 50) 
        X_mesh, Y_mesh = np.meshgrid(x_plot, y_vals)
        Z_mesh = np.tile(z_plot, (len(y_vals), 1))

        # --- RESULTADOS ---
        col_res_txt, col_res_graph = st.columns([1, 2])
        
        with col_res_txt:
            st.success("✅ Cálculo Exitoso")
            # Mostramos el resultado con formato de miles (,)
            st.metric("Resultado Exacto", f"{area_val:,.4f}")
            st.info("El cálculo ahora se realiza sobre el intervalo exacto [a, b] para máxima precisión.")

        with col_res_graph:
            fig = go.Figure(data=[go.Surface(
                z=Z_mesh,
                x=X_mesh,
                y=Y_mesh,
                colorscale='Jet', 
                colorbar=dict(title='f(x)'),
                opacity=0.9
            )])

            fig.update_layout(
                title="Visualización 3D de f(x)",
                scene=dict(
                    xaxis_title='Eje X',
                    yaxis_title='Profundidad',
                    zaxis_title='Altura f(x)',
                    aspectmode='cube'
                ),
                height=500,
                margin=dict(l=0, r=0, b=0, t=40)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error en la fórmula: {e}")
