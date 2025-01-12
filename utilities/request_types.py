from pydantic import BaseModel


class PercentageRequest(BaseModel):
    percentage: float
    flashing: bool = True


class SolidRequest(BaseModel):
    hex_code: str


class FlashRequest(BaseModel):
    direction: int
    number_of_flashes: int = 1


class PulseRequest(BaseModel):
    colours: list[str]
    pause_time_seconds: float = 1
