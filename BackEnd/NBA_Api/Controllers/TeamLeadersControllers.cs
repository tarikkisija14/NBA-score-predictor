using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TeamLeadersControllers : ControllerBase
    {
        private readonly ITeamLeadersService _teamLeadersService;

        public TeamLeadersControllers(ITeamLeadersService teamLeadersService)
        {
            _teamLeadersService = teamLeadersService;

        }
        [HttpGet]
        public IActionResult GetTeamLeaders()
        {
            var leaders = _teamLeadersService.GetTeamLeaders();
            return Ok(leaders);
        }



    }
}
