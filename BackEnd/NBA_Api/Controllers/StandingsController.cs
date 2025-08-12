using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/controller")]
    public class StandingsController : ControllerBase
    {
        private readonly PythonService _pythonService;

        public StandingsController(PythonService pythonService)
        {
            _pythonService = pythonService;
        }

        [HttpGet]
        public IActionResult GetStandings()
       {

            string jsonResult = _pythonService.RunFetchData("standings");
            return Content(jsonResult, "application/json");
        }
    }
}
