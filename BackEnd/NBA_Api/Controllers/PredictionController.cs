using Microsoft.AspNetCore.Mvc;
using NBA_Api.DTOs;
using System.Net.Http;
using System.Text;
using System.Text.Json;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PredictionController : ControllerBase
    {
        private readonly IHttpClientFactory _httpFactory;
        private readonly IConfiguration _config;
        private readonly ILogger<PredictionController> _logger;

        public PredictionController(
            IHttpClientFactory httpFactory,
            IConfiguration config,
            ILogger<PredictionController> logger)
        {
            _httpFactory = httpFactory;
            _config = config;
            _logger = logger;
        }

        [HttpPost("predict")]
        public async Task<IActionResult> Predict([FromBody] PredictRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.HomeTeam) ||
                string.IsNullOrWhiteSpace(request.AwayTeam))
                return BadRequest("Both teams must be provided.");

            if (request.HomeTeam.Trim().Equals(
                    request.AwayTeam.Trim(), StringComparison.OrdinalIgnoreCase))
                return BadRequest("Home and away teams must be different.");

            
            var fastApiUrl = _config["PythonSettings:PredictApiUrl"]
                             ?? "http://127.0.0.1:8000";

            var payload = JsonSerializer.Serialize(new
            {
                home_team = request.HomeTeam.Trim(),
                away_team = request.AwayTeam.Trim()
            });

            _logger.LogInformation(
                "Sending prediction request to FastAPI: {Home} vs {Away}",
                request.HomeTeam, request.AwayTeam);

            try
            {
                var client = _httpFactory.CreateClient("PredictApi");
                var content = new StringContent(payload, Encoding.UTF8, "application/json");
                var response = await client.PostAsync($"{fastApiUrl}/predict", content);

                var body = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                {
                    _logger.LogWarning(
                        "FastAPI returned {Status}: {Body}",
                        (int)response.StatusCode, body);

                    
                    if (response.StatusCode == System.Net.HttpStatusCode.BadRequest)
                        return BadRequest(body);

                    return StatusCode(502, "Prediction service returned an error.");
                }

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(body);
                return Ok(result);
            }
            catch (HttpRequestException ex)
            {
                _logger.LogError(ex, "Could not reach FastAPI prediction service.");
                return StatusCode(503,
                    "Prediction service is unavailable. " +
                    "Make sure predict_api.py is running on port 8000.");
            }
            catch (TaskCanceledException)
            {
                _logger.LogError("FastAPI prediction request timed out.");
                return StatusCode(504, "Prediction timed out. Please try again.");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error during prediction.");
                return StatusCode(500, "An unexpected error occurred.");
            }
        }
    }
}