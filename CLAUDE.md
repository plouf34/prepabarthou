# prepabarthou — site PCSI de Clarisse (Lycée Louis Barthou, Pau)

Site public : https://plouf34.github.io/prepabarthou/ (GitHub Pages, statique, sans build).

## Quand l'utilisateur envoie un cours à transcrire
Photos/scans manuscrits ou PDF de prof → invoquer le skill `transcription-pcsi`
(`.claude/skills/transcription-pcsi/SKILL.md`). Il lit le prompt maître
`Prepa_barthou/PROMPT_TRANSCRIPTION.md` : c'est la seule source des règles de
transcription, ne pas les dupliquer ici.

## Priorité absolue
Fidélité maximale au manuscrit ou au PDF du prof : rien d'inventé, rien d'omis.
Les erreurs manifestes sont corrigées ET signalées (encart ⚠️ Correction, source réelle citée).
En cas de doute sur un mot : `[?]` en rouge ; sur une variable clé : demander. Jamais de formule devinée.
Gabarits : `templates/` + chapitre Chimie du 29/09 pour le quiz (voir prompt maître).

## Règles de dépôt (à respecter à chaque session)
- Branche de travail : la branche par défaut du dépôt (`git symbolic-ref refs/remotes/origin/HEAD`).
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

## Fin de tâche
Pas de copie locale ni de pièce jointe : donner uniquement le lien public final pour relecture
(`https://plouf34.github.io/prepabarthou/Prepa_barthou/1ere_annee/<dossier>/<fichier>.html`),
après push. Le site peut mettre quelques minutes à se mettre à jour : le dire.
Ne pas toucher à la branche `claude/pcsi-prep-assistant-j9t2gd` (Home Assistant, sans rapport).
