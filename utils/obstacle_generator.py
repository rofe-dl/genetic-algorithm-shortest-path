from config.config_parser import parser
from random import randint
from shapely.geometry.polygon import Polygon

def generate_obstacles(obstacles, number_of_obstacles):
    print('Generating obstacles ....')
    for i in range(number_of_obstacles):

        while True:
            obstacle = _generate_obstacle()

            if not _obstacle_near_obstacle(obstacle, obstacles):
                break

        obstacles.append(obstacle)

def _generate_obstacle():
    axes = parser['Plot Axes']
    x_start = int(axes['x_start'])
    x_end = int(axes['x_end'])
    y_start = int(axes['y_start'])
    y_end = int(axes['y_end'])

    max_width = int(parser['Obstacles']['max_width'])
    max_height = int(parser['Obstacles']['max_height'])
    min_width = int(parser['Obstacles']['min_width'])
    min_height = int(parser['Obstacles']['min_height'])

    point_x_1 = randint(x_start + 3, x_end - 3)
    point_y_1 = randint(y_start + 3, y_end - 3)

    width = randint(min_width, max_width)
    height = randint(min_height, max_height)
    
    # to prevent obstacles from forming at the very edge of the axes
    point_x_2 = point_x_1 + width if point_x_1+width <= 0.8 * x_end else point_x_1 - width
    point_y_2 = point_y_1 + height if point_y_1+height <= 0.8 * y_end else point_y_1 - height

    # point_x_2 = point_x_1 + width if randint(1,10) <= 5 else point_x_1 - width
    # point_y_2 = point_y_1 + height if randint(1,10) <= 5 else point_y_1 - height

    return [(point_x_1, point_y_1), (point_x_2, point_y_1), (point_x_2, point_y_2), (point_x_1, point_y_2)]
    
def _obstacle_near_obstacle(obstacle, obstacles):
    obstacle = Polygon(obstacle)

    for o in obstacles:
        o = Polygon(o)

        if o.intersects(obstacle):
            return True

    return False