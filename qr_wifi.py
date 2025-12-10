import io
import qrcode
from qrcode.constants import ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H, ERROR_CORRECT_L
from PIL import Image
import streamlit as st

st.set_page_config(page_title="QR Wi-Fi", page_icon="📶", layout="centered")
st.title("📶 Generador de QR para Wi-Fi")
st.caption("Escanéalo con tu cámara o Google Lens para unirte a la red.")

# ---------------- Utilidades ----------------
def escape_wifi(value: str) -> str:
    """
    Escapa caracteres especiales según la convención de QR Wi-Fi:
    se escapan: backslash, punto y coma, coma, dos puntos y comillas.
    """
    return (
        value.replace("\\", r"\\")
             .replace(";", r"\;")
             .replace(",", r"\,")
             .replace(":", r"\:")
             .replace('"', r'\"')
    )

def make_wifi_payload(ssid: str, password: str, security: str, hidden: bool) -> str:
    s = escape_wifi(ssid)
    h = ";H:true" if hidden else ""
    if security == "Sin contraseña (abierta)":
        return f"WIFI:T:nopass;S:{s}{h};;"
    else:
        t = "WEP" if security == "WEP" else "WPA"  # WPA aplica a WPA/WPA2/WPA3-Personal
        p = escape_wifi(password)
        return f"WIFI:T:{t};S:{s};P:{p}{h};;"

def qr_png_bytes(data: str, box_size: int, border: int, ec_level, fill: str, back: str) -> bytes:
    qr = qrcode.QRCode(
        version=None,
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

# ---------------- Entrada principal ----------------
with st.form("wifi_form"):
    ssid = st.text_input("SSID (nombre de la red)", placeholder="MiRedKFC")
    security = st.selectbox(
        "Tipo de seguridad",
        ["WPA/WPA2/WPA3-Personal", "WEP", "Sin contraseña (abierta)"],
        index=0
    )
    col_pass = st.empty()
    password = ""
    if security != "Sin contraseña (abierta)":
        password = col_pass.text_input("Contraseña", type="password", placeholder="••••••••")
    hidden = st.checkbox("Red oculta (Hidden SSID)", value=False)

    st.markdown("**Opciones de imagen**")
    c1, c2, c3 = st.columns(3)
    with c1:
        size = st.slider("Tamaño (módulo)", 2, 20, 8, help="Escala de píxel por módulo del QR.")
    with c2:
        border = st.slider("Borde", 0, 10, 4, help="Márgenes alrededor del QR (en módulos).")
    with c3:
        ec_label = st.selectbox("Corrección de errores", ["Baja (L)", "Media (M)", "Alta (Q)", "Máx (H)"], index=1)
    fill_color = st.color_picker("Color del QR", "#000000")
    back_color = st.color_picker("Color de fondo", "#FFFFFF")

    submitted = st.form_submit_button("Generar QR", type="primary")

# Mapa de corrección de errores
ec_map = {
    "Baja (L)": ERROR_CORRECT_L,
    "Media (M)": ERROR_CORRECT_M,
    "Alta (Q)": ERROR_CORRECT_Q,
    "Máx (H)": ERROR_CORRECT_H,
}

if submitted:
    # Validaciones básicas
    if not ssid.strip():
        st.warning("Por favor ingresa un **SSID**.")
    elif security != "Sin contraseña (abierta)" and not password:
        st.warning("La red no es abierta, ingresa una **contraseña**.")
    else:
        payload = make_wifi_payload(
            ssid=ssid.strip(),
            password=password,
            security=security,
            hidden=hidden
        )
        png = qr_png_bytes(
            data=payload,
            box_size=size,
            border=border,
            ec_level=ec_map[ec_label],
            fill=fill_color,
            back=back_color
        )

        st.subheader("Vista previa")
        st.image(png, caption=f"QR Wi-Fi para «{ssid}»", use_container_width=False)

        st.download_button(
            "⬇️ Descargar PNG",
            data=png,
            file_name=f"wifi_{ssid.replace(' ', '_')}.png",
            mime="image/png"
        )

        with st.expander("Ver texto codificado (avanzado)"):
            st.code(payload, language="text")

st.divider()
st.caption("Nota: este QR funciona para redes personales (no Enterprise 802.1X). Mantén privada tu contraseña.")
