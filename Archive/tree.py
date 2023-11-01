from utils import State, Entity


def possible_moves(state:State):
    possible_states = []

    for i in range(len(state.state)):
        for j in range(len(state.state[0])):
            if state.state[i][j] in [Entity.white, Entity.king]:
                ## horizontal
                j_index = j 
                while True:
                    j_index += 1
                    if state.state[i][j_index] in [Entity.square, Entity.escape] and j_index in range(0,9):
                        new_board = state.state
                        new_board[i][j_index] = "W"
                        new_board[i][j] = "O" 
                        new_state = State(last_move="W", state=new_board)
                        possible_states.append(new_state)
                ...



class Node:
    def __init__(self, parent, state:State, children:list) -> None:
        self.parent = parent
        self.state = state 
        self.children = children
        self.score = 0

class Tree:
    def __init__(self, root:Node) -> None:
        self.root = root 
    
    def explore_node(self, node:Node):
        pass


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

possible_moves(state_0)