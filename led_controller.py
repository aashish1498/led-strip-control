from apa102_pi.driver import apa102
import time
from config import NUM_LEDS_TOTAL, CORNER_LED_POSITIONS, GLOBAL_BRIGHTNESS
import logging
import asyncio
from app_state import Status
from utilities.led_utils import (
    enhance_rgb_color,
    hex_to_rgb,
    rainbow_colour_from_index,
    red_amber_green_from_index,
    exponential_map,
)

scale_factor = 255 / NUM_LEDS_TOTAL
sleep_step = 0.1


class LedController:
    strip = apa102.APA102(num_led=NUM_LEDS_TOTAL, order="rgb")
    status: Status
    current_task: asyncio.Task = None

    def __init__(self):
        self.status = Status.RUNNING

    def set_task(self, task: asyncio.Task):
        self.cancel_task()
        self.current_task = task

    def cancel_task(self):
        if self.current_task is not None:
            self.current_task.cancel()
        self.clear()

    def clear(self, reset_status: bool = False):
        self.strip.clear_strip()
        if reset_status:
            self.status = Status.CLEARED

    async def run_rainbow_circle(self):
        self.status = Status.RUNNING
        await self.set_circular_pixels(
            GLOBAL_BRIGHTNESS, 0.005, color_selector=rainbow_colour_from_index
        )
        await self.safe_sleep(2)
        await self.rainbow_fade_out()

    async def rainbow_fade_out(self):
        for brightness in range(GLOBAL_BRIGHTNESS, 0, -1):
            await self.set_circular_pixels(
                brightness, 0, color_selector=rainbow_colour_from_index
            )
            self.strip.show()
            await self.safe_sleep(0.002)
        self.clear()

    def solid(self, hex_code: str):
        (r, g, b) = hex_to_rgb(hex_code)
        (r_mod, g_mod, b_mod) = enhance_rgb_color(r, g, b)
        logging.debug(f"Original: {r}, {g}, {b}. Enhanced: {r_mod}, {g_mod}, {b_mod}.")
        for led in range(0, NUM_LEDS_TOTAL):
            self.strip.set_pixel(led, r_mod, g_mod, b_mod, GLOBAL_BRIGHTNESS)
        self.strip.show()

    async def flash_direction(self, direction: int, num_flashes: int = 1):
        self.status = Status.RUNNING
        if direction < 0 or direction > 3:
            raise ValueError("Direction must be between 0 and 3.")
        logging.debug(f"Flashing direction {direction} {num_flashes} times.")
        buffer = 2
        for _ in range(num_flashes):
            for i in range(
                CORNER_LED_POSITIONS[direction] + buffer,
                CORNER_LED_POSITIONS[direction + 1] - buffer,
            ):
                self.strip.set_pixel(i, 156, 255, 250, GLOBAL_BRIGHTNESS)
            self.strip.show()
            await self.safe_sleep(0.1)
            self.strip.clear_strip()
            await self.safe_sleep(0.1)

    async def pulse(self, colours: list[str], pause_time_seconds: float):
        self.status = Status.RUNNING
        fade_time_seconds = pause_time_seconds * 0.8
        static_time_seconds = pause_time_seconds - fade_time_seconds
        while self.status is not Status.CLEARED:
            for i in range(len(colours)):
                if self.status is Status.CLEARED:
                    return
                colour = colours[i]
                next_colour = colours[(i + 1) % len(colours)]
                logging.debug(f"Pulsing from {colour} to {next_colour}.")
                await self.fade_between_colors(colour, next_colour, fade_time_seconds)
                await self.safe_sleep(static_time_seconds)
        self.clear()

    async def fade_between_colors(
        self, color_from: str, color_to: str, duration: float
    ):
        r_from, g_from, b_from = hex_to_rgb(color_from)
        r_to, g_to, b_to = hex_to_rgb(color_to)

        steps = int(duration * 20)
        step_duration = duration / steps

        for step in range(steps + 1):
            if self.status is Status.CLEARED:
                return

            r = exponential_map(step, 0, steps, r_from, r_to)
            g = exponential_map(step, 0, steps, g_from, g_to)
            b = exponential_map(step, 0, steps, b_from, b_to)
            for led in range(NUM_LEDS_TOTAL):
                self.strip.set_pixel(led, r, g, b, GLOBAL_BRIGHTNESS)

            self.strip.show()
            await self.safe_sleep(step_duration)

    async def set_circular_pixels(
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
                await self.safe_sleep(pause_seconds)

    async def set_percentage(self, percentage: float, flash: bool):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")

        leds_to_light = int(NUM_LEDS_TOTAL * (percentage / 100))
        await self.set_circular_pixels(
            GLOBAL_BRIGHTNESS,
            0.005,
            color_selector=red_amber_green_from_index,
            num_leds_to_light=leds_to_light,
        )

        buffer = 8
        if flash and leds_to_light > buffer:
            for _ in range(3):
                await self.safe_sleep(0.3)
                for i in range(leds_to_light, leds_to_light - buffer, -1):
                    self.set_pixel_brightness(i, 0)
                self.strip.show()
                await self.safe_sleep(0.3)
                for i in range(leds_to_light, leds_to_light - buffer, -1):
                    self.set_pixel_brightness(i, GLOBAL_BRIGHTNESS)
                self.strip.show()
            await self.set_circular_pixels(
                brightness=0,
                pause_seconds=0.005,
                color_selector=red_amber_green_from_index,
                num_leds_to_light=leds_to_light,
            )

    def set_pixel_brightness(self, led_num: int, brightness: int):
        self.strip.set_pixel_rgb(
            led_num, self.strip.get_pixel_rgb(led_num)["rgb_color"], brightness
        )

    async def safe_sleep(self, sleep_seconds: float):
        if sleep_seconds <= sleep_step:
            await asyncio.sleep(sleep_seconds)
            return
        current_time = 0
        while current_time < sleep_seconds:
            if self.status is Status.CLEARED:
                return
            await asyncio.sleep(sleep_step)
            current_time += sleep_step
