using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Models;
using Services;

namespace Controllers;

[ApiController]
[Route("api")]
public class UserController : ControllerBase
{
    private readonly UserService _userService;

    public UserController(UserService userService)
    {
        _userService = userService;
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register(User user) 
    {   
        try
        {
            await _userService.CreateAsync(user);
            return Ok();
        }
        catch (Exception e) 
        {
            Console.WriteLine(e);
            return StatusCode(500, "An error occurred while registering the user.");
        }
    }
}