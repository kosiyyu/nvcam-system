using DotNetEnv;

namespace Settings;

public class MongoDBSettings
{

    public string ConnectionURI { get; set; } = null!;
    public string DatabaseName { get; set; } = null!;

    public MongoDBSettings() 
    {
        Env.Load("../../../.env");

        var user = "root";
        var password = "password";
        var name = "Auth";

        // var user = Environment.GetEnvironmentVariable("MONGO_INITDB_ROOT_USERNAME");
        // var password = Environment.GetEnvironmentVariable("MONGO_INITDB_ROOT_PASSWORD");
        // var name = Environment.GetEnvironmentVariable("MONGO_DB_NAME");

        if (user == null || password == null || name == null)
        {
            Console.WriteLine("Failed to load environment variables.");
        }
        else
        {
            Console.WriteLine("Environment variables loaded successfully.");
        }

        var host = "localhost:27017";

        ConnectionURI = $"mongodb://{user}:{password}@{host}";
        // ConnectionURI = "mongodb://root:password@localhost:27017/";
        // Console.WriteLine(ConnectionURI);
        // Console.WriteLine($"mongodb://{user}:{password}@{host}");
        DatabaseName = name;
    }
}