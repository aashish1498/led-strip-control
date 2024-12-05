from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import threading
from config import SERVICE_PORT
from utilities import run_rainbow_circle, pulse_direction, solid, clear
import re

app = FastAPI()


@app.get("/api/circle")
async def api_circle():
    """Trigger the rainbow circle."""
    threading.Thread(target=run_rainbow_circle).start()
    return JSONResponse(content={"message": "Circle effect started."})


@app.get("/api/pulse-direction")
async def api_pulse(direction: int):
    """Pulses the LED strip in a given direction.

    Args:
        direction (int): 0: bottom, 1: left, 2: top, 3: right
    """
    threading.Thread(target=pulse_direction(direction)).start()
    return JSONResponse(content={"message": "Pulsing."})


@app.get("/api/clear")
async def api_clear():
    """Clears the strip."""
    clear()
    return JSONResponse(content={"message": "Clearing."})


@app.post("/api/solid")
async def api_solid(request: Request):
    """Sets the LED strip to a solid color.

    Expects a JSON body with a 'color' key and a valid hex code (without hash).
    """

    body = retrieve_valid_body(request, ["color"])

    color = body.get("color")
    if not re.match(r"^[0-9A-Fa-f]{6}$", color):
        raise HTTPException(status_code=400, detail="Invalid hex color code. Example: F5A9B8")

    threading.Thread(target=solid(color)).start()
    return JSONResponse(content={"message": "Solid color set."})


async def retrieve_valid_body(request: Request, required_keys: list) -> dict:
    """Validates and retrieves the JSON body of a request."""
    body = None
    try:
        body = await request.json()
        for key in required_keys:
            if key not in body:
                raise HTTPException(status_code=400, detail=f"Missing '{key}' key.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON body.")
    return body


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
