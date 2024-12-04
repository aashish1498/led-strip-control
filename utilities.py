from apa102_pi.driver import apa102
import time
from config import NUM_LEDS_TOTAL, CORNER_LED_POSITIONS, GLOBAL_BRIGHTNESS

strip = apa102.APA102(num_led=NUM_LEDS_TOTAL, order="rgb")
my_cycle = None


def run_rainbow_circle():
    set_rainbow_pixels(GLOBAL_BRIGHTNESS, 0.005)
    time.sleep(2)
    rainbow_fade_out()


def rainbow_fade_out():
    for brightness in range(GLOBAL_BRIGHTNESS, 0, -1):
        set_rainbow_pixels(brightness, 0)
        strip.show()
        time.sleep(0.002)
    clear()


def solid(hex_code: str):
    (r, g, b) = hex_to_rgb(hex_code)
    for led in range(0, NUM_LEDS_TOTAL):
        strip.set_pixel(led, r, g, b, GLOBAL_BRIGHTNESS)
    strip.show()


def pulse_direction(direction: int, num_pulses: int = 1):
    if direction < 0 or direction > 3:
        raise ValueError("Direction must be between 0 and 3.")

    buffer = 2

    for _ in range(num_pulses):
        for i in range(CORNER_LED_POSITIONS[direction] + buffer, CORNER_LED_POSITIONS[direction + 1] - buffer):
            strip.set_pixel(i, 156, 255, 250, GLOBAL_BRIGHTNESS)
        strip.show()
        time.sleep(0.1)
        strip.clear_strip()


def set_rainbow_pixels(brightness: int = GLOBAL_BRIGHTNESS, pause_seconds: float = 0):
    scale_factor = 255 / NUM_LEDS_TOTAL
    for i in range(NUM_LEDS_TOTAL):
        scaled_index = int(i * scale_factor)
        pixel_color = strip.wheel(scaled_index)
        strip.set_pixel_rgb(i, pixel_color, brightness)
        if pause_seconds > 0:
            strip.show()
            time.sleep(pause_seconds)


def clear():
    if my_cycle is not None:
        my_cycle.stop()
    strip.clear_strip()


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
