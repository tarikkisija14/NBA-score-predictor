namespace NBA_Api.Services
{
    public class TeamLeadersService:ITeamLeadersService
    {
        public object GetTeamLeaders()
        {
            return new
            {
                PPG = new[] { "Boston Celtics", "Denver Nuggets", "Milwaukee Bucks", "Sacramento Kings", "Golden State Warriors" },
                RPG = new[] { "Minnesota Timberwolves", "Los Angeles Lakers", "New York Knicks", "Cleveland Cavaliers", "Memphis Grizzlies" },
                APG = new[] { "Phoenix Suns", "Denver Nuggets", "Atlanta Hawks", "Indiana Pacers", "Golden State Warriors" },
                SPG = new[] { "Miami Heat", "Toronto Raptors", "Oklahoma City Thunder", "New Orleans Pelicans", "Boston Celtics" },
                BPG = new[] { "San Antonio Spurs", "Milwaukee Bucks", "Cleveland Cavaliers", "Los Angeles Lakers", "Minnesota Timberwolves" },
                FGPercent = new[] { "Denver Nuggets", "Boston Celtics", "Phoenix Suns", "Milwaukee Bucks", "Indiana Pacers" }
            };
        }
    }
}
