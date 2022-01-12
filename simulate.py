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
# source on very left, goal on very right
# obstacle not too close to each other
# importance of scaling each thing
# obstacles too close to wall, so  box them in

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

    if parser['Obstacles'].getboolean('generate_randomly'):
        number_of_obstacles = int(parser['Obstacles']['number_of_obstacles'])
        for i in range(number_of_obstacles):

            while True:
                obstacle = _generate_obstacle()

                if not _obstacle_near_obstacle(obstacle):
                    break

            obstacles.append(obstacle)

    else:
        for i in range(int(parser['Hardcoded Obstacles']['number_of_hardcoded_obstacles'])):
            obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
            obstacles.append(obstacle)

def _generate_obstacle():
    axes = parser['Plot Axes']
    x_start = int(axes['x_start'])
    x_end = int(axes['x_end'])
    y_start = int(axes['y_start'])
    y_end = int(axes['y_end'])

    max_width = int(parser['Obstacles']['max_width'])
    max_height = int(parser['Obstacles']['max_height'])

    point_x_1 = randint(x_start + 2, x_end - 2)
    point_y_1 = randint(y_start + 2, y_end - 2)

    width = randint(1, max_width)
    height = randint(1, max_height)

    point_x_2 = point_x_1 + width if point_x_1+width <= 0.75 * x_end else point_x_1 - width
    point_y_2 = point_y_1 + height if point_y_1+height <= 0.75 * y_end else point_y_1 - height

    return [(point_x_1, point_y_1), (point_x_2, point_y_1), (point_x_2, point_y_2), (point_x_1, point_y_2)]
    
def _obstacle_near_obstacle(obstacle):
    obstacle = Polygon(obstacle)

    for o in obstacles:
        o = Polygon(o)

        if o.intersects(obstacle):
            return True

    return False

if __name__ == '__main__':
    
    main()