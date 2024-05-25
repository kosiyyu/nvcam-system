using Microsoft.AspNetCore.Mvc;
using Models;
using Microsoft.IdentityModel.Tokens;
using Services;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Dto;

namespace Controller;

[ApiController]
[Route("api/")]
public class AuthController : ControllerBase
{
    private readonly UserService _userService;

    public AuthController(UserService userService)
    {
        _userService = userService;
    }

    [HttpPost("authenticate")]
    public async Task<IActionResult> Authentication(UserSimplified userSimplified)
    {   
        var fetchedUser = await _userService.GetAsync(userSimplified.Email);

        if(fetchedUser == null)
        {
            return Unauthorized();
        }

        if(!(userSimplified.Email == fetchedUser.Email && userSimplified.Password == fetchedUser.Password))
        {
            return Unauthorized();
        }

        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(EnvSettings.JwtKey));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        var claims = new List<Claim>
        {
            new Claim(ClaimTypes.NameIdentifier, fetchedUser.Id.ToString()),
            new Claim(ClaimTypes.Name, fetchedUser.Name)
        };

        var Sectoken = new JwtSecurityToken(
            issuer: EnvSettings.JwtIssuer,
            audience: EnvSettings.JwtIssuer,
            claims: claims,
            expires: DateTime.Now.AddMinutes(5),
            signingCredentials: credentials
        );

        var token =  new JwtSecurityTokenHandler().WriteToken(Sectoken);

        return Ok(token);
    }

    [Authorize]
    [HttpGet("validate")]
    public IActionResult ValidateBearer()
    {
        var userIdClaim = User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.NameIdentifier);
        var userNameClaim = User.Claims.FirstOrDefault(c => c.Type == ClaimTypes.Name);
  
        if (userIdClaim != null && userNameClaim != null)
        {
            return Ok();
        }

        return Unauthorized();
    }
}