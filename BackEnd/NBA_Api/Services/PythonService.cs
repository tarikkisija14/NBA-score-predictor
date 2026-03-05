using System.Diagnostics;

namespace NBA_Api.Services
{
   
    public partial class PythonService
    {
        private readonly string _pythonPath;
        private readonly string _scriptPath;
        private readonly ILogger<PythonService> _logger;
        private readonly IWebHostEnvironment _env;

       
        private const int TimeoutMs = 45_000;

        
        private const int MaxRetries = 2;

        public PythonService(
            IConfiguration config,
            ILogger<PythonService> logger,
            IWebHostEnvironment env)
        {
            _logger = logger;
            _env = env;

            _pythonPath = config["PythonSettings:PythonPath"] ?? "python";

            var rawPath = config["PythonSettings:FetchDataScriptPath"] ?? "fetch_data.py";
            _scriptPath = Path.IsPathRooted(rawPath)
                ? rawPath
                : Path.GetFullPath(Path.Combine(_env.ContentRootPath, rawPath));
        }

        
        public string? RunFetchData(string scriptType)
        {
            if (!File.Exists(_scriptPath))
            {
                _logger.LogError(
                    "fetch_data script not found at: {Path}", _scriptPath);
                return null;
            }

            for (int attempt = 1; attempt <= MaxRetries; attempt++)
            {
                _logger.LogInformation(
                    "Running fetch_data ({Type}), attempt {Attempt}/{Max}",
                    scriptType, attempt, MaxRetries);

                var result = RunProcess(_pythonPath, $"\"{_scriptPath}\" {scriptType}",
                                        Path.GetDirectoryName(_scriptPath)!);

                if (result.Success)
                    return result.Output;

                
                if (result.IsTimeout)
                {
                    _logger.LogWarning(
                        "fetch_data ({Type}) timed out on attempt {Attempt}. " +
                        "NBA API may be slow.", scriptType, attempt);
                }
                else if (result.IsRateLimit)
                {
                    _logger.LogWarning(
                        "NBA API rate-limit hit on attempt {Attempt}. " +
                        "Waiting 5s before retry...", attempt);
                    Thread.Sleep(5_000);
                }
                else
                {
                    
                    _logger.LogError(
                        "fetch_data ({Type}) failed: {Error}", scriptType, result.ErrorOutput);
                    return null;
                }
            }

            _logger.LogError(
                "fetch_data ({Type}) failed after {Max} attempts.", scriptType, MaxRetries);
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
                WorkingDirectory = workingDir
            };

            try
            {
                using var process = new Process { StartInfo = psi };
                process.Start();

               
                var outputTask = process.StandardOutput.ReadToEndAsync();
                var errorTask = process.StandardError.ReadToEndAsync();

                bool finished = process.WaitForExit(TimeoutMs);

                string output = outputTask.Result;
                string errors = errorTask.Result;

                if (!finished)
                {
                    try { process.Kill(entireProcessTree: true); } catch { /* ignore */ }
                    return ProcessResult.Timeout();
                }

                if (!string.IsNullOrEmpty(errors))
                    _logger.LogDebug("Python stderr: {Err}", errors);

                if (process.ExitCode != 0 || string.IsNullOrWhiteSpace(output))
                {
                    bool rateLimit = errors.Contains("429") ||
                                     errors.Contains("Too Many Requests") ||
                                     errors.Contains("rate limit", StringComparison.OrdinalIgnoreCase);
                    return ProcessResult.Failure(errors, rateLimit);
                }

                return ProcessResult.Ok(output);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception running Python process");
                return ProcessResult.Failure(ex.Message, false);
            }
        }
    }
}