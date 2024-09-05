import pygame
from generator import generate

SCREEN_SIZE = 500
DIFF = SCREEN_SIZE / 9

pygame.font.init()

display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

x = 0
y = 0

sodoku = generate()
grid = sodoku.board

font = pygame.font.SysFont("comicsans", 20)

def highlight_selection():
    for k in range(2):
        pygame.draw.line(display, (0, 0, 0), (x*DIFF-3, (y+k)*DIFF), (x*DIFF+DIFF+3, (y+k)*DIFF), 7)
        pygame.draw.line(display, (0, 0, 0), ((x+k)*DIFF, y*DIFF), ((x+k)*DIFF, y*DIFF+DIFF), 7)  
       
def draw_grid():
    for i in range (9):
        for j in range (9):
            pygame.draw.rect(display, (255, 255, 0), (i*DIFF, j*DIFF, DIFF+1, DIFF+1))
            text = font.render(str(grid[i][j] or ""), 1, (0, 0, 0))
            display.blit(text, (i*DIFF+(SCREEN_SIZE-7-7-1-1-1-1-1-1-7-7)//18-1, j*DIFF+(SCREEN_SIZE-7-7-1-1-1-1-1-1-7-7)//18-10))
    for l in range(10):
        if l % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(display, (0, 0, 0), (0, l*DIFF), (500, l*DIFF), thick)
        pygame.draw.line(display, (0, 0, 0), (l*DIFF, 0), (l *DIFF, 500), thick)      
 
def valid_value(grid, row, col, value):
    for i in range(9):
        #  Check if value exists in rows or cols
        if grid[row][i] == value or grid[i][col] == value:
            return False
    i, j = row//3, col//3
    for row in range(i*3, i*3+3):
        for col in range (j*3, j*3+3):
            # Check if value exits in subsection
            if grid[row][col] == value:
                return False
    return True

redraw_selection = False
running = True
while running:
    value = 0

    display.fill((255,182,193))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False   
        if event.type == pygame.MOUSEBUTTONDOWN:
            redraw_selection = True
            pos = pygame.mouse.get_pos()
            x = pos[0]//DIFF
            y = pos[1]//DIFF
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                redraw_selection = True
            if event.key == pygame.K_RIGHT:
                x += 1
                redraw_selection = True
            if event.key == pygame.K_UP:
                y -= 1
                redraw_selection = True
            if event.key == pygame.K_DOWN:
                y += 1
                redraw_selection = True

            if 49 <= event.key <= 57:
                value = event.key-48

            if event.key == pygame.K_r:
                grid = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            if event.key == pygame.K_d:
                grid = [
                    [0, 0, 4, 0, 6, 0, 0, 0, 5],
                    [7, 8, 0, 4, 0, 0, 0, 2, 0],
                    [0, 0, 2, 6, 0, 1, 0, 7, 8],
                    [6, 1, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 7, 5, 4, 0, 0, 6, 1],
                    [0, 0, 1, 7, 5, 0, 9, 3, 0],
                    [0, 7, 0, 3, 0, 0, 0, 1, 0],
                    [0, 4, 0, 2, 0, 6, 0, 0, 7],
                    [0, 2, 0, 0, 0, 7, 4, 0, 0],
                ]
                
    # Check if selected value can be added
    if value:           
        if valid_value(grid, int(x), int(y), value) == True:
            grid[int(x)][int(y)] = value
        else:
            grid[int(x)][int(y)] = 0 

    draw_grid() 
    if redraw_selection:
        highlight_selection()      
    pygame.display.update() 
   
pygame.quit()   