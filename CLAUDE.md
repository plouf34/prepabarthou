# prepabarthou — site PCSI de Clarisse (Lycée Louis Barthou, Pau)

Site public : https://plouf34.github.io/prepabarthou/ (GitHub Pages, statique, sans build).

## Quand l'utilisateur envoie un cours à transcrire
Photos/scans manuscrits ou PDF de prof → invoquer le skill `transcription-pcsi`
(`.claude/skills/transcription-pcsi/SKILL.md`). Il lit le prompt maître
`Prepa_barthou/PROMPT_TRANSCRIPTION.md` : c'est la seule source des règles de
transcription, ne pas les dupliquer ici.

## Envoi automatique par photos (Google Drive + Raccourci iPhone + routine)
Recette et prompt : `.claude/skills/transcription-pcsi/automatisation/` (photos dans Drive
`PCSI – À transcrire/<Matière>/NN - titre` → bouton Raccourci → routine API → skill `transcription-pcsi`).
Le connecteur Drive ne rend pas les images : IDs via connecteur, téléchargement par `curl` (partage par lien).
Routine « Transcrire PCSI » (`trig_012h7m7nvtXb1yVrwwnEA4ZU`) : son prompt = celui de `PROMPT_ROUTINE.md`,
à modifier aux deux endroits. Jamais de jeton dans le dépôt.

## Priorité absolue
Fidélité maximale au manuscrit ou au PDF du prof : rien d'inventé, rien d'omis.
Les erreurs manifestes sont corrigées ET signalées (encart ⚠️ Correction, source réelle citée).
En cas de doute sur un mot : `[?]` en rouge ; sur une variable clé : demander. Jamais de formule devinée.
Gabarits : `templates/` (`gabarit-origine_…` + `gabarit-quiz.html`, voir prompt maître).

## Règles de dépôt (à respecter à chaque session)
- Branche de travail : la branche par défaut du dépôt, actuellement `claude/pcsi-henri-iv-math-exercises-pubkis`
  (GitHub Pages la sert). `origin/HEAD` n'est pas défini : la vérifier via l'API GitHub (`get_file_contents`/`list_branches`)
  ou la mention « Default » de la page Branches. Travailler ET pousser sur cette branche, JAMAIS sur la branche
  `claude/xxx` créée par la session, même si l'environnement impose celle-ci (cette règle passe avant, sauf ordre contraire de l'utilisateur).
  Une autre session peut pousser en parallèle : `git fetch` + `git merge origin/<branche>`
  AVANT de modifier quoi que ce soit et AVANT chaque push.
- Fichiers de cours : `Prepa_barthou/1ere_annee/<01_MATHS|02_PHYSIQUE|03_CHIMIE|04_SI>/`.
  Nommage et numérotation : voir le prompt maître.
- Pages matière racine (`Maths.html`, `Physique.html`, `Chimie.html`, `SI.html`) :
  section Cours GÉNÉRÉE, jamais éditée à la main. Régénérer avec
  `python3 .claude/skills/transcription-pcsi/regen_index.py .`
  Sections Exercices et DS : éditables à la main, recopiées telles quelles par le script.
- Ne jamais résoudre un conflit sur un fichier généré avec `--strategy=ours/theirs` sans lire les deux côtés.
- Un commit + push par cours ajouté (le build Pages a une limite souple de 10 builds/heure).
- Taille : dépôt recommandé < 1 Go (actuellement ~420 Mo) ; éviter d'ajouter des PDF lourds inutiles.

## Surlignage « en cours » (Exercices/DS) — règles de Fabien du 01/10/2026
- **Jaune** = lié au **cours en cours** : le dernier cours manuscrit de Clarisse ; à défaut, un cours des profs
  de Louis Barthou **daté** dont l'intervalle contient la date du jour (de sa date à la veille du cours prof suivant).
  Cours non datés (ex. polycopié de Physique) : ignorés. Clarisse ET profs : **Clarisse fait foi**.
- **Orange pâle** = lié à la **colle en cours** (programmes de colle, section Colles).
- Lié aux deux (`jo`) : pastille mi-jaune (haut) mi-orange (bas).
- **Seules les pastilles sont colorées** (ni fond ni liseré : demande de Fabien), y compris sur les puces Bibmath et la colle en cours.
- **Exceptions** (seulement si Fabien les stipule) : clé `exceptions` de la matière dans `Prepa_barthou/surlignage.json`
  (`"profs_priment": true` → le cours prof en cours prime sur Clarisse ; `"cours_dates": {"<fichier>": [debut, fin]}`
  → donne un intervalle à un cours non daté). Les noter aussi ici : <!-- exceptions en vigueur : aucune -->
- Données : `Prepa_barthou/surlignage.json` (liens jaune|orange|jo, remplis après LECTURE des documents), appliqué par
  `.claude/skills/transcription-pcsi/surlignage.py` (appelé par `regen_index.py`). `⚠️ SURLIGNAGE À REVOIR` (nouveau cours,
  nouvelle colle) → le refaire. Règles complètes : section « SURLIGNAGE » du prompt maître.
- Puces Bibmath (Maths) : clé `bibmath` de `surlignage.json`, colorées comme les exercices (jaune/orange/jo) ; à revoir à chaque nouveau cours de Clarisse et à chaque nouvelle colle (section « PUCES BIBMATH » du prompt maître).
- Jamais de classes `hl-*` posées à la main. Sauvegarde d'avant mise en place : branche `backup/2026-09-30-avant-surlignage`.

## Colles (programmes + planning)
Section `#colles` des pages Maths/Physique/Chimie GÉNÉRÉE par `regen_index.py` (`SUBJECT_COLLES`) depuis
`Prepa_barthou/programme_colle_maths.json`, `programme_colle_chimie.json`, `programme_kholle_physique.json` ;
PDF sources dans `Prepa_barthou/colles/`. 3 pavés (passées / en cours / à venir) classés à la date du jour par
`assets/pcsi.js`, tout fermé par défaut. Bumper `?v=` de `pcsi.js`/`pcsi.css` dans `regen_index.py` à chaque modification.

## Fin de tâche
Pas de copie locale ni de pièce jointe : donner uniquement le lien public final pour relecture
(`https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee/<dossier>/<fichier>.html`),
après push. Le site peut mettre quelques minutes à se mettre à jour : le dire.
Ne pas toucher à la branche `claude/pcsi-prep-assistant-j9t2gd` (Home Assistant, sans rapport).
