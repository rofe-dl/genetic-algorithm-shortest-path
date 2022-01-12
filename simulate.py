# import matplotlib.pyplot as plt
# from configparser import ConfigParser
from random import randint

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from config_parser import parser
import genetic_algorithm

obstacles = []
path_points = []
source = ()
goal = ()

# obstacle within axis range, no overlap between obstacles
# without link probabilities, slower but more dynamic
# obstacle count low so low chance of overlap
# show length of the path and legend on the plot
# reward chromosome for reaching the goal
# problem of path point being very close to obstacle, so minus plus it out
# credit author and say what we did differently
# reward chromosome for reaching the goal
# repair chromosome if not valid as improvement
# check only nearest polygons for overlapping as improvement

def main():
    _init_obstacles()
    _init_path_points()

    genetic_algorithm.start(obstacles, path_points, source, goal)
    

# def plot():

#     flag = True

#     for i in range (5):

#         plt.clf()
#         plot_obstacles()
#         plot_path_points()
        
#         if flag:
#             plt.plot([3, 5], [2, 6], '-')
#         else:
#             plt.plot([3, 6], [2, 7], '-')

#         plt.pause(0.5)

#         flag = not flag

#     plt.show()
    

def _init_path_points():
    
    axes = parser['Plot Axes']

    if parser['Path Points'].getboolean('generate_randomly'):
        source_x = int(axes['x_start']) + 1
        source_y = randint(int(axes['y_start']), int(axes['y_end']))

        goal_x = int(axes['x_end']) - 1
        goal_y = randint(int(axes['y_start']), int(axes['y_end']))

        number_of_path_points = int(parser['Path Points']['number_of_path_points'])
        for i in range(number_of_path_points):
            path_points.append(_generate_path_point())

    else:
        source_x = eval(parser['Hardcoded Path Points']['source'])[0]
        source_y = eval(parser['Hardcoded Path Points']['source'])[1]

        goal_x = eval(parser['Hardcoded Path Points']['goal'])[0]
        goal_y = eval(parser['Hardcoded Path Points']['goal'])[1]

        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_points.append(element)

    global source, goal
    source = (source_x, source_y)
    goal = (goal_x, goal_y)


def _generate_path_point():
    axes = parser['Plot Axes']

    while True:
        x = randint( int(axes['x_start'])+1, int(axes['x_end'])-1 )
        y = randint( int(axes['y_start'])+1, int(axes['y_end'])-1 )
        
        if not _path_point_in_obstacle(x, y):
            return (x, y)

def _path_point_in_obstacle(x, y):
    point = Point(x, y)
    
    for obstacle in obstacles:
        obstacle = Polygon(obstacle)

        if obstacle.contains(point):
            return True
    
    return False

def _init_obstacles():

    for i in range(int(parser['Obstacles']['number_of_obstacles'])):
        obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
        obstacles.append(obstacle)

if __name__ == '__main__':
    
    main()