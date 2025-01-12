from apa102_pi.driver import apa102
import time
from config import NUM_LEDS_TOTAL, CORNER_LED_POSITIONS, GLOBAL_BRIGHTNESS
import logging
import asyncio
from app_state import Status
from utilities.led_utils import hex_to_rgb, rainbow_colour_from_index, red_amber_green_from_index

scale_factor = 255 / NUM_LEDS_TOTAL

class LedController():
    strip = apa102.APA102(num_led=NUM_LEDS_TOTAL, order="rgb")
    status: Status
    
    def __init__(self):
        self.status = Status.RUNNING
        
    def clear(self):
        self.strip.clear_strip()
        self.status = Status.CLEARED


    def run_rainbow_circle(self):
        self.set_circular_pixels(GLOBAL_BRIGHTNESS, 0.005, color_selector=rainbow_colour_from_index)
        time.sleep(2)
        self.rainbow_fade_out()


    def rainbow_fade_out(self):
        for brightness in range(GLOBAL_BRIGHTNESS, 0, -1):
            self.set_circular_pixels(brightness, 0, color_selector=rainbow_colour_from_index)
            self.strip.show()
            time.sleep(0.002)
        self.clear()


    def solid(self, hex_code: str):
        (r, g, b) = hex_to_rgb(hex_code)
        logging.debug(f"Setting solid color to: {r}, {g}, {b} (from hex: {hex_code})")
        for led in range(0, NUM_LEDS_TOTAL):
            self.strip.set_pixel(led, r, g, b, GLOBAL_BRIGHTNESS)
        self.strip.show()


    def flash_direction(self, direction: int, num_flashes: int = 1):
        if direction < 0 or direction > 3:
            raise ValueError("Direction must be between 0 and 3.")

        buffer = 2
        for _ in range(num_flashes):
            for i in range(
                CORNER_LED_POSITIONS[direction] + buffer,
                CORNER_LED_POSITIONS[direction + 1] - buffer,
            ):
                self.strip.set_pixel(i, 156, 255, 250, GLOBAL_BRIGHTNESS)
            self.strip.show()
            time.sleep(0.1)
            self.strip.clear_strip()


    async def pulse(self, colours: list[str], pause_time_seconds: str):
        self.status = Status.RUNNING
        while self.status is not Status.CLEARED:
            for colour in colours:
                self.solid(colour)
                asyncio.sleep(pause_time_seconds)


    def set_circular_pixels(
        self,
        brightness: int = GLOBAL_BRIGHTNESS,
        pause_seconds: float = 0,
        color_selector=rainbow_colour_from_index,
        num_leds_to_light=NUM_LEDS_TOTAL,
    ):
        for i in range(num_leds_to_light):
            pixel_color = color_selector(i)
            self.strip.set_pixel_rgb(i, pixel_color, brightness)
            if pause_seconds > 0:
                self.strip.show()
                time.sleep(pause_seconds)


    def set_percentage(self, percentage: float, flash: bool):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        leds_to_light = int(NUM_LEDS_TOTAL * (percentage / 100))
        self.set_circular_pixels(
            GLOBAL_BRIGHTNESS, 0.005, color_selector=red_amber_green_from_index, num_leds_to_light=leds_to_light
        )

        buffer = 8
        if flash and leds_to_light > buffer:
            for _ in range(3):
                time.sleep(0.3)
                for i in range(leds_to_light, leds_to_light - buffer, -1):
                    self.set_pixel_brightness(i, 0)
                self.strip.show()
                time.sleep(0.3)
                for i in range(leds_to_light, leds_to_light - buffer, -1):
                    self.set_pixel_brightness(i, GLOBAL_BRIGHTNESS)
                self.strip.show()
            self.set_circular_pixels(
                brightness=0,
                pause_seconds=0.005,
                color_selector=red_amber_green_from_index,
                num_leds_to_light=leds_to_light,
            )


    def set_pixel_brightness(self, led_num: int, brightness: int):
        self.strip.set_pixel_rgb(led_num, self.strip.get_pixel_rgb(led_num)["rgb_color"], brightness)
