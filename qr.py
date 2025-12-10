import io
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Generador de QR", page_icon="🔳", layout="centered")

st.title("🔳 Generador de Códigos QR")
st.caption("Escribe un texto o URL y genera tu código QR al instante.")

# --- Controles ---
with st.sidebar:
    st.header("Opciones")
    size = st.slider("Tamaño (escala de imagen)", min_value=2, max_value=20, value=8, help="Multiplica el tamaño de cada módulo (pixel) del QR.")
    border = st.slider("Borde (módulos)", min_value=0, max_value=10, value=4, help="Márgenes alrededor del QR en módulos.")
    ec_map = {
        "Baja (L)": ERROR_CORRECT_L,
        "Media (M)": ERROR_CORRECT_M,
        "Alta (Q)": ERROR_CORRECT_Q,
        "Máxima (H)": ERROR_CORRECT_H,
    }
    ec_label = st.selectbox("Corrección de errores", list(ec_map.keys()), index=1)
    fill_color = st.color_picker("Color del QR", "#000000")
    back_color = st.color_picker("Color de fondo", "#FFFFFF")

texto = st.text_area("Texto / URL", placeholder="https://ejemplo.com o cualquier texto…", height=100)

col1, col2 = st.columns([1,1])

def generar_qr_png_bytes(data: str, box_size: int, border: int, ec_level, fill: str, back: str) -> bytes:
    qr = qrcode.QRCode(
        version=None,  # Automático según longitud
        error_correction=ec_level,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img: Image.Image = qr.make_image(fill_color=fill, back_color=back).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()

with col1:
    generar = st.button("Generar QR", type="primary")

if generar:
    if not texto.strip():
        st.warning("Por favor escribe algún texto para generar el QR.")
    else:
        png_bytes = generar_qr_png_bytes(
            data=texto.strip(),
            box_size=size,
            border=border,
            ec_level=ec_map[ec_label],
            fill=fill_color,
            back=back_color
        )

        st.subheader("Vista previa")
        st.image(png_bytes, caption="Tu código QR", use_container_width=False)

        st.download_button(
            label="⬇️ Descargar PNG",
            data=png_bytes,
            file_name="qr.png",
            mime="image/png"
        )

        st.info("Tip: Escoge un nivel de corrección de errores más alto si planeas imprimir el QR o si podría ser parcialmente tapado.")

st.divider()
st.caption("Hecho con Streamlit y qrcode.")
