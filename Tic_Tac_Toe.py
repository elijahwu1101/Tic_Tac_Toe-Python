import pygame

screen_height = 900
screen_width = screen_height
screen = pygame.display.set_mode((screen_height, screen_width))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class game():
    def __init__(self, board):
        self.board = board
        self.turn = "X"
        self.box_state = "Empty"
    
    def handle_click(self):
        if self.turn == "X":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    height_length = (self.box_size // 10) * 11.5
                    width_height = self.box_size // 5 

                    rect_surface = pygame.Surface((height_length, width_height), pygame.SRCALPHA)
                    pygame.draw.rect(rect_surface, RED, (0, 0, height_length, width_height))

                    rect1 = pygame.transform.rotate(rect_surface, 45)
                    rect2 = pygame.transform.rotate(rect_surface, -45)

                    loc1 = rect1.get_rect(center=(self.current_box, self.current_box))
                    loc2 = rect2.get_rect(center=(self.current_box, self.current_box))

                    screen.blit(rect1, loc1)
                    screen.blit(rect2, loc2)
                    
class board():
    def __init__(self, x, y, box_grid_size, box_size, box_column, box_row, box_gap):
        self.box_size = box_size
        self.x = x
        self.y = y
        self.box_gap = box_gap
        self.box_column = box_column
        self.box_row = box_row
        self.box_grid_size = (3 * box_size + 2 * box_gap)
        self.occupied = {}

        self.rects = []
        self.last_box = None
        
    def draw(self, rect):
        if not self.rects:
            margin_x = (screen_width - self.box_grid_size)/2
            margin_y = margin_x

            for row in range (self.box_row):
                for column in range (self.box_column):
                    x = margin_x + (column * (self.box_size + self.box_gap))
                    y = margin_y + ( row * (self.box_size + self.box_gap))

                    rect = pygame.Rect(x, y, self.box_size, self.box_size)  

                    pygame.draw.rect(screen, WHITE,(x, y, self.box_size, self.box_size))
                    pygame.draw.rect(screen, BLACK, (x, y, self.box_size, self.box_size), 5)

                    self.rects.append((row, column, rect))

        for row, column, rect in self.rects:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 5)

    def get_mouse_box(self, mouse_x, mouse_y):
        current_box = None
        for row, column, rect, in self.rects:
            if rect.collidepoint(mouse_x, mouse_y):
                current_box = (row, column)
                break

        # No longer need the print statements, but useful for debugging
        if current_box != self.last_box:
            if self.last_box is not None:
                #print(f"Exited {self.last_box}")
                ...
            if current_box is not None:
                #print(f"Entered {current_box}")
                ...

        self.last_box = current_box
        return current_box

    def mark_box(self, row, column, player):
        if (row, column) not in self.occupied:
            self.occupied[(row, column)] = player

    def draw_symbols(self, screen):
        for (row, col), player in self.occupied.items():
            for r, c, rect in self.rects:
                if r == row and c == col:
                    x_center, y_center = rect.center
                    temp_player = player_symbol(x_center, y_center, self.box_size, player)
                    temp_player.draw(screen)
             
