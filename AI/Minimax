
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
        
