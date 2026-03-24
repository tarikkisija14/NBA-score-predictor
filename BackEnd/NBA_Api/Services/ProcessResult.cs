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
                => new(true, output, string.Empty, IsTimeout: false, IsRateLimit: false);

            public static ProcessResult Timeout()
                => new(false, string.Empty, "Process timed out", IsTimeout: true, IsRateLimit: false);

            public static ProcessResult Failure(string error, bool rateLimit)
                => new(false, string.Empty, error, IsTimeout: false, IsRateLimit: rateLimit);
        }
    }
}