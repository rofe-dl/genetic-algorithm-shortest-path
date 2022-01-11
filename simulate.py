# import matplotlib.pyplot as plt
from configparser import ConfigParser
from random import randint

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from plotter import init_plot

parser = ConfigParser()
parser.read('config.ini')

obstacles = []
path_point_x = []
path_point_y = []
source = []
goal = []

# random obstacles
# obstacle within axis range, no overlap between obstacles
# path points not in obstacles
# obstacle count low so low chance of overlap

def main():
    init_obstacles()
    init_path_points()

    init_plot(obstacles, path_point_x, path_point_y, source, goal)
    

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
    

def init_path_points():
    
    axes = parser['Plot Axes']

    if parser['Path Points'].getboolean('generate_randomly'):
        source_x = int(axes['x_start']) + 1
        source_y = randint(int(axes['y_start']), int(axes['y_end']))

        goal_x = int(axes['x_end']) - 1
        goal_y = randint(int(axes['y_start']), int(axes['y_end']))

        number_of_pathpoints = int(parser['Path Points']['number_of_pathpoints'])
        for i in range(number_of_pathpoints):
            path_point = generate_path_point()
            path_point_x.append(path_point[0])
            path_point_y.append(path_point[1])

    else:
        source_x = eval(parser['Hardcoded Path Points']['source'])[0] + 1
        source_y = eval(parser['Hardcoded Path Points']['source'])[1]

        goal_x = eval(parser['Hardcoded Path Points']['goal'])[0] - 1
        goal_y = eval(parser['Hardcoded Path Points']['goal'])[1]

        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_point_x.append(element[0])
            path_point_y.append(element[1])

    source.extend([source_x, source_y])
    goal.extend([goal_x, goal_y])


def generate_path_point():
    axes = parser['Plot Axes']

    while True:
        x = randint( int(axes['x_start'])+1, int(axes['x_end']) )
        y = randint( int(axes['y_start'])+1, int(axes['y_end']) )
        
        if not path_point_in_obstacle(x, y):
            return (x, y)

def path_point_in_obstacle(x, y):
    point = Point(x, y)
    
    for obstacle in obstacles:
        obstacle = Polygon(obstacle)

        if obstacle.contains(point):
            return True
    
    return False

def init_obstacles():

    for i in range(int(parser['Obstacles']['number_of_obstacles'])):
        obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
        obstacles.append(obstacle)

if __name__ == '__main__':
    
    main()