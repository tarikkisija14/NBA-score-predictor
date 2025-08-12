using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TeamLeadersController : ControllerBase
    {
       
        private readonly PythonService _pythonService;

        public TeamLeadersController(PythonService pythonService)
        {
            _pythonService = pythonService;
        }

        [HttpGet]
        public IActionResult GetTeamLeaders()
        {
            string jsonResult = _pythonService.RunFetchData("team_leaders");
            if (string.IsNullOrWhiteSpace(jsonResult))
                return StatusCode(500, "Failed to fetch team leaders data");

            return Content(jsonResult, "application/json");
        }



    }
}
