import matplotlib.pyplot as plt
from configparser import ConfigParser
from random import randint

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

parser = ConfigParser()
parser.read('./config.ini')
obstacles = []

# random obstacles
# obstacle within axis range, no overlap between obstacles
# path points not in obstacles
# obstacle count low so low chance of overlap

def main():
    axes = parser['Plot Axes']
    plt.axis([int(axes['x_start']), 
        int(axes['x_end']),
        int(axes['y_start']),
        int(axes['y_end'])])

    plot_obstacles()
    plot_path_points()
    plt.show()

def plot():

    flag = True

    for i in range (5):

        plt.clf()
        plot_obstacles()
        plot_path_points()
        
        if flag:
            plt.plot([3, 5], [2, 6], '-')
        else:
            plt.plot([3, 6], [2, 7], '-')

        plt.pause(0.5)

        flag = not flag

    plt.show()
    

def plot_path_points():
    node_x = []
    node_y = []

    if parser['Path Points'].getboolean('generate_randomly'):
        number_of_pathpoints = int(parser['Path Points']['number_of_pathpoints'])
        for i in range(number_of_pathpoints):
            path_point = generate_path_point()
            node_x.append(path_point[0])
            node_y.append(path_point[1])

    else:
        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            node_x.append(element[0])
            node_y.append(element[1])

    plt.plot(node_x, node_y, "k.")

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

def plot_obstacles():

    obs_1_x = [2.5, 3.5, 3.5, 2.5, 2.5]
    obs_1_y = [9, 9, 12, 12, 9]
    plt.fill(obs_1_x, obs_1_y, "r")
    obstacles.append([(2.5, 9), (3.5, 9), (3.5, 12), (2.5, 12)])

    obs_2_x = [3, 4, 4, 3, 3]
    obs_2_y = [6.5, 6.5, 4, 4, 6.5]
    plt.fill(obs_2_x, obs_2_y, "r")
    obstacles.append([(3, 6.5), (4, 6.5), (4, 4), (3, 4)])

    obs_3_x = [7, 9, 9, 7, 7]
    obs_3_y = [12, 12, 13, 13, 12]
    plt.fill(obs_3_x, obs_3_y, "r")
    obstacles.append([(7, 12), (9, 12), (9, 13), (7, 13)])

def generate_obstacle():
    pass

if __name__ == '__main__':
    
    main()