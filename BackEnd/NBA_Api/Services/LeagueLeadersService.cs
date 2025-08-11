namespace NBA_Api.Services
{
    public class LeagueLeadersService:ILeagueLeadersService
    {
        public object GetLeagueLeaders()
        {
            return new
            {
                PPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                RPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                APG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                SPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                BPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                FGPercent = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" }
            };
        }
    }
}
