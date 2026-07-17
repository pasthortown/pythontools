import sys
from yt_dlp import YoutubeDL

CLIENTS = ["android", "ios", "web"]  # evitamos 'tv' que dispara SABR

def intentar_cliente(url, client, outtmpl):
    """
    Intenta extraer y bajar SOLO VIDEO con el cliente dado.
    Prioriza MP4; si no hay, toma WebM. No mezcla audio.
    """
    # Formatos: mejor video (mp4), luego cualquier mejor video
    fmt = "bv*[ext=mp4]/bv"
    ydl_opts = {
        "format": fmt,
        "outtmpl": outtmpl,
        "noprogress": False,
        "quiet": False,
        "no_warnings": False,
        "ignoreerrors": False,
        "extractor_args": {"youtube": {"player_client": [client]}},
        # Estas dos opciones ayudan a evitar errores de conexión/servidor
        "force_ip": "0.0.0.0",       # fuerza IPv4 en la mayoría de entornos
        "geo_bypass": True,
        # Si el video requiere sesión, descomenta una de estas:
        # "cookiesfrombrowser": ("edge",),
        # "cookiesfrombrowser": ("chrome",),
    }
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=True)

def descargar_solo_video(url, nombre_salida="%(title)s [%(id)s].%(ext)s"):
    ultimo_error = None
    for client in CLIENTS:
        try:
            print(f"\n🧩 Probando client: {client}")
            info = intentar_cliente(url, client, nombre_salida)
            # Ruta final si está disponible
            filepath = None
            if isinstance(info, dict):
                filepath = info.get("_filename")
                if not filepath and "requested_downloads" in info and info["requested_downloads"]:
                    filepath = info["requested_downloads"][0].get("filepath")
            print(f"✅ Descargado con client '{client}': {filepath or '(ruta no detectada)'}")
            return
        except Exception as e:
            ultimo_error = e
            print(f"⚠️ Falló con client '{client}': {e}")
    # Si ninguno funcionó:
    raise RuntimeError(f"No fue posible descargar solo video. Último error: {ultimo_error}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python solo_video.py <URL_de_YouTube> [nombre_salida]")
        print('Ejemplo: python solo_video.py https://youtu.be/TuweVOWf-SU "solo_video_%(height)sp.%(ext)s"')
        sys.exit(1)

    url = sys.argv[1]
    nombre_salida = sys.argv[2] if len(sys.argv) >= 3 else "%(title)s [%(id)s].%(ext)s"

    try:
        descargar_solo_video(url, nombre_salida)
    except Exception as e:
        print("\n❌ Error definitivo:", e)
        print("\nSugerencias rápidas:")
        print("  1) Actualiza yt-dlp:          pip install -U yt-dlp")
        print("  2) Prueba nightly/pre:        pip install -U --pre yt-dlp")
        print("  3) Usa cookies del navegador: descomenta cookiesfrombrowser=('edge',) o ('chrome',)")
        print("  4) Si el 400 persiste, ejecuta con otra red o VPN (algunos CDN devuelven 400 por IP/ruta).")
