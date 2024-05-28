

def generate_smv(board):
    rows = len(board)
    cols = len(board[0])
    
    # Define position labels
    positions = [(i, j) for i in range(rows) for j in range(cols)]
    
    # Initialize the SMV model
    smv_model = ["MODULE main"]
    smv_model.append("VAR")
    
    # Define variables for each position
    for (i, j) in positions:
        smv_model.append(f"    pos_{i}_{j} : {{empty, wall, box, goal, player}};")
    
    # Define initial state
    smv_model.append("ASSIGN")
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#':
                smv_model.append(f"    init(pos_{i}_{j}) := wall;")
            elif board[i][j] == '.':
                smv_model.append(f"    init(pos_{i}_{j}) := empty;")
            elif board[i][j] == '$':
                smv_model.append(f"    init(pos_{i}_{j}) := box;")
            elif board[i][j] == 'G':
                smv_model.append(f"    init(pos_{i}_{j}) := goal;")
            elif board[i][j] == '@':
                smv_model.append(f"    init(pos_{i}_{j}) := player;")
    
    # Define transition relations
    smv_model.append("TRANS")
    smv_model.append("    -- Define transition relations here")
    # Define basic movement and box pushing transitions (to be detailed)
    
    # Define the win condition
    goal_positions = [(i, j) for i in range(rows) for j in range(cols) if board[i][j] == 'G']
    win_condition = " & ".join([f"pos_{i}_{j} = box" for (i, j) in goal_positions])
    smv_model.append(f"SPEC AG ({win_condition})")
    
    return "\n".join(smv_model)

# Example usage
board1 = [
    ['#', '#', '#', '#', '#'],
    ['#', '@', '$', '.', '#'],
    ['#', '#', '#', '#', '#']
]
board2 = [
    ['#', '#', '#', '#', '#'],
    ['#', '$', '@', '.', '#'],
    ['#', '#', '#', '#', '#']
]
board3 = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '@', '_', '_', '_', '_', '#'],
    ['#', '_', '_', '.', '$', '_', '#'],
    ['#', '_', '_', '_', '#', '#', '#'],
    ['#', '_', '_', '$', '_', '_', '#'],
    ['#', '_', '_', '_', '#', '.', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]
board4 = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '@', '_', '_', '_', '_', '#'],
    ['#', '_', '_', '_', '.', '.', '#'],
    ['#', '_', '_', '#', '$', '$', '#'],
    ['#', '_', '_', '#', '_', '_', '#'],
    ['#', '_', '_', '#', '_', '_', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]
board5 = [
    ['#', '#', '#', '#', '#', '#','#','#'],
    ['#', '@', '_', '_', '_' ,'_','_','#'],
    ['#', '_', '_', '_', '_' ,'#','#','#'],
    ['#', '_', '$', '_', '#' ,'_','_','#'],
    ['#', '_', '_', '_', '#' ,'_','$','#'],
    ['#', '_', '.', '_', '#' ,'_','.','#'],
    ['#', '#', '#', '#', '#' ,'#','#','#']
]
board6 = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '_', '_', '_', '_', '_', '_', '#', '#', '#', '#'],
    ['#', '_', '_', '#', '_', '_', '_', '.', '#', '#', '#'],
    ['#', '_', '$', '_', '_', '_', '_', '_', '#', '#', '#'],
    ['#', '_', '_', '@', '#', '_', '_', '_', '#', '#', '#'],
    ['#', '#', '#', '_', '_', '_', '_', '*', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '_', '_', '_', '_', '_', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '_', '_', '_', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '_', '_', '_', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]
boards = [board1, board2, board3, board4, board5, board6]
for board in boards:
    smv_output = generate_smv(board)
    print(f'{smv_output}')
    print("-------------------------------------------------------------------------------------")