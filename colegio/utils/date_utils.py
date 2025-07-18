import pytz
from django.utils import timezone

def get_user_timezone(user):
    return user.time_zone

def get_current_date(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    fecha_actual = timezone.now().astimezone(user_timezone).date()
    return fecha_actual.strftime('%Y-%m-%d')

def get_current_time(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    now = timezone.now().astimezone(user_timezone)
    return now.replace(second=0, microsecond=0).time()

def get_midnight(user):
    user_timezone_str = get_user_timezone(user)
    user_timezone = pytz.timezone(user_timezone_str)
    now = timezone.now().astimezone(user_timezone)
    midnight_user_tz = now.replace(hour=23, minute=59, second=0, microsecond=0)
    return midnight_user_tz