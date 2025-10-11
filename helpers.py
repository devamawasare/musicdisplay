from typing import Any, Dict, Optional
from xml.dom.pulldom import default_bufsize

def _get(d: Any, path: list, default=None):
    current = d
    for p in path:
        if isinstance(current, dict) and isinstance(p, str):
            current = current.get(p, default if p == path[-1] else None)
        else:
            return default
    return current
