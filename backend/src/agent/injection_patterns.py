from __future__ import annotations

from dataclasses import dataclass

import regex


@dataclass(frozen=True)
class InjectionPattern:
    id: str
    description: str
    pattern: regex.Pattern


def _c(pattern: str) -> regex.Pattern:
    return regex.compile(pattern, regex.IGNORECASE)


_GAP = r"[\s\S]{0,40}"

INJECTION_PATTERNS: list[InjectionPattern] = [
    InjectionPattern(
        "EN-OVR-1",
        "Aufforderung, vorherige Anweisungen zu ignorieren/zu vergessen (EN)",
        _c(
            r"\b(ignore|forget|discard|bypass|override|overrule|neglect|skip)\b"
            + _GAP
            + r"\b(all\s+)?(previous|prior|above|earlier|former|initial)\b"
            + _GAP
            + r"\b(instructions?|rules?|prompts?|directives?|messages?|context)\b"
        ),
    ),
    InjectionPattern(
        "EN-OVR-2",
        "Aufforderung, System-/Entwickler-Regeln nicht zu befolgen (EN)",
        _c(
            r"\b(disregard|do\s+not\s+follow|stop\s+following|no\s+longer\s+follow)\b"
            + _GAP
            + r"\b(instructions?|rules?|guidelines?|policies?|constraints?|system\s+message|developer\s+message)\b"
        ),
    ),
    InjectionPattern(
        "EN-OVR-3",
        "Einschleusen neuer/ersetzender Anweisungen (EN)",
        _c(
            r"\b(new|updated|replacement|alternative)\b"
            + _GAP
            + r"\b(instructions?|rules?|system\s+prompt|developer\s+message)\b"
            + _GAP
            + r"\b(start|begin|follow|obey|use)\b"
        ),
    ),

    InjectionPattern(
        "DE-OVR-1",
        "Aufforderung, vorherige Anweisungen zu ignorieren/zu vergessen (DE)",
        _c(
            r"\b(ignoriere|vergiss|verwirf|missachte|umgehe|überschreibe|ueberschreibe|ersetze)\b"
            + _GAP
            + r"\b(alle\s+)?(vorherigen|früheren|frueheren|obigen|bisherigen|alten)\b"
            + _GAP
            + r"\b(anweisungen|regeln|vorgaben|richtlinien|instruktionen|prompts?|kontext)\b"
        ),
    ),
    InjectionPattern(
        "DE-OVR-2",
        "Aufforderung, System-/Entwickler-Regeln nicht zu befolgen (DE)",
        _c(
            r"\b(befolge|folge)\b"
            + r"[\s\S]{0,30}"
            + r"\b(nicht|keine|niemals)\b"
            + _GAP
            + r"\b(anweisungen|regeln|vorgaben|richtlinien|systemnachricht|entwicklernachricht)\b"
        ),
    ),
    InjectionPattern(
        "DE-OVR-3",
        "Einschleusen neuer/ersetzender Anweisungen (DE)",
        _c(
            r"\b(neue|aktualisierte|alternative|ersatz)\b"
            + _GAP
            + r"\b(anweisungen|regeln|vorgaben|systemprompt|entwicklernachricht)\b"
            + _GAP
            + r"\b(beginnen|starte|befolge|verwende|nutze)\b"
        ),
    ),


    InjectionPattern(
        "EN-ROLE-1",
        "Annahme einer uneingeschraenkten Persona (DAN etc.) (EN)",
        _c(
            r"\b(you\s+are\s+now|act\s+as|pretend\s+to\s+be|simulate|roleplay\s+as)\b"
            + _GAP
            + r"\b(DAN|jailbroken|unrestricted|uncensored|unfiltered|developer\s+mode|god\s+mode|root|admin)\b"
        ),
    ),
    InjectionPattern(
        "EN-ROLE-2",
        "Aktivieren eines 'Modus' ohne Einschraenkungen (EN)",
        _c(
            r"\b(enable|activate|enter|switch\s+to)\b"
            + _GAP
            + r"\b(developer\s+mode|jailbreak\s+mode|unrestricted\s+mode|uncensored\s+mode|debug\s+mode|admin\s+mode)\b"
        ),
    ),
    InjectionPattern(
        "EN-ROLE-3",
        "Dauerhafte Aufhebung von Regeln 'from now on' (EN)",
        _c(
            r"\b(from\s+now\s+on|for\s+the\s+rest\s+of\s+this\s+conversation)\b"
            + _GAP
            + r"\b(no\s+rules|no\s+restrictions|no\s+limitations|ignore\s+safety|bypass\s+safety)\b"
        ),
    ),

    InjectionPattern(
        "DE-ROLE-1",
        "Annahme einer uneingeschraenkten Persona (DAN etc.) (DE)",
        _c(
            r"\b(du\s+bist\s+jetzt|handle\s+als|tu\s+so\s+als|spiele\s+die\s+rolle\s+von|simuliere)\b"
            + _GAP
            + r"\b(DAN|jailbroken|uneingeschränkt|uneingeschraenkt|unzensiert|ungefiltert|entwicklermodus|gottmodus|root|admin)\b"
        ),
    ),
    InjectionPattern(
        "DE-ROLE-2",
        "Aktivieren eines 'Modus' ohne Einschraenkungen (DE)",
        _c(
            r"\b(aktiviere|starte|wechsle\s+in|schalte\s+in)\b"
            + _GAP
            + r"\b(entwicklermodus|jailbreak\s*modus|uneingeschränkten\s+modus|uneingeschraenkten\s+modus|debug\s*modus|admin\s*modus)\b"
        ),
    ),
    InjectionPattern(
        "DE-ROLE-3",
        "Dauerhafte Aufhebung von Regeln 'ab jetzt' (DE)",
        _c(
            r"\b(ab\s+jetzt|von\s+nun\s+an|für\s+den\s+rest\s+dieser\s+unterhaltung|fuer\s+den\s+rest\s+dieser\s+unterhaltung)\b"
            + _GAP
            + r"\b(keine\s+regeln|keine\s+einschränkungen|keine\s+einschraenkungen|sicherheit\s+ignorieren|sicherheit\s+umgehen)\b"
        ),
    ),

    InjectionPattern(
        "EN-LEAK-1",
        "Aufforderung, den System-/Entwickler-Prompt offenzulegen (EN)",
        _c(
            r"\b(reveal|show|display|print|dump|output|expose|leak|tell\s+me)\b"
            + _GAP
            + r"\b(system\s+prompt|developer\s+prompt|system\s+message|developer\s+message|hidden\s+instructions?|internal\s+instructions?|initial\s+prompt)\b"
        ),
    ),
    InjectionPattern(
        "EN-LEAK-2",
        "Aufforderung, eigene Anweisungen woertlich zu wiederholen (EN)",
        _c(
            r"\b(what\s+are|repeat|verbatim|exactly)\b"
            + _GAP
            + r"\b(your\s+instructions|your\s+rules|your\s+system\s+prompt|your\s+developer\s+message|the\s+hidden\s+prompt)\b"
        ),
    ),
    InjectionPattern(
        "EN-LEAK-3",
        "Aufforderung, vertrauliche interne Regeln aufzulisten (EN)",
        _c(
            r"\b(list|print|show|reveal)\b"
            + _GAP
            + r"\b(confidential|private|internal|hidden)\b"
            + _GAP
            + r"\b(instructions?|rules?|policies?|prompts?|messages?)\b"
        ),
    ),

    InjectionPattern(
        "DE-LEAK-1",
        "Aufforderung, den System-/Entwickler-Prompt offenzulegen (DE)",
        _c(
            r"\b(zeige|gib\s+aus|drucke|verrate|offenbare|enthülle|enthuelle|leake|nenne\s+mir)\b"
            + _GAP
            + r"\b(system\s*prompt|entwickler\s*prompt|systemnachricht|entwicklernachricht|versteckte\s+anweisungen|interne\s+anweisungen|ursprünglicher\s+prompt|urspruenglicher\s+prompt)\b"
        ),
    ),
    InjectionPattern(
        "DE-LEAK-2",
        "Aufforderung, eigene Anweisungen woertlich zu wiederholen (DE)",
        _c(
            r"\b(wiederhole|zitiere|wortwörtlich|wortwoertlich|exakt|genau)\b"
            + _GAP
            + r"\b(deine\s+anweisungen|deine\s+regeln|deinen\s+system\s*prompt|deine\s+entwicklernachricht|den\s+versteckten\s+prompt)\b"
        ),
    ),
    InjectionPattern(
        "DE-LEAK-3",
        "Aufforderung, vertrauliche interne Regeln aufzulisten (DE)",
        _c(
            r"\b(liste|zeige|drucke|verrate|enthülle|enthuelle)\b"
            + _GAP
            + r"\b(vertrauliche|private|interne|versteckte)\b"
            + _GAP
            + r"\b(anweisungen|regeln|richtlinien|prompts?|nachrichten)\b"
        ),
    ),

    InjectionPattern(
        "EN-BYP-1",
        "Aufforderung, Schutzmechanismen zu deaktivieren/umgehen (EN)",
        _c(
            r"\b(ignore|bypass|disable|turn\s+off|remove|avoid)\b"
            + _GAP
            + r"\b(safety|guardrails?|policy|policies|filters?|moderation|restrictions?|limitations?)\b"
        ),
    ),
    InjectionPattern(
        "EN-BYP-2",
        "Aufforderung, nicht zu verweigern/warnen (EN)",
        _c(
            r"\b(do\s+not|don't)\b"
            + r"[\s\S]{0,30}"
            + r"\b(refuse|warn|apologize|mention\s+policy|mention\s+safety|follow\s+policy)\b"
        ),
    ),
    InjectionPattern(
        "EN-BYP-3",
        "Aufforderung, ohne Einschraenkungen zu antworten (EN)",
        _c(
            r"\b(answer|respond|comply)\b"
            + _GAP
            + r"\b(without\s+restrictions|without\s+limitations|without\s+filters|without\s+ethical\s+constraints|without\s+safety)\b"
        ),
    ),

    InjectionPattern(
        "DE-BYP-1",
        "Aufforderung, Schutzmechanismen zu deaktivieren/umgehen (DE)",
        _c(
            r"\b(ignoriere|umgehe|deaktiviere|schalte\s+aus|entferne|vermeide)\b"
            + _GAP
            + r"\b(sicherheit|schutzmechanismen|guardrails?|richtlinien|policy|filter|moderation|einschränkungen|einschraenkungen|begrenzungen)\b"
        ),
    ),
    InjectionPattern(
        "DE-BYP-2",
        "Aufforderung, nicht zu verweigern/warnen (DE)",
        _c(
            r"\b(weiger[e]?|verweigere|entschuldige|warne|erwähne|erwaehne)\b"
            + r"[\s\S]{0,30}"
            + r"\b(nicht|niemals|keinesfalls)\b"
            + _GAP
            + r"\b(policy|richtlinie|sicherheit|regel)\b"
        ),
    ),
    InjectionPattern(
        "DE-BYP-3",
        "Aufforderung, ohne Einschraenkungen zu antworten (DE)",
        _c(
            r"\b(antworte|reagiere|befolge)\b"
            + _GAP
            + r"\b(ohne\s+einschränkungen|ohne\s+einschraenkungen|ohne\s+begrenzungen|ohne\s+filter|ohne\s+ethische\s+vorgaben|ohne\s+sicherheit)\b"
        ),
    ),

    InjectionPattern(
        "EN-EXF-1",
        "Aufforderung, Secrets/Keys/Passwoerter auszugeben/zu senden (EN)",
        _c(
            r"\b(reveal|show|print|dump|extract|exfiltrate|send|forward|email|upload)\b"
            + r"[\s\S]{0,60}"
            + r"\b(secrets?|api\s*keys?|tokens?|passwords?|credentials?|private\s+keys?|environment\s+variables|\.env|confidential\s+data)\b"
        ),
    ),
    InjectionPattern(
        "EN-EXF-2",
        "Aufforderung, Quellen nach Secrets zu durchsuchen (EN)",
        _c(
            r"\b(search|scan|inspect|read)\b"
            + _GAP
            + r"\b(files?|documents?|emails?|messages?|database|memory|context|conversation)\b"
            + r"[\s\S]{0,60}"
            + r"\b(for|containing)\b"
            + _GAP
            + r"\b(secrets?|passwords?|tokens?|api\s*keys?|credentials?)\b"
        ),
    ),

    InjectionPattern(
        "DE-EXF-1",
        "Aufforderung, Secrets/Keys/Passwoerter auszugeben/zu senden (DE)",
        _c(
            r"\b(zeige|drucke|gib\s+aus|extrahiere|exfiltriere|sende|leite\s+weiter|mail[e]?|lade\s+hoch)\b"
            + r"[\s\S]{0,60}"
            + r"\b(geheimnisse|api\s*keys?|tokens?|passwörter|passwoerter|zugangsdaten|private\s+schlüssel|private\s+schluessel|umgebungsvariablen|\.env|vertrauliche\s+daten)\b"
        ),
    ),
    InjectionPattern(
        "DE-EXF-2",
        "Aufforderung, Quellen nach Secrets zu durchsuchen (DE)",
        _c(
            r"\b(durchsuche|scanne|prüfe|pruefe|lies)\b"
            + _GAP
            + r"\b(dateien|dokumente|emails?|nachrichten|datenbank|speicher|kontext|unterhaltung)\b"
            + r"[\s\S]{0,60}"
            + r"\b(nach|mit|enthaltend)\b"
            + _GAP
            + r"\b(geheimnissen|passwörtern|passwoertern|tokens?|api\s*keys?|zugangsdaten)\b"
        ),
    ),

    InjectionPattern(
        "EN-TOOL-1",
        "Aufforderung, Tools heimlich/ohne Bestaetigung zu nutzen (EN)",
        _c(
            r"\b(call|invoke|use|execute|run)\b"
            + _GAP
            + r"\b(tool|function|plugin|browser|python|shell|terminal|api)\b"
            + r"[\s\S]{0,60}"
            + r"\b(ignore|bypass|without\s+asking|without\s+confirmation|silently|secretly)\b"
        ),
    ),
    InjectionPattern(
        "EN-TOOL-2",
        "Aufforderung, ohne Nachfrage Aktionen auszufuehren (EN)",
        _c(
            r"\b(do\s+not\s+ask|without\s+asking|without\s+confirmation|silently|secretly)\b"
            + r"[\s\S]{0,60}"
            + r"\b(call|invoke|use|execute|run|send|delete|modify)\b"
        ),
    ),

    InjectionPattern(
        "DE-TOOL-1",
        "Aufforderung, Tools heimlich/ohne Bestaetigung zu nutzen (DE)",
        _c(
            r"\b(rufe|verwende|nutze|führe\s+aus|fuehre\s+aus|starte)\b"
            + _GAP
            + r"\b(tool|funktion|plugin|browser|python|shell|terminal|api)\b"
            + r"[\s\S]{0,60}"
            + r"\b(ignoriere|umgehe|ohne\s+nachfrage|ohne\s+bestätigung|ohne\s+bestaetigung|heimlich|verdeckt)\b"
        ),
    ),
    InjectionPattern(
        "DE-TOOL-2",
        "Aufforderung, ohne Nachfrage Aktionen auszufuehren (DE)",
        _c(
            r"\b(frage\s+nicht|ohne\s+nachfrage|ohne\s+bestätigung|ohne\s+bestaetigung|heimlich|verdeckt)\b"
            + r"[\s\S]{0,60}"
            + r"\b(rufe|verwende|nutze|führe\s+aus|fuehre\s+aus|sende|lösche|loesche|ändere|aendere)\b"
        ),
    ),

    InjectionPattern(
        "EN-IND-1",
        "Eingebettete 'Attention/System'-Anweisung in Fremdtext (EN)",
        _c(
            r"\b(attention|note|important|system|assistant|model|llm)\b"
            + r"[\s\S]{0,30}"
            + r"\b(ignore|disregard|override|forget|follow\s+these\s+instructions)\b"
            + _GAP
            + r"\b(previous|above|user|developer|system|instructions?|rules?)\b"
        ),
    ),
    InjectionPattern(
        "EN-IND-2",
        "Dokument/Email 'instructs the assistant' (EN)",
        _c(
            r"\b(this\s+document|this\s+email|this\s+webpage|this\s+page|the\s+following\s+text)\b"
            + r"[\s\S]{0,60}"
            + r"\b(instructs|commands|tells)\b"
            + _GAP
            + r"\b(the\s+assistant|the\s+model|the\s+llm|chatgpt)\b"
        ),
    ),
    InjectionPattern(
        "EN-IND-3",
        "Versteckte/unsichtbare Anweisungen (EN)",
        _c(
            r"\b(hidden|invisible|white\s+text|metadata|alt\s+text|comment)\b"
            + _GAP
            + r"\b(instructions?|prompt|commands?)\b"
        ),
    ),

    InjectionPattern(
        "DE-IND-1",
        "Eingebettete 'Achtung/System'-Anweisung in Fremdtext (DE)",
        _c(
            r"\b(achtung|hinweis|wichtig|system|assistent|modell|llm)\b"
            + r"[\s\S]{0,30}"
            + r"\b(ignoriere|missachte|überschreibe|ueberschreibe|vergiss|befolge\s+diese\s+anweisungen)\b"
            + _GAP
            + r"\b(vorherige|obige|benutzer|entwickler|system|anweisungen|regeln)\b"
        ),
    ),
    InjectionPattern(
        "DE-IND-2",
        "Dokument/Email 'weist den Assistenten an' (DE)",
        _c(
            r"\b(dieses\s+dokument|diese\s+email|diese\s+webseite|diese\s+seite|der\s+folgende\s+text)\b"
            + r"[\s\S]{0,60}"
            + r"\b(weist\s+an|befiehlt|sagt)\b"
            + _GAP
            + r"\b(den\s+assistenten|das\s+modell|das\s+llm|chatgpt)\b"
        ),
    ),
    InjectionPattern(
        "DE-IND-3",
        "Versteckte/unsichtbare Anweisungen (DE)",
        _c(
            r"\b(versteckte|unsichtbare|weiße\s+schrift|weisse\s+schrift|metadaten|alt\s*text|kommentar)\b"
            + _GAP
            + r"\b(anweisungen|prompt|befehle|kommandos)\b"
        ),
    ),

    InjectionPattern(
        "XX-OBF-1",
        "Dekodieren und anschliessend ausfuehren (EN/DE)",
        _c(
            r"\b(decode|decrypt|base64|rot13|hex|unicode|reverse\s+the\s+text|entschlüssle|entschluessle|dekodiere|decodiere)\b"
            + r"[\s\S]{0,60}"
            + r"\b(then|danach|anschließend|anschliessend)\b"
            + _GAP
            + r"\b(follow|execute|run|obey|befolge|führe\s+aus|fuehre\s+aus)\b"
        ),
    ),
    InjectionPattern(
        "XX-OBF-2",
        "Fremdtext als System-Prompt/Anweisung interpretieren (EN/DE)",
        _c(
            r"\b(treat|handle|interpret|behandle|interpretiere)\b"
            + _GAP
            + r"\b(as|als)\b"
            + _GAP
            + r"\b(system\s+prompt|developer\s+message|instructions?|commands?|systemprompt|entwicklernachricht|anweisungen|befehle)\b"
        ),
    ),

    InjectionPattern(
        "XX-FMT-1",
        "Doppelte Antwort (normal + jailbroken) (EN/DE)",
        _c(
            r"\b(answer|respond|reply|antworte|reagiere)\b"
            + _GAP
            + r"\b(two\s+ways|dual\s+response|normal\s+and\s+jailbroken|zweigeteilt|zwei\s+antworten|normal\s+und\s+jailbreak)\b"
        ),
    ),
    InjectionPattern(
        "XX-FMT-2",
        "Antwort mit Jailbreak-Praefix beginnen (EN/DE)",
        _c(
            r"\b(prefix|begin|start|präfix|praefix|beginne|starte)\b"
            + _GAP
            + r"\b(jailbroken|unfiltered|uncensored|DAN|unzensiert|ungefiltert|uneingeschränkt|uneingeschraenkt)\b"
        ),
    ),

    InjectionPattern(
        "EN-WORD-1",
        "Woertliche Nennung von Angriffstechniken (EN)",
        _c(
            r"\b(prompt\s*injection|jailbreak|policy\s*bypass|system\s*prompt\s*leak|instruction\s*override)\b"
        ),
    ),
    InjectionPattern(
        "DE-WORD-1",
        "Woertliche Nennung von Angriffstechniken (DE)",
        _c(
            r"\b(prompt\s*injektion|prompt\s*injection|jailbreak|richtlinien\s*umgehung|policy\s*umgehung|system\s*prompt\s*leak|anweisungs\s*überschreibung|anweisungs\s*ueberschreibung)\b"
        ),
    ),
]