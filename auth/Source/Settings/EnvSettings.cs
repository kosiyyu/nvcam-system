using DotNetEnv;

public static class EnvSettings
{
    public static readonly string MongoUsername;
    public static readonly string MongoPassword;
    public static readonly string MongoDatabaseName;
    public static readonly string JwtKey;
    public static readonly string JwtIssuer;

    static EnvSettings()
    {
        Env.Load("../.env");

        MongoUsername = GetRequiredEnvironmentVariable("MONGO_INITDB_ROOT_USERNAME");
        MongoPassword = GetRequiredEnvironmentVariable("MONGO_INITDB_ROOT_PASSWORD");
        MongoDatabaseName = GetRequiredEnvironmentVariable("MONGO_DB_NAME");
        JwtKey = GetRequiredEnvironmentVariable("JWT_KEY");
        JwtIssuer = GetRequiredEnvironmentVariable("JWT_ISSUER");
    }

    private static string GetRequiredEnvironmentVariable(string variableName)
    {
        string value = Environment.GetEnvironmentVariable(variableName);
        if (string.IsNullOrEmpty(value))
        {
            throw new InvalidOperationException($"Missing required environment variable: {variableName}");
        }
        return value;
    }
}
