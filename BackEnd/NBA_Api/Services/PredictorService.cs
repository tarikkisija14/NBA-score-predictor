using NBA_Api.DTOs;

namespace NBA_Api.Services
{
    public class PredictorService: IPredictorService
    {

        public PredictResult Predict(string homeTeam, string awayTeam)
        {
            return new PredictResult
            {
                Winner = "Los Angeles Lakers",
                HomeScore = 102,
                AwayScore = 97,
                Loser = "Boston Celtics"

            };
        }
    }
}
