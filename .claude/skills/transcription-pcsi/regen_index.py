#!/usr/bin/env python3
"""Regenerate Prepa_barthou/1ere_annee/index.html by scanning the 4 subject folders.
Usage: python3 regen_index.py <repo_root>

Rendu aligné sur celui de Kit_Revision_PCSI.html : onglets sticky, bandeau
"Sources" par matière, tableau N° / Intitulé / Lien avec lignes de section
("1. Cours de Clarisse" / "2. Cours Profs").

⚠️ AVANT DE LANCER CE SCRIPT : faire un `git fetch` + `git merge` (ou pull)
sur la branche courante. Une autre session travaille en parallèle sur ce
dépôt et pousse régulièrement sur cette même branche ; lancer ce script
depuis un checkout périmé régénère index.html en écrasant silencieusement
les correctifs poussés entre-temps (libellés, favicons, liens...). Le
fichier généré n'est JAMAIS à éditer à la main : toute modification passe
par les constantes ci-dessous (SUBJECT_SOURCES / SUBJECT_MANUALS /
SUBJECT_EXTRA_LINKS) ou par les fonctions de rendu, jamais par un patch
direct sur Prepa_barthou/1ere_annee/index.html.
"""
import sys
import os
import re
import html

SUBJECTS = [
    ("01_MATHS", "🔢", "Maths", "maths"),
    ("02_PHYSIQUE", "⚛️", "Physique", "physique"),
    ("03_CHIMIE", "🧪", "Chimie", "chimie"),
    ("04_SI", "⚙️", "SI", "si"),
]

BASE_URL = "https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee"

