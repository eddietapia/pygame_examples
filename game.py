"""
File Name: game.py
Author: Eddie Tapia
Description: This file will be used to run a simple pygame tutorial
Date: May 17, 2017
"""
import pygame
from pygame.locals import *

class App:
    """
    Our main class to run our pygame example
    """
    def __init__(self):
        """ Will initialize all pygame modules needed to create main display window"""
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 900, 800

    def on_init(self):
        """
        Calls pygame.init() to initialize the pygame modules
        It creates the main display and tries to use hardware
        acceleration as well as sets _running to True
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        """Checks if quit event ever happened"""
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        """TODO"""
        pass
    def on_render(self):
        """TODO"""
        pass
    def on_cleanup(self):
        """Calls pygame.quit() that quits all pygame modules"""
        pygame.quit()

    def on_execute(self):
        """
        Initializes pygame then enters main loop by calling
        check events and then compute and render everything
        till _running is True and only quit event will set it
        to False. Before quitting, it will clean up
        """
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    # Create an instance of App
    my_app = App()
    # Call the app's on_execute functin
    my_app.on_execute()
