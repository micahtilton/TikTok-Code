from math import isnan
from numpy import arange
import colorsys
import pygame

pygame.init()

def wait_for_keypress(key):
    global done
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                return
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return

class Color:
    stable = (0,0,0)

    unstable_start = colorsys.rgb_to_hsv(.6, .2, 1)
    unstable_end = colorsys.rgb_to_hsv(0, 0, 0.35)
    delta_h = unstable_end[0] - unstable_start[0]
    delta_s = unstable_end[1] - unstable_start[1]
    delta_v = unstable_end[2] - unstable_start[2]

    @staticmethod
    def interpolate(step, end):
        percent = step/end

        new_h = Color.unstable_start[0] + (percent*Color.delta_h)
        new_s = Color.unstable_start[1] + (percent*Color.delta_s)
        new_v = Color.unstable_start[2] + (percent*Color.delta_v)
        
        new_rgb = colorsys.hsv_to_rgb(new_h, new_s, new_v)

        r = round(new_rgb[0] * 255)
        g = round(new_rgb[1] * 255)
        b = round(new_rgb[2] * 255)
        
        return (r,g,b)

def get_color(a, b):
    steps = 90
    start = complex(0, 0)
    const = complex(a, b)

    for i in range(steps):
        if start.real > 4 or start.imag > 4:
            return Color.interpolate(i, steps)
        start = (start**2) + const
    else:
        return Color.stable

def draw_pixel(x, y, color):
    rect = pygame.Rect(x*delta_x, y*delta_y, delta_x, delta_y)
    pygame.draw.rect(surface, color, rect)

size = 1
resolution_x, resolution_y = 3840, 2160
aspect = resolution_y/resolution_x

graph_x_min, graph_x_max = -2.3, 1.1
center_y = 0
h = ((abs(graph_x_min) + abs(graph_x_max))/2)*aspect
graph_y_min, graph_y_max = -h+center_y, h+center_y

delta_gx = abs(graph_x_min - graph_x_max)/resolution_x
delta_gy = abs(graph_y_min - graph_y_max)/resolution_y
width, height = size*resolution_x, size*resolution_y
delta_x, delta_y = width//resolution_x, height//resolution_y

def mp(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)

def screen_to_graph(x, y):
    x_new = round(mp(x, 0, width, graph_x_min, graph_x_max)+graph_x_min, 4)
    y_new = round(mp(y, 0, height, graph_y_max, graph_y_min)+graph_y_max, 4)
    return (x_new, y_new)

surface = pygame.display.set_mode((width, height))
fps = pygame.time.Clock()
done = False

def check_events():
    global done
    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            done = True
            return True

def main():
    while not done:
        for j, y in enumerate(arange(graph_y_min, graph_y_max, delta_gy)):
            for i, x in enumerate(arange(graph_x_min, graph_x_max, delta_gx)):
                color = get_color(x, y)
                draw_pixel(i, j, color)
                if check_events():
                    return
            pygame.display.flip()

        pygame.image.save(surface, 'temp.png')
        while not done:
            if check_events():
                break
pygame.display.flip()
wait_for_keypress(pygame.K_SPACE)
main()
pygame.quit()