using System.Diagnostics;
using System.Runtime.CompilerServices;

namespace NBA_Api.Services
{
    public class PythonService
    {
        private readonly string _pythonPath;
        private readonly string _scriptPath;

        public PythonService(IConfiguration config)
        {
            _pythonPath = config["PythonSettings:PythonPath"];
            _scriptPath = config["PythonSettings:ScriptPath"];
        }
        public string RunFetchData(string scriptType)
        {
            try
            {
                if (!File.Exists(_scriptPath))
                {
                    Console.WriteLine($" Script not found at {_scriptPath}");
                    return null;
                }

                var psi = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = $"\"{_scriptPath}\" {scriptType}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = new Process { StartInfo = psi };
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();


                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine($" Python Error:\n{error}");
                    return null;
                }

                Console.WriteLine($" Script output ({output.Length} chars)");
                return output;
            }
            catch (Exception ex)
            {
                Console.WriteLine($" Process Error: {ex}");
                return null;
            }
        }


    }
}
