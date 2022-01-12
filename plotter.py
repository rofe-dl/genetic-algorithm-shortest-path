import matplotlib.pyplot as plt
from config.config_parser import parser

def init_plot(obstacles, path_points, population, path_lengths, gen, last_gen):
    axes = parser['Plot Axes']
    plt.axis([int(axes['x_start']), 
        int(axes['x_end']),
        int(axes['y_start']),
        int(axes['y_end'])])

    for i, chromosome in enumerate(population):
        plt.clf()
        plot_obstacles(obstacles)
        plot_path_points(path_points)
        
        path_x = [path_points[i][0] for i, c in enumerate(chromosome) if c == '1']
        path_y = [path_points[i][1] for i, c in enumerate(chromosome) if c == '1']

        plt.plot(path_x, path_y, '-')
        plt.text(1, 14, f"Generation: {gen}\nPath Length:{path_lengths[i]}")
        
        if last_gen:
            plt.show()
        else:
            plt.pause(0.25)

    
    
def plot_path_points(path_points):
    path_point_x = [path_point[0] for path_point in path_points]
    path_point_y = [path_point[1] for path_point in path_points]

    plt.plot(path_point_x[1:-1], path_point_y[1:-1], "k.")
    plt.plot(path_point_x[0], path_point_y[0], "bo", label='Source')
    plt.plot(path_point_x[-1], path_point_y[-1], "go", label='Goal')

def plot_obstacles(obstacles):
    
    for obstacle in obstacles:
        x_values, y_values = [], []

        for vertex in obstacle:
            x_values.append(vertex[0])
            y_values.append(vertex[1])
        
        plt.fill(x_values, y_values, 'r')