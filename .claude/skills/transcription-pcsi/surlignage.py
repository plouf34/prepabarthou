#!/usr/bin/env python3
"""Surlignage « chapitre en cours » des sections Exercices et DS des 4 pages
matière (Maths.html / Physique.html / Chimie.html / SI.html).

Usage :
    python3 surlignage.py <repo_root>            # vérifie puis applique
    python3 surlignage.py <repo_root> --check    # vérifie seulement (n'écrit rien)
    python3 surlignage.py <repo_root> --date 2026-10-05   # simule une autre date

Règles (voir aussi Prepa_barthou/PROMPT_TRANSCRIPTION.md) :
  - JAUNE        = documents liés au dernier chapitre des cours de Clarisse
                   (plus grand numéro ChNN des fichiers *_Cours_Clarisse_*).
  - ORANGE PÂLE  = documents liés au dernier chapitre des cours des profs de
                   Louis Barthou, seulement s'il est SUPÉRIEUR à celui de
                   Clarisse (ou s'il n'y a aucun cours de Clarisse). Même
                   numéro → jaune seul. Les cours des autres lycées
                   (Saint-Louis, Sainte-Geneviève, Janson…) sont ignorés.
  - Physique : les PDF Barthou (polycopié de toute l'année) n'ont pas de
    numéro ChNN ; le dernier chapitre Barthou est celui de la semaine en
    cours du programme de khôlle (Prepa_barthou/programme_kholle_physique.json).
    Si le dernier cours de Clarisse en Physique date de cette même semaine
    (ou plus tard), le cours de Clarisse prime : jaune seul.

Ce script NE DÉCIDE PAS quels documents sont liés à un chapitre : ce choix
demande de lire les documents, il est fait par Claude et consigné dans
Prepa_barthou/surlignage.json (clé "liens" de chaque matière, avec pour
chaque chapitre la "cle" attendue). Le script :
  1. calcule le chapitre attendu en jaune / orange pour chaque matière et
     signale « ⚠️ SURLIGNAGE À REVOIR » quand surlignage.json ne correspond
     plus (nouveau cours de Clarisse ou de Barthou, changement de semaine de
     khôlle) — Claude doit alors relire le nouveau cours et les documents,
     puis mettre à jour surlignage.json ;
  2. applique surlignage.json aux pages (idempotent : retire d'abord tout
     surlignage précédent, puis pose les classes hl-jaune / hl-orange sur
     les lignes <tr> et les puces .manual-chip dont un lien figure dans
     "liens", et ajoute une légende en tête des sections concernées).
"""
import datetime
import html
import json
import os
import re
import sys

SUBJECTS = [
    ("01_MATHS", "Maths"),
    ("02_PHYSIQUE", "Physique"),
    ("03_CHIMIE", "Chimie"),
    ("04_SI", "SI"),
]
BARTHOU = "Lycée Louis Barthou"
CONFIG = os.path.join("Prepa_barthou", "surlignage.json")
KHOLLE = os.path.join("Prepa_barthou", "programme_kholle_physique.json")

CLARISSE_RE = re.compile(r'^\d+_Ch(\d+)_Cours_Clarisse_(.+?)_(\d{4}-\d{2}-\d{2})\.(?:html|pdf)$')
PROFS_RE = re.compile(r'^(\d+)_Ch(\d+)_Cours_Profs_(.+?)_(\d{4}-\d{2}-\d{2})\.(?:html|pdf)$')


