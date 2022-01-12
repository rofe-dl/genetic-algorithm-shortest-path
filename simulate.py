# import matplotlib.pyplot as plt
# from configparser import ConfigParser
from random import randint

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from config.config_parser import parser
from utils.obstacle_generator import generate_obstacles
from utils.path_point_generator import generate_path_points
import genetic_algorithm

obstacles = []
path_points = []

# obstacle within axis range, no overlap between obstacles
# without link probabilities, slower but more dynamic
# obstacle count low so low chance of overlap
# problem of path point being very close to obstacle, so minus plus it out
# credit author and say what we did differently
# repair chromosome if not valid as improvement
# check only nearest polygons for overlapping as improvement
# first and last index of path_points is the source and goal
# randomizing obstacles as improvement
# had to prevent mutating source and goal genes
# source on very left, goal on very right
# obstacle not too close to each other
# importance of scaling each thing
# obstacles too close to wall, so  box them in

def main():
    _init_obstacles()
    _init_path_points()

    genetic_algorithm.start(obstacles, path_points)
    
def _init_path_points():

    if parser['Path Points'].getboolean('generate_randomly'):
        generate_path_points(path_points, obstacles)

    else:

        path_points.append(eval(parser['Hardcoded Path Points']['source']))

        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_points.append(element)

        path_points.append(eval(parser['Hardcoded Path Points']['goal']))

def _init_obstacles():

    if parser['Obstacles'].getboolean('generate_randomly'):
        number_of_obstacles = int(parser['Obstacles']['number_of_obstacles'])
        generate_obstacles(obstacles, number_of_obstacles)

    else:
        for i in range(int(parser['Hardcoded Obstacles']['number_of_hardcoded_obstacles'])):
            obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
            obstacles.append(obstacle)

if __name__ == '__main__':
    
    main()