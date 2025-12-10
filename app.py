import streamlit as st

# Título
st.title("Ejemplo de Slider con Streamlit")

# Slider de 0 a 100
valor = st.slider("Selecciona un valor", 0, 100, 50)

# Mostrar el valor
st.write(f"El valor seleccionado es: {valor}")
