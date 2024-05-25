using Microsoft.CodeAnalysis;
using Microsoft.Extensions.Options;
using Models;
using MongoDB.Driver;
using Settings;

namespace Services;

public class UserService
{
    private readonly IMongoCollection<User> _userColletion;

    public UserService(IOptions<MongoDBSettings> mongoDbSettings)
    {
        var client = new MongoClient(mongoDbSettings.Value.ConnectionURI);
        var database = client.GetDatabase(mongoDbSettings.Value.DatabaseName);
        _userColletion = database.GetCollection<User>("User");
    }

    public async Task CreateAsync(User user)
    {
        await _userColletion.InsertOneAsync(user);
    }

    public async Task DeleteAsync(string id)
    {
        var filter = Builders<User>.Filter.Eq("Id", id);
        await _userColletion.DeleteOneAsync(filter);
    }

    public async Task<User> GetAsync(string email)
    {
        var filter = Builders<User>.Filter.Eq("Email", email);
        var user = await _userColletion.Find(filter).FirstOrDefaultAsync();
        return user;
    }
}