class player_symbol():
    def __init__(self, mouse_x, mouse_y, box_size, player):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.box_size = box_size
        self.player = player

    def draw(self, screen):
        if self.player == "X":
            height_length = (self.box_size // 10) * 11.5
            width_height = self.box_size // 5 

            rect_surface = pygame.Surface((height_length, width_height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, RED, (0, 0, height_length, width_height))

            rect1 = pygame.transform.rotate(rect_surface, 45)
            rect2 = pygame.transform.rotate(rect_surface, -45)

            loc1 = rect1.get_rect(center=(self.mouse_x, self.mouse_y))
            loc2 = rect2.get_rect(center=(self.mouse_x, self.mouse_y))

            screen.blit(rect1, loc1)
            screen.blit(rect2, loc2)
        
        elif self.player == "O":
            #time.sleep(0.4)
            pygame.draw.circle(screen, BLUE, (self.mouse_x, self.mouse_y), self.box_size // 2 - 20, 50)
            
class player_possible_pos():
    def __init__(self, board, box_size ):
        self.board = board
        self.hovered_box = None
        self.box_size = box_size


    def calculate_and_draw(self, screen, mouse_x, mouse_y, fade = 100):
        hovered_box = self.board.get_mouse_box(mouse_x, mouse_y)
        if hovered_box is None:
            return

        row, col = hovered_box
                        
        if (row, col) in self.board.occupied:
            return

        for r, c, rect in self.board.rects:
            if (r, c) == (row, col):
                x_center = rect.centerx
                y_center = rect.centery

                height_length = (self.box_size // 10) * 11.5
                width_height = self.box_size // 5 

                rect_surface = pygame.Surface((height_length, width_height), pygame.SRCALPHA)
                pygame.draw.rect(rect_surface, (255, 0, 0, fade), (0, 0, height_length, width_height))

                rect1 = pygame.transform.rotate(rect_surface, 45)
                rect2 = pygame.transform.rotate(rect_surface, -45)

                loc1 = rect1.get_rect(center=(x_center, y_center))
                loc2 = rect2.get_rect(center=(x_center, y_center))

                screen.blit(rect1, loc1)
                screen.blit(rect2, loc2)
                break


class AI_symbol():
    def __init__(self, player = "O"):
        self.player = player
        self.opponent = "X"
    
    def check_winner(self, board_state):
        #___Rows___
        for row in range(3):
            if (row, 0) in board_state and (row, 1) in board_state and (row, 2) in board_state:
                if board_state[(row, 0)] == board_state[(row, 1)] == board_state[(row, 2)]:
                    return board_state[(row, 0)]
        
        #___Columns___
        for col in range(3):
            if (0, col) in board_state and (1, col) in board_state and (2, col) in board_state:
                if board_state[(0, col)] == board_state[(1, col)] == board_state[(2, col)]:
                    return board_state[(0, col)]
        
        if (0, 0) in board_state and (1, 1) in board_state and (2, 2) in board_state:
            if board_state[(0, 0)] == board_state[(1, 1)] == board_state[(2, 2)]:
                return board_state[(0, 0)]
        
        if (0, 2) in board_state and (1, 1) in board_state and (2, 0) in board_state:
            if board_state[(0, 2)] == board_state[(1, 1)] == board_state[(2, 0)]:
                return board_state[(0, 2)]
    
    def evaluate_board(self, board_state):
        winner = self.check_winner(board_state)
        if winner == self.player:
            return +1
        elif winner == self.opponent:
            return -1
        elif len(board_state) == 9:
            return 0
        else:
            return None
 
    def minimax_algorithm(self, board_state, depth, is_maximizing):
        score = self.evaluate_board(board_state)
        if score is not None:
            # Use a fixed WIN_SCORE to ensure earlier wins are preferred and
            # opponent wins remain negative. Previous code returned `-1 + depth`
            # for opponent wins which could become positive for larger depths.
            WIN_SCORE = 10
            if score == 1:
                return WIN_SCORE - depth
            elif score == -1:
                return depth - WIN_SCORE
            else:
                return 0
        
        empty_spots = [(row, col) for row in range(3) for col in range(3) if (row, col) not in board_state]

        if is_maximizing:
            best_score = -float("inf")
            for row, col in empty_spots:
                board_state[(row, col)] = self.player
                score = self.minimax_algorithm(board_state, depth + 1, False)
                del board_state[(row, col)]
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for row, col in empty_spots:
                board_state[(row, col)] = self.opponent
                score = self.minimax_algorithm(board_state, depth + 1, True)
                del board_state[(row, col)]
                best_score = min(best_score, score)
            return best_score

    def choose_move(self, board_state):
        best_score = -float("inf")
        best_move = None
        empty_spots = [(row, col) for row in range(3) for col in range(3) if (row, col) not in board_state]

        for row, col in empty_spots:
            board_state[(row, col)] = self.player
            score = self.minimax_algorithm(board_state, 0, False)
            del board_state[(row, col)]
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move


    def draw(self, screen, board, move):
        if move is None:
            return 
        
        row, col = move
        for r, c, rect in board.rects:
            if r == row and c == col:
                x_center, y_center = rect.center
                pygame.draw.circle(screen, BLUE, (x_center, y_center), board.box_size // 2 - 20, 5)
        
#Instances!!!!

Board = board(
    x = 0, 
    y = 0, 
    box_size = 280,
    box_column = 3,   
    box_row = 3,   
    box_gap = 10,      
    box_grid_size = (3 * 100 + 2 * 10)

    #IMPORTANT: If you are going to change box_size and box_gap, make sur eto change it inside the def get_mouse_box method inside the class.
    #You have to do this because i'm lazy.
)

Player = player_symbol(
    mouse_x = 0, 
    mouse_y = 0, 
    box_size = 280,
    player = "X"
    
)
ai = AI_symbol(player = "O")

PossibleX = player_possible_pos(Board, box_size=280)

game_turn = "X"

running = True
while running:

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    if game_turn == "X" and event.type == pygame.MOUSEBUTTONDOWN: 
        box = Board.get_mouse_box(*pygame.mouse.get_pos())
        if box: 
            row, col = box
            if Board.occupied.get((row, col))is None:
                Board.mark_box(row, col, "X")
                game_turn = "O"

    if game_turn == "O":

        print("AI sees Board: ", Board.occupied)

        ai_move = ai.choose_move(Board.occupied)
        if ai_move:
            row, col = ai_move
            Board.mark_box(row, col, "O")
            #ai.draw(screen, Board, ai_move)
            #No need for this line because of Board.draw_symbols(screen)
        game_turn = "X"

    Player.mouse_x, Player.mouse_y = pygame.mouse.get_pos()

    Board.draw(None)
    Board.draw_symbols(screen)
    Board.get_mouse_box(Player.mouse_x, Player.mouse_y)

    PossibleX.calculate_and_draw(screen, Player.mouse_x, Player.mouse_y)

    #Player.draw(screen)

    pygame.display.flip()

pygame.quit()
