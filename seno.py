import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seno interactivo", page_icon="📈", layout="centered")
st.title("📈 Seno interactivo: amplitud, frecuencia y desplazamiento en tiempo")

with st.sidebar:
    st.header("Parámetros")
    A = st.slider("Amplitud (A)", 0.0, 5.0, 1.0, 0.1)
    f = st.slider("Frecuencia (Hz)", 0.1, 20.0, 1.0, 0.1)
    tau = st.slider("Desplazamiento en tiempo τ (s)", -2.0, 2.0, 0.0, 0.01)
    dc = st.slider("Desplazamiento vertical (DC)", -5.0, 5.0, 0.0, 0.1)
    dur = st.slider("Duración mostrada (s)", 0.1, 10.0, 2.0, 0.1)
    fs = st.slider("Frecuencia de muestreo (Hz)", 50, 5000, 1000, 50)
    show_points = st.checkbox("Mostrar puntos de muestreo", value=False)

T = 1.0 / f
t = np.arange(0, dur, 1.0 / fs)
y = A * np.sin(2 * np.pi * f * (t - tau)) + dc

st.markdown(
    f"""
**Ecuación:** \( y(t) = A \cdot \sin\left(2\pi f (t - \\tau)\\right) + \\text{{DC}} \)  
**A** = {A:.2f}, **f** = {f:.2f} Hz, **τ** = {tau:.2f} s, **DC** = {dc:.2f}  
**Período** \(T = 1/f\) = **{T:.4f} s**
"""
)

fig = plt.figure(figsize=(8, 4))
plt.plot(t, y, label="y(t)")
if show_points:
    plt.plot(t, y, marker="o", linestyle="None", markersize=2, alpha=0.6, label="muestras")
plt.axhline(0, linewidth=1)
plt.grid(True, which="both", alpha=0.3)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.title("Señal seno con desfase temporal")
plt.legend(loc="upper right")
st.pyplot(fig)
