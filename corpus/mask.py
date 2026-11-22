from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerResult

__in_phone_pattern = Pattern(
    name="in_mobile_pattern",
    regex=r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b",
    score=0.85,
)

_recognize_phone_pattern = PatternRecognizer(
    supported_entity = "PHONE_NUMBER",
    patterns = [__in_phone_pattern],
)


_entity_priority ={
    "PHONE_NUMBER" : 0,
    "EMAIL_ADDRESS": 2,
    "PERSON": 3,
    "LOCATION": 4,
    "DATE_TIME": 5,
    "UK_NHS": 99,
}

_engine = AnalyzerEngine()
_engine.registry.add_recognizer(_recognize_phone_pattern)

def _priority_key(findings : RecognizerResult) -> tuple:
    priority = _entity_priority.get(findings.entity_type, 50)
    span_length = findings.end - findings.start 
    return(priority, -findings.score, span_length)

def _fix_overlapped(findings : list[RecognizerResult]) -> list[RecognizerResult]:
    if not findings :
        return []
    
    sorted_findings = sorted(findings, key= lambda f: (f.start , _priority_key(f)))
    trimmed = [sorted_findings[0]] # since that is oyr insitail best case in priority

    for current in sorted_findings[1:]:
        previous = trimmed[-1]
        if current.start < previous.end:
            if _priority_key(current) < _priority_key(previous):
                trimmed[-1] = current
        else:
            trimmed.append(current)

    return trimmed 



def mask_pii(text : str) -> str:
    if not text:
        return text

    findings = _engine.analyze(text = text, language="en")
    trimmed_clean_findings = _fix_overlapped(findings)

    masked = text

    for finding in sorted(trimmed_clean_findings, key = lambda f: f.start, reverse = True):
        placeholder = f"<{finding.entity_type}>"
        masked = masked[: finding.start] + placeholder + masked[finding.end : ]

    return masked

    