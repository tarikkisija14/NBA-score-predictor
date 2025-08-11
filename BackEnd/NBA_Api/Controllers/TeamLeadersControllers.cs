using Microsoft.AspNetCore.Mvc;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TeamLeadersControllers : Controller
    {
        [HttpGet("{teamId}")]
       public IActionResult GetTeamLeaders(string teamId)
        {
            var leaders = new
            {
                TeamId = teamId,
                PPG = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" },
                RPG = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" },
                APG = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" },
                SPG = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" },
                BPG = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" },
                FGPercent = new[] { "PlayerA", "PlayerB", "PlayerC", "PlayerD", "PlayerE" }
            };
            return Ok(leaders);
        }
    }
}
