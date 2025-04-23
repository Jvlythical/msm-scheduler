from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
from typing import Tuple

DAYS_MAP = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}

def parse_team_time(time_str: str) -> Tuple[str, int, int]:
    """Parse a team time string into day, hour, and minutes.
    
    Args:
        time_str: Time string in format "Day.HH" or "Day.HH.MM" or "Day.HH:MM" (e.g. "Friday.20" or "Friday.20.30" or "Friday.20:30")
        
    Returns:
        Tuple of (day, hour, minutes)
    """
    # Try format with minutes first (handling both . and : separators)
    match = re.match(r'(\w+)\.(\d{2})[.:](\d{2})', time_str)
    if match:
        day, hour, minutes = match.groups()
        return day, int(hour), int(minutes)
        
    # Try format without minutes
    match = re.match(r'(\w+)\.(\d{2})', time_str)
    if match:
        day, hour = match.groups()
        return day, int(hour), 0
        
    raise ValueError(f"Invalid time format: {time_str}")

def get_next_timestamp(day: str, hour: int, minutes: int) -> int:
    """Get the Unix timestamp for the next occurrence of the given day and time.
    
    Args:
        day: Day of week (e.g. "Friday")
        hour: Hour (0-23)
        minutes: Minutes (0-59)
        
    Returns:
        Unix timestamp
    """
    pst = ZoneInfo('America/Los_Angeles')
    now = datetime.now(pst)
    
    # Get the target day as an integer (0 = Monday, 6 = Sunday)
    target_day = DAYS_MAP[day.lower()]
    current_day = now.weekday()
    
    # Calculate days until next occurrence
    days_ahead = target_day - current_day
    if days_ahead < 0:  # Target day has passed this week
        days_ahead += 7
    
    # Create target datetime with the correct minutes
    target_date = now.date() + timedelta(days=days_ahead)
    target_time = datetime.combine(target_date, datetime.min.time().replace(hour=hour, minute=minutes))
    target_datetime = target_time.replace(tzinfo=pst)
    
    # Adjust for DST if needed
    if target_datetime.dst():
        target_datetime = target_datetime + timedelta(hours=1)
    
    return int(target_datetime.timestamp())

def format_team_time(team_time: str, boss_name: str = None) -> str:
    """
    Format team time into Discord timestamp and GT time
    
    Args:
        team_time: Time string in format 'day.hour' or 'day.hour:minutes' (e.g., 'monday.19' or 'monday.19:30')
        boss_name: Name of the boss for the team
    
    Returns:
        Formatted string with Discord timestamp and GT time
    """
    day, hour, minutes = parse_team_time(team_time)
    
    # Get timestamp using get_next_timestamp
    timestamp = get_next_timestamp(day, hour, minutes)
    
    # Create datetime from timestamp for calendar link
    pst = ZoneInfo('America/Los_Angeles')
    target_datetime_pst = datetime.fromtimestamp(timestamp, pst)
    
    # Create Google Calendar link
    # Convert to UTC for Google Calendar
    target_datetime_utc = target_datetime_pst.astimezone(ZoneInfo('UTC'))
    # Format for Google Calendar URL (YYYYMMDDTHHMMSSZ)
    calendar_time = target_datetime_utc.strftime('%Y%m%dT%H%M%SZ')
    # Create 1-hour event
    calendar_end_time = (target_datetime_utc + timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')
    
    # Format boss name for display (replace underscores with spaces and capitalize)
    display_boss_name = boss_name.replace('_', ' ').title() if boss_name else day.capitalize()
    
    # URL encode the event title with minutes
    event_title = f"{display_boss_name} at {hour:02d}{minutes:02d} Game Time"
    encoded_title = event_title.replace(' ', '%20')
    
    calendar_url = f"http://www.google.com/calendar/event?action=TEMPLATE&text={encoded_title}&details=&location=&dates={calendar_time}/{calendar_end_time}"
    
    # Return format with Discord timestamp, GT time with minutes, and calendar link
    return f"<t:{timestamp}:F> / {hour:02d}{minutes:02d} GT / [Add to Calendar]({calendar_url})"