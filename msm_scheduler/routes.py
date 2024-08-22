from .lib.simple_http_request_handler import SimpleHTTPRequestHandler
from .schedule import schedule

def get_schedule(context: SimpleHTTPRequestHandler):
  teams = schedule()
  lines = []
  for team in teams:
    lines.append(f"=== {team.boss_name} team at {team.time}")
    lines.append(f"~ Filled {len(team.players)}/{team.boss.capacity}")
    for player in team.players:
        lines.append(f"{player.name}")
    lines.append("")

  context.render(
    plain = "\n".join(lines),
    status = 200
  )

ROUTES = {
  'GET': [
      ['/schedule', get_schedule],
  ],
}