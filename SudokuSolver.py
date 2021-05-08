import pygame
from numpy import arange
from random import choice

def wait_for_keypress(key_pressed):
    global clock, done, stop_search
    done_curr = False
    while not done_curr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_search = True
                done = True
                done_curr = True

            if event.type == pygame.KEYDOWN:
                if event.key == key_pressed:
                    done_curr = True
        
        clock.tick(10)

def draw_lines():
    global screen
    for idx, i in enumerate(arange(0, width, delta_x)):
        pygame.draw.line(screen, (0,0,0), (i, 0), (i, height), width = (5 if idx%3==0 else 1))
    for idj, j in enumerate(arange(0, width, delta_y)):
        pygame.draw.line(screen, (0,0,0), (0, j), (width, j), width = (5 if idj%3==0 else 1))

def update_screen():
    global width, height, delta_x, delta_y, game_board, text_surfaces, offset_x, offset_y, screen
    for i, space_x in enumerate(arange(0, width, delta_x)):
        for j, space_y in enumerate(arange(0, height, delta_y)):
            surface = text_surfaces[game_board[j][i]]
            rect = surface.get_rect(center=(space_x+offset_x,space_y+offset_y))
            screen.blit(surface, rect)

def check_for_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def update():
    global screen
    screen.fill((255,255,255))
    draw_lines()
    update_screen()
    pygame.display.flip()

def possible(x, y, n):
    global game_board

    for i in range(0, 9):
        if game_board[y][i] == n:
            return False
    
    for j in range(0, 9):
        if game_board[j][x] == n:
            return False

    start_x, start_y = (x//3)*3, (y//3)*3

    for i in range(start_x, start_x+3):
        for j in range(start_y, start_y+3):
            if game_board[j][i] == n:
                return False
    
    return True

stop_search = False
iterations = 0
def solve_sudoku():
    global game_board, stop_search, clock, iterations

    for j, row in enumerate(game_board):
        for i, num in enumerate(row):
            if num == 0:
                for check in range(1,10):
                    if stop_search:
                        return
                    if check_for_quit():
                        stop_search = True
                    if possible(i, j, check):
                        game_board[j][i] = check
                        iterations += 1
                        update()
                        clock.tick(30)
                        solve_sudoku()
                        game_board[j][i] = 0
                return
    update()
    print(iterations)
    iterations = 0
    wait_for_keypress(pygame.K_SPACE)
    

pygame.init()

pygame.display.set_caption('Sudoku Solver')
width, height = 700, 700
rows, columns = 9, 9
delta_x, delta_y = width/columns, height/rows
offset_x, offset_y = delta_x/2, delta_y/2

screen = pygame.display.set_mode((width, height))

font = pygame.font.Font('freesansbold.ttf' , 50)

text_surfaces = dict()
for i in range(1, 10):
    text_surfaces[i] = font.render(str(i), True, (0,0,0), (255,255,255)) 
text_surfaces[0] = font.render(' ', True, (0,0,0), (255,255,255)) 

with open("sudoku_file.txt", "r") as game_file:
    level = 0
    game = game_file.read().split('\n\n')[level]
    game_board = [[int(i) for i in row] for row in game.split('\n')]

clock = pygame.time.Clock()
done = False

update()
wait_for_keypress(pygame.K_SPACE)

while not done:
    update()
    solve_sudoku()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    clock.tick(10)

pygame.quit()
