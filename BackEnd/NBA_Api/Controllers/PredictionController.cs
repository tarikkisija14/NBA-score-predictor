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
        [HttpPost("predict")]
        public IActionResult Predict([FromBody] PredictRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.HomeTeam) || string.IsNullOrWhiteSpace(request.AwayTeam))
            {
                return BadRequest("Both teams must be provided");
            }

            var psi = new ProcessStartInfo
            {
                FileName = @"C:\Users\tarik\AppData\Local\Programs\Python\Python313\python.exe",
                Arguments = $"\"C:\\Users\\tarik\\Desktop\\nba score predictor\\AI Model\\scripts\\Predictor.py\" \"{request.HomeTeam}\" \"{request.AwayTeam}\"",

                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };

            try
            {
                using var process = Process.Start(psi);
                string output = process.StandardOutput.ReadToEnd();
                string errors = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(errors))
                {

                    Debug.WriteLine($"Python Error: {errors}");
                    return StatusCode(500, errors);
                }
                Debug.WriteLine($"Python Output: {output}");
                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(output);
                return Ok(result);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Exception: {ex.Message}");
                return StatusCode(500, ex.Message);
            }
        }
    }
}
