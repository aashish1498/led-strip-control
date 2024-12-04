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

    Expects a JSON body with a 'color' key and a valid hex code.
    """
    body = await request.json()
    color = body.get("color")

    if color is None:
        raise HTTPException(status_code=400, detail="Missing 'color' key.")

    if not re.match(r"^#[0-9A-Fa-f]{6}$", color):
        raise HTTPException(status_code=400, detail="Invalid hex color code.")

    threading.Thread(target=solid(color)).start()
    return JSONResponse(content={"message": "Solid color set."})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
