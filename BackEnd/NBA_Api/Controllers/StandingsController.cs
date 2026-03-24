using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
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
            var json = _pythonService.RunFetchData("standings");

            if (string.IsNullOrWhiteSpace(json))
                return StatusCode(500, new
                {
                    error = "Python script returned empty response",
                    solution = "Check backend console for Python errors"
                });

            return Content(json, "application/json");
        }
    }
}