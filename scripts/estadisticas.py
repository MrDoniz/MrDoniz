"""Genera las tarjetas SVG de estadísticas del perfil, en español.

Uso: GITHUB_TOKEN=... python scripts/estadisticas.py <usuario> <carpeta_salida>
     python scripts/estadisticas.py --probar
"""
import json
import os
import pathlib
import sys
import urllib.request
from collections import Counter
from datetime import date, timedelta
from html import escape

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
FONDO, TITULO, ACENTO, TEXTO, APAGADO = "#0b1a30", "#e0f2fe", "#7dd3fc", "#c9d1d9", "#8aa4c2"
# de la orilla al fondo: cuanto más profundo, más contribuciones
MAREA = {"NONE": "#15304f", "FIRST_QUARTILE": "#0e4f7a", "SECOND_QUARTILE": "#1172a8",
         "THIRD_QUARTILE": "#2a9fd6", "FOURTH_QUARTILE": "#7dd3fc"}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"]  # mismo orden que weekday de GitHub


def miles(n):
    return f"{n:,}".replace(",", ".")


def porcentaje(p):
    return f"{p:.1f}".replace(".", ",") + " %"


def fecha_corta(d):
    return f"{d.day} {MESES[d.month - 1]}"


def consultar(token, query, variables):
    peticion = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "estadisticas-perfil"},
    )
    with urllib.request.urlopen(peticion, timeout=60) as respuesta:
        datos = json.load(respuesta)
    if datos.get("errors"):
        sys.exit(f"GitHub respondió con errores: {datos['errors']}")
    return datos["data"]


def rachas(dias):
    """dias: [(fecha, contribuciones)] en orden, el último es hoy. Devuelve (actual, mejor)."""
    mejor = seguidos = 0
    for _, n in dias:
        seguidos = seguidos + 1 if n else 0
        mejor = max(mejor, seguidos)
    actual = 0
    # hoy sin contribuciones todavía no rompe la racha
    for i, (_, n) in enumerate(reversed(dias)):
        if n:
            actual += 1
        elif i:
            break
    return actual, mejor


