using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ScoresController : ControllerBase
    {
        private readonly PythonService _pythonService;

        public ScoresController(PythonService pythonService)
        {
            _pythonService = pythonService;
        }

        [HttpGet]
        public IActionResult GetScores()
        {
            string jsonResult = _pythonService.RunFetchData("scores");

            if (string.IsNullOrWhiteSpace(jsonResult))
                return StatusCode(500, new { error = "Failed to fetch scores" });

            return Content(jsonResult, "application/json");
        }
    }
}