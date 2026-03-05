namespace NBA_Api.Services
{
public partial class PythonService
    {
        private record ProcessResult(
            bool Success,
            string Output,
            string ErrorOutput,
            bool IsTimeout,
            bool IsRateLimit)
        {
            public static ProcessResult Ok(string output)
                => new(true, output, "", false, false);

            public static ProcessResult Timeout()
                => new(false, "", "Process timed out", true, false);

            public static ProcessResult Failure(string error, bool rateLimit)
                => new(false, "", error, false, rateLimit);
        }
    }
}