from datetime import datetime
from pytz import timezone, utc


def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    asia = timezone('Asia/Makassar')
    converted = utc_dt.astimezone(asia)
    return converted.timetuple()
