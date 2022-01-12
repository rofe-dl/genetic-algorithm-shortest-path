# import matplotlib.pyplot as plt
# from configparser import ConfigParser
from random import randint

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from config.config_parser import parser
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

def main():
    _init_obstacles()
    _init_path_points()

    genetic_algorithm.start(obstacles, path_points)
    
def _init_path_points():
    
    axes = parser['Plot Axes']

    if parser['Path Points'].getboolean('generate_randomly'):
        source_x = int(axes['x_start']) + 1
        source_y = randint(int(axes['y_start']), int(axes['y_end']))
        path_points.append((source_x, source_y))

        goal_x = int(axes['x_end']) - 1
        goal_y = randint(int(axes['y_start']), int(axes['y_end']))

        number_of_path_points = int(parser['Path Points']['number_of_path_points'])
        for i in range(number_of_path_points):
            path_points.append(_generate_path_point())

        path_points.append((goal_x, goal_y))

    else:

        path_points.append(eval(parser['Hardcoded Path Points']['source']))

        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_points.append(element)

        path_points.append(eval(parser['Hardcoded Path Points']['goal']))


def _generate_path_point():
    axes = parser['Plot Axes']

    while True:
        x = randint( int(axes['x_start'])+1, int(axes['x_end'])-1 )
        y = randint( int(axes['y_start'])+1, int(axes['y_end'])-1 )
        
        if not _path_point_near_obstacle(x, y):
            return (x, y)

def _path_point_near_obstacle(x, y):
    point = Point(x, y)

    # forms a radius of 1 around the point to check if point is near any obstacle
    circle_perimeter = point.buffer(1).boundary
    
    for obstacle in obstacles:
        obstacle = Polygon(obstacle)

        if circle_perimeter.intersection(obstacle):
            return True
    
    return False

def _init_obstacles():

    for i in range(int(parser['Obstacles']['number_of_obstacles'])):
        obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
        obstacles.append(obstacle)

if __name__ == '__main__':
    
    main()