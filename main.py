from fastapi import FastAPI
from fastapi.responses import JSONResponse
import threading
from utilities import run_rainbow_circle, pulse_direction, clear

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3001)
