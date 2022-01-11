import matplotlib.pyplot as plt
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

def init_plot(obstacles, path_point_x, path_point_y, source, goal):
    axes = parser['Plot Axes']
    plt.axis([int(axes['x_start']), 
        int(axes['x_end']),
        int(axes['y_start']),
        int(axes['y_end'])])
    
    plot_obstacles(obstacles)
    plot_path_points(path_point_x, path_point_y, source, goal)
    # plt.pause(0.5)
    plt.show()

def plot_path_points(path_point_x, path_point_y, source, goal):
    plt.plot(path_point_x, path_point_y, "k.")
    plt.plot(source[0], source[1], "bo")
    plt.plot(goal[0], goal[1], "go")

def plot_obstacles(obstacles):
    
    for obstacle in obstacles:
        x_values, y_values = [], []

        for vertex in obstacle:
            x_values.append(vertex[0])
            y_values.append(vertex[1])
        
        plt.fill(x_values, y_values, 'r')