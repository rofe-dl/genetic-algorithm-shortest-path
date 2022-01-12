from config.config_parser import parser
from random import randint
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def generate_path_points(path_points, obstacles):

    axes = parser['Plot Axes']

    source_x = int(axes['x_start']) + 1
    source_y = randint(int(axes['y_start']), int(axes['y_end']))
    path_points.append((source_x, source_y))

    goal_x = int(axes['x_end']) - 1
    goal_y = randint(int(axes['y_start']), int(axes['y_end']))

    number_of_path_points = int(parser['Path Points']['number_of_path_points'])
    for i in range(number_of_path_points):
        path_points.append(_generate_path_point(obstacles))

    path_points.append((goal_x, goal_y))

def _generate_path_point(obstacles):
    axes = parser['Plot Axes']

    while True:
        x = randint( int(axes['x_start'])+1, int(axes['x_end'])-1 )
        y = randint( int(axes['y_start'])+1, int(axes['y_end'])-1 )
        
        if not _path_point_near_obstacle(x, y, obstacles):
            return (x, y)

def _path_point_near_obstacle(x, y, obstacles):
    point = Point(x, y)

    # forms a radius of 1 around the point to check if point is near any obstacle
    circle_perimeter = point.buffer(1).boundary
    
    for obstacle in obstacles:
        obstacle = Polygon(obstacle)

        if circle_perimeter.intersection(obstacle):
            return True
    
    return False