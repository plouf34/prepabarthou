# Raccourci iPhone « Transcrire PCSI » — bouton « Go »

Clarisse dépose d'abord ses photos dans Google Drive
(`PCSI – À transcrire / <Matière> / Chapitre NN - <titre>`), puis touche ce bouton.
Il ne manipule aucun fichier : il appelle seulement la routine (prompt : `PROMPT_ROUTINE.md`).

**Aucun secret dans ce fichier** (dépôt public). Le jeton de la routine se colle dans le Raccourci.

## Prérequis (une fois)
1. Dossier Drive `PCSI – À transcrire` partagé « Tous les utilisateurs disposant du lien — Lecteur ».
2. Réglages iPhone → Appareil photo → Formats → **Le plus compatible** (JPEG). (L'import par l'app
   Drive a converti en JPEG lors du test, mais ce réglage évite de dépendre de ce comportement.)
3. Routine créée sur claude.ai/code/routines, déclencheur **API** ajouté : copier l'URL
   `…/routines/trig_…/fire` et le jeton (**Generate token**, affiché une seule fois).

## Actions du Raccourci (app Raccourcis → +)
Nom : « Transcrire PCSI ». Icône au choix, puis **Ajouter à l'écran d'accueil**.

1. **Choisir dans le menu** — invite « Matière ? » — options `Maths`, `Physique`, `Chimie`, `SI`.
   Dans chaque branche : **Texte** (le nom exact) → après le menu, **Définir la variable** `matiere`
   avec *Résultat du menu*.
2. **Demander une entrée** — type **Nombre** — invite « Numéro du chapitre ? » → variable `chapitre`.
3. **Demander confirmation** — « Lancer la transcription de [matiere], chapitre [chapitre] ?
   Toutes les photos sont bien dans Drive ? » (annuler = rien n'est envoyé). C'est le « Go ».
4. **Obtenir le contenu de l'URL**
   - URL : l'URL de la routine (`https://api.anthropic.com/v1/claude_code/routines/trig_…/fire`)
   - Méthode : **POST**
   - En-têtes :
     - `Authorization` = `Bearer <JETON_ROUTINE>`
     - `anthropic-beta` = `experimental-cc-routine-2026-04-01`
     - `anthropic-version` = `2023-06-01`
     - `Content-Type` = `application/json`
   - Corps : **JSON** → clé `text` (Texte) = `matiere=[matiere]; chapitre=[chapitre]`
5. **Obtenir la valeur du dictionnaire** `claude_code_session_url` depuis *Contenu de l'URL*.
6. **Si** la valeur *a une valeur* → **Afficher la notification** « C'est parti ✅ »
   ; **Sinon** → **Afficher le résultat** *Contenu de l'URL* (montre l'erreur).

## Test (une fois, puis retirer)
Pour publier un essai sous un autre numéro, ajouter temporairement `; publier_comme=04` à la fin
du texte de l'action 4.

## Pièges connus
- Ne pas partager le Raccourci par lien iCloud : il contient le jeton. Le construire sur l'iPhone
  de Clarisse, ou l'envoyer en privé (AirDrop).
- Jeton compromis : routine → API → **Regenerate**, puis remplacer dans l'action 4.
- L'endpoint `/fire` est en bêta : s'il change, seule l'action 4 est à mettre à jour.
