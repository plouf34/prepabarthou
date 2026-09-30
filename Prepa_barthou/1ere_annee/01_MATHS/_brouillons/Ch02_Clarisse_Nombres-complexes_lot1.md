# Brouillon — Ch02 Nombres complexes (Clarisse) — lot 1/2 (photos 1 à 5)

> Transcription fidèle de travail, **non publiée** (le script d'index ignore ce dossier).
> Sert de base au HTML final, généré après réception du lot 2.
> Conventions : `⚠️ CORR` = correction à signaler par un encart ⚠️ Correction dans le HTML ;
> `[?]` = mot illisible ; `NOTE` = remarque de mise en forme / notation.

## Ordre des pages reçues

| Photo | Contenu | Place supposée |
|---|---|---|
| 1 | Chapitre 2, situation, définition, addition/multiplication, égalité, propriétés de l'addition | début du chapitre (I) |
| 2 gauche | Propriétés de la multiplication, inverse, Re/Im, notation ℂ | suite du I |
| 2 droite | II ① Racines carrées : proposition, démonstration (début) | II ① |
| 3 gauche | Fin de la démonstration (cas B ≠ 0), remarque équation bicarrée | II ① |
| 3 droite | « Chapitre 2 : nombres complexes ② », suite II, ② équation de degré 2 | II ② |
| 4 gauche | Théorème du discriminant, remarque cas réel, exemples ① ② ③ | II ② |
| 4 droite | Fin exemple ③, III Deux applications (récurrences, EDL2) | II ② puis III |
| 5 | Module (propriétés ② ③), conjugué, forme exponentielle | **plus loin** (IV ?) : le début (définition du module, propriété ①) manque → attendu dans le lot 2 |

---

## Chapitre 2 : Nombres complexes

*(En marge, en haut à gauche : « II. » — numéro de chapitre.)*

**Situation :** Pour une équat° de degré 2 à coef. réels :
$$ax^2+bx+c=0 \quad \text{avec } a\neq 0.$$

**Procédé :** on invente une solut° $\sqrt{-1}=i$ à l'éq. $x^2+1=0$.

> NOTE (notation non standard, à conserver + note de bas de section) : l'écriture $\sqrt{-1}$ est à
> éviter en PCSI ; on définit $i$ par $i^2=-1$ (la racine carrée $\sqrt{\ }$ n'est définie que sur $\mathbb{R}_+$).

**Déf :** On appelle nb. complexes des expressions de la forme $a+bi$ avec $a$ et $b$ réels, soumises aux règles de calcul :

① addition :
$$(a_1+b_1 i)+(a_2+b_2 i)=a_1+a_2+(b_1+b_2)\times i$$
*(manuscrit : « $(b_i+b_2)$ » → $b_1$ : faute d'indice, corrigée sans encart.)*

② multiplicat° :
$$(a_1+b_1 i)\times(a_2+b_2 i)=a_1a_2-b_1b_2+(a_1b_2+b_1a_2)\times i$$

**Égalité :** pour $a_1,a_2,b_1,b_2$ réels,
$$a_1+b_1 i=a_2+b_2 i \iff \begin{cases}a_1=a_2\\ b_1=b_2\end{cases}$$

**Propriété :**
① L'addit° :
- est associative : $(z_1+z_2)+z_3=z_1+(z_2+z_3)$ ;
- est commutative : $z_1+z_2=z_2+z_1$ ;
- admet un élément neutre : le nb $0_{\mathbb{C}}=0_{\mathbb{R}}+0_{\mathbb{R}}\,i$ vérifie $z+0_{\mathbb{C}}=z\ \ \forall z$ ;
- est tq chaque nb complexe admet un opposé : si $z=a+bi$ avec $a,b$ réels alors
  $z+\underbrace{(-a+(-b)\times i)}_{\text{notée } -z}=0_{\mathbb{C}}$.

On définit alors $z_1-z_2=z_1+(-z_2)$.

② La multiplicat° :
- est associative ;
- est commutative ;
- admet pour élément neutre le nb $1_{\mathbb{C}}=1_{\mathbb{R}}+0_{\mathbb{R}}\cdot i$ ;
- est tq chaque $z\in\mathbb{C}$ non nul admet un inverse.

**Formule de l'inverse :** si $z=a+bi$ avec $a,b$ réels et $z\neq0$, alors
$$z^{-1}=\frac1z=\frac{a}{a^2+b^2}-\frac{b}{a^2+b^2}\,i$$
Vérification :
$$(a+bi)\times\Big(\frac{a}{a^2+b^2}-\frac{b}{a^2+b^2}i\Big)=\frac{a^2}{a^2+b^2}+\frac{b^2}{a^2+b^2}+\Big(-\frac{ab}{a^2+b^2}+\frac{ba}{a^2+b^2}\Big)i=\frac{a^2+b^2}{a^2+b^2}=1.$$

**Voc :** si $z=a+bi$ avec $a$ et $b$ réels, on dit que $a$ est la partie réelle de $z$, $b$ est la partie imaginaire de $z$ ; on note $\begin{cases}a=\mathrm{Re}(z)\\ b=\mathrm{Im}(z)\end{cases}$

Ainsi, l'équivalence pour $a_1,a_2,b_1,b_2$ réels
$a_1+b_1i=a_2+b_2i\iff\begin{cases}a_1=a_2\\b_1=b_2\end{cases}$
est ce qu'on appelle une identificat° des parties réelles et imaginaires.

**Notat° :** $\mathbb{C}$ : ens. des nb complexes. Inclusion canonique $\mathbb{R}\subset\mathbb{C}$ :
si $x\in\mathbb{R}$ on le voit comme $x=x+$ [?]
*(fin de ligne coupée en bas de la photo 2 ; sens attendu $x+0\cdot i$ — à confirmer, NE PAS compléter sans signaler.)*

---

## II – Résolut° des éq. du 2nd degré

### ① Racines carrées

**Prop :** ∀ nb complexe non nul admet 2 racines carrées opposées l'une à l'autre.

**Dém :** soit $Z=A+Bi$ *(A, B réels : implicite dans le manuscrit)*.
Cherchons les nb $\mathfrak{z}=a+bi$ *(a, b réels, implicite)* tq $\mathfrak{z}^2=Z$, càd $\mathfrak{z}$ est une racine carrée de $Z$.
$$\mathfrak{z}^2=Z \iff (a+bi)^2=A+Bi\iff a^2-b^2+2abi=A+Bi\iff\begin{cases}a^2-b^2=A\\2ab=B\end{cases}\quad(S)$$

> ⚠️ CORR 1 : le manuscrit écrit « $=A+B$ » (deux fois) : il manque le $i$ ($Z=A+Bi$).
> La suite (identification $2ab=B$) montre que c'est bien $A+Bi$.

→ **pour le cas $B=0$** ($\iff Z\in\mathbb{R}$) : la 2ème éq devient $2ab=0$, soit $a=0$ ou $b=0$.
- si $a=0$ : la 1ère éq devient $A=-b^2$, qui impose $A\le0$ et $b=\pm\sqrt{A}$ ;

> ⚠️ CORR 2 : $A=-b^2 \Rightarrow b^2=-A \Rightarrow b=\pm\sqrt{-A}$ (et non $\pm\sqrt{A}$, non défini si $A<0$).
> Le bilan ci-dessous ($\pm i\sqrt{-A}$) est d'ailleurs cohérent avec $\sqrt{-A}$.

- si $b=0$ : la 1ère éq devient $A=a^2$, qui impose $A\ge0$ et $a=\pm\sqrt{A}$.

**Bilan du cas $B=0$** → un nb réel $Z=A$ admet 2 racines carrées complexes opposées :
$$\begin{cases}\pm\sqrt{A} & \text{si } A\ge0\\ \pm i\sqrt{-A} & \text{si } A\le0\end{cases}$$
*(NOTE : pour $A=0$ les deux lignes donnent 0, une seule racine « double » — cohérent avec « non nul » dans la prop.)*

→ **pour le cas $B\neq0$** : la 2ème éq devient $2ab=B\neq0$, impose $a\neq0$ et $b\neq0$. On écrit alors :
$$(S)\iff\begin{cases}a^2-\dfrac{B^2}{4a^2}=A\\[4pt] b=\dfrac{B}{2a}\end{cases}
\iff\begin{cases}4a^4-4Aa^2-B^2=0\\[2pt] b=\dfrac{B}{2a}\end{cases}$$

On pose le changement d'inconnue $\alpha=a^2\ge0$. L'éq devient $4\alpha^2-4A\alpha-B^2=0$, dont on cherche les sol. réelles positives.
Discriminant : $16A^2+16B^2=16(A^2+\underbrace{B^2}_{>0})>0$.
Les sol. sont
$$\frac{4A\pm4\sqrt{A^2+B^2}}{2\times4}=\frac12A\pm\frac12\underbrace{\sqrt{A^2+B^2}}_{\ge|A|}$$

> NOTE (précision à ajouter, pas une erreur) : comme $B\neq0$, $\sqrt{A^2+B^2}>|A|$, donc la racine avec « − » est
> $<0$ et est rejetée ($\alpha=a^2\ge0$) ; seule $\alpha=\tfrac12\big(A+\sqrt{A^2+B^2}\big)>0$ convient, d'où $a=\pm\sqrt{\alpha}$.

**Bilan :** si $B\neq0$, le nombre $Z=A+iB$ admet 2 racines carrées, qui sont
$$\pm\left(\sqrt{\tfrac12\big(A+\sqrt{A^2+B^2}\big)}+i\,\frac{B}{2\sqrt{\tfrac12\big(A+\sqrt{A^2+B^2}\big)}}\right)
=\pm\frac1{\sqrt2}\left(\sqrt{A+\sqrt{A^2+B^2}}+\frac{iB}{\sqrt{A+\sqrt{A^2+B^2}}}\right)$$
*(manuscrit : « $\sqrt{A^2+6^2}$ » au dénominateur → $B^2$, faute de plume corrigée sans encart. Formule vérifiée : $2\sqrt{X/2}=\sqrt2\sqrt X$.)*

**Rq :** une éq de forme $ax^4+bx^2+c=0$ où $a,b,c$ sont des nb réels (ou complexes) est appelée une éq **biquadratique** (ou **bicarrée**).
Technique : poser le changement d'inconnue $X=x^2$, pour se ramener à une éq de degré 2 : $aX^2+bX+c=0$.

---

*(Nouvelle feuille : « II. Chapitre 2 : nombres complexes ② ». En tête de feuille, ajout de Clarisse : « **Lemme** : résultat intermédiaire » — définition du mot « lemme ».)*

### Suite II – ② Éq de degré 2

Soit $a,b,c$ des nombres réels ou complexes avec $a\neq0$. Sont à résoudre l'éq : $aZ^2+bZ+c=0$ où $Z$ est l'inconnue.

Posons $P(Z)=\underbrace{aZ^2+bZ+c}_{\text{polynôme du 2nd degré}}$.

On le met sous forme canonique :
$$P(Z)=a\Big(Z^2+\frac baZ+\frac ca\Big)=a\Big(\Big(Z+\frac b{2a}\Big)^2-\frac{b^2}{4a^2}+\frac ca\Big)=a\Big[\Big(Z+\frac b{2a}\Big)^2+\frac{4ac-b^2}{4a^2}\Big]$$

D'où les équivalences :
$$P(Z)=0\iff a\times\Big[\Big(Z+\frac b{2a}\Big)^2+\frac{4ac-b^2}{4a^2}\Big]=0$$

**Lemme :** $z_1\times z_2=0$ sur $\mathbb{C}$ $\iff z_1=0$ ou $z_2=0$.

D'où
$$P(Z)=0\iff\Big(Z+\frac b{2a}\Big)^2+\frac{4ac-b^2}{4a^2}=0\iff\Big(Z+\frac b{2a}\Big)^2=\frac{b^2-4ac}{4a^2}$$
$$\iff Z+\frac b{2a}=\pm\delta\quad\text{où }\delta^2=\frac{b^2-4ac}{(2a)^2}$$
$$\iff Z=-\frac b{2a}\pm\delta\qquad\Big\|\qquad\frac{-b\pm\sqrt\Delta}{2a}=-\frac b{2a}\pm\frac{\sqrt\Delta}{2a}$$

> ⚠️ CORR 3 : le manuscrit écrit « $Z=-\frac ba\pm\delta$ » : c'est $-\frac{b}{2a}$ (on retranche $\frac b{2a}$ de la ligne précédente).
> ⚠️ CORR 4 (notation, imprécision) : ici $\delta$ désigne une racine carrée de $\frac{\Delta}{4a^2}$, alors que dans le
> théorème qui suit $\delta$ désigne une racine carrée de $\Delta$ (solutions $\frac{-b\pm\delta}{2a}$). Même lettre, deux sens.
> Et $\sqrt\Delta$ n'a de sens que si $\Delta\ge0$ réel ; pour $\Delta$ complexe on écrit $\pm\delta$ avec $\delta^2=\Delta$.

**Théorème :** soit $aZ^2+bZ+c=0$ ↳ une éq de degré 2 avec $a\neq0$. On appelle **discriminant** le nb $\Delta=b^2-4ac$.
Soit $\pm\delta$ les racines carrées de $\Delta$, alors les sol. de (E) sont $\dfrac{-b\pm\delta}{2a}$.

**Rq :** cas $a,b,c$ réels :
- si $\Delta\ge0$ → cours de 1ère ;
- si $\Delta<0$ → alors $\delta$ est un imaginaire pur, càd de la forme … *(ligne laissée inachevée dans le manuscrit)*

> NOTE : complétion usuelle, à présenter comme ajout et non comme texte du cours : $\delta=\pm i\sqrt{-\Delta}$,
> solutions $\frac{-b\pm i\sqrt{-\Delta}}{2a}$ (conjuguées).

**Exemple :**

① $Z^2+Z+1=0$ : le discriminant est $-3$ ; ses racines carrées sont $\pm i\sqrt3$. Donc les sol. de (E) sont $\dfrac{-1\pm i\sqrt3}2$.
*En marge :* « $A+iB$ avec $A=-3<0$, $B=0$ ; $\begin{cases}a^2+b^2=A=-3\\2ab=B=0\end{cases}$ → $b=\pm\sqrt3$, $a=0$ ».
> ⚠️ CORR 5 (marge) : c'est $a^2-b^2=A$ (système (S)), pas $a^2+b^2$ ; avec $a=0$ : $-b^2=-3$, $b=\pm\sqrt3$ ✓.

② $Z^2-Z+1=0$ : le discriminant est $-3$ ; ses racines carrées sont $\pm i\sqrt3$ ; donc les sol. de (E) sont $\dfrac{1\pm i\sqrt3}2$.
*En marge :* $\Delta=(1)^2-4\times1\times1=-3$.
> ⚠️ CORR 6 : le manuscrit écrit « $Z-Z+1=0$ » : le carré manque sur le premier $Z$ ($\Delta=-3$ et les solutions
> $\frac{1\pm i\sqrt3}2$ correspondent à $Z^2-Z+1=0$). Marge : $(-1)^2$ plutôt que $(1)^2$ (même valeur).

③ $Z^2+2Z+i=0$ : le discriminant est $4-4i=4(1-i)$. Ses racines carrées sont $\delta=a+bi$ :
$$\delta^2=4(1-i)\iff a^2-b^2+2abi=4-4i\iff\begin{cases}a^2-b^2=4\\2ab=-4\end{cases}\iff\begin{cases}a^2-\frac4{a^2}=4\\b=-\frac2a\end{cases}\iff\begin{cases}a^4-4a^2-4=0\\b=-\frac2a\end{cases}$$
*En marge :* $\Delta=(2)^2-4\times1\times i=4-4i$ ; « $a^2-b^2=A=4$ » ; « $2ab=B=-4i$ » ; « $a+b=\sqrt4=1$ » ; « $a=-b$ ».
> ⚠️ CORR 7 (marge, brouillon) : $B=-4$ (partie imaginaire, réelle), pas $-4i$. Les lignes « $a+b=\sqrt4=1$ » et « $a=-b$ »
> sont fausses ($\sqrt4=2$, et rien n'impose $a+b=\sqrt4$) ; elles ne sont pas utilisées dans le calcul principal.
> À présenter comme « brouillon en marge » barré/grisé, ou à omettre en le disant.

On pose $\alpha=a^2$, soit $\alpha^2-4\alpha-4=0$ ;
$\Delta=(-4)^2-4\times1\times(-4)=16+16=32$ ;
les sol. sont $\dfrac{4\pm\sqrt{32}}2=\sqrt{2\pm2\sqrt2}$.
> ⚠️ CORR 8 : $\dfrac{4\pm\sqrt{32}}2=\dfrac{4\pm4\sqrt2}2=2\pm2\sqrt2$ : ce sont les valeurs de $\alpha$, pas de $a$.
> Comme $\alpha=a^2\ge0$ et $2-2\sqrt2<0$, seule $\alpha=2+2\sqrt2$ convient, d'où $a=\pm\sqrt{2+2\sqrt2}$ et $b=-\frac2a$.
> Le manuscrit écrit « $=\sqrt{2\pm2\sqrt2}$ », qui mélange $\alpha$ et $a$ ; la suite du calcul est juste.

Donc les racines carrées de $4(1-i)$ sont
$$\pm\left(\sqrt{2+2\sqrt2}-\frac2{\sqrt{2+2\sqrt2}}\,i\right)=\pm\sqrt2\left(\sqrt{1+\sqrt2}-\frac{i}{\sqrt{1+\sqrt2}}\right)$$
Les sol. de (E) sont
$$-1\pm\frac{\sqrt2}2\sqrt{1+\sqrt2}\mp\frac{i\sqrt2}{2\sqrt{1+\sqrt2}}$$
*(vérifié : $\frac{-2\pm\delta}{2}=-1\pm\frac\delta2$.)*

---

## III – Deux applicat°

**Objectif :** résoudre
- les équations de récurrence linéaire d'ordre 2 homogène à coeff constants ;
- les EDL② à coeff constants.

**Théorème :** soit $a,b,c$ des nb. réels ou complexes avec $a\neq0$, on considère :
$$(E)\quad \forall n\in\mathbb{N},\ a\,u_{n+2}+b\,u_{n+1}+c\,u_n=0$$
$$(F)\quad a\,y''+b\,y'+c\,y=0\ \text{ sur }\mathbb{R}$$
Dans un cas comme dans l'autre, on associe l'éq **caractéristique** $aZ^2+bZ+c=0$. Notons $R_1$ et $R_2$ ses 2 sol. dans $\mathbb{C}$.

**Cas $R_1\neq R_2$ :**
- les sol. de (E) sont les suites $(\lambda R_1^{\,n}+\mu R_2^{\,n})_{n\in\mathbb{N}}$ où $(\lambda,\mu)\in\mathbb{R}^2$ ou $\mathbb{C}^2$ ;
- les sol. de (F) sont les f° $t\mapsto\lambda e^{R_1t}+\mu e^{R_2t}$ où $(\lambda,\mu)\in\mathbb{R}^2$ ou $\mathbb{C}^2$.

**Cas $R_1=R_2$** (si le discriminant de l'éq caractéristique est nul) :
- les sol. de (E) sont les suites $\big((\lambda n+\mu)R_1^{\,n}\big)_{n\in\mathbb{N}}$ où $(\lambda,\mu)\in\mathbb{R}^2$ ou $\mathbb{C}^2$ ;
- les sol. de (F) sont les f° $t\mapsto(\lambda t+\mu)e^{R_1t}$ où $(\lambda,\mu)\in\mathbb{R}^2$ ou $\mathbb{C}^2$.

> ⚠️ CORR 9 (imprécision) : « $\mathbb{R}^2$ ou $\mathbb{C}^2$ » est à préciser. Ces formes donnent **toutes les solutions
> complexes** avec $(\lambda,\mu)\in\mathbb{C}^2$. Si $a,b,c$ sont réels et qu'on cherche les solutions **réelles** :
> racines réelles → mêmes formes avec $(\lambda,\mu)\in\mathbb{R}^2$ ; racines complexes conjuguées $r e^{\pm i\theta}$
> (resp. $\alpha\pm i\omega$) → $u_n=r^n(\lambda\cos n\theta+\mu\sin n\theta)$ et $y(t)=e^{\alpha t}(\lambda\cos\omega t+\mu\sin\omega t)$,
> $(\lambda,\mu)\in\mathbb{R}^2$. À vérifier dans le cours prof Ch03 (Problèmes linéaires bidimensionnels) pour citer la source.

---

## (Photo 5 — plus loin dans le chapitre : module, conjugué, forme exponentielle)

*Le début de cette partie (définition du module, propriété ①) n'est pas dans le lot 1.*

② si $z=x+iy$ avec $\begin{cases}x\in\mathbb{R}\\y\in\mathbb{R}\end{cases}$, on sait que :
$$z=0\iff x=0=y\iff\underbrace{x^2}_{\ge0}+\underbrace{y^2}_{\ge0}=0$$
Si une somme de réels positifs est nulle alors ∀ ses termes sont nuls.
$$\iff\sqrt{x^2+y^2}=0\iff|z|=0.$$

**Rq :** 2 contextes d'utilisat° du symbole $\iff$ : ① résolut° d'éq. ; ② dém. d'une équivalence logique.

③ calculons pour $z\in\mathbb{C}$ avec $z\neq0$ :
$$\Big|\frac1z\Big|\times|z|=\Big|\frac1z\times z\Big|=|1|=1\quad\text{donc}\quad\Big|\frac1z\Big|=\frac1{|z|}.$$

**Rq :** $\Big|\dfrac{z_1}{z_2}\Big|=\dfrac{|z_1|}{|z_2|}$ et $\dfrac1z=\dfrac{x-iy}{|z|^2}$ *(« $x-iy$ » entouré en rouge, avec un « ? » de Clarisse)*.
> NOTE : la formule est juste ($\frac1z=\frac{\bar z}{|z|^2}$, cf. formule de l'inverse du I) ; répondre au « ? » dans une remarque.

→ **Déf :** soit $z=x+iy$ un complexe écrit sous forme cartésienne *(mot peu lisible, lu « cartésienne », cf. « forme cart. » plus loin)* ;
on appelle **conjugué** de $z$, noté $\bar z$, le nb $\bar z=x-iy$.

**Prté :**
① pour $z\neq0$ : $\dfrac1z=\dfrac{\bar z}{z^2}$, soit encore $|z|^2=z\times\bar z$.
> ⚠️ CORR 10 : c'est $\dfrac1z=\dfrac{\bar z}{|z|^2}$ (module au carré), comme dans la Rq juste au-dessus et dans
> « soit encore $|z|^2=z\bar z$ ». $\frac{\bar z}{z^2}$ est faux (ex. $z=i$ : $\frac{-i}{-1}=i\neq\frac1i=-i$).

② $\overline{z_1+z_2}=\bar z_1+\bar z_2$ ; $\overline{z_1\times z_2}=\bar z_1\times\bar z_2$ ; $\overline{-z}=-\bar z$ ; $\dfrac1{\bar z}=\overline{\Big(\dfrac1z\Big)}$

③ $|\bar z|=|z|$

④ $\overline{(e^z)}=\ ?$ pour $z=x+iy$ sous forme cart. :
$$\overline{e^z}=\overline{e^{x+iy}}=\overline{e^x\cos(y)+e^x\sin(y)\,i}=e^x\cos(-y)-e^x\sin(-y)\,i=e^{x-iy}=e^{\bar z}$$
> ⚠️ CORR 11 : ligne du milieu lue « $e^x\cos(-y)-e^x\sin(-y)\,i$ » (signe et parenthèse peu nets).
> Correct : $e^x\cos(y)-e^x\sin(y)\,i=e^x\cos(-y)+e^x\sin(-y)\,i$ (parité rappelée juste en dessous). Avec « $-\sin(-y)$ » on retrouverait $e^z$.
> NOTE : la 1ère égalité suppose connue $e^{x+iy}=e^x(\cos y+i\sin y)$ (définition de l'exponentielle complexe, pas dans le lot 1).

Rappel : • cosinus est paire : $\cos(-a)=\cos(a)$ ; • sinus est impaire : $\sin(-a)=-\sin(a)$.

**Prté :** soit $z\in\mathbb{C}$ : $z\in\mathbb{R}\iff\bar z=z$ ; $z\in i\mathbb{R}\iff\bar z=-z$ — *exo pour dém.*

**Théorème :** soit $z\in\mathbb{C}$, alors il existe un couple $(\rho,\theta)$ avec $\begin{cases}\rho\in\mathbb{R}_+^*\\\theta\in\mathbb{R}\\z=\rho e^{i\theta}\end{cases}$ ; de +, $\rho$ est unique et $\rho=|z|$, $\theta$ est déf. modulo $2\pi$.
> ⚠️ CORR 12 : il faut $z\in\mathbb{C}^*$ ($z\neq0$) : pour $z=0$, aucun $\rho>0$ ne convient ($|\rho e^{i\theta}|=\rho>0$).

Càd : si $\rho_1e^{i\theta_1}=z=\rho_2e^{i\theta_2}$ avec $\begin{cases}\rho_1>0,\ \rho_2>0\\\theta_1,\theta_2\text{ réels}\end{cases}$ alors
$\begin{cases}\rho_1=\rho_2\\\theta_1-\theta_2=2k\pi\text{ avec }k\text{ entier}\end{cases}$ (il existe $k\in\mathbb{Z}$ tq $\theta_1-\theta_2=2k\pi$).
*(manuscrit : « $\theta_1-\theta=2k\pi$ » → $\theta_2$, indice oublié, corrigé sans encart.)*

**Déf :** L'écriture $z=\rho e^{i\theta}$ est appelée **écriture exponentielle** d'un complexe et les $\theta$ qui conviennent sont appelés les **arguments** de $z$. On parle d'**argument principal** lorsqu'on impose l'unicité de l'argument, l'intervalle étant fixé.
> NOTE : préciser l'intervalle usuel, $]-\pi,\pi]$ (programme PCSI) — à vérifier dans le cours prof.

**Exemple :**
① $z=1+i$, $|z|=\sqrt2$ → $\dfrac z{|z|}=\dfrac{1+i}{\sqrt2}=\dfrac{\sqrt2}2+i\dfrac{\sqrt2}2=e^{i\frac\pi4}$, soit $1+i=\sqrt2\,e^{i\frac\pi4}$.

*(suite attendue dans le lot 2)*

---

## À traiter au rendu final
- Définition du module et propriété ① du module (manquent) ; définition de $e^{i\theta}$ / $e^{x+iy}$.
- Numérotation Définition 2.x / Théorème 2.x continue sur tout le chapitre.
- Remplacer l'actuel `02_Ch02_Cours_Clarisse_Nombres-complexes_2026-09-27.html` (même nom, même lien public).
- Le fichier non numéroté `chapitre_2_nombres_complexes.html` du dossier (ancien brouillon ?) : demander avant de supprimer.
- Quiz 10 questions (gabarit `templates/gabarit-quiz.html`), sources, surlignage, puce Bibmath (déjà Ch02).