def barthou_range(folder):
    """Plage de numéros de fichiers « Cours Profs » attribués à Louis Barthou,
    lue dans SUBJECT_SOURCES de regen_index.py (source unique de vérité)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from regen_index import SUBJECT_SOURCES
    for name, _ville, _url, _icon, num_range, _pwd in SUBJECT_SOURCES.get(folder, []):
        if name == BARTHOU:
            return num_range or (0, 10**6)
    return None


def latest_clarisse(dir_path):
    best = None
    for f in os.listdir(dir_path) if os.path.isdir(dir_path) else []:
        m = CLARISSE_RE.match(f)
        if m:
            key = (int(m.group(1)), m.group(3))
            if best is None or key > best[0]:
                best = (key, m.group(2).replace("-", " "))
    if not best:
        return None
    (ch, date), titre = best
    return {"cle": f"Ch{ch:02d}", "num": ch, "date": date, "titre": titre}


def latest_barthou_files(dir_path, folder):
    rng = barthou_range(folder)
    if rng is None:
        return None
    best = None
    for f in os.listdir(dir_path) if os.path.isdir(dir_path) else []:
        m = PROFS_RE.match(f)
        if m and rng[0] <= int(m.group(1)) <= rng[1]:
            key = (int(m.group(2)), m.group(4))
            if best is None or key > best[0]:
                best = (key, m.group(3).replace("-", " "))
    if not best:
        return None
    (ch, date), titre = best
    return {"cle": f"Ch{ch:02d}", "num": ch, "date": date, "titre": titre}


def kholle_week(repo_root, today):
    path = os.path.join(repo_root, KHOLLE)
    if not os.path.isfile(path):
        return None
    weeks = json.load(open(path, encoding="utf-8"))["semaines"]
    current = None
    for w in weeks:
        if w["debut"] <= today:
            current = w
    return current


def expected(repo_root, today):
    """Chapitre attendu en jaune / orange pour chaque matière."""
    out = {}
    for folder, label in SUBJECTS:
        dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
        cla = latest_clarisse(dir_path)
        exp = {"jaune": None, "orange": None}
        if cla:
            exp["jaune"] = {"cle": cla["cle"], "libelle": f'{cla["cle"]} — {cla["titre"]} (cours de Clarisse du {cla["date"]})'}
        if folder == "02_PHYSIQUE":
            w = kholle_week(repo_root, today)
            if w and w.get("chapitre"):
                cle = f'{w["theme"]}-Ch{w["chapitre"]}'
                clarisse_prime = cla is not None and cla["date"] >= w["debut"]
                if not clarisse_prime:
                    exp["orange"] = {"cle": cle, "libelle": f'{w["theme"]} Ch{w["chapitre"]} — {w["titre"]} (khôlle {w["semaine"]} du {w["debut"]} ; {w["exercices"]})'}
        else:
            bar = latest_barthou_files(dir_path, folder)
            if bar and (cla is None or bar["num"] > cla["num"]):
                exp["orange"] = {"cle": bar["cle"], "libelle": f'{bar["cle"]} — {bar["titre"]} (cours des profs de Louis Barthou du {bar["date"]})'}
        out[label] = exp
    return out


def load_config(repo_root):
    path = os.path.join(repo_root, CONFIG)
    if not os.path.isfile(path):
        return {}
    return json.load(open(path, encoding="utf-8"))


def check(repo_root, today):
    """Compare l'état attendu à surlignage.json. Renvoie la liste des écarts."""
    cfg = load_config(repo_root)
    exp = expected(repo_root, today)
    issues = []
    for label, e in exp.items():
        c = cfg.get(label, {})
        for couleur in ("jaune", "orange"):
            want = e[couleur]["cle"] if e[couleur] else None
            have = (c.get(couleur) or {}).get("cle")
            if want != have:
                issues.append(f"{label} / {couleur} : attendu {e[couleur]['libelle'] if e[couleur] else 'aucun surlignage'}"
                              f" — surlignage.json contient {have or 'rien'}")
    return exp, issues


LEGEND_RE = re.compile(r'<div class="hl-legend"[^>]*>.*?</div>\s*', re.S)
TR_RE = re.compile(r'<tr(?P<attrs>(?:\s[^>]*)?)>(?P<body>.*?)</tr>', re.S)
CHIP_RE = re.compile(r'<a class="(?P<cls>manual-chip[^"]*)"(?P<rest>[^>]*)>')


def _set_classes(attrs, add):
    """Retire hl-* / data-hl / title posé par ce script, puis ajoute `add`."""
    attrs = re.sub(r'\s+data-hl-title="[^"]*"', '', attrs)
    attrs = re.sub(r'\s+data-hl="1"\s+title="[^"]*"', '', attrs)
    m = re.search(r'\sclass="([^"]*)"', attrs)
    classes = m.group(1).split() if m else []
    classes = [c for c in classes if c not in ("hl-jaune", "hl-orange")]
    if add:
        classes.append(add)
    new_cls = f' class="{" ".join(classes)}"' if classes else ""
    if m:
        attrs = attrs[:m.start()] + new_cls + attrs[m.end():]
    else:
        attrs = new_cls + attrs
    return attrs


