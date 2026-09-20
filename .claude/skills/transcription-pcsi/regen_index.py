#!/usr/bin/env python3
"""Regenerate the 4 subject pages (Maths.html / Physique.html / Chimie.html /
SI.html, à la racine du dépôt) en scannant les 4 dossiers de cours.
Usage: python3 regen_index.py <repo_root>

Chaque page matière est une SEULE page qui défile de haut en bas à travers 3
sections (Cours puis Exercices puis DS), avec une barre d'onglets sticky en
haut qui ne fait que sauter à l'ancre correspondante (#cours/#exercices/#ds)
dans la même page — ce n'est plus une navigation entre fichiers séparés.
Seule la section <section id="cours"> est ENTIÈREMENT générée par ce script ;
les sections <section id="exercices"> et <section id="ds"> sont tenues à la
main (comme l'était Kit_Revision_PCSI.html) et PRÉSERVÉES telles quelles à
chaque régénération : main() relit le fichier existant, extrait ces deux
sections verbatim, et ne remplace que la section Cours.

⚠️ AVANT DE LANCER CE SCRIPT : faire un `git fetch` + `git merge` (ou pull)
sur la branche courante. Une autre session travaille en parallèle sur ce
dépôt et pousse régulièrement sur cette même branche ; lancer ce script
depuis un checkout périmé régénère la section Cours en écrasant silencieusement
les correctifs poussés entre-temps (libellés, favicons, liens...).
Toute modification du contenu de la section Cours (libellés, sources,
manuels, liens complémentaires) doit passer par les constantes ci-dessous
(SUBJECT_SOURCES / SUBJECT_MANUALS / SUBJECT_EXTRA_LINKS / SUBJECT_EXTERNAL_PROFS)
ou par les fonctions de rendu, puis relancer ce script. Les sections
Exercices et DS, elles, s'éditent directement dans le fichier <Matière>.html
(ce script ne les touche jamais, il se contente de les recopier telles
qu'elles étaient avant de régénérer la section Cours).
"""
import sys
import os
import re
import html

SUBJECTS = [
    ("01_MATHS", "🔢", "Maths"),
    ("02_PHYSIQUE", "⚛️", "Physique"),
    ("03_CHIMIE", "🧪", "Chimie"),
    ("04_SI", "⚙️", "SI"),
]

# (clé d'ancre, emoji, libellé affiché) — ordre = ordre d'apparition en
# défilant la page (barre d'onglets sticky en haut = simples ancres #<clé>).
TABS = [
    ("cours", "📘", "Cours"),
    ("exercices", "📝", "Exercices"),
    ("ds", "🎯", "DS"),
]

BASE_URL = "https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee"

