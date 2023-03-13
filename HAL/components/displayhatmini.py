import os
import pygame
from HAL.hal import *


try:
    from displayhatmini import DisplayHATMini as Dhm
except ImportError:
    # Set up dummy classes for developing without a RPi and hat.
    print("FAILED TO IMPORT DisplayHATMini, mocking...")

    class ST7789:
        def __init__(self):
            pass

        def set_window(self):
            pass

        def data(self, data):
            pygame.display.flip()

    class Dhm:
        def __init__(self, param):
            self.screen = pygame.display.set_mode((320, 240))
            self.st7789 = ST7789()


class DisplayHATMini(HALComponent):
    """
        Pins:
        Led r 17
        Led g 27
        Led b 22
        swa 5
        swb 6
        swx 16
        swy 24
    """
    _screen = None

    def __init__(self, assets):
        super(HALComponent, self).__init__()
        self._dhm = Dhm(None)
        self._init_display()

        self._screen.fill((0, 0, 0))
        self._updatefb()

        self._running = False

        self.i = 0
        self._assets_folder = assets
        self._background = pygame.image.load(f"{self._assets_folder}/background.png").convert()
        # self._font = pygame.font.SysFont(pygame.font.get_default_font(), 50)

    def _init_display(self):
        os.putenv('SDL_VIDEODRIVER', 'dummy')
        pygame.display.init()  # Need to init for .convert() to work
        pygame.font.init()
        self._screen = pygame.Surface((640, 480))

    def _updatefb(self):
        self._dhm.st7789.set_window()
        # Grab the pygame screen as a bytes object
        pixelbytes = pygame.transform.rotate(self._screen, 180).convert(16, 0).get_buffer()
        # Lazy (slow) byteswap:
        pixelbytes = bytearray(pixelbytes)
        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
        for i in range(0, len(pixelbytes), 4096):
            self._dhm.st7789.data(pixelbytes[i:i + 4096])

    def refresh(self, hal):
        # TODO: Draw everything in the screen buffer
        self._screen.blit(self._background, (0, 0))
        # img = self._font.render('hello', True, (255, 255, 255))
        # self._screen.blit(pygame.transform.rotate(img, 90), (img.get_width()/2, img.get_height()/2))
        self._dhm.screen.blit(self._screen, (0, 0))
        # Draw the demo effect
        self._updatefb()
