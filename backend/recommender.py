import sqlite3
from typing import Dict, List

ALLOWED_FIELDS = ['id','model','brand','price','camera_mp','battery_mah','display_inch','ram_gb','storage_gb','soc','notes']

def row_to_dict(row, cols):
    return {c: row[i] for i,c in enumerate(cols) if c in ALLOWED_FIELDS}


def query_phones(db_path: str, intent: Dict) -> List[Dict]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    where = []
    params = []
    if 'budget_max' in intent:
        where.append('price <= ?')
        params.append(intent['budget_max'])
    if 'brands' in intent:
        where.append('brand IN ({})'.format(','.join('?' for _ in intent['brands'])))
        params += intent['brands']
    # base query
    q = 'SELECT ' + ','.join(ALLOWED_FIELDS) + ' FROM phones'
    if where:
        q += ' WHERE ' + ' AND '.join(where)
    q += ' ORDER BY price ASC LIMIT 10'
    cur.execute(q, params)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()

    items = [row_to_dict(r, cols) for r in rows]

    # scoring: simple feature boost if user asked for camera or battery
    if intent.get('features'):
        feature = intent['features'][0]
        if feature == 'camera':
            items.sort(key=lambda x: (-(x.get('camera_mp') or 0), x['price']))
        if feature == 'battery':
            items.sort(key=lambda x: (-(x.get('battery_mah') or 0), x['price']))
    return items


def compare_models(db_path: str, models: List[str]) -> List[Dict]:
    # Accept model names (full match preferred), return structured compare rows
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    placeholders = ','.join('?' for _ in models)
    q = f"SELECT {','.join(ALLOWED_FIELDS)} FROM phones WHERE model IN ({placeholders})"
    cur.execute(q, models)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r, cols) for r in rows]