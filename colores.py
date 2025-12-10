import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="RGB 1cm Square", page_icon="🎨", layout="centered")

st.title("🎨 Cuadrado 1 cm × 1 cm con RGB")

st.write(
    "Ajusta los valores **R, G, B** y visualiza un cuadrado de **10 mm × 10 mm** con ese color. "
    "Ten en cuenta que el tamaño físico puede variar levemente según el dispositivo."
)

col1, col2, col3 = st.columns(3)
with col1:
    r = st.slider("R", 0, 255, 128)
with col2:
    g = st.slider("G", 0, 255, 128)
with col3:
    b = st.slider("B", 0, 255, 128)

hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

st.markdown(f"**RGB:** ({r}, {g}, {b}) | **HEX:** `{hex_color}`")

# --- Cuadrado de 10 mm x 10 mm usando CSS (aprox. 1 cm) ---
square_html = f"""
<div style="
    width:10mm;
    height:10mm;
    background: rgb({r},{g},{b});
    border-radius: 2px;
    border: 1px solid rgba(0,0,0,0.15);
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
">
</div>
"""
st.markdown(square_html, unsafe_allow_html=True)

st.caption("El cuadrado anterior usa 10 mm CSS para aproximar 1 cm real en tu pantalla.")

# --- (Opcional) Exportar el color como imagen PNG ---
st.subheader("Descargar color como PNG (opcional)")
png_size = st.slider("Tamaño PNG (px por lado)", 32, 1024, 256, help="Solo afecta la imagen exportada.")
img = Image.new("RGB", (png_size, png_size), (r, g, b))
buf = io.BytesIO()
img.save(buf, format="PNG")
st.download_button(
    label="⬇️ Descargar PNG",
    data=buf.getvalue(),
    file_name=f"color_{hex_color[1:]}.png",
    mime="image/png"
)

# --- Vista previa en píxeles (informativa) ---
st.subheader("Vista previa adicional (imagen raster)")
st.image(img, caption=f"Vista previa {png_size}×{png_size}px — {hex_color}", use_container_width=False)
