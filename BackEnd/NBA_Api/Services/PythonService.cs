using System.Diagnostics;

namespace NBA_Api.Services
{
  
    public partial class PythonService
    {
        private readonly string _pythonPath;
        private readonly string _scriptPath;
        private readonly ILogger<PythonService> _logger;

        public PythonService(
            IConfiguration config,
            ILogger<PythonService> logger,
            IWebHostEnvironment env)
        {
            _logger = logger;

            _pythonPath = config["PythonSettings:PythonPath"] ?? "python";

            var rawScriptPath = config["PythonSettings:FetchDataScriptPath"] ?? "fetch_data.py";
            _scriptPath = Path.IsPathRooted(rawScriptPath)
                ? rawScriptPath
                : Path.GetFullPath(Path.Combine(env.ContentRootPath, rawScriptPath));
        }

      
        public string? RunFetchData(string scriptType)
        {
            if (!File.Exists(_scriptPath))
            {
                _logger.LogError("fetch_data script not found at: {Path}", _scriptPath);
                return null;
            }

            for (int attempt = 1; attempt <= AppConstants.PythonMaxRetries; attempt++)
            {
                _logger.LogInformation(
                    "Running fetch_data ({Type}), attempt {Attempt}/{Max}",
                    scriptType, attempt, AppConstants.PythonMaxRetries);

                var result = RunProcess(
                    _pythonPath,
                    $"\"{_scriptPath}\" {scriptType}",
                    workingDir: Path.GetDirectoryName(_scriptPath)!);

                if (result.Success)
                    return result.Output;

                if (result.IsTimeout)
                {
                    _logger.LogWarning(
                        "fetch_data ({Type}) timed out on attempt {Attempt}. NBA API may be slow.",
                        scriptType, attempt);
                }
                else if (result.IsRateLimit)
                {
                    _logger.LogWarning(
                        "NBA API rate-limit hit on attempt {Attempt}. Waiting {Delay}ms before retry...",
                        attempt, AppConstants.RateLimitRetryDelayMs);
                    Thread.Sleep(AppConstants.RateLimitRetryDelayMs);
                }
                else
                {
                    _logger.LogError(
                        "fetch_data ({Type}) failed: {Error}", scriptType, result.ErrorOutput);
                    return null;
                }
            }

            _logger.LogError(
                "fetch_data ({Type}) failed after {Max} attempts.",
                scriptType, AppConstants.PythonMaxRetries);
            return null;
        }

        
        private ProcessResult RunProcess(string fileName, string arguments, string workingDir)
        {
            var psi = new ProcessStartInfo
            {
                FileName = fileName,
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                WorkingDirectory = workingDir,
            };

            try
            {
                using var process = new Process { StartInfo = psi };
                process.Start();

                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();

                bool finished = process.WaitForExit(AppConstants.PythonTimeoutMs);

                string output = outputTask.Result;
                string errors = errorTask.Result;

                if (!finished)
                {
                    TryKillProcess(process);
                    return ProcessResult.Timeout();
                }

                if (!string.IsNullOrEmpty(errors))
                    _logger.LogDebug("Python stderr: {Err}", errors);

                if (process.ExitCode != 0 || string.IsNullOrWhiteSpace(output))
                {
                    bool isRateLimit = IsRateLimitError(errors);
                    return ProcessResult.Failure(errors, isRateLimit);
                }

                return ProcessResult.Ok(output);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception running Python process");
                return ProcessResult.Failure(ex.Message, rateLimit: false);
            }
        }

        private static void TryKillProcess(Process process)
        {
            try { process.Kill(entireProcessTree: true); }
            catch { /* best-effort */ }
        }

        private static bool IsRateLimitError(string errorOutput) =>
            AppConstants.RateLimitKeywords.Any(
                kw => errorOutput.Contains(kw, StringComparison.OrdinalIgnoreCase));
    }
}