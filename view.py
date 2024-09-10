from board import Board
import pygame, sys

SCREEN_SIZE = 500
DIFF = SCREEN_SIZE / 9
DIFFICULTY = 0.4

# .venv\Scripts\activate
# deactivate

pygame.font.init()
display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
font = pygame.font.SysFont("comicsans", 20)

def highlight_selection(row, col):
    for k in range(2):
        pygame.draw.line(display, (0, 0, 0), (row*DIFF-3, (col+k)*DIFF), (row*DIFF+DIFF+3, (col+k)*DIFF), 7)
        pygame.draw.line(display, (0, 0, 0), ((row+k)*DIFF, col*DIFF), ((row+k)*DIFF, col*DIFF+DIFF), 7)  
       
def draw_board(board):
    for i in range (9):
        for j in range (9):
            pygame.draw.rect(display, (255, 255, 0), (i*DIFF, j*DIFF, DIFF+1, DIFF+1))
            text = font.render(str(board.get_board()[i][j] or ""), 1, (0, 0, 0))
            display.blit(text, (i*DIFF+(SCREEN_SIZE-7-7-1-1-1-1-1-1-7-7)//18-1, j*DIFF+(SCREEN_SIZE-7-7-1-1-1-1-1-1-7-7)//18-10))
    for l in range(10):
        if l % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(display, (0, 0, 0), (0, l*DIFF), (500, l*DIFF), thick)
        pygame.draw.line(display, (0, 0, 0), (l*DIFF, 0), (l *DIFF, 500), thick)      

board = Board(difficulty=DIFFICULTY)
redraw_selection = False
row = 0
col = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            redraw_selection = True
            pos = pygame.mouse.get_pos()
            row = pos[0]//DIFF
            col = pos[1]//DIFF
        if event.type == pygame.KEYDOWN:
            if 49 <= event.key <= 57:
                value = event.key-48
                # Check if selected value can be added
                if board.is_valid_move(int(row), int(col), value):
                    board.set_board(int(row), int(col), value)

            if event.key == pygame.K_c:
                board.reset(False)
            if event.key == pygame.K_r:
                board.reset(True, difficulty=DIFFICULTY)
    
    display.fill((255,182,193))
    draw_board(board) 
    if redraw_selection:
        highlight_selection(row, col)      
    pygame.display.update()