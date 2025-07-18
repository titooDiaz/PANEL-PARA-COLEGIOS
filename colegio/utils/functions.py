from django.utils import timezone
import pytz
from datetime import datetime 

def time_zone_user_location(location):
    zona_horaria_usuario = pytz.timezone(location)
    nowDate = datetime.now(zona_horaria_usuario).date()
    nowTime = datetime.now(zona_horaria_usuario).time()
    
    return nowDate, nowTime