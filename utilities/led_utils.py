from apa102_pi.driver import apa102
from config import NUM_LEDS_TOTAL

default_strip = apa102.APA102()
my_cycle = None
rgb_scale_factor = 255 / NUM_LEDS_TOTAL
percentage_scale_factor = 100 / NUM_LEDS_TOTAL


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


def rainbow_colour_from_index(index: int) -> tuple[int, int, int]:
    scaled_index = int(index * rgb_scale_factor)
    return default_strip.wheel(scaled_index)


def red_amber_green_from_index(index: int) -> any:
    scaled_index = int(index * percentage_scale_factor)
    green_value = exponential_map(scaled_index)
    red_value = 255 - green_value
    return default_strip.combine_color(red_value, green_value, 0)


def exponential_map(
    value, input_min=0, input_max=100, output_min=0, output_max=255, exponent=2
) -> int:
    normalized = (value - input_min) / (input_max - input_min)
    exp_value = normalized**exponent
    mapped_value = output_min + (exp_value * (output_max - output_min))
    return int(mapped_value)

def enhance_channel(value, gamma=0.8):
    normalized = value / 255.0
    enhanced = pow(normalized, gamma)
    return min(max(int(enhanced * 255), 0), 255)

def enhance_rgb_color(r, g, b, gamma=0.8):
    return enhance_channel(r, gamma), enhance_channel(g, gamma), enhance_channel(b, gamma)
