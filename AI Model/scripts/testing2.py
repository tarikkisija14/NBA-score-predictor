from nba_api.stats.endpoints import leaguestandingsv3
import json


def inspect_league_standings():
    standings = leaguestandingsv3.LeagueStandingsV3().get_dict()

    headers = standings['resultSets'][0]['headers']
    rows = standings['resultSets'][0]['rowSet']

    print(f"Broj timova: {len(rows)}\n")
    print("Headers:")
    print(headers)
    print("\nPrimjer prvog tima:")
    print(json.dumps(rows[0], indent=2))

    # Ako želiš sve timove:
    print("\nSvi timovi i njihova polja:")
    for team in rows:
        print(json.dumps(team, indent=2))


if __name__ == "__main__":
    inspect_league_standings()
