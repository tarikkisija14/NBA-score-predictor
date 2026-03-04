using NBA_Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddSingleton<PythonService>();

builder.Services.AddCors(options => {
    options.AddPolicy("AllowAngular", policy =>
    {
        // Origins are read from appsettings.json ("AllowedOrigins" array).
        // This avoids hardcoding localhost so the app works in production too.
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
app.UseCors("AllowAngular");

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();