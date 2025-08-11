using Microsoft.AspNetCore.Mvc;
using NBA_Api.Services;
using NBA_Api.DTOs;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PredictorController : Controller
    {
       private readonly IPredictorService _predictorService;


        public PredictorController(IPredictorService predictorService)
        {
            _predictorService = predictorService;
        }

        [HttpPost("predict")]
        public IActionResult PredictGame([FromBody] PredictRequest request)
        {
            var result = _predictorService.Predict(request.HomeTeam, request.AwayTeam);
            return Ok(result);
        }

    }
}
