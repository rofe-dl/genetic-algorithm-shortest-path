from config.config_parser import parser
from random import randint
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def generate_path_points(path_points, obstacles):
    print('Generating path points ....')

    axes = parser['Plot Axes']

    source_x = int(axes['x_start']) + 1
    source_y = int(axes['y_start']) + 1
    # source_y = randint(int(axes['y_start']), int(axes['y_end']))
    path_points.append((source_x, source_y))

    goal_x = int(axes['x_end']) - 1
    goal_y = int(axes['y_end']) - 1
    # goal_y = randint(int(axes['y_start']), int(axes['y_end']))

    number_of_path_points = int(parser['Path Points']['number_of_path_points'])
    for i in range(number_of_path_points):
        path_points.append(_generate_path_point(obstacles, path_points))

    path_points.append((goal_x, goal_y))

def _generate_path_point(obstacles, path_points):
    axes = parser['Plot Axes']

    while True:
        # avoid path points being formed on the edges of the axes
        x = randint( int(axes['x_start'])+2, int(axes['x_end'])-2 )
        y = randint( int(axes['y_start'])+2, int(axes['y_end'])-2 )
        
        if not _path_point_near_obstacle(x, y, obstacles) and not _path_point_near_another(x, y, path_points):
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

def _path_point_near_another(x, y, path_points):
    point1 = Point(x, y)
    circle_perimeter_1 = point1.buffer(2).boundary

    for point in path_points:
        point2 = Point(point[0], point[1])
        circle_perimeter_2 = point2.buffer(2).boundary

        if circle_perimeter_1.intersection(circle_perimeter_2):
            return True

    return False        