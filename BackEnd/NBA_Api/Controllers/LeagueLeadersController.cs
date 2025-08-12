using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class LeagueLeadersController : ControllerBase
    {
        private readonly PythonService _pythonService;

        public LeagueLeadersController(PythonService pythonService)
        {
            _pythonService = pythonService;
        }

        [HttpGet]
       public IActionResult GetLeagueLeaders()
        {
            string jsonResult = _pythonService.RunFetchData("league_leaders");
            if (string.IsNullOrWhiteSpace(jsonResult))
                return StatusCode(500, "Failed to fetch league leaders data");

            return Content(jsonResult, "application/json");
        }
    }
}
