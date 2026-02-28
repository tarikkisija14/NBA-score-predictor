using System.Diagnostics;

namespace NBA_Api.Services
{
    public class PythonService
    {
        private readonly string _pythonPath;
        private readonly string _scriptPath;
        private readonly ILogger<PythonService> _logger;
        private readonly IWebHostEnvironment _env;

        public PythonService(IConfiguration config, ILogger<PythonService> logger, IWebHostEnvironment env)
        {
            _pythonPath = config["PythonSettings:PythonPath"] ?? "python";
            _logger = logger;
            _env = env;

            
            var rawPath = config["PythonSettings:FetchDataScriptPath"] ?? "fetch_data.py";
            _scriptPath = Path.IsPathRooted(rawPath)
                ? rawPath
                : Path.GetFullPath(Path.Combine(_env.ContentRootPath, rawPath));
        }

        public string? RunFetchData(string scriptType)
        {
            if (!File.Exists(_scriptPath))
            {
                _logger.LogError("fetch_data script not found at: {Path}", _scriptPath);
                return null;
            }

            var psi = new ProcessStartInfo
            {
                FileName = _pythonPath,
                Arguments = $"\"{_scriptPath}\" {scriptType}",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                
                WorkingDirectory = Path.GetDirectoryName(_scriptPath)!
            };

            try
            {
                using var process = new Process { StartInfo = psi };
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(error))
                    _logger.LogError("Python fetch_data stderr: {Error}", error);

                if (process.ExitCode != 0 || string.IsNullOrWhiteSpace(output))
                    return null;

                return output;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception running fetch_data script");
                return null;
            }
        }
    }
}