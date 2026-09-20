---
name: transcription-pcsi
description: Transforme les photos/PDF de cours manuscrits PCSI de Clarisse (Maths, Physique, Chimie, SI - Lycée Louis Barthou) en pages HTML de référence autonomes, vérifiées scientifiquement, avec quiz final, puis les commit/push sur github.com/plouf34/prepabarthou. Utiliser dès que l'utilisateur envoie des photos de cours manuscrits ou un PDF de prof à transcrire, ou invoque /transcription-pcsi.
---

# Transcription des cours PCSI de Clarisse

Charge et applique intégralement le prompt maître stocké dans
`Prepa_barthou/PROMPT_TRANSCRIPTION.md` à la racine de ce dépôt — lis ce
fichier en premier avec l'outil Read avant de commencer toute transcription.

Ce fichier définit : le rôle, les règles de fidélité aux notations du prof,
la vérification scientifique des formules et des schémas (SVG, relecture en
plusieurs passes), le rendu LaTeX/MathJax, la gestion des passages
illisibles, le quiz obligatoire de 10 questions en fin de chapitre, le
gabarit HTML (`ch01-bases-optique-geometrique.html`), la convention de
nommage des fichiers, et le workflow de publication.

## Rappel du workflow de publication (à la fin de chaque transcription)

1. Nommer le fichier `NN-Date_Matière_Type_NomDuLienSourceSansAccents.html`
   (NN = prochain numéro disponible dans le sous-dossier concerné).
   Si le cours transcrit est une prise de notes manuscrite de Clarisse
   (pas un document du professeur), inclure le mot `Clarisse` dans le nom
   de fichier (ex. `..._Cours_Clarisse_...`) — l'index le classe
   automatiquement dans « 1. Cours Clarisse » ; tout fichier sans ce mot est
   classé dans « 2. Cours Profs » (documents récupérés sur le site du prof
   ou de Louis Barthou).
2. Le placer dans `Prepa_barthou/1ere_annee/<01_MATHS|02_PHYSIQUE|03_CHIMIE|04_SI>/`
   du dépôt `plouf34/prepabarthou`, branche `claude/pcsi-henri-iv-math-exercises-pubkis`.
3. **Avant toute chose** : `git fetch` + `git merge origin/<branche>` (ou
   `pull`) pour être certain de partir d'un checkout à jour — une autre
   session travaille en parallèle sur ce dépôt et pousse régulièrement sur
   cette branche. Régénérer ou committer une page matière depuis un checkout
   périmé écrase silencieusement les correctifs poussés entre-temps par
   l'autre session (c'est arrivé plusieurs fois : libellés de boutons,
   favicons, liens repoussés en arrière). Ne JAMAIS committer un
   `git merge` avec `--strategy=ours`/`theirs` sur un fichier généré sans
   avoir lu le contenu des deux côtés.
4. Le site est organisé par matière, à la racine du dépôt : `Maths.html`,
   `Physique.html`, `Chimie.html`, `SI.html`. Chacune est une SEULE page qui
   défile de haut en bas à travers 3 sections dans l'ordre `<section
   id="cours">` / `<section id="exercices">` / `<section id="ds">` ; la barre
   d'onglets sticky en haut (Cours/Exercices/DS) ne fait que sauter à l'ancre
   correspondante dans la même page (pas de changement de fichier). Seule la
   section Cours est **entièrement générée** — ne jamais l'éditer à la main
   (ni par un patch direct, ni en copiant un ancien contenu). Toute
   modification de son contenu (libellés, sources, manuels, liens
   complémentaires) doit passer par `.claude/skills/transcription-pcsi/regen_index.py` :
   éditer les constantes `SUBJECT_SOURCES` / `SUBJECT_MANUALS` /
   `SUBJECT_EXTRA_LINKS` / `SUBJECT_EXTERNAL_PROFS` ou les fonctions de rendu
   en tête de fichier, puis relancer
   `python3 .claude/skills/transcription-pcsi/regen_index.py <repo_root>`.
   Le script scanne le contenu réel des 4 sous-dossiers et répartit chaque
   matière en 2 sous-parties « Cours Clarisse » / « Cours Profs » — ne pas
   se fier à une liste mémorisée, d'autres sessions peuvent avoir ajouté ou
   supprimé des fichiers entre-temps. Le script relit le fichier existant et
   RECOPIE TELLES QUELLES les sections Exercices et DS avant de réécrire :
   il ne les régénère jamais, donc les éditer directement dans
   `<Matière>.html` est sûr, mais toujours après un `git fetch`+`merge`. Le
   gabarit commun (en-tête, barre d'onglets, sélecteur de matière) vit dans
   `page_shell()`/`tab_bar_html()`/`subject_switch_html()`/`section_title_html()`
   du même script — à réutiliser si le gabarit doit changer sur les 4 pages à
   la fois. Le CSS partagé est dans `assets/pcsi.css`, le script de
   surbrillance de l'onglet visible au défilement dans `assets/pcsi.js`.
5. Commit puis push sur la branche ci-dessus (avec un `git fetch`+`merge`
   juste avant le push, pour la même raison qu'à l'étape 3).
6. Fournir une copie du fichier à l'utilisateur (pièce jointe/téléchargement)
   pour récupération locale.

Avant de committer : vérifier que les balises HTML/SVG sont équilibrées,
que le nombre de `$$` est pair, et que le quiz contient bien 10 questions.
