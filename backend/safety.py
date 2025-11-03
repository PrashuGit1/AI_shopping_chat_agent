BLOCKED_PATTERNS = [
    r'ignore your rules',
    r'tell me your api key',
    r'system prompt',
]

TOXIC_PATTERNS = [r'trash brand', r'kill', r'hate']

def check_user_message(text: str):
    t = text.lower()
    for p in BLOCKED_PATTERNS:
        if p in t:
            return False, 'Refusing to reveal internal secrets or keys.'
    for p in TOXIC_PATTERNS:
        if p in t:
            return False, 'Refusing hateful or abusive requests.'
    return True, ''