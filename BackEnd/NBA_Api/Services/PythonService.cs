using System.Diagnostics;
using System.Runtime.CompilerServices;

namespace NBA_Api.Services
{
    public class PythonService
    {
        private readonly string _pytonpath;
        private readonly string _scriptpath;

        public PythonService(IConfiguration config)
        {
            _pytonpath = config["PythonSettings:PythonPath"] ?? "python";
            _scriptpath = config["PythonSettings:ScriptPath"] ?? "PythonScripts/fetch_data.py";
        }
        public string RunFetchData(string command)
        {
            var psi = new ProcessStartInfo
            {
                FileName = _pytonpath,
                Arguments = $"\"{_scriptpath}\" {command}",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardError = true,
            };
            
            using var process=Process.Start(psi);
            if(process == null)
            {
                return string.Empty;
            }

            string result = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            process.WaitForExit();

            if (!string.IsNullOrEmpty(error))
            {
                return $"ERROR: {error}";
            }

            return result;

        }


    }
}
