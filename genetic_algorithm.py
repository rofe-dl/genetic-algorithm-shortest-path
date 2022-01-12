import math
from config_parser import parser
from random import randint

from shapely.geometry import Polygon, LineString

from plotter import init_plot

def start(obstacles, path_points, source, goal):
    population = _generate_population(path_points, source, goal, obstacles)

    init_plot(obstacles, path_points, source, goal, population)

def _mutation():
    pass

def _fitness():
    pass

def _sort_by_fitness():
    pass

def _choose_parents():
    pass

def _crossover():
    pass

def _generate_population(path_points, source, goal, obstacles):

    population_size = int(parser['Genetic Algorithm']['population_size'])

    population = []

    for i in range(population_size):
        while True:

            chromosome = _generate_chromosome(path_points)

            if _chromosome_valid(chromosome, obstacles, path_points):
                # add the source and goal separately afterwards
                chromosome = '1' + chromosome + '0' if randint(1, 10) > 5 else '1'
                population.append(chromosome)
                break

    return population

def _generate_chromosome(path_points):

    chromosome = ''
    for i in range(len(path_points)):
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

            if path_point_1 and path_point_2 and _path_overlaps_obstacle(path_point_1, path_point_2, obstacles):
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