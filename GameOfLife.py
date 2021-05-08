import pygame
from random import randint

width, height = 1920, 1080
square_size = 5
line_width = 0
fps = 20
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game Of Life")

def wait_for_keypress(key):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    done = True
        clock.tick(15)

def update_board():
    global board, generation
    copy = [[n for n in row] for row in board]
    alive = 0
    for j in range(y_length):
        for i in range(x_length):
            neighbors = get_neighbors(i, j)

            if board[j][i] == 1:
                if neighbors == 2 or neighbors == 3:
                    alive += 1
                    continue
            else:
                if neighbors == 3:
                    copy[j][i] = 1
                    alive += 1
                    continue
            # if randint(0,999) else 1 
            copy[j][i] = 0
    
    board = copy
    generation += 1
    return alive

def get_neighbors(x, y):
    DIRECTIONS = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))

    neighbors = 0
    for i, j in DIRECTIONS:
        nx, ny = x + i, y + j
        if 0 <= nx < x_length and 0 <= ny < y_length:
            neighbors += board[ny][nx]
    
    return neighbors

def draw_board():
    global surface, board
    for j in range(y_length):
        for i in range(x_length):
            rect = pygame.Rect(i*square_size+line_width, j*square_size+line_width, square_size-(line_width*2), square_size-(line_width*2))
            color = (0,0,0) if board[j][i] else (255,255,255)
            pygame.draw.rect(surface, color, rect)

x_length, y_length = width//square_size, height//square_size
board = [[randint(0, 1) for _ in range(x_length)] for _ in range(y_length)]

done = False
clock = pygame.time.Clock()

generation = 0
update_board()
draw_board()
pygame.display.flip()
wait_for_keypress(pygame.K_SPACE)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    alive = update_board()
    draw_board()
    pygame.display.set_caption(f'Population: {alive} Generation: {generation}')
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
