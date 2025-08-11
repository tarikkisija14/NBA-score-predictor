namespace NBA_Api.Services
{
    public class StandingsService : IStandingsService
    {
        public IEnumerable<object>GetStandings()
        {
            return new[]
            {
                new { Team = "Boston Celtics", Wins = 45, Losses = 20, WinPct = 0.692 },
                new { Team = "Milwaukee Bucks", Wins = 43, Losses = 22, WinPct = 0.661 }
            };
        }
    }
}
