import os 
from PIL import Image, ImageDraw


class Entity:
    square = "O"
    escape = "*"
    castle = "+"
    camp = "0"
    white = "W" 
    black = "B"
    king = "K"

class LastMoves:
    white = "W"
    black = "B"
    initial_state = "I"

class State:
    def __init__(self, state=None, last_move=None) -> None:
        self.last_move = last_move
        if not state:
            self.state = [
            ['O', '*', '*', '0', '0', '0', '*', '*', 'O'],
            ['*', 'O', 'O', 'O', '0', 'O', 'O', 'O', '*'],
            ['*', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '*'],
            ['0', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '0'],
            ['0', '0', 'O', 'O', '+', 'O', 'O', '0', '0'],
            ['0', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '0'],
            ['*', 'O', 'O', 'O', 'O', 'O', 'O', 'O', '*'],
            ['*', 'O', 'O', 'O', '0', 'O', 'O', 'O', '*'],
            ['O', '*', '*', '0', '0', '0', '*', '*', 'O']
            ]
        else: 
            self.state = state
    
    def __str__(self) -> str:
        border = "+---" * len(self.state[0]) + "+"
        string = f"Moved By: {self.last_move} \n"
        string += border + "\n"
        for row in self.state:
            string += "| " + " | ".join(row) + " |" + "\n"
            string += border  + "\n"
        return string

    def visualize_board(self):
        white_img_path = Image.open(r"D:\tablut_bot\Assets\w.png")
        black_img_path = Image.open(r"D:\tablut_bot\Assets\b.png")
        king_img_path = Image.open(r"D:\tablut_bot\Assets\k.png")
        empty_cell_color = (255,233,127)
        
        square_size = 40  # Adjust the size of each square as needed
        board_width = len(self.state[0]) * square_size
        board_height = len(self.state) * square_size

        board_image = Image.new("RGB", (board_width, board_height), "white")
        draw = ImageDraw.Draw(board_image)

        for row_idx, row in enumerate(self.state):
            for col_idx, cell in enumerate(row):
                left = col_idx * square_size
                top = row_idx * square_size
                right = left + square_size
                bottom = top + square_size
                

                # You can customize this part to load and paste the appropriate image based on the 'cell' value
                if cell == Entity.white:
                    cell_image = white_img_path
                elif cell == Entity.black:
                    cell_image = black_img_path
                elif cell == Entity.king:
                    cell_image = king_img_path
                else:
                    cell_image = Image.new("RGB", (square_size, square_size), empty_cell_color)

                cell_image = cell_image.resize((square_size, square_size), Image.ANTIALIAS)
                board_image.paste(cell_image, (left, top, right, bottom))
                # Draw a border (grid line) between cells
                draw.rectangle((left, top, right, bottom), outline="black")

        board_image.show()  # Show the board using the default image viewer


class Record:
    def __init__(self) -> None:
        self.states = []
        self.winner = None

    def add_state(self, state:State):
        self.states.append(state)

def convert_dataset_txt_to_record(txt_path):
    with open(txt_path, 'r') as t:
        string_data = t.read()
    data_blocks = string_data.split('-\n')
    
    record = Record()

    for db in data_blocks[:-1]:
        new_state = State()

        mvd_by = db.split("\n")[0]
        if mvd_by == "W":
            new_state.last_move = LastMoves.white
        elif mvd_by == "B":
            new_state.last_move = LastMoves.black
        else:
            new_state.last_move = LastMoves.initial_state
        
        board_state_str = db.split("Stato:")[1]
        board_state = [list(a.strip()) for a in board_state_str.split("\n")]
        for r in board_state: 
            if not r:
                board_state.remove(r) 
        for i, row in enumerate(board_state):
            for j, sqr in enumerate(row):
                if sqr == 'W': new_state.state[i][j] = 'W'
                elif sqr == 'B': new_state.state[i][j] = 'B'
                elif sqr == 'K': new_state.state[i][j] = 'K'

        record.add_state(new_state)
    
    winner_state = data_blocks[-1].strip("\n")
    if winner_state == "WW":
        record.winner = Entity.white
    elif winner_state == "BW":
        record.winner = Entity.black
    elif winner_state == "D":
        record.winner = 'D'
    else:
        return
    
    record.states[-1].visualize_board()
    return record


if __name__ == "__main__":
    dataset_path = "Dataset"
    dataset_files = []
    for filename in os.listdir(dataset_path): 
        if filename.endswith("txt"):
            dataset_files.append(os.path.join(dataset_path, filename))

    records = []
    for df in dataset_files:
        data_record = convert_dataset_txt_to_record(df)
        if data_record:
            records.append(data_record)
    ...