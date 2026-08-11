from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def format_ist(dt: datetime) -> str:
    from zoneinfo import ZoneInfo
    return dt.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %H:%M")