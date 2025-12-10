import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Línea interactiva", page_icon="📐", layout="centered")
st.title("📐 Línea recta interactiva")

with st.sidebar:
    st.header("Parámetros de la recta")
    m = st.slider("Pendiente (m)", -10.0, 10.0, 1.0, 0.1)
    b = st.slider("Desplazamiento en y (b)", -20.0, 20.0, 0.0, 0.5)
    x_min = st.slider("x mínimo", -20.0, 0.0, -10.0, 0.5)
    x_max = st.slider("x máximo", 0.0, 20.0, 10.0, 0.5)

# Generar datos
x = np.linspace(x_min, x_max, 400)
y = m * x + b

# Mostrar ecuación
st.markdown(
    f"""
    **Ecuación de la recta:**  
    \( y = {m:.2f} \cdot x + {b:.2f} \)
    """
)

# Graficar
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, label=f"y = {m:.2f}x + {b:.2f}", color="blue")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.grid(True, alpha=0.3)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
st.pyplot(fig)