# Établissement(s) source des documents "Cours Profs" pour chaque matière
# (ville affichée à titre indicatif, sans classement — ce n'est pas le Kit de révision).
# 5e élément = (num_min, num_max) des fichiers "Cours Profs" attribués à cette source
# (None = source unique, capte tous les fichiers profs de la matière).
SUBJECT_SOURCES = {
    "01_MATHS": [
        ("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "logo-barthou.png", (1, 1), None),
        ("Lycée Saint-Louis", "Paris", "https://pcsi1-saint-louis.ovh/site/", "logo-saint-louis.png", (2, 5), None),
    ],
    "02_PHYSIQUE": [("Lycée Louis Barthou", "Pau", "https://www.prepabarthou.fr/cours/my/courses.php", "logo-barthou.png", None, None)],
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
    "01_MATHS": ("Maths — Ellipses", "manuels/Maths_PCSI_Ellipses_2021.pdf"),
    "02_PHYSIQUE": ("Physique — Ellipses", "manuels/Physique_PCSI_Ellipses_2021.pdf"),
    "04_SI": ("SI — Vuibert", "manuels/SI_Vuibert.pdf"),
}

# Ressources complémentaires libres (chaînes vidéo, sites tiers...) affichées
# sous le manuel, sous forme de puces cliquables. Chaînes YouTube complémentaires
# par matière : (libellé court — nom de l'école ou du site/chaîne YouTube —, url).
# Le logo YouTube est ajouté automatiquement au rendu (cf. YOUTUBE_ICON).
SUBJECT_EXTRA_LINKS = {
    "01_MATHS": [
        ("Lycée du Parc", "https://www.youtube.com/@Giraud-Laignel-hy9hb"),
        ("Bibmath", "https://www.youtube.com/@bibmath001/featured"),
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
# local n'existe pour ce cours. Liste de (nom_source, numero, titre, url_pdf)
# par matière ; nom_source doit correspondre exactement au nom déclaré dans
# SUBJECT_SOURCES pour cette matière (la numérotation repart donc à 01 pour
# chaque source, indépendamment des fichiers réels d'une autre source).
SUBJECT_EXTERNAL_PROFS = {
    "01_MATHS": [
        ("Lycée Saint-Louis", "01", "Rudiments de logique, généralités et révisions sur les suites et les fonctions", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch1_LogiqueFonctions.pdf"),
        ("Lycée Saint-Louis", "02", "Étude de fonctions, fonctions logarithme, exponentielle et puissances", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch2_LnExp.pdf"),
        ("Lycée Saint-Louis", "03", "Arithmétique", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/ch3_Arithmetique.pdf"),
        ("Lycée Saint-Louis", "04", "Arithmétique — exemples", "https://pcsi1-saint-louis.ovh/site/images/Doc2627/exe3_Arithmetique.pdf"),
    ],
}


def esc(s):
    return html.escape(s or "")


def is_clarisse(filename):
    return "_Clarisse_" in filename or "_Clarisse." in filename


def is_td_or_exercice(titre):
    """Un fichier "Cours Profs" dont l'intitulé contient TD/Exercice n'est pas
    un cours mais un TD (= un exercice) : il ne doit pas apparaître dans le
    tableau Cours, mais dans l'onglet Exercices (ajouté à la main)."""
    return bool(re.search(r'\bTD\b', titre) or re.search(r'\bExercice', titre, re.I))


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


def build_subject_body(repo_root, folder):
    """Contenu de l'onglet Cours pour une matière : puce manuel/liens vidéo
    puis tableau N° / Intitulé / Lien (sections « Cours de Clarisse » /
    « Cours Profs »)."""
    dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
    entries = list_entries(dir_path, folder)

    clarisse_entries = [e for e in entries if is_clarisse(e[0])]
    # Chaque entrée "Cours Profs" devient (source_tag, numero, titre, url_html,
    # url_pdf) : fichiers réellement présents dans le dépôt (source_tag=None,
    # attribués par num_range ci-dessous), complétés par les documents externes
    # déclarés dans SUBJECT_EXTERNAL_PROFS (source_tag = nom exact de la
    # source, PDF hébergés directement chez elle, jamais téléchargés ici — leur
    # numérotation repart donc à 01 indépendamment des fichiers réels).
    profs_entries = []
    for f, url, pdf_url in entries:
        if is_clarisse(f):
            continue
        num, titre = parse_number_and_title(f)
        if is_td_or_exercice(titre):
            continue
        profs_entries.append((None, num, titre, url, pdf_url))
    for source_name, num, titre, pdf_url in SUBJECT_EXTERNAL_PROFS.get(folder, []):
        profs_entries.append((source_name, num, titre, None, pdf_url))

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
            for _tag, num, titre, url, pdf_url in profs_entries:
                body += table_row(num, titre, url, pdf_url)
        else:
            body += empty_row()
    else:
        # Plusieurs sources : un pavé "Cours Profs — <source>" par source.
        # Un fichier réel (tag=None) est attribué selon son numéro (num_range) ;
        # un document externe (tag=nom de la source) est attribué directement
        # par correspondance de nom, sans jouer avec les plages numériques des
        # autres sources.
        assigned_idx = set()
        section_idx = 2
        for name, ville, url, icon, num_range, password in sources:
            chip = source_chip_html(name, ville, url, icon, password)
            body += section_row(f"{section_idx}. Cours Profs", chip)
            section_idx += 1
            matched = []
            for i, (tag, num, titre, e_url, e_pdf_url) in enumerate(profs_entries):
                if i in assigned_idx:
                    continue
                belongs = tag == name or (
                    tag is None and num_range and num.isdigit() and num_range[0] <= int(num) <= num_range[1]
                )
                if belongs:
                    matched.append((num, titre, e_url, e_pdf_url))
                    assigned_idx.add(i)
            if matched:
                for num, titre, url, pdf_url in matched:
                    body += table_row(num, titre, url, pdf_url)
            else:
                body += empty_row()
        leftover = [(num, titre, url, pdf_url) for i, (_tag, num, titre, url, pdf_url) in enumerate(profs_entries) if i not in assigned_idx]
        if leftover:
            body += section_row(f"{section_idx}. Cours Profs — autres")
            for num, titre, url, pdf_url in leftover:
                body += table_row(num, titre, url, pdf_url)
    body += table_close()

    return manual_line_html(folder) + body


def tab_bar_html():
    links = [f'<a href="#{key}">{emoji} {esc(name)}</a>' for key, emoji, name in TABS]
    return f'<nav class="tab-bar">{"".join(links)}</nav>'


def subject_switch_html(current_folder):
    links = []
    for folder, emoji, label in SUBJECTS:
        cls = ' class="active"' if folder == current_folder else ""
        links.append(f'<a href="{esc(label)}.html"{cls}>{emoji} {esc(label)}</a>')
    return f'<nav class="subject-switch">{"".join(links)}</nav>'


def section_title_html(key):
    emoji, name = next((e, n) for k, e, n in TABS if k == key)
    return f'<h2 class="section-title">{emoji} {esc(name)}</h2>'


def page_shell(folder, emoji, label, sections_html, banner=""):
    """Gabarit commun aux 4 pages matière : en-tête, barre d'onglets sticky
    Cours/Exercices/DS (simples ancres #cours/#exercices/#ds dans CETTE même
    page — on ne change plus de fichier), sélecteur de matière, les 3
    sections empilées, script de mise en surbrillance de l'onglet visible."""
    return f"""{banner}<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(label)} — Prépa PCSI</title>
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="assets/pcsi.css?v=4">
</head>
<body>

<header>
  <div class="crosslinks">
    <a href="index.html">🏠 Accueil</a>
    <a href="Ressources_MP.html">🔗 Liens</a>
  </div>
  <h1>{emoji} {esc(label)}</h1>
  <p>Cours, exercices et DS — mis à jour au fil de l'année</p>
</header>

{tab_bar_html()}
{subject_switch_html(folder)}

<main>
{sections_html}
</main>

<script src="assets/pcsi.js" defer></script>
</body>
</html>
"""


def existing_section(repo_root, label, section_id, fallback_inner_html):
    """Relit le fichier <Matière>.html déjà présent (s'il existe) et renvoie
    sa section #<section_id> telle quelle, pour ne jamais écraser un contenu
    tenu à la main (Exercices/DS) en régénérant la section Cours."""
    path = os.path.join(repo_root, f"{label}.html")
    if os.path.isfile(path):
        data = open(path, encoding="utf-8").read()
        m = re.search(rf'<section id="{section_id}">.*?</section>', data, re.S)
        if m:
            return m.group(0)
    return f'<section id="{section_id}">{section_title_html(section_id)}{fallback_inner_html}</section>'


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    banner = (
        "<!-- Section Cours GÉNÉRÉE AUTOMATIQUEMENT — ne pas l'éditer à la main.\n"
        "     Toute modification doit passer par .claude/skills/transcription-pcsi/regen_index.py\n"
        "     (constantes SUBJECT_SOURCES / SUBJECT_MANUALS / SUBJECT_EXTRA_LINKS / SUBJECT_EXTERNAL_PROFS,\n"
        "     ou fonctions de rendu), puis relancer :\n"
        "     python3 .claude/skills/transcription-pcsi/regen_index.py <repo_root>\n"
        "     Faire un git fetch + merge AVANT de relancer ce script : une autre session\n"
        "     travaille en parallèle sur ce dépôt et pousse régulièrement sur cette branche.\n"
        "     Les sections Exercices et DS de ce même fichier sont tenues à la main et\n"
        "     préservées telles quelles par ce script — seule la section Cours est réécrite.\n"
        "     Convention de libellé (Exercices ET DS) : utiliser \"Sujet\"/\"Corrigés\", jamais\n"
        "     \"Énoncé\"/\"Indications\" — a été renommé plusieurs fois, merci de garder ces mots. -->\n"
    )
    placeholder = (
        '<div class="placeholder"><div class="placeholder-icon">📝</div>'
        '<div class="placeholder-title">Bientôt disponible</div>'
        '<div class="placeholder-sub">Le contenu arrivera ici au fil de l\'année.</div></div>'
    )
    for folder, emoji, label in SUBJECTS:
        cours_section = f'<section id="cours">{section_title_html("cours")}{build_subject_body(repo_root, folder)}</section>'
        exercices_section = existing_section(repo_root, label, "exercices", placeholder)
        ds_section = existing_section(repo_root, label, "ds", placeholder)
        sections_html = cours_section + exercices_section + ds_section
        out = page_shell(folder, emoji, label, sections_html, banner=banner)
        out_path = os.path.join(repo_root, f"{label}.html")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
