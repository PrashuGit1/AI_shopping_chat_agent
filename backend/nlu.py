import re
from typing import Dict, Any

BRANDS = ['samsung','oneplus','xiaomi','realme','google','apple']
FEATURES = ['camera','battery','display','performance','storage','ram']

money_re = re.compile(r'\u20B9?\s?([0-9,]+)k?', re.I)  # crude

def parse_intent(text: str) -> Dict[str, Any]:
    text_l = text.lower()
    intent = {'raw': text}

    # budget detection (e.g., 'under ₹30k' or 'below 20000')
    m = re.search(r'under\s+₹?\s?([0-9,]+)k?', text_l)
    if m:
        num = m.group(1).replace(',','')
        # handle k
        if 'k' in text_l:
            budget = int(num) * 1000
        else:
            budget = int(num)
        intent['budget_max'] = budget

    # brands
    found_brands = [b for b in BRANDS if b in text_l]
    if found_brands:
        intent['brands'] = found_brands

    # features
    found_features = [f for f in FEATURES if f in text_l]
    if found_features:
        intent['features'] = found_features

    # compare request detection
    if 'compare' in text_l or 'vs' in text_l or 'versus' in text_l:
        intent['compare'] = True
        # extract model names roughly using 'vs'
        parts = re.split(r'vs|versus', text_l)
        if len(parts) >= 2:
            left = parts[0].strip()
            right = parts[1].strip()
            # naive extraction
            intent['models'] = [left.split()[-2:], right.split()[:2]]
    return intent