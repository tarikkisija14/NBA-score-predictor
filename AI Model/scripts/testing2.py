from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandingsv3

# Dohvati sve timove iz NBA static module
all_teams = teams.get_teams()
nickname_to_id = {t['nickname'].lower(): t['id'] for t in all_teams}

# Dohvati standings
standings_data = leaguestandingsv3.LeagueStandingsV3().get_dict()
rows = standings_data['resultSets'][0]['rowSet']

print("=== API team[4] vs nickname from static teams ===")
for team in rows:
    api_name = team[4]  # ovo je ime iz API standings
    api_name_lower = api_name.lower()
    mapped_id = nickname_to_id.get(api_name_lower, "NOT FOUND")
    print(f"API team[4]: '{api_name}' | mapped nickname: '{mapped_id}'")

print("\n=== All static team nicknames ===")
for t in all_teams:
    print(f"Nickname: '{t['nickname']}' | id: {t['id']}")
