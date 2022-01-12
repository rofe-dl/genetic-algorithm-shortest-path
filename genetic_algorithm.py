import math
from config.config_parser import parser
from random import randint

from shapely.geometry import Polygon, LineString

from plotter import init_plot

def start(obstacles, path_points):
    population = _generate_population(path_points, obstacles)
    init_plot(obstacles, path_points, population, True)

def _mutation(chromosome):
    pass

def _fitness(chromosome, path_points):
    path_point_1, path_point_2 = (), ()
    last_path_point = ()
    fitness = 0

    for i, gene in enumerate(chromosome):
        if gene == '1':
            last_path_point = path_points[i]

            if not path_point_1:
                path_point_1 = path_points[i] 
            else:
                path_point_2 = path_points[i]

            if path_point_1 and path_point_2:

                fitness += _distance(path_point_1, path_point_2)

                path_point_1 = path_point_2
                path_point_2 = ()

    fitness = 1 / fitness

    if chromosome[-1] == '1':
        # if last path point is the goal, add a fixed 0.3 to fitness
        fitness += 0.3
    else:
        # else increase the fitness depending on the distance left to the goal
        fitness += 1 / _distance(path_points[-1], last_path_point)

    return fitness


def _sort_by_fitness():
    pass

def _choose_parents():
    pass

def _crossover():
    pass

def _generate_population(path_points, obstacles):

    population_size = int(parser['Genetic Algorithm']['population_size'])

    population = []

    for i in range(population_size):
        while True:

            chromosome = _generate_chromosome(path_points)

            if _chromosome_valid(chromosome, obstacles, path_points):
                population.append(chromosome)
                print(_fitness(chromosome, path_points))
                break

    return population

def _generate_chromosome(path_points):

    chromosome = '1' # source is always visited, so do it outside loop
    for i in range(len(path_points) - 1):
        chromosome += '0' if randint(1, 10) > 5 else '1'
    
    return chromosome

def _chromosome_valid(chromosome, obstacles, path_points):
    path_point_1, path_point_2 = (), ()

    for i, gene in enumerate(chromosome):
        if gene == '1':

            if not path_point_1:
                path_point_1 = path_points[i] 
            else:
                path_point_2 = path_points[i]

            if path_point_1 and path_point_2:

                if _path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
                    return False

                path_point_1 = path_point_2
                path_point_2 = ()
    
    return True

def _path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
    path = LineString([path_point_1, path_point_2])

    for obstacle in obstacles:

        obstacle = Polygon(obstacle)
        if path.intersects(obstacle):
            return True

    return False


def _distance(path_point_1, path_point_2):
    return math.sqrt( (path_point_2[0] - path_point_1[0])**2 + (path_point_2[0] - path_point_1[1])**2 )