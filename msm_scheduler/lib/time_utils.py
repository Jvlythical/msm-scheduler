from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

DAYS_MAP = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

def get_next_timestamp(day: str, hour: int) -> int:
    """
    Convert day and hour (PST) to the next occurrence's Unix timestamp
    
    Args:
        day: Day of week (e.g., 'monday')
        hour: Hour in 24-hour format (PST)
    
    Returns:
        Unix timestamp for next occurrence
    """
    pst = ZoneInfo('America/Los_Angeles')
    now = datetime.now(pst)
    
    # Get the target day as an integer (0 = Monday, 6 = Sunday)
    target_day = DAYS_MAP[day.lower()]
    current_day = now.weekday()
    
    # Calculate days until next occurrence
    days_ahead = target_day - current_day
    if days_ahead <= 0:  # Target day has passed this week
        days_ahead += 7
    
    # Create target datetime
    target_date = now.date() + timedelta(days=days_ahead)
    target_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour))
    target_datetime = target_time.replace(tzinfo=pst)
    
    # Adjust for DST if needed
    if target_datetime.dst():
        target_datetime = target_datetime + timedelta(hours=1)
    
    return int(target_datetime.timestamp())

def format_team_time(team_time: str, boss_name: str = None) -> str:
    """
    Format team time into Discord timestamp and GT time
    
    Args:
        team_time: Time string in format 'day.hour' (e.g., 'monday.19')
        boss_name: Name of the boss for the team
    
    Returns:
        Formatted string with Discord timestamp and GT time
    """
    day, hour = team_time.split('.')
    hour = int(hour)
    
    # Get current datetime to check DST
    pst = ZoneInfo('America/Los_Angeles')
    now = datetime.now(pst)
    
    # Create a datetime for the target time to check DST
    target_day = DAYS_MAP[day.lower()]
    current_day = now.weekday()
    days_ahead = target_day - current_day
    if days_ahead <= 0:
        days_ahead += 7
    target_date = now.date() + timedelta(days=days_ahead)
    target_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour))
    target_datetime_pst = target_time.replace(tzinfo=pst)
    
    # During DST, add an hour to display times
    if target_datetime_pst.dst():
        target_datetime_pst = target_datetime_pst + timedelta(hours=1)
    
    # Get Unix timestamp for Discord
    timestamp = int(target_datetime_pst.timestamp())
    
    # Create Google Calendar link
    # Convert to UTC for Google Calendar
    target_datetime_utc = target_datetime_pst.astimezone(ZoneInfo('UTC'))
    # Format for Google Calendar URL (YYYYMMDDTHHMMSSZ)
    calendar_time = target_datetime_utc.strftime('%Y%m%dT%H%M%SZ')
    # Create 1-hour event
    calendar_end_time = (target_datetime_utc + timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')
    
    # Format boss name for display (replace underscores with spaces and capitalize)
    display_boss_name = boss_name.replace('_', ' ').title() if boss_name else day.capitalize()
    
    # URL encode the event title
    event_title = f"{display_boss_name} at {hour:02d}00 Game Time"
    encoded_title = event_title.replace(' ', '%20')
    
    calendar_url = f"http://www.google.com/calendar/event?action=TEMPLATE&text={encoded_title}&details=&location=&dates={calendar_time}/{calendar_end_time}"
    
    # Return format with Discord timestamp, GT time, and calendar link
    # Use markdown link format [Text](Link)
    return f"<t:{timestamp}:F> / {hour:02d}00 GT / [Add to Calendar]({calendar_url})" 