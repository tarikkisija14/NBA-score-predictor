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
            _pytonpath = config["Python:path"] ?? "python";
            _scriptpath = config["Python:FetchDataScript"]?? "PythonScripts/fetch_data.py";
        }
        public string RunFetchData(string command)
        {
            var psi = new ProcessStartInfo
            {
                FileName = _pytonpath,
                Arguments = $"{_scriptpath}{command}",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            
            using var process=Process.Start(psi);
            if(process == null)
            {
                return string.Empty;
            }

            using var reader = process.StandardOutput;
            string result=reader.ReadToEnd();

            process.WaitForExit();
            return result;

        }


    }
}
