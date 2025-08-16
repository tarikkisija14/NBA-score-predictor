from nba_api.stats.endpoints import leagueleaders

data = leagueleaders.LeagueLeaders(
    stat_category_abbreviation="PTS",
    per_mode48="PerGame",
    season="2024-25",
    season_type_all_star="Regular Season"
).get_dict()

print(data['resultSet']['headers'])
print(data['resultSet']['rowSet'][:5])
