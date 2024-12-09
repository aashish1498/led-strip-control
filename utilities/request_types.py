from pydantic import BaseModel


class PercentageRequest(BaseModel):
    percentage: float
    flashing: bool = True


class SolidRequest(BaseModel):
    hex_code: str
