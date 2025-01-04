from datetime import datetime, timezone
from tzlocal import get_localzone


def time_diff(timestamp: int) -> tuple[int, int]:
    user_timezone = get_localzone()
    api_datetime = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    current_time = datetime.now(user_timezone)
    api_local_time = api_datetime.astimezone(user_timezone)
    time_difference = api_local_time - current_time
    minutes, seconds = divmod(int(time_difference.total_seconds()), 60)
    return minutes, seconds
