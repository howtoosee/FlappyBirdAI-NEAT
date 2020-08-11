from components.constants import *


class Bird:
    """
    Bird object
    """

    IMGS = BIRD_IMGS  # list of images
    MAX_ROTATION = 25  # maximum tilt angle when in facing up
    ROT_VEL = 20  # rotation speed
    ANIMATION_TIME = 5  # time for each animation


    def __init__(self, x, y):
        """
        Initialise bird object
        :param x: initial x coordinate
        :param y: initial y coordinate
        """

        self.x = x
        self.y = y

        self.tilt = 0  # tilt degree, initially 0

        self.tick_count = 0  # tick count for physics, keeps track of when the bird last jumped
        self.vel = 0  # current velocity, initially 0
        self.height = self.y  # current height, initially at height y

        self.image_ind = 0  # keep track of image index
        self.img = self.IMGS[0]  # keep track of actual image

        self.genome = None  # genome
        self.network = None  # brain / neural network


    def jump(self) -> None:
        """
        Make the bird jump
        :return: None
        """

        self.vel = -9
        self.tick_count = 0
        self.height = self.y


    def move(self) -> None:
        """
        Move the bird by making it fall and tilting the image
        :return: None
        """

        self.tick_count += 1

        vel = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # failsafe for terminal velocity
        if vel >= 16:
            vel = 16

        if vel < 0:
            vel -= 2

        self.y = self.y + vel

        if vel < 0 or self.y < self.height + 50:
            # tilt upwards
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL


    def draw(self, window) -> None:
        """
        Draw the bird
        :param window: pygame window
        :return: None
        """

        self.image_ind += 1

        if self.image_ind < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.image_ind < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.image_ind < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.image_ind < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.image_ind == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.image_ind = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.image_ind = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)


    def get_mask(self) -> pygame.mask.Mask:
        """
        Get mask of bird for collision detection
        :return: pygame mask
        """

        return pygame.mask.from_surface(self.img)
