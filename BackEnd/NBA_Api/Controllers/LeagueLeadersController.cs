using Microsoft.AspNetCore.Mvc;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class LeagueLeadersController : Controller
    {
        [HttpGet("leaders")]
       public IActionResult GetLeagueLeaders()
        {
            var leaders = new
            {
                PPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                RPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                APG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                SPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                BPG = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" },
                FGPercent = new[] { "Player1", "Player2", "Player3", "Player4", "Player5" }
            };
            return Ok(leaders);
        }
    }
}
