from .lib.simple_http_request_handler import SimpleHTTPRequestHandler
from .availability import build_boss_players
from .schedule import schedule

def get_availability(context: SimpleHTTPRequestHandler):
  try:
    boss_players = build_boss_players()
  except RuntimeError as e:
    return context.render(
      plain = str(e),
      status = 400
    )
  except Exception as e:
    return context.render(
      plain = str(e),
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
    teams = schedule()
  except RuntimeError as e:
    return context.render(
      plain = str(e),
      status = 400
    )
  except Exception as e:
    return context.render(
      plain = str(e),
      status = 500
    )
  
  lines = []
  for team in teams:
    lines.append(f"=== {team.boss_name} team at {team.time}")
    lines.append(f"~ Filled {len(team.players)}/{team.boss.capacity}")
    for player in team.players:
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