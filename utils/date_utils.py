from dateutil import parser
from datetime import datetime

def parse_iso(s):
    try:
        return parser.parse(s)
    except Exception:
        return None

def now_iso():
    return datetime.utcnow().isoformat() + "Z"
