import pygame
from random import choice

class Rect:
    def __init__(self, i, j, size):
        self.i = i
        self.j = j
        self.size = size
        self.walls = [True, True, True, True]
        self.found = False
    
    def show(self):
        if self.walls[0]:
            pygame.draw.line(surface, (255,255,255), (self.i*size, self.j*size), ((self.i+1)*size, self.j*size))
        if self.walls[1]:
            pygame.draw.line(surface, (255,255,255), ((self.i+1)*size, self.j*size), ((self.i+1)*size, (self.j+1)*size))
        if self.walls[2]:
            pygame.draw.line(surface, (255,255,255), (self.i*size, (self.j+1)*size), ((self.i+1)*size, (self.j+1)*size))
        if self.walls[3]:
            pygame.draw.line(surface, (255,255,255), (self.i*size, self.j*size), (self.i*size, (self.j+1)*size))

    def highlight(self, surface, color):
        pygame.draw.rect(surface, color, pygame.Rect(self.i*size, self.j*size, size, size))

def wait_for_keypress(key):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    done = True
        clock.tick(15)

DIRECTIONS = ((0,-1),(1,0),(0,1),(-1,0))
def get_random_neighbor(x, y):
    global rects

    neighbors = []
    for DIRECTION in DIRECTIONS:
        i, j = DIRECTION
        ni, nj = x+i, y+j
        if 0 <= ni < amount and 0 <= nj < amount:
            neighbor = rects[nj][ni]
            if not neighbor.found:
                neighbors.append(neighbor)
    if neighbors: 
        return (choice(neighbors), len(neighbors))
    else:
        return (None, 0)

def carve_walls(curr, nxt):
    x, y = curr.i-nxt.i, curr.j-nxt.j

    if y == 1:
        curr.walls[0] = False
        nxt.walls[2] = False
    elif y == -1:
        curr.walls[2] = False
        nxt.walls[0] = False
    
    if x == -1:
        curr.walls[1] = False
        nxt.walls[3] = False
    elif x == 1:
        curr.walls[3] = False
        nxt.walls[1] = False

size = 35
amount = 15
rects = [[Rect(i, j, size) for i in range(amount)] for j in range(amount)]
width, height = size*amount+1, size*amount+1

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Maze Generator')
alpha_surface = pygame.Surface((width, height))
alpha_surface.set_alpha(100)

done = False
clock = pygame.time.Clock()
stack = []
current = rects[0][0]
finished = True
wait_for_keypress(pygame.K_SPACE)
while not done:
    surface.fill((0,0,0))

    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            done = True
    
    (next_neighbor, count_neighbors) = get_random_neighbor(current.i, current.j)
    current.found = True
    if next_neighbor:
        if count_neighbors > 1:
            stack.append(current)
        carve_walls(current, next_neighbor)
        current = next_neighbor
    elif stack:
        current = stack.pop(-1)
    else:
        finished = True
    
    if finished:
        alpha_surface.fill((0,0,0,0))
        current.highlight(alpha_surface, (0,255,0))
        for line_up in stack:
            line_up.highlight(alpha_surface, (0,0,255))
        rects[-1][-1].highlight(alpha_surface, (255,0,0))
        surface.blit(alpha_surface, (0,0))

        for row in rects:
            for rect in row:
                rect.show()

        pygame.display.flip()
        clock.tick(60)
        
pygame.quit()