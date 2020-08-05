from constants import *


class Base:
    """
    Base object (ground)
    """

    IMG = BASE_IMG  # image of floor
    WIDTH = BASE_IMG.get_width()  # width of floor image
    VEL = ENV_VEL  # velocity to move at


    def __init__(self, y):
        """
        Initialise base object (ground)
        :param y: y coordinate of ground
        """

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self) -> None:
        """
        Move the two images
        :return: None
        """

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # If the left image is completely out of screen,
        # move it to the right of the second image.
        # Simulates a infinite loop of the ground
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, window) -> None:
        """
        Draw the images of the grounds
        :param window: pygame window
        :return: None
        """

        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))
