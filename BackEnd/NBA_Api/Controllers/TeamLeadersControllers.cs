using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TeamLeadersControllers : ControllerBase
    {
       
        private readonly PythonService _pythonService;

        public TeamLeadersControllers(PythonService pythonService)
        {
            _pythonService = pythonService;
        }

        [HttpGet]
        public IActionResult GetTeamLeaders()
        {
            string jsonResult = _pythonService.RunFetchData("team_leaders");
            return Content(jsonResult, "application/json");
        }



    }
}
