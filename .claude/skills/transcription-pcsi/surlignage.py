#!/usr/bin/env python3
"""Surlignage « en cours » des sections Exercices et DS des 4 pages matière
(Maths.html / Physique.html / Chimie.html / SI.html). Règles décidées par
Fabien le 01/10/2026 (voir CLAUDE.md et la section SURLIGNAGE du prompt maître).

Usage :
    python3 surlignage.py <repo_root>            # vérifie puis applique
    python3 surlignage.py <repo_root> --check    # vérifie seulement (n'écrit rien)
    python3 surlignage.py <repo_root> --date 2026-10-05   # simule une autre date

  - JAUNE  = documents liés au COURS EN COURS :
             * le dernier cours manuscrit de Clarisse (plus grand ChNN des
               fichiers *_Cours_Clarisse_*) ;
             * sinon le cours des profs de Louis Barthou DATÉ dont l'intervalle
               contient la date du jour (de sa date jusqu'à la veille du cours
               prof suivant). Cours non datés (ex. polycopié de Physique) :
               ignorés.
             * Clarisse ET profs : Clarisse fait foi.
             Exceptions (seulement si stipulées) : clé "exceptions" de la
             matière dans surlignage.json — "profs_priment": true (le cours
             prof en cours prime sur Clarisse), "cours_dates": {fichier:
             [debut, fin]} (donne un intervalle à un cours non daté).
  - ORANGE = documents liés à la COLLE EN COURS (programmes de colle :
             SUBJECT_COLLES de regen_index.py). Une colle est en cours de sa
             date de début jusqu'au dimanche qui suit sa date de fin.
  - JAUNE + ORANGE (couleur "jo") = documents liés aux deux : pastille et
             pavé en dégradé du jaune (haut) vers l'orange (bas).

Ce script NE DÉCIDE PAS quels documents sont liés au cours ou à la colle :
ce choix demande de lire les documents, il est fait par Claude et consigné
dans Prepa_barthou/surlignage.json (clé "liens" : url + couleur
jaune|orange|jo + note ; "jaune"/"orange" = {cle, libelle} attendus). Le script :
  1. calcule le cours (jaune) et la colle (orange) en cours pour chaque matière
     et signale « ⚠️ SURLIGNAGE À REVOIR » quand surlignage.json ne
     correspond plus (nouveau cours, changement de colle) — Claude doit alors
     relire les documents et mettre à jour surlignage.json ;
  2. applique surlignage.json aux pages (idempotent) : classes hl-jaune /
     hl-orange / hl-jo sur les lignes <tr> Exercices/DS dont un lien figure
     dans "liens", légende en tête des sections. Dans la section Cours : la
     ligne du cours en cours (jaune), les cours d'autres lycées de la clé
     "cours" (jaune), et en Physique le chapitre du polycopié de la colle en
     cours (orange).
  Ne sont surlignés que des exercices, TD, DS et interros : jamais les puces
  de sites (Bibmath, Exo7…) ni les cahiers de calcul.
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
# « _Cours_Profs_ » sans suffixe de lycée uniquement : un fichier
# « _Cours_Profs-SaintLouis_ » (autre lycée) n'est jamais un cours Barthou.
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
                best = (key, m.group(2).replace("-", " "), f)
    if not best:
        return None
    (ch, date), titre, f = best
    return {"cle": f"Ch{ch:02d}", "num": ch, "date": date, "titre": titre, "fichier": f}


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
                best = (key, m.group(3).replace("-", " "), f)
    if not best:
        return None
    (ch, date), titre, f = best
    return {"cle": f"Ch{ch:02d}", "num": ch, "date": date, "titre": titre, "fichier": f}


def _sans_accents(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def physique_barthou_file(dir_path, theme, num):
    """PDF du polycopié Barthou de Physique correspondant à un chapitre du
    programme de khôlle (ex. « Électricité », 2 → 02-..._Cours_Electricite_-_2_-_...pdf)."""
    t = _sans_accents(theme)
    for f in sorted(os.listdir(dir_path)) if os.path.isdir(dir_path) else []:
        m = re.search(r'_Cours_([A-Za-z]+)_-_(\d+)_-_', f)
        if m and _sans_accents(m.group(1)) == t and int(m.group(2)) == num:
            return f
    return None


def latest_barthou_dated(dir_path, folder, today):
    """Cours des profs de Louis Barthou DATÉ dont l'intervalle contient
    `today` : le plus récent dont la date est <= today (son intervalle court
    jusqu'à la veille du cours prof suivant)."""
    rng = barthou_range(folder)
    if rng is None:
        return None
    best = None
    for f in os.listdir(dir_path) if os.path.isdir(dir_path) else []:
        m = PROFS_RE.match(f)
        if m and rng[0] <= int(m.group(1)) <= rng[1] and m.group(4) <= today:
            key = (m.group(4), int(m.group(2)))
            if best is None or key > best[0]:
                best = (key, m.group(3).replace("-", " "), f)
    if not best:
        return None
    (date, ch), titre, f = best
    return {"cle": f"Ch{ch:02d}", "num": ch, "date": date, "titre": titre, "fichier": f}


def colle_en_cours(repo_root, folder, today):
    """Colle en cours (programmes de colle de regen_index.SUBJECT_COLLES) :
    de sa date de début jusqu'au dimanche qui suit sa date de fin."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from regen_index import SUBJECT_COLLES, colles_from_kholle
    if folder not in SUBJECT_COLLES:
        return None
    path = os.path.join(repo_root, SUBJECT_COLLES[folder])
    if not os.path.isfile(path):
        return None
    data = json.load(open(path, encoding="utf-8"))
    brut = data
    if "semaines" in data:
        data = colles_from_kholle(data)
    pref = data.get("prefixe", "Q")
    for q in data["quinzaines"]:
        fin = (datetime.date.fromisoformat(q["fin"]) + datetime.timedelta(days=2)).isoformat()
        if q["debut"] <= today <= fin:
            sem = next((w for w in brut.get("semaines", []) if int(w["semaine"][1:]) == q["numero"]), None)
            return {"cle": f'{pref}{q["numero"]}', "debut": q["debut"], "fin": q["fin"],
                    "titre": re.sub(r"<[^>]+>", "", q["titre"]), "kholle": sem}
    return None


def expected(repo_root, today, cfg=None):
    """Cours (jaune) et colle (orange) attendus pour chaque matière."""
    cfg = cfg if cfg is not None else load_config(repo_root)
    out = {}
    for folder, label in SUBJECTS:
        dir_path = os.path.join(repo_root, "Prepa_barthou", "1ere_annee", folder)
        exc = (cfg.get(label) or {}).get("exceptions") or {}
        cla = latest_clarisse(dir_path)
        bar = latest_barthou_dated(dir_path, folder, today)
        # Cours non datés auxquels une exception donne un intervalle.
        for f, (deb, fin) in (exc.get("cours_dates") or {}).items():
            if deb <= today <= fin:
                bar = {"cle": f, "date": deb, "titre": os.path.splitext(f)[0], "fichier": f}
        exp = {"jaune": None, "orange": None, "cours": []}
        src = cla
        if bar and (cla is None or exc.get("profs_priment")):
            src = bar
        if src:
            qui = "cours de Clarisse" if src is cla else "cours des profs de Louis Barthou"
            exp["cours"].append((src["fichier"], "jaune", f"Cours en cours ({qui})"))
            exp["jaune"] = {"cle": src["cle"], "libelle": f'{src["cle"]} — {src["titre"]} ({qui} du {src["date"]})'}
        col = colle_en_cours(repo_root, folder, today)
        if col:
            exp["orange"] = {"cle": col["cle"], "libelle": f'Colle {col["cle"]} du {col["debut"]} — {col["titre"]}'}
            w = col.get("kholle")
            if w and w.get("chapitre"):
                f = physique_barthou_file(dir_path, w["theme"], w["chapitre"])
                if f:
                    exp["cours"].append((f, "orange", f'Chapitre de la colle {w["semaine"]} ({w["exercices"]})'))
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
    exp = expected(repo_root, today, cfg)
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


HL_CLASSES = ("hl-jaune", "hl-orange", "hl-vert", "hl-jv", "hl-jo")


def _couleur_active(couleur, cfg_subject):
    """Couleur effective d'un lien selon ce qui est en cours : un lien « jv »
    dont la colle (ou le cours) n'est plus en cours ne garde que l'autre."""
    j = bool((cfg_subject.get("jaune") or {}).get("cle"))
    v = bool((cfg_subject.get("orange") or {}).get("cle"))
    if couleur == "jo":
        return "jo" if (j and v) else ("jaune" if j else ("orange" if v else None))
    if couleur == "jaune":
        return "jaune" if j else None
    if couleur == "orange":
        return "orange" if v else None
    return None


def _set_classes(attrs, add):
    """Retire hl-* / data-hl / title posé par ce script, puis ajoute `add`."""
    attrs = re.sub(r'\s+data-hl-title="[^"]*"', '', attrs)
    attrs = re.sub(r'\s+data-hl="1"\s+title="[^"]*"', '', attrs)
    m = re.search(r'\sclass="([^"]*)"', attrs)
    classes = m.group(1).split() if m else []
    classes = [c for c in classes if c not in HL_CLASSES]
    if add:
        classes.append(add)
    new_cls = f' class="{" ".join(classes)}"' if classes else ""
    if m:
        attrs = attrs[:m.start()] + new_cls + attrs[m.end():]
    else:
        attrs = new_cls + attrs
    return attrs


def _apply_section(section, liens, cfg_subject, sid=None):
    section = LEGEND_RE.sub("", section)
    used = set()

    def tr_sub(m):
        attrs, body = m.group("attrs"), m.group("body")
        hrefs = [html.unescape(h) for h in re.findall(r'href="([^"]+)"', body)]
        hit = next((liens[h] for h in hrefs if h in liens), None) if 'section-row' not in attrs else None
        coul = _couleur_active(hit["couleur"], cfg_subject) if hit else None
        attrs = _set_classes(attrs, f'hl-{coul}' if coul else None)
        if coul:
            used.update(("jaune", "orange") if coul == "jo" else (coul,))
            note = hit.get("note")
            if note:
                attrs += f' data-hl="1" title="{html.escape(note, quote=True)}"'
        return f'<tr{attrs}>{body}</tr>'

    section = TR_RE.sub(tr_sub, section)

    def chip_sub(m):
        cls = [c for c in m.group("cls").split() if c not in HL_CLASSES]
        rest = m.group("rest")
        rest = re.sub(r'\s+data-hl="1"\s+title="[^"]*"', '', rest)
        href = re.search(r'href="([^"]+)"', rest)
        hit = None  # puces (Bibmath, sites…) jamais surlignées : seulement les lignes exercices/TD/DS/interros
        if hit:
            cls.append(f'hl-{hit["couleur"]}')
            used.add(hit["couleur"])
            if hit.get("note"):
                rest += f' data-hl="1" title="{html.escape(hit["note"], quote=True)}"'
        return f'<a class="{" ".join(cls)}"{rest}>'

    section = CHIP_RE.sub(chip_sub, section)

    # Puces Bibmath (clé "bibmath" de surlignage.json, Maths) : affichées dans la
    # légende de la section Exercices, colorées comme les exercices (couleur
    # jaune = cours en cours, orange = colle en cours, jo = les deux).
    bibmath = []
    if sid == "exercices":
        for b in cfg_subject.get("bibmath") or []:
            coul = _couleur_active(b.get("couleur", "jaune"), cfg_subject)
            if coul:
                bibmath.append((b, coul))
                used.update(("jaune", "orange") if coul == "jo" else (coul,))
    if used:
        parts = []
        for couleur in ("jaune", "orange"):
            if couleur in used and cfg_subject.get(couleur):
                qui = "cours en cours" if couleur == "jaune" else "colle en cours"
                parts.append(f'<span><span class="hl-swatch {couleur}"></span>{html.escape(qui)} : '
                             f'<b>{html.escape(cfg_subject[couleur]["libelle"])}</b></span>')
        if "jaune" in used and "orange" in used:
            parts.append('<span><span class="hl-swatch jo"></span>les deux</span>')
        parts.extend(f'<a class="legend-chip hl-{c}" href="{html.escape(b["url"], quote=True)}" target="_blank" rel="noopener">'
                     f'🔗 {html.escape(b["libelle"])} <span class="arrow">↗</span></a>' for b, c in bibmath)
        legend = f'<div class="hl-legend">{"".join(parts)}</div>'
        section = re.sub(r'(<h2 class="section-title">.*?</h2>\s*)', lambda m: m.group(1) + legend, section, count=1, flags=re.S)
    return section


def _apply_cours(section, cours, autres=None):
    """Surligne, dans la section Cours, la ligne du cours en cours (jaune) et,
    en Physique, le chapitre du polycopié de la colle en cours (orange ;
    ou jaune si même chapitre que Clarisse ; Physique : chapitre de khôlle)."""
    targets = {os.path.splitext(f)[0]: (c, note) for f, c, note in cours}
    # Cours d'autres lycées en rapport avec le chapitre en cours (choisis par
    # Claude après lecture, clé "cours" de surlignage.json) : match sur l'URL.
    autres = {u["url"]: (u["couleur"], u.get("note", "")) for u in (autres or [])}

    def tr_sub(m):
        attrs, body = m.group("attrs"), m.group("body")
        hit = None
        if 'section-row' not in attrs:
            for h in re.findall(r'href="([^"]+)"', body):
                h = html.unescape(h)
                base = os.path.splitext(h.rsplit("/", 1)[-1])[0]
                if base in targets:
                    hit = targets[base]
                    break
                if h in autres:
                    hit = autres[h]
                    break
        attrs = _set_classes(attrs, f"hl-{hit[0]}" if hit else None)
        if hit:
            attrs += f' data-hl="1" title="{html.escape(hit[1], quote=True)}"'
        return f'<tr{attrs}>{body}</tr>'

    return TR_RE.sub(tr_sub, section)


def apply(repo_root, today=None):
    today = today or datetime.date.today().isoformat()
    cfg = load_config(repo_root)
    exp = expected(repo_root, today, cfg)
    for _folder, label in SUBJECTS:
        path = os.path.join(repo_root, f"{label}.html")
        if not os.path.isfile(path):
            continue
        data = open(path, encoding="utf-8").read()
        c = cfg.get(label, {})
        liens = {l["url"]: l for l in c.get("liens", []) if _couleur_active(l["couleur"], c)}
        data = re.sub(r'<section id="cours">.*?</section>',
                      lambda m: _apply_cours(m.group(0), exp[label]["cours"], cfg.get(label, {}).get("cours")), data, count=1, flags=re.S)
        for sid in ("exercices", "ds"):
            data = re.sub(rf'<section id="{sid}">.*?</section>',
                          lambda m, sid=sid: _apply_section(m.group(0), liens, c, sid), data, count=1, flags=re.S)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(data)
        n = len(re.findall(r'class="[^"]*\bhl-(?:jaune|orange|jo)\b', data))
        print(f"Surlignage appliqué à {label}.html : {n} élément(s)")


def report(exp, issues):
    for label, e in exp.items():
        j = e["jaune"]["libelle"] if e["jaune"] else "—"
        v = e["orange"]["libelle"] if e["orange"] else "—"
        print(f"  {label:9s} jaune  : {j}\n  {'':9s} orange : {v}")
    if issues:
        print("⚠️ SURLIGNAGE À REVOIR — relire le(s) nouveau(x) cours et les documents Exercices/DS,")
        print("   puis mettre à jour Prepa_barthou/surlignage.json (cle + libelle + liens) :")
        for i in issues:
            print("   - " + i)
    else:
        print("✅ surlignage.json est à jour avec le cours en cours et la colle en cours.")


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
        apply(repo_root, today)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
