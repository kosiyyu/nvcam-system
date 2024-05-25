using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Controllers;

[ApiController]
[Route("")]
public class DefaultController : ControllerBase
{

    [HttpGet]
    public IActionResult HelloWorld() 
    {
        return Ok("Service is running!");
    }
}