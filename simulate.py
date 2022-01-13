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
