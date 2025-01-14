from pydantic import BaseModel


class PercentageRequest(BaseModel):
    percentage: float
    flashing: bool = True


class SolidRequest(BaseModel):
    hex_code: str


class PulseRequest(BaseModel):
    colours: list[str]
    pause_time_seconds: float = 1
