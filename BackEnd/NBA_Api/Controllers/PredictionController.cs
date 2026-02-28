using Microsoft.AspNetCore.Mvc;
using NBA_Api.DTOs;
using System.Diagnostics;
using System.Text.Json;

namespace NBA_Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PredictionController : ControllerBase
    {
        private readonly IConfiguration _config;
        private readonly ILogger<PredictionController> _logger;
        private readonly IWebHostEnvironment _env;

        public PredictionController(IConfiguration config, ILogger<PredictionController> logger, IWebHostEnvironment env)
        {
            _config = config;
            _logger = logger;
            _env = env;
        }

        [HttpPost("predict")]
        public IActionResult Predict([FromBody] PredictRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.HomeTeam) || string.IsNullOrWhiteSpace(request.AwayTeam))
                return BadRequest("Both teams must be provided.");

            if (request.HomeTeam.Trim().Equals(request.AwayTeam.Trim(), StringComparison.OrdinalIgnoreCase))
                return BadRequest("Home and away teams must be different.");

            var pythonPath = _config["PythonSettings:PythonPath"] ?? "python";
            var predictorScript = _config["PythonSettings:PredictorScriptPath"] ?? "";

            _logger.LogInformation("=== PREDICTION DEBUG ===");
            _logger.LogInformation("PythonPath: '{Python}'", pythonPath);
            _logger.LogInformation("PredictorScriptPath from config: '{Script}'", predictorScript);
            _logger.LogInformation("File exists: {Exists}", System.IO.File.Exists(predictorScript));
            _logger.LogInformation("Teams: '{Home}' vs '{Away}'", request.HomeTeam, request.AwayTeam);

            if (!System.IO.File.Exists(predictorScript))
            {
                _logger.LogError("Script not found at: '{Path}'", predictorScript);
                return StatusCode(500, $"Script not found at: {predictorScript}");
            }

            var psi = new ProcessStartInfo
            {
                FileName = pythonPath,
                Arguments = $"\"{predictorScript}\" \"{request.HomeTeam}\" \"{request.AwayTeam}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                WorkingDirectory = Path.GetDirectoryName(predictorScript)!
            };

            _logger.LogInformation("Running: {Python} {Args}", pythonPath, psi.Arguments);

            try
            {
                using var process = Process.Start(psi)!;
                string output = process.StandardOutput.ReadToEnd();
                string errors = process.StandardError.ReadToEnd();
                process.WaitForExit();

                _logger.LogInformation("Exit code: {Code}", process.ExitCode);
                _logger.LogInformation("Output: '{Output}'", output);
                if (!string.IsNullOrEmpty(errors))
                    _logger.LogError("Stderr: '{Errors}'", errors);

                if (process.ExitCode != 0 || string.IsNullOrWhiteSpace(output))
                    return StatusCode(500, $"Python exited {process.ExitCode}. Stderr: {errors}");

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(output);

                if (result != null && result.TryGetValue("error", out var errVal))
                    return BadRequest(errVal?.ToString());

                return Ok(result);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception while running predictor");
                return StatusCode(500, ex.Message);
            }
        }
    }
}