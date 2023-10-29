from enum import Enum


class PieceEnum(Enum):
    ATTACKER = 'A'
    KING = 'K'
    DEFENDER = 'D'


class TablutBoard:
    CASTLE_LOCATION = (4, 4)
    LEFT_CAMP_LOCATION = [(i, 0) for i in range(3, 6)] + [(4, 1)]
    RIGHT_CAMP_LOCATION = [(i, -1) for i in range(3, 6)] + [(4, -2)]
    UP_CAMP_LOCATION = [(0, i) for i in range(3, 6)] + [(1, 4)]
    DOWN_CAMP_LOCATION = [(-1, i) for i in range(3, 6)] + [(-2, 4)]
    CAMP_LOCATIONS = LEFT_CAMP_LOCATION + RIGHT_CAMP_LOCATION + UP_CAMP_LOCATION + DOWN_CAMP_LOCATION

    def __init__(self):
        self.board = [[None for i in range(9)] for j in range(9)]
        for i in range(2, 7):
            self.board[i][4] = PieceEnum.DEFENDER
            self.board[4][i] = PieceEnum.DEFENDER
        self.board[4][4] = PieceEnum.KING
        for i, j in self.CAMP_LOCATIONS:
            self.board[i][j] = PieceEnum.ATTACKER
        self.is_player_one_to_move = True

    def get_current_pieces(self):
        wanted_pieces = [PieceEnum.DEFENDER.value, PieceEnum.KING.value] if self.is_player_one_to_move else [PieceEnum.ATTACKER.value]
        pieces = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] in wanted_pieces:
                    pieces.append((i,j))
        return pieces

    def get_all_possible_moves(self, start_x, start_y):
        possible_moves = {(i, start_y) for i in range(9)} + {(start_x, i) for i in range(9)} - \
                         {(start_x, start_y), self.CASTLE_LOCATION}
        if self.is_player_one_to_move:
            possible_moves = possible_moves - set(self.CAMP_LOCATIONS)
        return [move for move in possible_moves if self.is_valid_move(start_x, start_y, move[0], move[1])]



    def print_board(self):
        print("    A   B   C   D   E   F   G   H   I")
        for i in range(9):
            print(f"{i + 1} |", end="")
            for j in range(9):
                print(f" {self.board[i][j].value if self.board[i][j] else 'E'} |", end="")
            print()
        print("  |---|---|---|---|---|---|---|---|---|")

    def is_valid_move(self, start_x, start_y, end_x, end_y):
        if end_x < 0 or end_x > 8 or end_y < 0 or end_y > 8:
            return False

        if self.board[start_x][start_y] and not self.board[end_x][end_y]:
            return False

        if start_x != end_x and start_y != end_y:
            return False
        for i in range(start_x, end_x + 1) if start_x < end_x else range(end_x, start_x + 1):
            if self.is_moving_illegal(start_x, start_y, i, end_y):
                return False
        for i in range(start_y, end_y + 1) if start_y < end_y else range(end_y, start_y + 1):
            if self.is_moving_illegal(start_x, start_y, end_x, i):
                return False
        return True

    def is_moving_illegal(self, start_x, start_y, current_x, current_y):
        return self.board[current_x][current_y] or \
               ((start_x, start_y) != self.CASTLE_LOCATION and (current_x, current_y) == self.CASTLE_LOCATION) or \
               ((start_x, start_y) not in self.LEFT_CAMP_LOCATION and (current_x, current_y) in self.LEFT_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.RIGHT_CAMP_LOCATION and (current_x, current_y) in self.RIGHT_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.UP_CAMP_LOCATION and (current_x, current_y) in self.UP_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.DOWN_CAMP_LOCATION and (current_x, current_y) in self.DOWN_CAMP_LOCATION)

    def move_piece(self, start_x, start_y, end_x, end_y):
        # Check if the move is valid
        if not self.is_valid_move(start_x, start_y, end_x, end_y):
            raise Exception("Invalid move")

        # TODO add the logic for capturing players

        # Move the piece
        self.board[end_x][end_y] = self.board[start_x][start_y]
        self.board[start_x][start_y] = None
        self.is_player_one_to_move = not self.is_player_one_to_move

    def is_game_over(self):
        for i in range(0, 9):
            if self.board[i][0] == "K" or self.board[i][8] == "K":
                return 1
        # TODO add other cases
        return 0

    def get_piece(self, x, y):
        if x < 0 or x > 8 or y < 0 or y > 8:
            raise Exception("Invalid coordinates")
        return self.board[x][y]


class TablutGame:
    def __init__(self):
        self.board = TablutBoard()
        self.current_player = "A"  # Attacker goes first

    def play(self):
        while not self.board.is_game_over():
            self.print_board()

            # Get the player's move
            move = input(f"Player {self.current_player}: Enter your move (e.g. A4 B5): ")

            # Parse the move
            try:
                piece_x, piece_y, dest_x, dest_y = move.split()
                piece_x = int(piece_x) - 1
                piece_y = int(piece_y) - 1
                dest_x = int(dest_x) - 1
                dest_y = int(dest_y) - 1
            except ValueError:
                print("Invalid move")
                continue

            # Get the piece to move
            piece = self.board.get_piece(piece_x, piece_y)

            # Move the piece
            self.board.move_piece(piece, dest_x, dest_y)

            # Switch players
            self.current_player = "D" if self.current_player == "A" else "A"

        # Game over
        self.print_board()
        if self.board.get_winner() == "A":
            print("Attacker wins!")
        else:
            print("Defender wins!")

    def print_board(self):
        self.board.print_board()


if __name__ == "__main__":
    # game = TablutGame()
    # game.play()
    b = TablutBoard()
    b.print_board()
