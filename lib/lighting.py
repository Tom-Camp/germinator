from lib.neopixel import Neopixel


class Lighting:
    def __init__(self, count: int, pin: int):
        self.status: bool = False
        self.pixel_count = count
        self.pixels = Neopixel(
            num_leds=self.pixel_count,
            state_machine=0,
            pin=pin,
            mode="GRB",
        )
        self.pixels.brightness(240)

    def turn_on_all(self, profile: list) -> None:
        if not isinstance(profile, list):
            profile = [(255, 0, 0)]
        profile_count: int = 0
        for pix in range(self.pixel_count - 1):
            self.pixels.set_pixel(pix, profile[profile_count])
            profile_count += 1
            profile_count = profile_count if profile_count < len(profile) else 0
        self.pixels.show()
        self.status = True

    def sun_position(self, rows_lit: int, row_size: int, profile: list) -> None:
        if not isinstance(profile, list):
            profile = [(255, 0, 0)]
        lit_pixels = rows_lit * row_size
        profile_count = 0
        for pix in range(self.pixel_count):
            if pix < lit_pixels:
                self.pixels.set_pixel(pix, profile[profile_count])
                profile_count += 1
                if profile_count >= len(profile):
                    profile_count = 0
            else:
                self.pixels.set_pixel(pix, (0, 0, 0))
        self.pixels.show()
        self.status = rows_lit > 0

    def turn_off(self) -> None:
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        self.status = False
