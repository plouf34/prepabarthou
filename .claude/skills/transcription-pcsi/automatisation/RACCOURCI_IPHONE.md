# Raccourci iPhone « Transcrire PCSI » — recette de construction

But : Clarisse sélectionne ses photos, Partager → « Transcrire PCSI », choisit la matière,
confirme. Le Raccourci dépose les photos dans le dépôt privé `plouf34/prepabarthou-inbox`
puis lance la routine Claude. À construire UNE fois (app « Raccourcis », native).

**Aucun secret dans ce fichier** (dépôt public). Les 2 jetons se collent directement dans le Raccourci.

## Prérequis (une fois, par le propriétaire du dépôt)
1. Créer le dépôt **privé** `prepabarthou-inbox` (avec un README, pour que la branche `main` existe).
2. GitHub → Settings → Developer settings → Fine-grained tokens : jeton limité à ce seul dépôt,
   permission **Contents : Read and write**, expiration 1 an (à renouveler, noter la date).
3. claude.ai/code/routines → la routine « Transcrire PCSI » (prompt : `PROMPT_ROUTINE.md`) →
   Edit → Add another trigger → **API** → copier l'URL `…/routines/trig_…/fire`
   et **Generate token** (affiché une seule fois).
4. Sur l'iPhone de Clarisse : Réglages → Appareil photo → Formats → **Le plus compatible** (JPEG).

## Actions du Raccourci (dans l'ordre)
Réglages du Raccourci : activer **Afficher dans la feuille de partage**, types acceptés : **Images**.
Nom : « Transcrire PCSI ».

1. **Choisir dans le menu** : Maths / Physique / Chimie / SI → dans chaque branche,
   **Définir la variable** `matiere` = le nom exact (`Maths`, `Physique`, `Chimie`, `SI`).
2. **Date actuelle** → **Formater la date** (personnalisé `yyyy-MM-dd_HHmm`) → variable `stamp`.
3. **Texte** `inbox/[stamp]_[matiere]` → variable `dossier`.
4. **Compter** les *Entrée du raccourci* → variable `n`.
5. **Demander confirmation** : « Envoyer [n] photos de [matiere] pour transcription ? »
   (annuler = le Raccourci s'arrête, rien n'est envoyé). C'est le « Go ».
6. **Répéter avec chaque élément** de *Entrée du raccourci* :
   1. **Obtenir les détails de l'image** : *Date de prise de vue* → **Formater la date**
      (`yyyyMMdd-HHmmss`) → variable `t`.
   2. **Redimensionner l'image** : largeur **2000** (hauteur automatique).
   3. **Convertir l'image** en **JPEG**, qualité **Moyenne** (≈ 0,7) — lisible et léger.
   4. **Encoder en Base64** (retours à la ligne : **Désactivé**) → variable `b64`.
   5. **Obtenir le contenu de l'URL** :
      - URL : `https://api.github.com/repos/plouf34/prepabarthou-inbox/contents/[dossier]/[t]_[Index de répétition].jpg`
      - Méthode : **PUT**
      - En-têtes : `Authorization` = `Bearer <JETON_GITHUB>` ; `Accept` = `application/vnd.github+json`
      - Corps de la requête : **JSON** → `message` (texte) = `photo` ; `content` (texte) = `[b64]`
7. **Vérification** (après la boucle) : **Obtenir le contenu de l'URL** en GET sur
   `https://api.github.com/repos/plouf34/prepabarthou-inbox/contents/[dossier]` (mêmes en-têtes)
   → **Compter** les éléments. **Si** ≠ `n` : **Afficher l'alerte** « Envoi incomplet, réessaie »
   et **Arrêter le raccourci**.
8. **Obtenir le contenu de l'URL** :
   - URL : celle de la routine (`https://api.anthropic.com/v1/claude_code/routines/<ID>/fire`)
   - Méthode : **POST**
   - En-têtes : `Authorization` = `Bearer <JETON_ROUTINE>` ; `anthropic-beta` = `experimental-cc-routine-2026-04-01` ;
     `anthropic-version` = `2023-06-01` ; `Content-Type` = `application/json`
   - Corps **JSON** : `text` (texte) = `matiere=[matiere]; dossier=[dossier]`
9. **Afficher la notification** : « Envoyé ✅ — [n] photos de [matiere]. »

## Pièges connus
- Le nom des fichiers commence par la date de prise de vue : c'est ce qui conserve l'ordre du cours.
  Si *Date de prise de vue* est vide au premier essai, remplacer `[t]` par l'index seul et vérifier
  que l'ordre de sélection dans Photos correspond à l'ordre de prise de vue.
- Un `PUT` en double sur un même nom échoue (422) : l'index de répétition dans le nom l'évite.
- **Ne pas partager le Raccourci par lien iCloud public** : il contient les 2 jetons. Le construire
  directement sur l'iPhone de Clarisse, ou l'envoyer en privé.
- Si un jeton fuite : révoquer (GitHub / routine → Regenerate) puis le remplacer dans le Raccourci.
- L'endpoint `/fire` est en bêta (`experimental-cc-routine-2026-04-01`) : s'il change, seul le
  point 8 est à mettre à jour.

## Test de validation (avant usage réel)
Envoyer 2 photos d'un vrai cours, laisser tourner, vérifier : (1) les fichiers apparaissent dans l'inbox,
(2) une session démarre sur claude.ai/code, (3) le cours est publié, (4) le dossier est supprimé de l'inbox.
