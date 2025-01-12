from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import threading
from config import SERVICE_PORT
import re
from led_controller import clear, flash_direction, pulse, run_rainbow_circle, set_percentage, solid
from utilities.request_types import PercentageRequest, PulseRequest, SolidRequest

app = FastAPI()


@app.get("/api/circle")
async def api_circle():
    """Trigger the rainbow circle."""
    threading.Thread(target=run_rainbow_circle).start()
    return JSONResponse(content={"message": "Circle effect started."})


@app.get("/api/flash-direction")
async def api_flash(direction: int, number_of_flashes: int):
    """Flashes the LED strip in a given direction.

    Args:
        direction (int): 0: bottom, 1: left, 2: top, 3: right
    """
    threading.Thread(target=flash_direction(direction, number_of_flashes)).start()
    return JSONResponse(content={"message": "Flashing."})


@app.get("/api/pulse")
async def api_pulse(request: PulseRequest):
    """Pulses the LED strip between given colours.
    """
    cleaned_colors = []
    for color in request.colours:
        cleaned_colors.append(clean_and_validate_hex(color))

    threading.Thread(target=pulse(cleaned_colors, request.pause_time_seconds)).start()
    return JSONResponse(content={"message": "Pulsing."})


@app.get("/api/clear")
async def api_clear():
    """Clears the strip."""
    clear()
    return JSONResponse(content={"message": "Clearing."})


@app.post("/api/solid")
async def api_solid(request: SolidRequest):
    """Sets the LED strip to a solid colour."""
    hex_code = clean_and_validate_hex(request.hex_code)
    threading.Thread(target=solid(hex_code)).start()
    return JSONResponse(content={"message": "Solid colour set."})


@app.post("/api/percentage")
async def api_circle(request: PercentageRequest):
    """Set the LED to a red-amber-green based percentage."""
    threading.Thread(target=set_percentage(request.percentage, request.flashing)).start()
    return JSONResponse(content={"message": "Percentage started effect started."})


def clean_and_validate_hex(hex_code: str) -> str:
    hex_code = hex_code.lstrip('#')
    if not re.match(r"^[0-9A-Fa-f]{6}$", hex_code):
        raise HTTPException(status_code=400, detail="Invalid hex colour code. Example: F5A9B8")
    return hex_code

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
