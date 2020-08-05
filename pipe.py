import random

from constants import *


class Pipe:
    """
    Pipe object (top and bottom)
    """

    GAP = 200  # gap between top and bottom pipe
    VEL = ENV_VEL  # velocity at which the pipes move to the left


    def __init__(self, x):
        """
        Initialise pipes
        :param x: x coordinate of pipe
        """

        self.x = x

        self.height = 0  # y coordinate of bottom of top pipe

        self.y_top = 0  # y coordinate for top pipe
        self.y_bottom = 0  # y coordinate for bottom pipe

        self.PIPE_TOP_IMG = pygame.transform.flip(PIPE_IMG, False, True)  # image for top pipe
        self.PIPE_BOTTOM_IMG = PIPE_IMG  # image for bottom pipe

        self.passed = False
        self.set_height()


    def set_height(self) -> None:
        """
        Generate and set a random height for the gap
        :return: None
        """

        self.height = random.randrange(50, 450)  # get a random height for the gap

        self.y_top = self.height - self.PIPE_TOP_IMG.get_height()  # calculate top y coordinate of top pipe
        self.y_bottom = self.height + self.GAP


    def move(self) -> None:
        """
        Move the pipes
        :return: None
        """

        self.x -= self.VEL


    def draw(self, window) -> None:
        """
        Draw the pipes
        :param window: pygame window
        :return: None
        """

        window.blit(self.PIPE_TOP_IMG, (self.x, self.y_top))
        window.blit(self.PIPE_BOTTOM_IMG, (self.x, self.y_bottom))


    def collide(self, bird) -> bool:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP_IMG)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM_IMG)

        # coordinate offsets between top left corners of bird mask and pipe mask
        # using bird mask's coordinates as (0, 0), convert pipe coordinates to be relative to bird mask
        top_offset = (self.x - bird.x, self.y_top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.y_bottom - round(bird.y))

        top_collision_point = bird_mask.overlap(top_mask, top_offset)
        # get point of overlap between bird and tpp pipe masks,
        # returns None if no overlap

        bottom_collision_point = bird_mask.overlap(bottom_mask, bottom_offset)
        # get point of overlap between bird and bottom pipe masks,
        # returns None if no overlap

        return top_collision_point or bottom_collision_point
        # return if bird collides with pipe
