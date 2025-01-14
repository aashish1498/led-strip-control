from pydantic import BaseModel, Field


class PercentageRequest(BaseModel):
    percentage: float
    flashing: bool = True


class SolidRequest(BaseModel):
    hex_code: str = Field(description="A list of hex codes for the colours to pulse through", examples=["#FF0000", "#00FF00", "#0000FF"])


class PulseRequest(BaseModel):
    colours: list[str] = Field(description="A list of hex codes for the colours to pulse through", examples=[["#FF00A6", "#00C8FF", "#0000FF"]])
    pause_time_seconds: float = 1
