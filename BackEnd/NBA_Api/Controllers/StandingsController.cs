using Microsoft.AspNetCore.Mvc;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/controller")]
    public class StandingsController : ControllerBase
    {
       
        [HttpGet]
        public IActionResult GetStandings()
       {
            
            var standings = new[]
            {
                new { Team = "Boston Celtics", Wins = 45, Losses = 20, WinPct = 0.692 },
                new { Team = "Milwaukee Bucks", Wins = 43, Losses = 22, WinPct = 0.661 }
            };
            return Ok(standings);
       }
    }
}
