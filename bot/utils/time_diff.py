from datetime import datetime, timezone
from tzlocal import get_localzone


def time_diff(str):
    api_date_str = str
    user_timezone = get_localzone()
    api_datetime = datetime.strptime(api_date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
        tzinfo=timezone.utc
    )
    current_time = datetime.now(user_timezone)
    api_local_time = api_datetime.astimezone(user_timezone)
    time_difference = api_local_time - current_time
    minutes, seconds = divmod(int(time_difference.total_seconds()), 60)
    return (minutes, seconds)
