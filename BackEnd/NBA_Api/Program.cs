using NBA_Api;
using NBA_Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddSingleton<PythonService>();

builder.Services.AddHttpClient(AppConstants.PredictApiClientName, client =>
{
    client.Timeout = AppConstants.PredictApiTimeout;
});

builder.Services.AddCors(options =>
{
    options.AddPolicy(AppConstants.CorsPolicyName, policy =>
    {
        var allowedOrigins = builder.Configuration
            .GetSection("AllowedOrigins")
            .Get<string[]>()
            ?? ["http://localhost:4200", "https://localhost:4200"];

        policy
            .WithOrigins(allowedOrigins)
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials();
    });
});

var app = builder.Build();

app.UseRouting();
app.UseCors(AppConstants.CorsPolicyName);

if (app.Environment.IsDevelopment())
    app.MapOpenApi();

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

WarmCacheInBackground(app);

app.Run();


static void WarmCacheInBackground(WebApplication app)
{
    var pythonService = app.Services.GetRequiredService<PythonService>();
    var logger = app.Services.GetRequiredService<ILogger<Program>>();

    foreach (var scriptType in AppConstants.CacheWarmupScriptTypes)
    {
        var type = scriptType; 
        Task.Run(() =>
        {
            logger.LogInformation("Cache warm-up starting: {Type}", type);
            var result = pythonService.RunFetchData(type);
            if (result is not null)
                logger.LogInformation("Cache warm-up done: {Type}", type);
            else
                logger.LogWarning("Cache warm-up failed: {Type}", type);
        });
    }
}