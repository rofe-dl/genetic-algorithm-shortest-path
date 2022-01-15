from config.config_parser import parser
from utils.obstacle_generator import generate_obstacles
from utils.path_point_generator import generate_path_points
from genetic_algorithm import start, path_overlaps_obstacle

obstacles = []
path_points = []
path_validity = dict()

def main():
    _init_obstacles()
    _init_path_points()

    _init_path_validity()

    start(obstacles, path_points, path_validity)
    
def _init_path_points():

    if parser['Path Points'].getboolean('generate_randomly'):
        generate_path_points(path_points, obstacles)

    else:
        # eval will create the list from the string representation of list in config.ini
        for element in eval(parser['Hardcoded Path Points']['path_points']):
            path_points.append(element)

def _init_obstacles():

    if parser['Obstacles'].getboolean('generate_randomly'):
        number_of_obstacles = int(parser['Obstacles']['number_of_obstacles'])
        generate_obstacles(obstacles, number_of_obstacles)

    else:
        for i in range(int(parser['Hardcoded Obstacles']['number_of_hardcoded_obstacles'])):
            obstacle = eval(parser['Hardcoded Obstacles'][f"obstacle_{i+1}"])
            obstacles.append(obstacle)

def _init_path_validity():
    
    for i, path_point_start in enumerate(path_points):

        if path_point_start not in path_validity:
            path_validity[path_point_start] = [True] * len(path_points)

        for j, path_point_end in enumerate(path_points):

            if path_point_end not in path_validity:
                path_validity[path_point_end] = [True] * len(path_points)

            if path_overlaps_obstacle(path_point_start, path_point_end, obstacles):
                path_validity[path_point_start][j] = False
                path_validity[path_point_end][i] = False

if __name__ == '__main__':
    
    main()
