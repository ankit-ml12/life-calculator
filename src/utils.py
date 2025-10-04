from datetime import datetime

START_DATE = datetime(1999, 2, 14)

def get_elapsed_time():
    """Calculate elapsed time from start date to now"""
    now = datetime.now()
    elapsed = now - START_DATE
    
    total_seconds = int(elapsed.total_seconds())
    years, remaining = divmod(total_seconds, 31536000)
    months, remaining = divmod(remaining, 2592000)
    days, remaining = divmod(remaining, 86400)
    hours, remaining = divmod(remaining, 3600)
    minutes, seconds = divmod(remaining, 60)
    
    return {
        'years': years,
        'months': months, 
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }