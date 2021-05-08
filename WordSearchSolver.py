import pygame
from string import ascii_uppercase
from numpy import arange

words = """MERCURY
VENUS
EARTH
MARS
JUPITER
SATURN
URANUS
NEPTUNE
PLUTO
ASTRONOMY
CONSTELLATION
METEORITE
NEBULA
SATELLITE
UNIVERSE
STARLIGHT
TELESCOPE
GRAVITY
COSMONAUT
OBSERVATORY"""

word_search = """ZTBGJDBHERFFADFAKIFDDDNOYDQQKN
EQYGTBGHDNVNFOEQIHMFHXLOCGNMNJ
SXCKUYWEAHRSUIHILCXIPBJDSMXEMF
MHNBTRAXMAAALZKYZJAMLXKSSPBCOX
UUDVHHGOVLAYFKUFSPNSOVEZQUONHJ
VWVOGEKQEGTYMQHXSAAGGODGLIXWKY
SOJOIMFRNASPYGOFBBCXLCPASHBWKX
KPWQLAEYKGRETILLETASUDIOIPTCHH
COZTRRSJJUCTIELGUBRYKQXSTPFOJV
MCLPASNUWHDUHFOGTYRPUAIGIOPIBH
XVOFTGATNUROETKTRUWITWWPFXAKHF
TDFNSLHAEAVUUIOGCEMNFYXREAUWMN
AIKZSRMCSKRLUXIRGNSRDKRVYCLCGT
HVDCMTEYKMPUNPEINUQSFHBUKMORCH
SDNUOBEGDRHPVMJWETLHUNBZMFDPSQ
DONRTSKLRLGPFTAKQPPTAJDQJIIVIH
CZUAZRMDLOKGZMMXDEHBDGAEXVIDSY
QIQXFESOGAQTCQBTDNIXCMPAKFQIOM
TJXDPKLMNGTOFLNLTJKEQOHJPQBXLO
GFCVTMMWIAXISBNEUNLOCSDOIOSTGU
YDVZBQEVENUSOIIPTXZSQBFBLBOEXX
YSQEDFTSIQXTFNIEUUEJCJJAJSQOFL
EQRCOFEKRSDBMTQDELGRAVITYEDGEA
NRUTASOLAEJHEKXGEHLIRPOHYRTCRJ
RJEOPWRELBVRSASTRONOMYILIVIQLG
NRIBZYIZDCHIQSCLRAEBXIRIHANZUA
SXBZXCTALKTJNYNPYOQHFYSRDTOMPV
HSKPBLEMBCRAIULGSHFNGFOCMOFQJC
OAWFBAPWASWQAIGWDBMYLWKQKRYEJN
OZDJSOGDJTMHQBPHQQFQQIHYAYEFLV"""

font_size = 30
line_size = 20
checked = 0
def update_screen():
    global text_surface, check_words_surface, found_words_surface
    screen.blit(text_surface, (0,0))
    screen.blit(check_words_surface, (0,0))
    screen.blit(found_words_surface, (0,0))
    pygame.display.flip()

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
        clock.tick(10)

def draw_line_perm(start, end):
    start_pos = (start[0]*delta_x+offset_x, start[1]*delta_y+offset_y)
    end_pos = (end[0]*delta_x+offset_x, end[1]*delta_y+offset_y)
    pygame.draw.line(found_words_surface, (0,255,0,100), start_pos, end_pos, width=line_size)

def draw_check_line(start, end):
    check_words_surface.fill((0,0,0,0))
    pygame.display.flip()
    start_pos = (start[0]*delta_x+offset_x, start[1]*delta_y+offset_y)
    end_pos = (end[0]*delta_x+offset_x, end[1]*delta_y+offset_y)
    pygame.draw.line(check_words_surface, (255,0,0,100), start_pos, end_pos, width=line_size)

def word_up(x, y, length):
    ny = y - (length - 1)
    if 0 <= ny < word_search_height:
        return ("".join(word_search[j][x] for j in reversed(range(ny, y+1))), (x, ny))

