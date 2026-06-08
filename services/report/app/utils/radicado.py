from datetime import datetime
from uuid import uuid4


def generate_radicado() -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    unique_part = uuid4().hex[:8].upper()
    return f"RPT-{date_part}-{unique_part}"
