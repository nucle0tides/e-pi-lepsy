from datetime import datetime as dt
from datetime import timezone as tz

def get_timestamp():
    return dt.now(tz.utc).strftime(("%Y-%m-%dT%H:%M:%SZ"))