def word_down(x, y, length):
    ny = y + (length - 1)
    if 0 <= ny < word_search_height:
        return ("".join(word_search[j][x] for j in range(y, ny+1)), (x, ny))

def word_left(x, y, length):
    nx = x - (length - 1)
    if 0 <= nx < word_search_width:
        return ("".join(word_search[y][i] for i in reversed(range(nx, x+1))), (nx, y))

def word_right(x, y, length):
    nx = x + (length - 1)
    if 0 <= nx < word_search_width:
        return ("".join(word_search[y][i] for i in range(x, nx+1)), (nx, y))

def word_up_right(x, y, length):
    nx = x + (length - 1)
    ny = y - (length - 1)
    if 0 <= ny < word_search_height and 0 <= nx < word_search_width:
        return ("".join(word_search[y-d][x+d] for d in range(length)), (nx, ny))

def word_down_right(x, y, length):
    nx = x + (length - 1)
    ny = y + (length - 1)
    if 0 <= ny < word_search_height and 0 <= nx < word_search_width:
        return ("".join(word_search[y+d][x+d] for d in range(length)), (nx, ny))

def word_down_left(x, y, length):
    nx = x - (length - 1)
    ny = y + (length - 1)
    if 0 <= ny < word_search_height and 0 <= nx < word_search_width:
        return ("".join(word_search[y+d][x-d] for d in range(length)), (nx, ny))

def word_up_left(x, y, length):
    nx = x - (length - 1)
    ny = y - (length - 1)
    if 0 <= ny < word_search_height and 0 <= nx < word_search_width:
        return ("".join(word_search[y-d][x-d] for d in range(length)), (nx, ny))

word_find_funcs = [word_up, word_up_right, word_right, word_down_right, word_down, word_down_left, word_left, word_up_left]

def update_words(word):
    global start_letters, word_lengths, words
    words.remove(word)
    start_letters = set(word[0] for word in words)
    word_lengths = [len(word) for word in words]
    print(words, start_letters, word_lengths)


def find_words(fps):
    global word_search, words, done, checked

    for word in words:
        done_curr = False
        start_letter = word[0]
        length = len(word)
        for j in range(word_search_height):
            for i in range(word_search_width):
                if done_curr:
                    break

                if word_search[j][i] != start_letter:
                    continue
                
                for word_find in word_find_funcs:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                            return
                    checked += 1
                    ans = word_find(i, j, length)

                    if not ans:
                        continue

                    string, end_pos = ans

                    draw_check_line((i, j), end_pos)
                    
                    if string == word:
                        draw_line_perm((i, j), end_pos)
                        done_curr = True

                    update_screen()
                    clock.tick(fps)
            if done_curr:
                break

word_search = word_search.split('\n')
words = words.split('\n')

word_search_height = len(word_search)
word_search_width = len(word_search[0])

width, height = 1200, 1200
delta_x, delta_y = width/word_search_width, height/word_search_height
offset_x, offset_y = delta_x/2, delta_y/2

pygame.init()

font = pygame.font.Font('freesansbold.ttf' , font_size)

text_surface = pygame.Surface((width, height))
text_surface.fill((255,255,255))

text_renders = dict()
for upper_letter in ascii_uppercase:
    text_renders[upper_letter] = font.render(upper_letter, True, (0,0,0))

for j, d_y in enumerate(arange(0, height, delta_y)):
    for i, d_x in enumerate(arange(0, width, delta_x)):
        text_render = text_renders[word_search[j][i]]
        text_surface.blit(text_render, (d_x, d_y))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Word Search Solver")
screen.blit(text_surface, (0,0))

found_words_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
found_words_surface = found_words_surface.convert_alpha()

check_words_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
check_words_surface = check_words_surface.convert_alpha()

clock = pygame.time.Clock()
done = False

update_screen()
wait_for_keypress(pygame.K_SPACE)
if not done:
    find_words(45)
check_words_surface.fill((0,0,0,0))
print(checked)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    update_screen()
    clock.tick(10)

pygame.quit()