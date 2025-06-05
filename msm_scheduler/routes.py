from .lib.simple_http_request_handler import SimpleHTTPRequestHandler
from .availability import build_boss_players
from .schedule import schedule
from .lib.time_utils import get_next_timestamp, format_team_time, parse_team_time

def get_availability(context: SimpleHTTPRequestHandler):
  try:
    boss_players = build_boss_players()
  except RuntimeError as e:
    return context.render(
      plain = __to_html(str(e)),
      status = 400
    )
  except Exception as e:
    return context.render(
      plain = __to_html(str(e)),
      status = 500
    )

  availability_distribution = boss_players.availability_distribution()

  lines = []
  for boss_name in availability_distribution:
    lines.append(f"=== {boss_name} availability distribution")
    lines.append(f"~ There are {len(boss_players.get(boss_name))} available players")
    times = availability_distribution[boss_name]

    sorted_times = list(times.keys())
    sorted_times.sort()
    for time in sorted_times:
      key = "{:<15}".format(time)
      lines.append(f"{key}: {' '.join(times[time])}")
    lines.append("")

  context.render(
    plain = __to_html("\n".join(lines)),
    status = 200
  )

def get_schedule(context: SimpleHTTPRequestHandler):
  try:
    schedules = schedule()
  except RuntimeError as e:
    return context.render(
      plain = __to_html(str(e)),
      status = 400
    )
  except Exception as e:
    return context.render(
      plain = __to_html(str(e)),
      status = 500
    )
  
  lines = []
  for _schedule in schedules:
    teams = _schedule.teams
    # Format boss name in Title Case and replace underscores with spaces
    formatted_boss_name = _schedule.boss_name.replace('_', ' ').title()

    lines.append(f"=== {formatted_boss_name} schedules")
    lines.append("")

    for team in teams:
      day, hour, minutes = parse_team_time(team.time)
      
      # Format team name as "Boss Name Day: TeamName"
      formatted_team_name = f"{formatted_boss_name} {day.capitalize()}: {team.team_name}"
      lines.append(f"~ {formatted_team_name}")
      lines.append(format_team_time(team.time, _schedule.boss_name))

      # Get formatted players
      formatted_players = list(team.get_formatted_players())
      
      # Add numbered entries for all players
      for i, (player, role_label) in enumerate(formatted_players, 1):
        discord_tag = f"@{player.discord_id}" if player.discord_id else player.name
        lines.append(f"{i}. {discord_tag} ({player.name}){role_label}")
      
      # Add FILL entries for remaining slots
      for i in range(len(formatted_players) + 1, team.boss.capacity + 1):
        lines.append(f"{i}. FILL")

      if len(team.availability_conflicts) > 0:
        lines.append("")
        lines.append(f"~ Availability Conflicts")
        for player in team.availability_conflicts:
          lines.append(f"{player.name}")

      if len(team.interest_conflicts) > 0:
        lines.append("")
        lines.append(f"~ Interest Conflicts")
        for player in team.interest_conflicts:
          lines.append(f"{player.name}")

      lines.append("")

    if len(_schedule.fills) > 0:
        lines.append(f"~ Fills")
        for player in _schedule.fills:
            discord_tag = f"@{player.discord_id}" if player.discord_id else player.name
            lines.append(f"{discord_tag} ({player.name})")
        lines.append("")

  context.render(
    plain = __to_html("\n".join(lines)),
    status = 200
  )

def __to_html(body: str):
  # Escape HTML characters to display Discord tags correctly
  body = body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
  
  # Convert markdown links to HTML links, but preserve calendar links
  import re
  link_pattern = r'\[(.*?)\]\((.*?)\)'
  body = re.sub(link_pattern, lambda m: m.group(0) if 'calendar' in m.group(2) else f'<a href="{m.group(2)}" target="_blank">{m.group(1)}</a>', body)
  
  head = ['<head>', '<meta charset="UTF-8">', '</head>']
  body = ['<body>', '<pre>', body, '</pre>', '</body>']
  return "\n".join(head + body)

ROUTES = {
  'GET': [
      ['/availability', get_availability],
      ['/schedule', get_schedule],
  ],
}