def tarjeta(ancho, alto, titulo, subtitulo, cuerpo, estilo=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" role="img" aria-labelledby="t">
  <title id="t">{escape(titulo)}</title>
  <style>{estilo}
    @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
  </style>
  <rect width="{ancho}" height="{alto}" rx="14" fill="{FONDO}"/>
  <text x="24" y="38" font-family="{SANS}" font-size="18" font-weight="700" fill="{TITULO}">{escape(titulo)}</text>
  <text x="24" y="60" font-family="{MONO}" font-size="12" fill="{ACENTO}">{escape(subtitulo)}</text>
{cuerpo}
</svg>
"""


def marea(semanas, total):
    dias = [d for s in semanas for d in s]
    activos = sum(1 for d in dias if d["contributionCount"])
    mejor = max(dias, key=lambda d: d["contributionCount"])
    sub = (f"{miles(total)} en el último año · {activos} días activos · mejor día: "
           f"{fecha_corta(date.fromisoformat(mejor['date']))} ({mejor['contributionCount']})")
    x0, y0, paso, lado = 56, 92, 17, 13
    partes = []
    for i, semana in enumerate(semanas):
        x = x0 + i * paso
        # el mes se rotula en la semana donde cae su día 1
        dia_uno = next((d["date"] for d in semana if d["date"].endswith("-01")), None)
        if dia_uno:
            partes.append(f'  <text x="{x}" y="{y0 - 10}" font-family="{MONO}" font-size="11" fill="{APAGADO}">{MESES[int(dia_uno[5:7]) - 1]}</text>')
        celdas = "".join(
            f'<rect x="{x}" y="{y0 + d["weekday"] * paso}" width="{lado}" height="{lado}" rx="3" fill="{MAREA[d["contributionLevel"]]}">'
            f'<title>{fecha_corta(date.fromisoformat(d["date"]))}: {d["contributionCount"]}</title></rect>'
            for d in semana)
        partes.append(f'  <g class="ola" style="animation-delay:{i * 18}ms">{celdas}</g>')
    for fila in (1, 3, 5):
        partes.append(f'  <text x="24" y="{y0 + fila * paso + 11}" font-family="{MONO}" font-size="11" fill="{APAGADO}">{DIAS[fila]}</text>')
    leyenda_x = 990 - 24 - 5 * paso - 40
    partes.append(f'  <text x="{leyenda_x - 8}" y="{y0 + 7 * paso + 23}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{APAGADO}">orilla</text>')
    partes += [f'  <rect x="{leyenda_x + i * paso}" y="{y0 + 7 * paso + 12}" width="{lado}" height="{lado}" rx="3" fill="{c}"/>'
               for i, c in enumerate(MAREA.values())]
    partes.append(f'  <text x="{leyenda_x + 5 * paso + 4}" y="{y0 + 7 * paso + 23}" font-family="{MONO}" font-size="11" fill="{APAGADO}">fondo</text>')
    partes.append(f'  <text x="24" y="{y0 + 7 * paso + 23}" font-family="{MONO}" font-size="11" fill="{APAGADO}">una casilla, un día · se actualiza a diario</text>')
    estilo = ".ola{animation:sube .6s ease-out both}@keyframes sube{from{opacity:0}to{opacity:1}}"
    return tarjeta(990, 250, "Mi marea de contribuciones", sub, "\n".join(partes), estilo)


def resumen(total_historico, desde, ultimo_anio, dias_anio, actual, mejor):
    activos = sum(1 for _, n in dias_anio if n)
    mejor_dia = max(dias_anio, key=lambda d: d[1])
    datos = [
        (miles(total_historico), f"contribuciones desde {desde}"),
        (miles(ultimo_anio), "en el último año"),
        (str(activos), "días activos este año"),
        (str(actual), "días de racha actual"),
        (str(mejor), "días de mejor racha"),
        (str(mejor_dia[1]), f"mejor día · {fecha_corta(mejor_dia[0])}"),
    ]
    partes = []
    for i, (valor, etiqueta) in enumerate(datos):
        x, y = 24 + (i % 3) * 152, 104 + (i // 3) * 62
        color = ACENTO if i == 3 else TITULO
        partes.append(f'  <text x="{x}" y="{y}" font-family="{SANS}" font-size="28" font-weight="700" fill="{color}">{valor}</text>')
        partes.append(f'  <text x="{x}" y="{y + 20}" font-family="{SANS}" font-size="12" fill="{APAGADO}">{escape(etiqueta)}</text>')
    return tarjeta(495, 195, "En números", "contribuciones públicas y privadas", "\n".join(partes))


def lenguajes(repos, con_privados):
    tamanos, colores = Counter(), {}
    for repo in repos:
        for arista in repo["languages"]["edges"]:
            nombre = arista["node"]["name"]
            tamanos[nombre] += arista["size"]
            colores[nombre] = arista["node"]["color"] or APAGADO
    total = sum(tamanos.values()) or 1
    top = tamanos.most_common(7)
    resto = total - sum(t for _, t in top)
    if resto:
        top.append(("Otros", resto))
        colores["Otros"] = APAGADO
    partes = ['  <clipPath id="barra"><rect x="24" y="74" width="447" height="10" rx="5"/></clipPath>', '  <g clip-path="url(#barra)">']
    x = 24.0
    for nombre, t in top:
        w = 447 * t / total
        partes.append(f'    <rect x="{x:.2f}" y="74" width="{w + 0.5:.2f}" height="10" fill="{colores[nombre]}"/>')
        x += w
    partes.append("  </g>")
    for i, (nombre, t) in enumerate(top):
        cx, cy = 30 + (i // 4) * 224, 110 + (i % 4) * 22
        partes.append(f'  <circle cx="{cx}" cy="{cy - 4}" r="5" fill="{colores[nombre]}"/>')
        partes.append(f'  <text x="{cx + 12}" y="{cy}" font-family="{SANS}" font-size="13" fill="{TEXTO}">{escape(nombre)} '
                      f'<tspan fill="{APAGADO}">{porcentaje(100 * t / total)}</tspan></text>')
    sub = "en todos mis repositorios" if con_privados else "en mis repositorios públicos"
    return tarjeta(495, 195, "Lenguajes", sub, "\n".join(partes))


def meses(dias_anio):
    por_mes = Counter()
    for d, n in dias_anio:
        por_mes[(d.year, d.month)] += n
    claves = sorted(por_mes)[-12:]
    maximo = max(por_mes[c] for c in claves) or 1
    partes, paso, ancho_barra, base, alto_max = [], 447 / 12, 22, 160, 76
    for i, clave in enumerate(claves):
        n = por_mes[clave]
        alto = max(2, alto_max * n / maximo)
        x = 24 + i * paso + (paso - ancho_barra) / 2
        color = ACENTO if n == maximo else "#1172a8"
        partes.append(f'  <rect class="barra" x="{x:.1f}" y="{base - alto:.1f}" width="{ancho_barra}" height="{alto:.1f}" rx="4" fill="{color}" style="animation-delay:{i * 40}ms"/>')
        centro = x + ancho_barra / 2
        if n:
            partes.append(f'  <text x="{centro:.1f}" y="{base - alto - 6:.1f}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{TEXTO}">{miles(n)}</text>')
        partes.append(f'  <text x="{centro:.1f}" y="{base + 18}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{APAGADO}">{MESES[clave[1] - 1]}</text>')
    estilo = ".barra{transform-box:fill-box;transform-origin:bottom;animation:crece .7s ease-out both}@keyframes crece{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    return tarjeta(495, 195, "Actividad por mes", "últimos 12 meses", "\n".join(partes), estilo)


def dias_semana(dias_anio):
    por_dia = Counter()
    for d, n in dias_anio:
        por_dia[(d.weekday() + 1) % 7] += n  # a la numeración de GitHub (0 = domingo)
    total = sum(por_dia.values()) or 1
    maximo = max(por_dia.values()) or 1
    partes = []
    for fila, dia in enumerate([1, 2, 3, 4, 5, 6, 0]):  # de lunes a domingo
        y, n = 74 + fila * 16, por_dia[dia]
        ancho = max(2, 330 * n / maximo)
        color = ACENTO if n == maximo else "#1172a8"
        partes.append(f'  <text x="24" y="{y + 9}" font-family="{MONO}" font-size="11" fill="{APAGADO}">{DIAS[dia]}</text>')
        partes.append(f'  <rect class="barra" x="64" y="{y}" width="{ancho:.1f}" height="11" rx="4" fill="{color}" style="animation-delay:{fila * 60}ms"/>')
        partes.append(f'  <text x="{64 + ancho + 8:.1f}" y="{y + 9}" font-family="{MONO}" font-size="11" fill="{TEXTO}">{porcentaje(100 * n / total)}</text>')
    estilo = ".barra{transform-box:fill-box;transform-origin:left;animation:crece .7s ease-out both}@keyframes crece{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    return tarjeta(495, 195, "Qué días programo", "reparto del último año", "\n".join(partes), estilo)


CONSULTA = """query($login: String!) {
  user(login: $login) {
    createdAt
    contributionsCollection { contributionCalendar { totalContributions
      weeks { contributionDays { date contributionCount contributionLevel weekday } } } }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes { isPrivate languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}"""


def main(login, salida):
    token = os.environ["GITHUB_TOKEN"]
    datos = consultar(token, CONSULTA, {"login": login})
    usuario = datos["user"]
    calendario = usuario["contributionsCollection"]["contributionCalendar"]
    semanas = [s["contributionDays"] for s in calendario["weeks"]]
    dias_anio = [(date.fromisoformat(d["date"]), d["contributionCount"]) for s in semanas for d in s]
    hoy = dias_anio[-1][0]

    desde = int(usuario["createdAt"][:4])
    anios = " ".join(
        f'a{a}: contributionsCollection(from: "{a}-01-01T00:00:00Z", to: "{a}-12-31T23:59:59Z") '
        "{ contributionCalendar { weeks { contributionDays { date contributionCount } } } }"
        for a in range(desde, hoy.year + 1))
    historico = consultar(token, f"query($login: String!) {{ user(login: $login) {{ {anios} }} }}", {"login": login})["user"]
    por_fecha = {}
    for coleccion in historico.values():
        for semana in coleccion["contributionCalendar"]["weeks"]:
            for d in semana["contributionDays"]:
                fecha = date.fromisoformat(d["date"])
                if fecha <= hoy:
                    por_fecha[fecha] = d["contributionCount"]
    actual, mejor = rachas(sorted(por_fecha.items()))

    # shortcut: solo los 100 primeros repos; paginar si algún día hay más
    repos = usuario["repositories"]["nodes"]
    con_privados = any(r["isPrivate"] for r in repos)

    carpeta = pathlib.Path(salida)
    carpeta.mkdir(parents=True, exist_ok=True)
    tarjetas = {
        "marea.svg": marea(semanas, calendario["totalContributions"]),
        "resumen.svg": resumen(sum(por_fecha.values()), desde, calendario["totalContributions"], dias_anio, actual, mejor),
        "lenguajes.svg": lenguajes(repos, con_privados),
        "meses.svg": meses(dias_anio),
        "dias.svg": dias_semana(dias_anio),
    }
    for nombre, svg in tarjetas.items():
        (carpeta / nombre).write_text(svg, encoding="utf-8")
    print(f"{len(tarjetas)} tarjetas en {carpeta} (privados: {'sí' if con_privados else 'no'})")


def probar():
    d = date(2026, 1, 1)
    dias = [(d + timedelta(i), n) for i, n in enumerate([1, 1, 0, 2, 3, 4, 0])]
    assert rachas(dias) == (3, 3), rachas(dias)          # hoy a cero no corta la racha
    assert rachas(dias[:-1]) == (3, 3)
    assert rachas(dias[:-2] + [(d, 0), (d, 0)]) == (0, 2)  # dos días a cero sí
    assert rachas([(d, 0)]) == (0, 0)
    assert miles(2194) == "2.194" and porcentaje(41.83) == "41,8 %"
    print("ok")


if __name__ == "__main__":
    probar() if sys.argv[1:] == ["--probar"] else main(*sys.argv[1:3])
