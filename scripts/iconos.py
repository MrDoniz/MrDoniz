"""Convierte los iconos de image/ que no existen en skillicons.dev en fichas SVG con su mismo estilo.

Uso: python scripts/iconos.py
"""
import base64
import pathlib

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

salida = RAIZ / "assets" / "iconos"
salida.mkdir(parents=True, exist_ok=True)
for nombre, (imagen, fondo, margen) in FICHAS.items():
    ruta = RAIZ / "image" / imagen
    tipo = "jpeg" if ruta.suffix == ".jpg" else "png"
    datos = base64.b64encode(ruta.read_bytes()).decode()
    (salida / f"{nombre}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
        # el borde gris evita que la ficha blanca desaparezca en el tema claro de GitHub
        + (f'<rect x="4" y="4" width="248" height="248" rx="56" fill="{fondo}" stroke="#d0d7de" stroke-width="8"/>'
           if fondo == BLANCO else f'<rect width="256" height="256" rx="60" fill="{fondo}"/>')
        + f'<image href="data:image/{tipo};base64,{datos}" x="{margen}" y="{margen}" width="{256 - 2 * margen}" height="{256 - 2 * margen}"/></svg>\n',
        encoding="utf-8")
print(f"{len(FICHAS)} fichas en {salida}")
