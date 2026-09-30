#!/usr/bin/env python3
"""Génère le Raccourci « Transcrire PCSI » (non signé, sans secret).

Usage : python3 genere_raccourci.py <sortie.shortcut>
Puis sur macOS : shortcuts sign -m anyone -i <sortie.shortcut> -o Transcrire_PCSI.shortcut
L'URL et le jeton de la routine sont demandés à l'import (questions d'import).
"""
import plistlib, sys, uuid

OBJ = "￼"

def U():
    return str(uuid.uuid4()).upper()

def var(name):
    return {"Type": "Variable", "VariableName": name}

def out(uid, name):
    return {"Type": "ActionOutput", "OutputUUID": uid, "OutputName": name}

def tok(*parts):
    """Chaîne avec variables : parts = str ou dict d'attachement."""
    s, att = "", {}
    for p in parts:
        if isinstance(p, str):
            s += p
        else:
            pos = len(s.encode("utf-16-le")) // 2
            att["{%d, 1}" % pos] = p
            s += OBJ
    return {"Value": {"string": s, "attachmentsByRange": att},
            "WFSerializationType": "WFTextTokenString"}

def attach(a):
    return {"Value": a, "WFSerializationType": "WFTextTokenAttachment"}

def dico(pairs):
    items = [{"WFItemType": 0, "WFKey": tok(k), "WFValue": v if isinstance(v, dict) else tok(v)}
             for k, v in pairs]
    return {"Value": {"WFDictionaryFieldValueItems": items},
            "WFSerializationType": "WFDictionaryFieldValue"}

def act(ident, **p):
    return {"WFWorkflowActionIdentifier": "is.workflow.actions." + ident,
            "WFWorkflowActionParameters": p}

actions = []
# 0-3 : URL et jeton (remplis par les questions d'import)
t_url, t_tok = U(), U()
actions += [
    act("gettext", UUID=t_url, WFTextActionText=""),
    act("setvariable", WFVariableName="url", WFInput=attach(out(t_url, "Texte"))),
    act("gettext", UUID=t_tok, WFTextActionText=""),
    act("setvariable", WFVariableName="jeton", WFInput=attach(out(t_tok, "Texte"))),
]
# Menu matière
g = U()
matieres = ["Maths", "Physique", "Chimie", "SI"]
actions.append(act("choosefrommenu", GroupingIdentifier=g, WFControlFlowMode=0,
                   WFMenuPrompt="Matière ?", WFMenuItems=matieres))
for m in matieres:
    t = U()
    actions += [
        act("choosefrommenu", GroupingIdentifier=g, WFControlFlowMode=1, WFMenuItemTitle=m),
        act("gettext", UUID=t, WFTextActionText=m),
        act("setvariable", WFVariableName="matiere", WFInput=attach(out(t, "Texte"))),
    ]
actions.append(act("choosefrommenu", GroupingIdentifier=g, WFControlFlowMode=2))
# Chapitre
a = U()
actions += [
    act("ask", UUID=a, WFAskActionPrompt="Numéro du chapitre ?", WFInputType="Number"),
    act("setvariable", WFVariableName="chapitre", WFInput=attach(out(a, "Entrée fournie"))),
]
# Go
actions.append(act("alert", WFAlertActionTitle="Transcrire PCSI",
                   WFAlertActionMessage=tok("Lancer la transcription de ", var("matiere"),
                                            ", chapitre ", var("chapitre"),
                                            " ? Toutes les photos sont bien dans Drive ?"),
                   WFAlertActionCancelButtonShown=True))
# Appel de la routine
d, k = U(), U()
actions.append(act("downloadurl", UUID=d, WFURL=tok(var("url")), WFHTTPMethod="POST",
                   ShowHeaders=True,
                   WFHTTPHeaders=dico([
                       ("Authorization", tok("Bearer ", var("jeton"))),
                       ("anthropic-beta", "experimental-cc-routine-2026-04-01"),
                       ("anthropic-version", "2023-06-01"),
                       ("Content-Type", "application/json"),
                   ]),
                   WFHTTPBodyType="JSON",
                   WFJSONValues=dico([
                       ("text", tok("matiere=", var("matiere"), "; chapitre=", var("chapitre"))),
                   ])))
actions.append(act("getvalueforkey", UUID=k, WFGetDictionaryValueType="Value",
                   WFDictionaryKey="claude_code_session_url",
                   WFInput=attach(out(d, "Contenu de l'URL"))))
# Résultat
c = U()
actions += [
    act("conditional", GroupingIdentifier=c, WFControlFlowMode=0, WFCondition=100,
        WFInput={"Type": "Variable", "Variable": attach(out(k, "Valeur du dictionnaire"))}),
    act("notification", WFNotificationActionTitle="Transcrire PCSI",
        WFNotificationActionBody="C'est parti ✅ Transcription lancée."),
    act("conditional", GroupingIdentifier=c, WFControlFlowMode=1),
    act("showresult", Text=tok(out(d, "Contenu de l'URL"))),
    act("conditional", GroupingIdentifier=c, WFControlFlowMode=2),
]

wf = {
    "WFWorkflowActions": actions,
    "WFWorkflowClientVersion": "2607.0.2",
    "WFWorkflowMinimumClientVersion": 900,
    "WFWorkflowMinimumClientVersionString": "900",
    "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4282601983, "WFWorkflowIconGlyphNumber": 59511},
    "WFWorkflowImportQuestions": [
        {"ActionIndex": 0, "Category": "Parameter", "ParameterKey": "WFTextActionText",
         "DefaultValue": "", "Text": "URL de la routine (…/routines/trig_…/fire)"},
        {"ActionIndex": 2, "Category": "Parameter", "ParameterKey": "WFTextActionText",
         "DefaultValue": "", "Text": "Jeton de la routine (sk-ant-oat01-…)"},
    ],
    "WFWorkflowInputContentItemClasses": [],
    "WFWorkflowOutputContentItemClasses": [],
    "WFWorkflowTypes": [],
    "WFWorkflowHasOutputFallback": False,
    "WFWorkflowHasShortcutInputVariables": False,
    "WFQuickActionSurfaces": [],
}
with open(sys.argv[1], "wb") as f:
    plistlib.dump(wf, f, fmt=plistlib.FMT_BINARY)
print("OK", len(actions), "actions")
