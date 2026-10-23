"""Convierte los iconos de image/ que no existen en skillicons.dev en fichas SVG con su mismo estilo.

Uso: python scripts/iconos.py
"""
import base64
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OSCURO, BLANCO = "#242938", "#ffffff"  # los dos fondos de skillicons; blanco para imágenes con fondo blanco
FICHAS = {  # nombre de la ficha: (imagen original, fondo, margen)
    "proxmox": ("proxmox.png", BLANCO, 36),
    "esxi": ("esxi.png", OSCURO, 40),
    "hyperv": ("hyperv.png", BLANCO, 28),
    "plesk": ("plesk.jpg", BLANCO, 28),
    "cpanel": ("cp.png", OSCURO, 40),
    "sqlserver": ("sql.png", OSCURO, 40),
    "phpmyadmin": ("phpma.png", OSCURO, 6),
    "notepadpp": ("notepadpp.jpg", BLANCO, 32),
}
SIMPLE_ICONS = {  # iconos de un solo trazo de simple-icons.org, coloreados con su marca (aclarada si no se lee)
    "sap": ("sap.svg", "#0FAAFF"),
    "uipath": ("uipath.svg", "#FF7043"),
    "powerautomate": ("powerautomate.svg", "#3D8BFF"),
    "powerapps": ("powerapps.svg", "#C25BD3"),
}
TEXTOS = {"soapui": ("SoapUI", "#85C440")}  # sin icono libre: ficha con el nombre


def ficha(fondo, contenido):
    # el borde gris evita que la ficha blanca desaparezca en el tema claro de GitHub
    marco = (f'<rect x="4" y="4" width="248" height="248" rx="56" fill="{fondo}" stroke="#d0d7de" stroke-width="8"/>'
             if fondo == BLANCO else f'<rect width="256" height="256" rx="60" fill="{fondo}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">{marco}{contenido}</svg>\n'


salida = RAIZ / "assets" / "iconos"
salida.mkdir(parents=True, exist_ok=True)
fichas = {}
for nombre, (imagen, fondo, margen) in FICHAS.items():
    ruta = RAIZ / "image" / imagen
    tipo = "jpeg" if ruta.suffix == ".jpg" else "png"
    datos = base64.b64encode(ruta.read_bytes()).decode()
    lado = 256 - 2 * margen
    fichas[nombre] = ficha(fondo, f'<image href="data:image/{tipo};base64,{datos}" x="{margen}" y="{margen}" width="{lado}" height="{lado}"/>')
for nombre, (imagen, color) in SIMPLE_ICONS.items():
    trazo = re.search(r'<path d="([^"]+)"', (RAIZ / "image" / imagen).read_text(encoding="utf-8")).group(1)
    fichas[nombre] = ficha(OSCURO, f'<path transform="translate(48 48) scale(6.6667)" fill="{color}" d="{trazo}"/>')
for nombre, (texto, color) in TEXTOS.items():
    fichas[nombre] = ficha(OSCURO, f'<text x="128" y="150" text-anchor="middle" font-family="\'Segoe UI\', Ubuntu, Arial, sans-serif" '
                                   f'font-size="62" font-weight="800" fill="{color}">{texto}</text>')
for nombre, svg in fichas.items():
    (salida / f"{nombre}.svg").write_text(svg, encoding="utf-8")
print(f"{len(fichas)} fichas en {salida}")
