from apa102_pi.driver import apa102
from config import NUM_LEDS_TOTAL

default_strip = apa102.APA102()
my_cycle = None
scale_factor = 255 / NUM_LEDS_TOTAL


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


def rainbow_colour_from_index(index: int) -> tuple[int, int, int]:
    scaled_index = int(index * scale_factor)
    return default_strip.wheel(scaled_index)


def red_amber_green_from_index(index: int) -> tuple[int, int, int]:
    scaled_index = int(index * scale_factor)
    if scaled_index < 50:
        return (255, 0, 0)
    if 50 <= scaled_index < 85:
        return (255, 255, 0)
    return (0, 255, 0)
