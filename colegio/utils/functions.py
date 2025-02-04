from django.utils import timezone
import pytz
from datetime import datetime 

def time_zone_user_location(location):
    zona_horaria_usuario = pytz.timezone(location)
    nowDate = datetime.now(zona_horaria_usuario).date()
    nowTime = datetime.now(zona_horaria_usuario).time()
    
    ## Obtener la zona horaria local ## Get time zone 
    # DateNow, TimeNow = time_zone_user_location(request.user.time_zone)
    return nowDate, nowTime