import matplotlib.pyplot as plt
from config_parser import parser

def init_plot(obstacles, path_points, source, goal, population):
    axes = parser['Plot Axes']
    plt.axis([int(axes['x_start']), 
        int(axes['x_end']),
        int(axes['y_start']),
        int(axes['y_end'])])

    for chromosome in population:
        plt.clf()
        plot_obstacles(obstacles)
        plot_path_points(path_points, source, goal)
        
        path_x, path_y = [source[0]], [source[1]] # add the source separately
        
        path_x.extend([path_points[i][0] for i, c in enumerate(chromosome[1:-1]) if c == '1'])
        path_y.extend([path_points[i][1] for i, c in enumerate(chromosome[1:-1]) if c == '1'])

        if chromosome[-1] == '1':
            path_x.append(goal[0])
            path_y.append(goal[1])

        plt.plot(path_x, path_y, '-')

        plt.pause(2)

    plt.show()
    
def plot_path_points(path_points, source, goal):
    path_point_x = [path_point[0] for path_point in path_points]
    path_point_y = [path_point[1] for path_point in path_points]

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