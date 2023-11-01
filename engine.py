from enum import Enum
from functools import reduce

import numpy as np


class PieceEnum(Enum):
    ATTACKER = 1
    DEFENDER = 2
    KING = 3


class TablutBoard:
    CASTLE_LOCATION = (4, 4)
    LOCATIONS_AROUND_CASTLE = [(3, 4), (4, 3), (5, 4), (4, 5)]
    LEFT_CAMP_LOCATION = [(i, 0) for i in range(3, 6)] + [(4, 1)]
    RIGHT_CAMP_LOCATION = [(i, 8) for i in range(3, 6)] + [(4, 7)]
    UP_CAMP_LOCATION = [(0, i) for i in range(3, 6)] + [(1, 4)]
    DOWN_CAMP_LOCATION = [(8, i) for i in range(3, 6)] + [(7, 4)]
    CAMP_LOCATIONS = LEFT_CAMP_LOCATION + RIGHT_CAMP_LOCATION + UP_CAMP_LOCATION + DOWN_CAMP_LOCATION

    def __init__(self):
        self.board = np.zeros((9, 9))
        for i in range(2, 7):
            self.board[i][4] = PieceEnum.DEFENDER.value
            self.board[4][i] = PieceEnum.DEFENDER.value
        self.board[4][4] = PieceEnum.KING.value
        for i, j in self.CAMP_LOCATIONS:
            self.board[i][j] = PieceEnum.ATTACKER.value
        self.is_player_one_to_move = True
        self.old_boards = []

    def get_current_pieces(self):
        wanted_pieces = [PieceEnum.DEFENDER.value, PieceEnum.KING.value] if self.is_player_one_to_move else [
            PieceEnum.ATTACKER.value]
        pieces = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] in wanted_pieces:
                    pieces.append((i, j))
        return pieces

    def get_all_possible_moves(self):
        current_checkers = [PieceEnum.DEFENDER.value, PieceEnum.KING.value] \
            if self.is_player_one_to_move else [PieceEnum.ATTACKER.value]
        possible_moves = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] in current_checkers:
                    possible_moves += self.get_all_possible_moves_by_checker((i, j))
        return possible_moves

    def get_all_possible_moves_by_checker(self, checker_location):
        checker_x, checker_y = checker_location
        possible_moves = {(i, checker_y) for i in range(9)} | {(checker_x, i) for i in range(9)} - \
                         {(checker_x, checker_y), self.CASTLE_LOCATION}

        if self.is_player_one_to_move:
            possible_moves = possible_moves - set(self.CAMP_LOCATIONS)
        return [(checker_location, move) for move in possible_moves if
                self.is_valid_move(checker_x, checker_y, move[0], move[1])]

    def __str__(self):
        return "".join(map(lambda a: str(a), self.board.flatten().tolist()))

    def print_board(self):
        print("    0     1     2     3     4     5     6     7     8")
        for i in range(9):
            print(f"{i} |", end="")
            for j in range(9):
                print(f" {self.board[i][j]} |", end="")
            print()
        print("  |-----|-----|-----|-----|-----|-----|-----|-----|-----|")
        print()

    def is_valid_move(self, start_x, start_y, end_x, end_y):
        if end_x < 0 or end_x > 8 or end_y < 0 or end_y > 8:
            return False

        if not self.board[start_x][start_y] or self.board[end_x][end_y]:
            return False

        if start_x != end_x and start_y != end_y:
            return False

        for i in range(start_x + 1, end_x + 1) if start_x < end_x else range(end_x, start_x):
            if self.is_moving_illegal(start_x, start_y, i, end_y):
                return False

        for i in range(start_y + 1, end_y + 1) if start_y < end_y else range(end_y, start_y):
            if self.is_moving_illegal(start_x, start_y, end_x, i):
                return False
        return True

    def is_moving_illegal(self, start_x, start_y, current_x, current_y):
        return self.board[current_x][current_y] or \
               ((start_x, start_y) != self.CASTLE_LOCATION and (current_x, current_y) == self.CASTLE_LOCATION) or \
               ((start_x, start_y) not in self.LEFT_CAMP_LOCATION and (
                   current_x, current_y) in self.LEFT_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.RIGHT_CAMP_LOCATION and (
                   current_x, current_y) in self.RIGHT_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.UP_CAMP_LOCATION and (current_x, current_y) in self.UP_CAMP_LOCATION) or \
               ((start_x, start_y) not in self.DOWN_CAMP_LOCATION and (current_x, current_y) in self.DOWN_CAMP_LOCATION)

    def move_piece(self, start_x, start_y, end_x, end_y):
        if not self.is_valid_move(start_x, start_y, end_x, end_y):
            raise Exception("Invalid move")
        opposite_checkers = [PieceEnum.ATTACKER.value] if self.is_player_one_to_move else [PieceEnum.DEFENDER.value,
                                                                                           PieceEnum.KING.value]
        current_checkers = [PieceEnum.ATTACKER.value] if not self.is_player_one_to_move else [PieceEnum.DEFENDER.value,
                                                                                              PieceEnum.KING.value]
        checker_neighbours = self.generate_neighbours(end_x, end_y)

        # Move the piece
        self.board[end_x][end_y] = self.board[start_x][start_y]
        self.board[start_x][start_y] = 0

        for (x, y) in checker_neighbours:
            if self.board[x][y] != PieceEnum.KING.value and self.board[x][y] in opposite_checkers \
                    and self.is_checker_surrounded((x, y), current_checkers):
                self.board[x][y] = 0
        self.is_player_one_to_move = not self.is_player_one_to_move
        self.old_boards.append(str(self))

    @staticmethod
    def generate_neighbours(checker_x, checker_y):
        return [(x, y) for (x, y) in
                [(checker_x, checker_y + 1), (checker_x, checker_y - 1), (checker_x + 1, checker_y),
                 (checker_x - 1, checker_y)]
                if 0 <= x <= 8 and 0 <= y <= 8]

    def is_king_surrounded(self, king_location):
        if king_location == (4, 4) and \
                reduce(lambda a, b: a and b, [self.board[x][y] == PieceEnum.ATTACKER.value
                                              for (x, y) in self.LOCATIONS_AROUND_CASTLE]):
            return True
        if king_location in self.LOCATIONS_AROUND_CASTLE and \
                reduce(lambda a, b: a and b, [self.board[x][y] == PieceEnum.ATTACKER.value
                                              for (x, y) in set(self.LOCATIONS_AROUND_CASTLE) - {king_location}]):
            return True

        if self.is_checker_surrounded_from_opposite_sides(king_location, [PieceEnum.ATTACKER.value]):
            return True
        return False

    def is_checker_surrounded_from_opposite_sides(self, checker_location, opposite_checkers):
        return self.is_checker_surrounded_up_down(checker_location, opposite_checkers) \
               or self.is_checker_surrounded_left_right(checker_location, opposite_checkers)

    def is_checker_surrounded_up_down(self, checker_location, opposite_checkers):
        checker_x, checker_y = checker_location
        if checker_x > 8 or checker_x < 0:
            return False
        return self.board[checker_x - 1][checker_y] in opposite_checkers and \
               self.board[checker_x + 1][checker_y] in opposite_checkers

    def is_checker_surrounded_left_right(self, checker_location, opposite_checkers):
        checker_x, checker_y = checker_location
        if checker_y > 8 or checker_y < 0:
            return False
        return self.board[checker_x][checker_y - 1] in opposite_checkers and \
               self.board[checker_x][checker_y + 1] in opposite_checkers

    def is_checker_surrounded_to_camp(self, checker_location, opposite_checkers):
        checker_x, checker_y = checker_location

        checker_neighbours = self.generate_neighbours(checker_x, checker_y)
        for (x, y) in checker_neighbours:
            if (x, y) in self.CAMP_LOCATIONS:
                # if (x, y) in self.CAMP_LOCATIONS and 0<=2 * x - checker_x <9 and 0 <= 2 * y - checker_y < 9 \
                #         and self.board[2 * x - checker_x][2 * y - checker_y] in opposite_checkers:
                return True
        return False

    def is_checker_surrounded_to_castle(self, checker_location, opposite_checkers):
        for (x, y) in self.LOCATIONS_AROUND_CASTLE:
            if checker_location == (x, y):
                if x == 4 and self.board[x][2 * y - 4] in opposite_checkers:
                    return True
                if y == 4 and self.board[2 * x - 4][y] in opposite_checkers:
                    return True
                break
        return False

    def is_checker_surrounded(self, checker_location, opposite_checkers):
        return self.is_checker_surrounded_to_castle(checker_location, opposite_checkers) \
               or self.is_checker_surrounded_to_camp(checker_location, opposite_checkers) \
               or self.is_checker_surrounded_from_opposite_sides(checker_location, opposite_checkers)

    def is_game_over(self, possible_moves):
        """
        :return: Not finished - -1
                 Draw - 0
                 Defenders wins - 1
                 Attacker wins - 2
        """
        if not possible_moves:
            return 2 if self.is_player_one_to_move else 1
        king_location = (-1, -1)
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == PieceEnum.KING.value:
                    king_location = (i, j)
        if king_location[0] in (0, 8) or king_location[1] in (0, 8):
            return 1
        if self.is_king_surrounded(king_location):
            return 2
        if str(self) in self.old_boards[:-1]:
            return 0
        return -1


class TablutGame:
    def __init__(self):
        self.board = TablutBoard()
        self.current_player = 'D'  # Attacker goes first

    def game(self):
        winner = -1
        while winner == -1:
            self.print_board()
            move = input(f"Player {self.current_player}: Enter your move (e.g. 1 4 1 5): ")

            try:
                piece_x, piece_y, dest_x, dest_y = move.split()
                piece_x = int(piece_x)
                piece_y = int(piece_y)
                dest_x = int(dest_x)
                dest_y = int(dest_y)
            except ValueError:
                print("Invalid move")
                continue
            try:
                self.board.move_piece(piece_x, piece_y, dest_x, dest_y)
            except Exception as e:
                print(e)
                continue
            self.current_player = "D" if self.current_player == "A" else "A"
            possible_moves = self.board.get_all_possible_moves()
            winner = self.board.is_game_over(possible_moves)

        # Game over
        self.print_board()
        if winner == 2:
            print("Attacker wins!")
        elif winner == 1:
            print("Defender wins!")
        else:
            print("Draw!")

    def print_board(self):
        self.board.print_board()


if __name__ == "__main__":
    game = TablutGame()
    game.game()