def _apply_section(section, liens, cfg_subject):
    section = LEGEND_RE.sub("", section)
    used = set()

    def tr_sub(m):
        attrs, body = m.group("attrs"), m.group("body")
        hrefs = [html.unescape(h) for h in re.findall(r'href="([^"]+)"', body)]
        hit = next((liens[h] for h in hrefs if h in liens), None) if 'section-row' not in attrs else None
        attrs = _set_classes(attrs, hit["couleur"] and f'hl-{hit["couleur"]}' if hit else None)
        if hit:
            used.add(hit["couleur"])
            note = hit.get("note")
            if note:
                attrs += f' data-hl="1" title="{html.escape(note, quote=True)}"'
        return f'<tr{attrs}>{body}</tr>'

    section = TR_RE.sub(tr_sub, section)

    def chip_sub(m):
        cls = [c for c in m.group("cls").split() if c not in ("hl-jaune", "hl-orange")]
        rest = m.group("rest")
        rest = re.sub(r'\s+data-hl="1"\s+title="[^"]*"', '', rest)
        href = re.search(r'href="([^"]+)"', rest)
        hit = liens.get(html.unescape(href.group(1))) if href else None
        if hit:
            cls.append(f'hl-{hit["couleur"]}')
            used.add(hit["couleur"])
            if hit.get("note"):
                rest += f' data-hl="1" title="{html.escape(hit["note"], quote=True)}"'
        return f'<a class="{" ".join(cls)}"{rest}>'

    section = CHIP_RE.sub(chip_sub, section)

    if used:
        parts = []
        for couleur in ("jaune", "orange"):
            if couleur in used and cfg_subject.get(couleur):
                qui = "dernier cours de Clarisse" if couleur == "jaune" else "dernier cours des profs de Louis Barthou"
                parts.append(f'<span><span class="hl-swatch {couleur}"></span>{html.escape(qui)} : '
                             f'<b>{html.escape(cfg_subject[couleur]["libelle"])}</b></span>')
        legend = f'<div class="hl-legend">{"".join(parts)}</div>'
        section = re.sub(r'(<h2 class="section-title">.*?</h2>\s*)', lambda m: m.group(1) + legend, section, count=1, flags=re.S)
    return section


def apply(repo_root):
    cfg = load_config(repo_root)
    for _folder, label in SUBJECTS:
        path = os.path.join(repo_root, f"{label}.html")
        if not os.path.isfile(path):
            continue
        data = open(path, encoding="utf-8").read()
        c = cfg.get(label, {})
        liens = {l["url"]: l for l in c.get("liens", []) if (c.get(l["couleur"]) or {}).get("cle")}
        for sid in ("exercices", "ds"):
            data = re.sub(rf'<section id="{sid}">.*?</section>',
                          lambda m: _apply_section(m.group(0), liens, c), data, count=1, flags=re.S)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
        n = len(re.findall(r'class="[^"]*\bhl-(?:jaune|orange)\b', data))
        print(f"Surlignage appliqué à {label}.html : {n} élément(s)")


def report(exp, issues):
    for label, e in exp.items():
        j = e["jaune"]["libelle"] if e["jaune"] else "—"
        o = e["orange"]["libelle"] if e["orange"] else "—"
        print(f"  {label:9s} jaune : {j}\n  {'':9s} orange : {o}")
    if issues:
        print("⚠️ SURLIGNAGE À REVOIR — relire le(s) nouveau(x) cours et les documents Exercices/DS,")
        print("   puis mettre à jour Prepa_barthou/surlignage.json (cle + libelle + liens) :")
        for i in issues:
            print("   - " + i)
    else:
        print("✅ surlignage.json est à jour avec les derniers cours et la semaine de khôlle.")


def main():
    args = sys.argv[1:]
    repo_root = args[0] if args and not args[0].startswith("--") else "."
    today = datetime.date.today().isoformat()
    if "--date" in args:
        today = args[args.index("--date") + 1]
    exp, issues = check(repo_root, today)
    print(f"Chapitres en cours au {today} :")
    report(exp, issues)
    if "--check" not in args:
        apply(repo_root)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
