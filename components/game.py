import neat  # !! this refers to `neat_python` not `neat` !! #

from components.constants import *
from components.bird import Bird
from components.pipe import Pipe
from components.base import Base


MIN_JUMP_THRESHOLD = 0.5  # minimum output value from neural network to jump


class Game:
    """
    Game object
    """


    def __init__(self, draw_lines=True):
        """
        Initialise the game object
        :param draw_lines: defines whether to draw lines from bird to pipe, defaults to True
        """

        self.draw_lines = draw_lines

        self.score = 0
        self.max_score = 0

        self.gen = 0
        self.clock = pygame.time.Clock()

        self.nets = []  # brains list
        self.ge = []  # genomes list
        self.birds = []  # birds list
        # these 3 lists have corresponding indexes

        self.pipes = [Pipe(WIN_WIDTH)]
        self.base = Base(FLOOR_HEIGHT)

        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


    def reset(self) -> None:
        """
        Resets game to prepare for a generation
        :return: None
        """

        self.score = 0

        self.gen += 1

        self.nets = []  # brains list
        self.ge = []  # genomes list
        self.birds = []  # birds list
        # these 3 lists have corresponding indexes

        self.pipes = [Pipe(WIN_WIDTH)]
        self.base = Base(FLOOR_HEIGHT)


    def should_quit(self, events) -> bool:
        """
        Determines if we should quit the game
        :param events: pygame events
        :return: whether to quit game
        """

        for event in events:
            if event.type == pygame.QUIT:
                return True

        return False


    def draw_window(self, pipe_ind) -> None:
        """
        Draw window with all the elements
        :param pipe_ind: index of upcoming pipe in self.pipes
        :return: None
        """

        # background
        self.window.blit(BG_IMG, (0, 0))

        # pipes
        for pipe in self.pipes:
            pipe.draw(self.window)

        # base
        self.base.draw(self.window)

        # draw lines from bird to pipe
        for bird in self.birds:
            if self.draw_lines:
                try:
                    LINE_THICKNESS = 1
                    # line to left corners of pipes
                    pygame.draw.line(self.window, (255, 0, 100),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                     (self.pipes[pipe_ind].x, self.pipes[pipe_ind].height),
                                     LINE_THICKNESS)
                    pygame.draw.line(self.window, (255, 0, 100),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                     (self.pipes[pipe_ind].x, self.pipes[pipe_ind].y_bottom),
                                     LINE_THICKNESS)

                    # line to right corners of pipes
                    pygame.draw.line(self.window, (255, 100, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                     (self.pipes[pipe_ind].x + self.pipes[pipe_ind].PIPE_TOP_IMG.get_width(),
                                      self.pipes[pipe_ind].height),
                                     LINE_THICKNESS)
                    pygame.draw.line(self.window, (255, 100, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                     (self.pipes[pipe_ind].x + self.pipes[pipe_ind].PIPE_BOTTOM_IMG.get_width(),
                                      self.pipes[pipe_ind].y_bottom),
                                     LINE_THICKNESS)
                except:
                    pass

            # birds
            bird.draw(self.window)

        # score and max_score
        score_text = STAT_FONT.render('Score: ' + str(self.score), 1, (255, 255, 255))
        max_score_text = STAT_FONT.render('Max: ' + str(self.max_score), 1, (255, 255, 255))
        self.window.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))
        self.window.blit(max_score_text, (WIN_WIDTH - 10 - max_score_text.get_width(), 50))

        # generation
        score_label = STAT_FONT.render("Gen: " + str(self.gen), 1, (255, 255, 255))
        self.window.blit(score_label, (10, 10))

        # alive
        score_label = STAT_FONT.render("Alive: " + str(len(self.birds)), 1, (255, 255, 255))
        self.window.blit(score_label, (10, 50))

        pygame.display.update()


    def init_birds(self, genomes, config) -> None:
        """
        Initialise birds, genomes, neural networks
        :param genomes: genomes
        :param config: nn config
        :return: None
        """

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            self.nets.append(net)
            self.ge.append(genome)
            self.birds.append(Bird(230, 350))


    def kill_bird(self, i, decrease_fitness=True) -> None:
        """
        Kill a bird at index i and decrease fitness if necessary
        :param i: index of bird
        :param decrease_fitness: whether to decrease fitness
        :return: None
        """

        if decrease_fitness:
            self.ge[i].fitness -= 3

        # remove birds from lists
        self.birds.pop(i)
        self.nets.pop(i)
        self.ge.pop(i)


    def increase_fitness(self) -> None:
        """
        Increase fitness of all birds alive
        :return: None
        """

        for genome in self.ge:
            genome.fitness += 5


    def make_birds_jump(self, pipe_ind) -> None:
        """
        Make birds jump based on output from neural network
        :param pipe_ind: index of upcoming pipe
        :return: None
        """

        for (i, bird) in enumerate(self.birds):
            self.ge[i].fitness += 1
            bird.move()

            output = self.nets[i].activate((
                bird.y,
                abs(bird.y - self.pipes[pipe_ind].y_bottom),
                abs(bird.y - self.pipes[pipe_ind].height),
                abs(bird.x - self.pipes[pipe_ind].x),
                abs(bird.x - self.pipes[pipe_ind].x - self.pipes[pipe_ind].PIPE_BOTTOM_IMG.get_width())
            ))

            # if output value is more than the min threshold to jump, jump
            if output[0] > MIN_JUMP_THRESHOLD:
                bird.jump()


    def get_pipe_ind(self) -> int:
        """
        Get the index of the upcoming pipe
        :return: index of upcoming pipe
        """

        pipe_ind = 0
        if len(self.birds) > 0 and len(self.pipes) > 1 and self.birds[0].x + self.pipes[0].PIPE_TOP_IMG.get_width():
            pipe_ind = 1

        return pipe_ind


    def add_score_and_update_fitness(self):
        self.score += 1

        if self.max_score < self.score:
            self.max_score = self.score

        self.increase_fitness()
        self.pipes.append(Pipe(WIN_WIDTH))


    def move_pipes_and_collision_detection(self) -> list:
        """
        Move pipes and perform collision detection with birds.
        :return: if pipe has passed, list of pipes to remove
        """

        removed_pipes = []
        passed_pipe = False

        for pipe in self.pipes:
            pipe.move()

            # collision detection with pipe
            for (i, bird) in enumerate(self.birds):
                if pipe.collide(bird):
                    self.kill_bird(i, decrease_fitness=True)

            if not pipe.passed and pipe.x + pipe.PIPE_TOP_IMG.get_width() < bird.x:
                pipe.passed = True

                if not passed_pipe:
                    passed_pipe = True

            if pipe.x + pipe.PIPE_TOP_IMG.get_width() < 0:
                # pipe is offscreen, remove this pipe
                removed_pipes.append(pipe)

        if passed_pipe:
            self.add_score_and_update_fitness()

        return removed_pipes


    def update_birds(self) -> None:
        """
        Kill birds that are touching the ceiling or the floor
        :return: None
        """

        for (i, bird) in enumerate(self.birds):
            if bird.y + bird.img.get_height() - 10 >= FLOOR_HEIGHT or bird.y < -50:
                self.kill_bird(i, decrease_fitness=True)


    def update_pipes_and_score(self, removed_pipes) -> None:
        """
        Remove pipes that are offscreen
        :param removed_pipes: list of pipes to be removed
        :return: None
        """

        for removed in removed_pipes:
            self.pipes.remove(removed)


    def start(self, genomes, config) -> None:
        """
        Initialise and start game
        :param genomes: genomes
        :param config: nn config
        :return: None
        """

        self.init_birds(genomes, config)
        self.game()


    def quit_game(self) -> None:
        """
        Quit game
        :return: None
        """

        print('Max score reached:', self.max_score)
        pygame.quit()
        quit()


    def game(self) -> None:
        """
        Start game
        :return: None
        """

        run = True
        while run and len(self.birds) > 0:
            self.clock.tick(30)

            if self.should_quit(pygame.event.get()):
                run = False
                self.quit_game()
                break

            # move ground
            self.base.move()

            # get appropriate pipe index depending on position of pipes
            pipe_ind = self.get_pipe_ind()

            # make birds jump
            self.make_birds_jump(pipe_ind)

            # move pipes and determine if birds have collided with pipe
            removed_pipes = self.move_pipes_and_collision_detection()

            # remove birds that have hit the ground or ceiling
            self.update_birds()

            # update pipes list and score
            self.update_pipes_and_score(removed_pipes)

            # re-render window
            self.draw_window(pipe_ind)

        self.reset()