# Établissement(s) source des documents "Cours Profs" pour chaque matière
# (ville affichée à titre indicatif, sans classement — ce n'est pas le Kit de révision).
# 5e élément = (num_min, num_max) des fichiers "Cours Profs" attribués à cette source
# (None = source unique, capte tous les fichiers profs de la matière).
SUBJECT_SOURCES = {
    "01_MATHS": [
        ("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "../../logo-barthou.png", (1, 1), None),
        ("Lycée Saint-Louis", "Paris", "https://pcsi1-saint-louis.ovh/site/", "../../logo-saint-louis.png", (2, 5), None),
    ],
    "02_PHYSIQUE": [("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "../../logo-barthou.png", None, None)],
    "03_CHIMIE": [
        ("Sainte-Geneviève", "Versailles", "http://www.pcsi1.bginette.com/Chim/Polys.php", "https://www.google.com/s2/favicons?domain=bginette.com&sz=32", (1, 7), None),
        ("Janson de Sailly", "Paris", "http://chimie-pcsi-jds.net", "https://www.janson-de-sailly.fr/wp-content/uploads/2025/05/favicon.png", (8, 11), None),
    ],
    "04_SI": [
        ("Jean Perrin", "Lyon", "http://nmesnier.free.fr/SII-PCSI.html", "https://www.google.com/s2/favicons?domain=jperrin.fr&sz=32", (0, 8), None),
        ("Gustave Eiffel", "Bordeaux", "https://aroux-sii.fr/", "https://www.eiffel-bordeaux.org/wp-content/themes/bootscore-child-main/img/favicon/favicon-32x32.png", (9, 13), "psi*2627"),
    ],
}

# Manuel de référence (PDF perso, hébergé localement dans manuels/ à la racine
# du dépôt) affiché sous le titre de chaque matière, quand disponible.
SUBJECT_MANUALS = {
    "01_MATHS": ("Mathématiques PCSI — Ellipses 2021", "../../manuels/Maths_PCSI_Ellipses_2021.pdf"),
    "02_PHYSIQUE": ("Physique PCSI — Ellipses 2021", "../../manuels/Physique_PCSI_Ellipses_2021.pdf"),
    "04_SI": ("Sciences industrielles de l'ingénieur — Vuibert", "../../manuels/SI_Vuibert.pdf"),
}

# Ressources complémentaires libres (chaînes vidéo, sites tiers...) affichées
# sous le manuel, sous forme de puces cliquables. Liste de (emoji, label, url).
# Chaînes YouTube complémentaires par matière : (libellé court — nom de
# l'école ou du site/chaîne YouTube —, url). Le logo YouTube est ajouté
# automatiquement au rendu (cf. YOUTUBE_ICON).
SUBJECT_EXTRA_LINKS = {
    "01_MATHS": [
        ("Lycée du Parc", "https://www.youtube.com/@Giraud-Laignel-hy9hb"),
    ],
    "02_PHYSIQUE": [
        ("Physique Chimie Prépa", "https://www.youtube.com/@physiquechimieprepa/featured"),
        ("e-Learning Physique", "https://www.youtube.com/@e-learningphysique4910/featured"),
    ],
    "03_CHIMIE": [
        ("Prépa Chimie", "https://www.youtube.com/@Pr%C3%A9paChimie/videos"),
    ],
    "04_SI": [
        ("Sciences de l'ingénieur", "https://www.youtube.com/@sciences-ingenieur0/courses"),
    ],
}

YOUTUBE_ICON = "https://www.google.com/s2/favicons?domain=youtube.com&sz=32"

# Documents "Cours Profs" externes : PDF hébergés directement sur le site de
# la source (jamais téléchargés dans ce dépôt), utilisés quand aucun fichier
# local n'existe pour ce cours. Liste de (numero, titre, url_pdf) par matière ;
# le numero doit tomber dans le num_range attribué à la source correspondante
# dans SUBJECT_SOURCES.
SUBJECT_EXTERNAL_PROFS = {
    "01_MATHS": [
        ("02", "Rudiments de logique, généralités et révisions sur les suites et les fonctions", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch1_LogiqueFonctions.pdf"),
        ("03", "Étude de fonctions, fonctions logarithme, exponentielle et puissances", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch2_LnExp.pdf"),
        ("04", "Arithmétique", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch3_Arithmetique.pdf"),
        ("05", "Arithmétique — exemples", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/exe3_Arithmetique.pdf"),
    ],
}


def esc(s):
    return html.escape(s or "")


def is_clarisse(filename):
    return "_Clarisse_" in filename or "_Clarisse." in filename


def parse_number_and_title(filename):
    """Extrait le numéro de séquence et un intitulé lisible depuis le nom de fichier."""
    name = filename
    for ext in (".html", ".pdf"):
        if name.endswith(ext):
            name = name[: -len(ext)]
            break
    display = name.replace("_", " ")
    m = re.match(r'^(\d+)[\s-]+(.*)$', display)
    num, rest = (m.group(1), m.group(2)) if m else ("", display)
    rest = re.sub(r'^\d{4}-\d{2}-\d{2}\s+', '', rest)
    rest = re.sub(r'\s+\d{4}-\d{2}-\d{2}\s*$', '', rest)
    rest = re.sub(r'\bCours Clarisse\b', 'Cours de Clarisse', rest)
    return num, rest.strip()


def source_chip_html(name, ville, url, icon, password=None):
    icon_html = f'<img src="{esc(icon)}" class="source-icon" alt="">' if icon else "🏫"
    pin = f'<span class="source-pin">📍 {esc(ville)}</span>'
    if password:
        pin += f'<span class="source-pin">🔑 {esc(password)}</span>'
    if url:
        return (f'<a class="source-chip-inline" href="{esc(url)}" target="_blank" rel="noopener">'
                f'{icon_html} {esc(name)} {pin} <span class="arrow">↗</span></a>')
    return f'<span class="source-chip-inline source-chip-static">{icon_html} {esc(name)} {pin}</span>'


def manual_chip_html(folder):
    entry = SUBJECT_MANUALS.get(folder)
    if not entry:
        return ""
    title, url = entry
    return (f'<a class="manual-chip" href="{esc(url)}" target="_blank" rel="noopener">'
            f'📘 {esc(title)} <span class="arrow">↗</span></a>')


def extra_links_chips_html(folder):
    entries = SUBJECT_EXTRA_LINKS.get(folder, [])
    chips = ""
    for label, url in entries:
        chips += (f'<a class="manual-chip video-chip" href="{esc(url)}" target="_blank" rel="noopener">'
                  f'<img src="{esc(YOUTUBE_ICON)}" class="source-icon" alt="">{esc(label)}</a>')
    return chips


def manual_line_html(folder):
    """Ligne regroupant la puce manuel et les puces liens complémentaires
    (chaînes vidéo, sites tiers) côte à côte, dans un conteneur flex qui
    ne passe à la ligne que si la largeur disponible l'exige."""
    chips = manual_chip_html(folder) + extra_links_chips_html(folder)
    if not chips:
        return ""
    return f'<div class="manual-line">{chips}</div>'


def table_row(num, titre, url, pdf_url=None):
    n_html = esc(num) if num else "—"
    parts = []
    if url:
        parts.append(f'<a class="pill pill-sujet" href="{esc(url)}" target="_blank" rel="noopener">📄 HTML</a>')
    if pdf_url:
        parts.append(f'<a class="pill pill-pdf" href="{esc(pdf_url)}" target="_blank" rel="noopener">📕 PDF</a>')
    link_html = "".join(parts) if parts else '<span class="pill pill-off">—</span>'
    return (f'<tr><td class="col-n">{n_html}</td><td class="col-titre">{esc(titre)}</td>'
            f'<td class="col-link">{link_html}</td></tr>')


def section_row(title, chip_html=""):
    sep = " — " if chip_html else ""
    return f'<tr class="section-row"><td colspan="3">{esc(title)}{sep}{chip_html}</td></tr>'


def empty_row():
    return '<tr><td colspan="3" class="empty-cell">Aucun fichier pour l\'instant.</td></tr>'


def table_open():
    return ('<table><thead><tr>'
            '<th class="col-n">N°</th><th class="col-titre">Intitulé</th>'
            '<th class="col-link">Lien</th></tr></thead><tbody>')


def table_close():
    return '</tbody></table>'


def pdf_url_for(dir_path, folder, f):
    """Si un PDF source du même nom existe à côté du HTML, renvoie son URL."""
    pdf_name = f[:-5] + ".pdf" if f.endswith(".html") else None
    if pdf_name and os.path.isfile(os.path.join(dir_path, pdf_name)):
        return f"{BASE_URL}/{folder}/{pdf_name}"
    return None


def list_entries(dir_path, folder):
    """Liste les cours à afficher sous forme de tuples
    (nom_representatif, url_html_ou_None, url_pdf_ou_None), triés par nom.
    Un cours qui n'a plus de .html (juste le PDF, par ex. après suppression
    d'une page jugée non fidèle) reste affiché avec uniquement le pill PDF."""
    if not os.path.isdir(dir_path):
        return []
    all_files = os.listdir(dir_path)
    html_files = sorted(f for f in all_files if f.endswith(".html"))
    pdf_files = sorted(f for f in all_files if f.endswith(".pdf"))
    html_basenames = {f[:-5] for f in html_files}

    entries = []
    for f in html_files:
        entries.append((f, f"{BASE_URL}/{folder}/{f}", pdf_url_for(dir_path, folder, f)))
    for f in pdf_files:
        if f[:-4] in html_basenames:
            continue
        entries.append((f, None, f"{BASE_URL}/{folder}/{f}"))
    entries.sort(key=lambda e: e[0])
    return entries


def build_subject_block(repo_root, folder, emoji, label, anchor):
    dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
    entries = list_entries(dir_path, folder)

    clarisse_entries = [e for e in entries if is_clarisse(e[0])]
    # Chaque entrée "Cours Profs" devient (numero, titre, url_html, url_pdf) :
    # fichiers réellement présents dans le dépôt (parsés depuis leur nom),
    # complétés par les documents externes déclarés dans SUBJECT_EXTERNAL_PROFS
    # (PDF hébergés directement chez la source, jamais téléchargés ici).
    profs_entries = []
    for f, url, pdf_url in entries:
        if is_clarisse(f):
            continue
        num, titre = parse_number_and_title(f)
        profs_entries.append((num, titre, url, pdf_url))
    for num, titre, pdf_url in SUBJECT_EXTERNAL_PROFS.get(folder, []):
        profs_entries.append((num, titre, None, pdf_url))
    profs_entries.sort(key=lambda e: e[0].zfill(4) if e[0].isdigit() else e[0])

    body = table_open()
    body += section_row("1. Cours de Clarisse")
    if clarisse_entries:
        for f, url, pdf_url in clarisse_entries:
            num, titre = parse_number_and_title(f)
            body += table_row(num, titre, url, pdf_url)
    else:
        body += empty_row()

    sources = SUBJECT_SOURCES.get(folder, [])
    if len(sources) <= 1:
        # Source unique (ou aucune) : un seul pavé "Cours Profs", avec la
        # puce source (nom + ville + lien cliquable) directement dans l'en-tête.
        if sources:
            name, ville, url, icon, _num_range, password = sources[0]
            chip = source_chip_html(name, ville, url, icon, password)
        else:
            chip = ""
        body += section_row("2. Cours Profs", chip)
        if profs_entries:
            for num, titre, url, pdf_url in profs_entries:
                body += table_row(num, titre, url, pdf_url)
        else:
            body += empty_row()
    else:
        # Plusieurs sources : un pavé "Cours Profs — <source>" par source,
        # avec la puce source dans l'en-tête, les fichiers étant attribués
        # selon leur numéro (num_range).
        assigned_idx = set()
        section_idx = 2
        for name, ville, url, icon, num_range, password in sources:
            chip = source_chip_html(name, ville, url, icon, password)
            body += section_row(f"{section_idx}. Cours Profs", chip)
            section_idx += 1
            matched = []
            for i, (num, titre, e_url, e_pdf_url) in enumerate(profs_entries):
                if num_range and num.isdigit() and num_range[0] <= int(num) <= num_range[1]:
                    matched.append((num, titre, e_url, e_pdf_url))
                    assigned_idx.add(i)
            if matched:
                for num, titre, url, pdf_url in matched:
                    body += table_row(num, titre, url, pdf_url)
            else:
                body += empty_row()
        leftover = [e for i, e in enumerate(profs_entries) if i not in assigned_idx]
        if leftover:
            body += section_row(f"{section_idx}. Cours Profs — autres")
            for num, titre, url, pdf_url in leftover:
                body += table_row(num, titre, url, pdf_url)
    body += table_close()

    return (f'<section id="{anchor}" class="subject">'
            f'<h2 class="subject-title">{emoji} {esc(label)}</h2>'
            f'{manual_line_html(folder)}'
            f'{body}</section>')


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    blocks = "".join(build_subject_block(repo_root, folder, emoji, label, anchor)
                      for folder, emoji, label, anchor in SUBJECTS)
    nav_links = "".join(f'<a href="#{anchor}">{emoji} {esc(label)}</a>'
                         for _, emoji, label, anchor in SUBJECTS)

    out = f"""<!-- FICHIER GÉNÉRÉ AUTOMATIQUEMENT — NE PAS ÉDITER À LA MAIN.
     Toute modification doit passer par .claude/skills/transcription-pcsi/regen_index.py
     (constantes SUBJECT_SOURCES / SUBJECT_MANUALS / SUBJECT_EXTRA_LINKS, ou fonctions de rendu),
     puis relancer : python3 .claude/skills/transcription-pcsi/regen_index.py <repo_root>
     Faire un git fetch + merge AVANT de relancer ce script : une autre session
     travaille en parallèle sur ce dépôt et pousse régulièrement sur cette branche. -->
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Prépa Barthou — 1ère année</title>
<link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32.png">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<style>
  :root {{
    --bg: #f2f2f7;
    --card-bg: #ffffff;
    --text: #1c1c1e;
    --sub: #6e6e73;
    --accent: #0a63d3;
    --accent-2: #0a8a4a;
    --border: #e2e2e7;
    --nav-bg: rgba(255,255,255,0.92);
    --section-bg: #dfe8f7;
    --section-text: #1F4E78;
    --row-alt: #fafafc;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #000000;
      --card-bg: #1c1c1e;
      --text: #f5f5f7;
      --sub: #9a9a9e;
      --accent: #4da3ff;
      --accent-2: #4fd97a;
      --border: #2c2c2e;
      --nav-bg: rgba(28,28,30,0.92);
      --section-bg: #16344f;
      --section-text: #bcd6f2;
      --row-alt: #232325;
    }}
  }}
  * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
  html, body {{
    margin: 0; padding: 0;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  header {{ padding: max(env(safe-area-inset-top, 14px), 14px) 16px 8px 16px; text-align: center; }}
  .crosslinks {{ display:flex; justify-content:center; align-items:center; gap:14px; margin-bottom:8px; flex-wrap:wrap; }}
  .crosslinks a {{ display:inline-flex; align-items:center; gap:4px; font-size:12px; font-weight:600; color:var(--accent); text-decoration:none; }}
  .crosslinks img {{ height:16px; width:auto; border-radius:3px; vertical-align:middle; }}
  header h1 {{ font-size: 19px; margin: 4px 0 2px 0; font-weight: 700; }}
  header h1 a {{ display:flex; align-items:center; justify-content:center; gap:8px; color:var(--text); text-decoration:none; }}
  header h1 img {{ height:26px; width:auto; vertical-align:middle; }}
  header p {{ margin: 0; color: var(--sub); font-size: 12px; }}
  html {{ scroll-behavior: smooth; }}
  nav#tabs {{
    position: sticky; top: 0; z-index: 20;
    display: flex; gap: 4px; overflow-x: auto;
    max-width: 760px; margin: 0 auto;
    padding: 6px 8px;
    -webkit-overflow-scrolling: touch;
  }}
  nav#tabs a {{
    flex: 1 1 0; border-radius: 16px;
    padding: 6px 4px; font-size: 12px; font-weight: 600;
    background: var(--card-bg); color: var(--text);
    text-decoration: none; white-space: nowrap;
    border: 1px solid var(--border);
    text-align: center;
  }}
  nav#tabs a.tab-home {{ flex: 0 0 auto; padding: 6px 10px; }}
  main {{ padding: 10px 8px 40px 8px; max-width: 760px; margin: 0 auto; }}
  .subject {{ scroll-margin-top: 56px; padding-top: 4px; }}
  .subject-title {{
    font-size: 18px; font-weight: 700; margin: 22px 4px 6px 4px;
    padding-top: 10px; border-top: 1px solid var(--border);
  }}
  .subject:first-of-type .subject-title {{ border-top: none; margin-top: 4px; }}

  .source-chip-inline {{
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--card-bg); border: 1px solid var(--border);
    padding: 3px 9px; border-radius: 12px; margin-left: 4px;
    color: var(--accent); font-weight: 600; text-decoration: none;
    font-size: 11px; text-transform: none; letter-spacing: normal;
  }}
  .source-chip-inline.source-chip-static {{ color: var(--section-text); }}
  .source-chip-inline .arrow {{ opacity: .6; }}
  .source-icon {{ height:13px; width:auto; border-radius:2px; vertical-align:middle; }}
  .source-pin {{ opacity: .7; font-weight: 500; }}

  .manual-line {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 2px 4px 8px 4px; }}
  .manual-chip {{
    display: inline-flex; align-items: center; gap: 3px;
    background: rgba(10,138,74,0.10); border: 1px solid var(--border);
    padding: 3px 8px; border-radius: 10px;
    color: var(--accent-2); font-weight: 600; text-decoration: none; font-size: 10.5px;
  }}
  .manual-chip .arrow {{ opacity: .6; }}
  .manual-chip.video-chip {{ background: rgba(214,40,40,0.08); color: #d62828; }}

  table {{
    width: 100%; border-collapse: collapse;
    background: var(--card-bg); border-radius: 12px;
    overflow: hidden; font-size: 12.5px;
    border: 1px solid var(--border);
  }}
  thead th {{
    background: #1F4E78; color: #fff;
    font-size: 11px; text-transform: uppercase; letter-spacing: .03em;
    padding: 8px 6px; text-align: left; font-weight: 700;
  }}
  tbody tr:nth-child(even):not(.section-row) {{ background: var(--row-alt); }}
  tbody tr:not(.section-row) {{ border-top: 1px solid var(--border); }}
  td {{ padding: 7px 6px; vertical-align: middle; }}
  .section-row td {{
    background: var(--section-bg); color: var(--section-text);
    font-weight: 700; font-size: 11.5px; text-transform: uppercase;
    letter-spacing: .02em; padding: 7px 8px;
  }}
  .col-n {{ width: 40px; color: var(--sub); font-size: 11.5px; white-space: nowrap; }}
  .col-titre {{ min-width: 140px; }}
  .col-link {{ width: 1%; white-space: nowrap; text-align: center; }}
  .empty-cell {{ color: var(--sub); font-size: 12.5px; font-style: italic; text-align: center; }}

  .pill {{ display: inline-block; font-size: 11px; font-weight: 700; text-decoration: none; padding: 4px 8px; border-radius: 8px; white-space: nowrap; margin: 2px; }}
  .pill-sujet {{ background: rgba(10,99,211,0.12); color: var(--accent); }}
  .pill-pdf {{ background: rgba(214,40,40,0.12); color:#d62828; }}
  .pill-off {{ color: var(--sub); font-size: 12px; }}

  footer {{ text-align: center; padding: 16px; color: var(--sub); font-size: 10.5px; }}

  @media (max-width: 420px) {{ table {{ font-size: 11.5px; }} nav#tabs a {{ font-size: 11px; padding: 6px 2px; }} .manual-chip {{ font-size: 9.5px; padding: 3px 6px; }} }}
</style>
</head>
<body>

<header>
  <div class="crosslinks">
    <a href="../../index.html">🏠 Accueil</a>
    <a href="../../Kit_Revision_PCSI.html">🎯 DS</a>
    <a href="../../Ressources_MP.html">🔗 Liens</a>
  </div>
  <h1><a href="https://www.prepabarthou.fr/cours/my/courses.php" target="_blank" rel="noopener"><img src="../../logo-barthou.png" alt="">Prépa Barthou — 1ère année</a></h1>
  <p>Cours, TD et exercices — mis à jour au fil de l'année</p>
</header>

<nav id="tabs">
  <a href="../../index.html" class="tab-home" title="Accueil">🏠</a>
{nav_links}
</nav>

<main>
{blocks}
</main>

<footer>Lien fixe — recharge la page pour voir les derniers fichiers ajoutés.</footer>

</body>
</html>
"""
    index_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", "index.html")
    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
