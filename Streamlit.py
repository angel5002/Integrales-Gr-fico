import streamlit as st
import numpy as np
import pandas as pd

# --- 1. CONFIGURACIÓN Y ESTILO (SOLIDO) ---
st.set_page_config(page_title="Calculadora de Integrales", layout="wide")

st.markdown("""
<style>
    /* Estilo robusto para botones: Gris oscuro, texto blanco, borde visible */
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
    /* Input grande y visible */
    .stTextInput > div > div > input {
        font-size: 1.4rem;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librería gráfica
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Falta 'plotly'. Revisa requirements.txt")
    st.stop()

# --- 2. LÓGICA DE MEMORIA (CORE FIX) ---
# Usamos 'formula_state' para controlar el texto sin que se borre
if 'formula_state' not in st.session_state:
    st.session_state.formula_state = "6 - 0.0006*x"

def btn_click(val):
    """Callback que añade texto sin romper el estado"""
    st.session_state.formula_state += str(val)

def btn_clear():
    st.session_state.formula_state = ""

def btn_delete():
    st.session_state.formula_state = st.session_state.formula_state[:-1]

# --- 3. INTERFAZ ---
st.title("∫ Calculadora de Área Bajo la Curva")

col_calc, col_opts = st.columns([1.5, 1], gap="large")

with col_calc:
    st.subheader("1. Función f(x)")
    
    # INPUT VINCULADO AL ESTADO
    # Al escribir aquí, se actualiza 'formula_state' automáticamente gracias al key
    formula_txt = st.text_input(
        "Ecuación:", 
        key="formula_state", 
        label_visibility="collapsed"
    )

    # --- BOTONERA NUMÉRICA Y DE FUNCIONES ---
    # Fila 1
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.button("CLR", on_click=btn_clear, use_container_width=True)
    b2.button("DEL", on_click=btn_delete, use_container_width=True)
    b3.button("(", on_click=btn_click, args=("(",), use_container_width=True)
    b4.button(")", on_click=btn_click, args=(")",), use_container_width=True)
    b5.button("^", on_click=btn_click, args=("**",), use_container_width=True)

    # Fila 2
    b6, b7, b8, b9, b10 = st.columns(5)
    b6.button("7", on_click=btn_click, args=("7",), use_container_width=True)
    b7.button("8", on_click=btn_click, args=("8",), use_container_width=True)
    b8.button("9", on_click=btn_click, args=("9",), use_container_width=True)
    b9.button("÷", on_click=btn_click, args=(" / ",), use_container_width=True)
    b10.button("√", on_click=btn_click, args=("sqrt(",), use_container_width=True)

    # Fila 3
    b11, b12, b13, b14, b15 = st.columns(5)
    b11.button("4", on_click=btn_click, args=("4",), use_container_width=True)
    b12.button("5", on_click=btn_click, args=("5",), use_container_width=True)
    b13.button("6", on_click=btn_click, args=("6",), use_container_width=True)
    b14.button("×", on_click=btn_click, args=(" * ",), use_container_width=True)
    b15.button("sin", on_click=btn_click, args=("sin(",), use_container_width=True)

    # Fila 4
    b16, b17, b18, b19, b20 = st.columns(5)
    b16.button("1", on_click=btn_click, args=("1",), use_container_width=True)
    b17.button("2", on_click=btn_click, args=("2",), use_container_width=True)
    b18.button("3", on_click=btn_click, args=("3",), use_container_width=True)
    b19.button("－", on_click=btn_click, args=(" - ",), use_container_width=True)
    b20.button("cos", on_click=btn_click, args=("cos(",), use_container_width=True)

    # Fila 5
    b21, b22, b23, b24, b25 = st.columns(5)
    b21.button("0", on_click=btn_click, args=("0",), use_container_width=True)
    b22.button(".", on_click=btn_click, args=("."), use_container_width=True)
    b23.button("x", on_click=btn_click, args=("x",), use_container_width=True)
    b24.button("＋", on_click=btn_click, args=(" + ",), use_container_width=True)
    b25.button("π", on_click=btn_click, args=("pi",), use_container_width=True)

    # Vista matemática simple
    if formula_txt:
        try:
            # Renderizado visual limpio
            nice_tex = formula_txt.replace("**", "^").replace("*", "") \
                                  .replace("sqrt", "\\sqrt").replace("sin", "\\sin")
            st.latex(f"f(x) = {nice_tex}")
        except:
            pass

with col_opts:
    st.subheader("2. Límites de Integración")
    
    with st.container(border=True):
        st.markdown("**Intervalo en el Eje X**")
        st.caption("Calcularemos el área entre estos dos puntos.")
        
        c1, c2 = st.columns(2)
        # Valores por defecto de tu ejemplo (4000 a 6500)
        lim_a = c1.number_input("Desde (a)", value=4000.0, step=100.0)
        lim_b = c2.number_input("Hasta (b)", value=6500.0, step=100.0)

    st.markdown("---")
    
    if st.button("🚀 CALCULAR ÁREA", type="primary", use_container_width=True):
        calc_active = True
    else:
        calc_active = False

# --- 4. CÁLCULO Y GRÁFICO 2D ---
if calc_active and formula_txt:
    st.divider()
    
    try:
        # A. GENERACIÓN DE DATOS
        # Creamos un rango un poco más amplio que a-b para que el gráfico se vea bien
        margin = (lim_b - lim_a) * 0.15 
        if margin == 0: margin = 1
        
        x_plot = np.linspace(lim_a - margin, lim_b + margin, 400)
        
        # B. DICCIONARIO MATEMÁTICO
        ctx = {
            "x": x_plot, 
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "sqrt": np.sqrt, "log": np.log, "exp": np.exp,
            "pi": np.pi, "e": np.e
        }

        # C. EVALUACIÓN DE LA FUNCIÓN
        # Reemplazo de seguridad para potencias
        f_safe = formula_txt.replace("^", "**")
        y_plot = eval(f_safe, {"__builtins__": None}, ctx)

        # D. CÁLCULO DEL ÁREA (Solo en el rango a-b)
        # Filtramos los puntos que están exactamente dentro de los límites
        mask = (x_plot >= lim_a) & (x_plot <= lim_b)
        x_area = x_plot[mask]
        y_area = y_plot[mask]
        
        # Integral Numérica (Regla del Trapecio)
        area_val = np.trapz(y_area, x_area)

        # E. VISUALIZACIÓN
        col_res_txt, col_res_graph = st.columns([1, 2])
        
        with col_res_txt:
            st.success("✅ Cálculo Exitoso")
            st.metric("Área Aproximada", f"{area_val:,.4f}")
            st.markdown(f"""
            **Detalles:**
            * Límite inf: `{lim_a}`
            * Límite sup: `{lim_b}`
            """)

        with col_res_graph:
            fig = go.Figure()

            # 1. Línea de la función (Verde)
            fig.add_trace(go.Scatter(
                x=x_plot, y=y_plot,
                mode='lines',
                name='Función f(x)',
                line=dict(color='#2ECC71', width=3)
            ))

            # 2. Área Sombreada (Integral)
            # Truco para cerrar el área perfectamente: bajar a y=0 en los bordes
            x_fill = np.concatenate(([x_area[0]], x_area, [x_area[-1]]))
            y_fill = np.concatenate(([0], y_area, [0]))

            fig.add_trace(go.Scatter(
                x=x_fill, y=y_fill,
                fill='toself',
                fillcolor='rgba(231, 76, 60, 0.3)', # Rojo transparente
                line=dict(color='rgba(255,255,255,0)'),
                name='Área Integrada',
                hoverinfo='skip'
            ))

            fig.update_layout(
                title="Gráfico del Área Bajo la Curva",
                xaxis_title="Eje X",
                yaxis_title="f(x)",
                template="plotly_dark",
                height=450,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error en la fórmula: {e}")
        st.warning("Revisa que hayas usado el asterisco para multiplicar (ej: 0.0006 * x)")
