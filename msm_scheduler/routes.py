from .lib.simple_http_request_handler import SimpleHTTPRequestHandler
from .availability import build_boss_players
from .schedule import schedule

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

    lines.append(f"=== {_schedule.boss_name} schedules")
    lines.append("")

    for team in teams:
      lines.append(f"~ {team.time} filled {len(team.players)}/{team.boss.capacity}")

      for player in team.players:
          lines.append(f"{player.name}") 

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
            lines.append(f"{player.name}")
        lines.append("")

  context.render(
    plain = __to_html("\n".join(lines)),
    status = 200
  )

def __to_html(body: str):
  head = ['<head>', '<meta charset="UTF-8">', '</head>']
  body = ['<body>', '<pre>', body, '</pre>', '</body>']
  return "\n".join(head + body)

ROUTES = {
  'GET': [
      ['/availability', get_availability],
      ['/schedule', get_schedule],
  ],
}