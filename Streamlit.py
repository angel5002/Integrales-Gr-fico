import streamlit as st
import numpy as np
import pandas as pd

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Calculadora de Integrales", layout="wide")

st.markdown("""
<style>
    /* Estilo de Botones para que NO sean blancos ni invisibles */
    div.stButton > button {
        background-color: #2b2d42 !important; 
        color: #ffffff !important;             
        border: 1px solid #8d99ae !important;  
        border-radius: 8px !important;
        height: 60px !important;               
        font-size: 22px !important;            
        font-weight: bold !important;
        margin: 2px !important;
    }

    /* Efecto Hover */
    div.stButton > button:hover {
        background-color: #ef233c !important; 
        border-color: white !important;
        color: white !important;
    }

    /* Input de texto */
    .stTextInput > div > div > input {
        font-size: 1.5rem;
        background-color: #1a1b26;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Verificación de librería
try:
    import plotly.graph_objects as go
except ImportError:
    st.error("⚠️ Error: Falta 'plotly'. Revisa requirements.txt.")
    st.stop()

# --- 2. LÓGICA DE MEMORIA (SOLUCIÓN AL BORRADO) ---
# Usamos una clave específica 'user_formula' para conectar el input con los botones
if 'user_formula' not in st.session_state:
    st.session_state.user_formula = ""

def agregar(simbolo):
    """Añade el símbolo al final del texto actual"""
    st.session_state.user_formula += str(simbolo)

def limpiar():
    """Borra todo"""
    st.session_state.user_formula = ""

def borrar_uno():
    """Borra solo el último caracter"""
    if len(st.session_state.user_formula) > 0:
        st.session_state.user_formula = st.session_state.user_formula[:-1]

# --- 3. INTERFAZ GRÁFICA ---

st.title("∫ Calculadora de Integrales Definidas")
st.markdown("Calcula el área bajo la curva de una función $f(x)$.")

col_izq, col_der = st.columns([1.5, 1], gap="large")

with col_izq:
    st.subheader("1. Función f(x)")
    
    # INPUT VINCULADO: El valor se alimenta de session_state.user_formula
    formula_input = st.text_input(
        "Escribe la función:", 
        value=st.session_state.user_formula,
        placeholder="Ej: 6 - 0.0006*x",
        label_visibility="collapsed",
        key="input_visual" # Clave temporal para detectar escritura manual
    )
    
    # Sincronización: Si el usuario escribe a mano, actualizamos el estado
    if formula_input != st.session_state.user_formula:
        st.session_state.user_formula = formula_input

    # --- BOTONERA ---
    # Fila 1
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("CLR", on_click=limpiar, use_container_width=True)
    c2.button("DEL", on_click=borrar_uno, use_container_width=True)
    c3.button("＋", on_click=agregar, args=(" + ",), use_container_width=True)
    c4.button("－", on_click=agregar, args=(" - ",), use_container_width=True)
    c5.button("^", on_click=agregar, args=("**",), use_container_width=True)

    # Fila 2
    c6, c7, c8, c9, c10 = st.columns(5)
    c6.button("x", on_click=agregar, args=("x",), use_container_width=True)
    c7.button("7", on_click=agregar, args=("7",), use_container_width=True)
    c8.button("8", on_click=agregar, args=("8",), use_container_width=True)
    c9.button("9", on_click=agregar, args=("9",), use_container_width=True)
    c10.button("÷", on_click=agregar, args=(" / ",), use_container_width=True)

    # Fila 3
    c11, c12, c13, c14, c15 = st.columns(5)
    c11.button("(", on_click=agregar, args=("(",), use_container_width=True)
    c12.button("4", on_click=agregar, args=("4",), use_container_width=True)
    c13.button("5", on_click=agregar, args=("5",), use_container_width=True)
    c14.button("6", on_click=agregar, args=("6",), use_container_width=True)
    c15.button("×", on_click=agregar, args=(" * ",), use_container_width=True)

    # Fila 4
    c16, c17, c18, c19, c20 = st.columns(5)
    c16.button(")", on_click=agregar, args=(")",), use_container_width=True)
    c17.button("1", on_click=agregar, args=("1",), use_container_width=True)
    c18.button("2", on_click=agregar, args=("2",), use_container_width=True)
    c19.button("3", on_click=agregar, args=("3",), use_container_width=True)
    c20.button("√", on_click=agregar, args=("sqrt(",), use_container_width=True)

    # Fila 5 (Cero y punto)
    c21, c22, c23, c24, c25 = st.columns(5)
    c21.button("0", on_click=agregar, args=("0",), use_container_width=True)
    c22.button(".", on_click=agregar, args=("."), use_container_width=True)
    c23.button("sin", on_click=agregar, args=("sin(",), use_container_width=True)
    c24.button("cos", on_click=agregar, args=("cos(",), use_container_width=True)
    c25.button("π", on_click=agregar, args=("pi",), use_container_width=True)

    # Vista matemática
    if st.session_state.user_formula:
        try:
            tex = st.session_state.user_formula.replace("**", "^").replace("*", "") \
                               .replace("sqrt", "\\sqrt").replace("sin", "\\sin") \
                               .replace("cos", "\\cos").replace("pi", "\\pi")
            st.info("Interpretación:")
            st.latex(f"f(x) = {tex}")
        except:
            pass

with col_der:
    st.subheader("2. Límites de Integración")
    
    # Contenedor limpio para los límites
    with st.container(border=True):
        st.markdown("**Intervalo [a, b]**")
        # Usamos columnas para ponerlos lado a lado
        l1, l2 = st.columns(2)
        # Valores por defecto basados en tu imagen (4000 a 6500)
        lim_a = l1.number_input("Límite Inferior (a)", value=4000.0, step=10.0)
        lim_b = l2.number_input("Límite Superior (b)", value=6500.0, step=10.0)
        
    st.markdown("---")
    
    # Botón de calcular
    if st.button("🚀 CALCULAR INTEGRAL", type="primary", use_container_width=True):
        validado = True
else:
    validado = False

# --- 4. RESULTADOS (ABAJO) ---
if validado and st.session_state.user_formula:
    st.divider()
    try:
        # A. Preparar datos para el gráfico
        # Creamos puntos X un poco más allá de los límites para ver el contexto
        margen = (lim_b - lim_a) * 0.2
        if margen == 0: margen = 1.0 # Evitar error si a=b
        
        x_plot = np.linspace(lim_a - margen, lim_b + margen, 500)
        
        # B. Contexto matemático
        contexto = {"x": x_plot, "sin": np.sin, "cos": np.cos, "sqrt": np.sqrt, "pi": np.pi, "e": np.e, "abs": np.abs}
        
        # C. Evaluar función
        formula_py = st.session_state.user_formula.replace("^", "**")
        y_plot = eval(formula_py, {"__builtins__": None}, contexto)
        
        # D. Calcular el ÁREA (Integral numérica)
        # Solo tomamos los puntos DENTRO del rango [a, b]
        mask = (x_plot >= lim_a) & (x_plot <= lim_b)
        x_area = x_plot[mask]
        y_area = y_plot[mask]
        
        # Regla del trapecio para integrar
        area = np.trapz(y_area, x_area)
        
        # --- GRAFICAR CON PLOTLY (2D Interactivo) ---
        fig = go.Figure()

        # 1. Línea de la función completa
        fig.add_trace(go.Scatter(
            x=x_plot, y=y_plot,
            mode='lines',
            name='f(x)',
            line=dict(color='#00CC96', width=3)
        ))

        # 2. Área sombreada (La integral)
        # Añadimos puntos base para cerrar el polígono y que se pinte bien
        x_fill = np.concatenate(([lim_a], x_area, [lim_b]))
        y_fill = np.concatenate(([0], y_area, [0]))
        
        fig.add_trace(go.Scatter(
            x=x_fill, y=y_fill,
            fill='toself',
            fillcolor='rgba(239, 35, 60, 0.3)', # Rojo transparente
            line=dict(color='rgba(255,255,255,0)'),
            name='Área (Integral)',
            hoverinfo='skip'
        ))

        # Diseño del gráfico
        fig.update_layout(
            title="Gráfico de la Función y Área",
            xaxis_title="Eje X",
            yaxis_title="f(x)",
            template="plotly_dark",
            height=500,
            showlegend=True
        )

        # Mostrar resultado numérico GRANDE
        c_res1, c_res2 = st.columns([1, 2])
        with c_res1:
            st.success(f"**Resultado:**\n# {area:,.4f}")
        with c_res2:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.info("Revisa la sintaxis. Ejemplo para tu imagen: 6 - 0.0006 * x")
