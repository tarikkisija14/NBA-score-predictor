namespace NBA_Api
{
    
    internal static class AppConstants
    {
       
        
        public const int PythonTimeoutMs = 240_000;

      
        public const int PythonMaxRetries = 2;

       
        public const int RateLimitRetryDelayMs = 5_000;

       
        
        public const string PredictApiClientName = "PredictApi";

        
        public static readonly TimeSpan PredictApiTimeout = TimeSpan.FromSeconds(10);

        
        public const string CorsPolicyName = "AllowAngular";

     
       
        public static readonly IReadOnlyList<string> CacheWarmupScriptTypes =
            ["standings", "league_leaders", "team_leaders", "scores"];

       
        public static readonly IReadOnlyList<string> RateLimitKeywords =
            ["429", "Too Many Requests", "rate limit"];
    }
}