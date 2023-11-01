from Utils import State, Entity
from copy import deepcopy

class Node:
    def __init__(self, parent, state:State, children:list, name = "H") -> None:
        self.parent = parent
        self.state = state 
        self.children = children
        self.score = 0

    def possible_moves(self, black_or_white="W"):
        possible_states = []
        node = self.state
        for i in range(len(node.board)):
            for j in range(len(node.board[0])):
                if node.board[i][j] in [Entity.white, Entity.king]:
                    ## possible move  
                    possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
                    for rl, ud in possible_directions:
                        counter = 0
                        while True:
                            counter += 1
                            new_i = i + counter*rl  
                            new_j = j + counter*ud
                            if inside_board(node, new_i, new_j) and node.board[new_i][new_j] in [Entity.square, Entity.escape]:
                                possible_states.append((i, j, new_i, new_j))
                            else: break
        return possible_states
    
    def expand_node(self, moves:list):
        for move in moves:
            i, j, new_i, new_j = move
            new_state = deepcopy(self.state.board)
            new_state[new_i][new_j] = new_state[i][j]
            new_state[i][j] = State().board[i][j] 
            new_node = Node(parent=self, state=new_state, children=[])
            self.children.append(new_node)

class Tree:
    def __init__(self, root:Node) -> None:
        self.root = root 
        moves = self.root.possible_moves()
        self.root.expand_node(moves)

    def highest_score_child(): pass 
    def black_random_select(): pass 


def inside_board(state, i, j):
    board_size = len(state.board)
    return 0 <= i < board_size and 0 <= j < board_size


initial_state = [
    ['O', '*', '*', 'B', 'B', 'B', '*', '*', 'O'],
    ['*', 'O', 'O', 'O', 'B', 'O', 'O', 'O', '*'],
    ['*', 'O', 'O', 'O', 'W', 'O', 'O', 'O', '*'],
    ['B', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'B'],
    ['B', 'B', 'W', 'W', 'K', 'W', 'W', 'B', 'B'],
    ['B', 'O', 'O', 'O', 'W', 'O', 'O', 'O', 'B'],
    ['*', 'O', 'O', 'O', 'W', 'O', 'O', 'O', '*'],
    ['*', 'O', 'O', 'O', 'B', 'O', 'O', 'O', '*'],
    ['O', '*', '*', 'B', 'B', 'B', '*', '*', 'O']
    ]

state_0 = State(initial_state, "I")
game_tree = Tree( Node(None, state_0, []) )

...