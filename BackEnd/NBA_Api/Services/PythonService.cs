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
            //path to python exe
            _pythonPath = config["PythonSettings:PythonPath"];
            //path to the python script
            _scriptPath = config["PythonSettings:ScriptPath"];
        }
        public string RunFetchData(string scriptType)
        {
            try
            {
                if (!File.Exists(_scriptPath))
                {
                    Debug.WriteLine($" Script not found at {_scriptPath}");
                    return null;
                }
                //set up process info to run python script
                var psi = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = $"\"{_scriptPath}\" {scriptType}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                //start python process
                using var process = new Process { StartInfo = psi };
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();


                if (!string.IsNullOrEmpty(error))
                {
                    Debug.WriteLine($" Python Error:\n{error}");
                    return null;
                }

                Debug.WriteLine($" Script output ({output.Length} chars)");
                //return json result as string
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
