import os
import neat  # !! this refers to `neat_python` not `neat` !! #

from components import Game


def run(config_path) -> None:
    """
    Set up NEAT config, create population and run the AI
    :param config_path: absolute path to config file
    :return: None
    """

    # set up config
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # create a new population
    population = neat.Population(config)

    # create stdout reporters
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # create new game
    game = Game()

    # run generations to evolve genome
    final = population.run(game.start, 100)

    # show stats of best genome
    print('Best genome:', final)


if __name__ == '__main__':
    # get absolute path to config file !IMPORTANT!
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config.txt')

    # run the AI
    run(config_path)
