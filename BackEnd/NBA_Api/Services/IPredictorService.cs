using NBA_Api.DTOs;

namespace NBA_Api.Services
{
    public interface IPredictorService
    {
        PredictResult Predict(string homeTeam, string awayTeam);
    }
}
