import os
import time
import subprocess

NUXMV_PATH = r'C:\Users\ykupfer\Personal\nuXmv-2.0.0-win64\bin'
BOARD_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project\boards\board1.txt"

def printBoard(board):
    print("****SOKOBAN****")
    for row in board:
        print(row)
    print("****************")


                                           

def get_initial_state(board):
    rows = len(board)

    cols = len(board[0])
    print(cols)
    init = ''
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#':
                init += f'init(board[{i}][{j}]) := Wall;\n\t\t'
            elif board[i][j] == '@':
                init += f'init(board[{i}][{j}]) := Keeper;\n\t\t'
            elif board[i][j] == '+':
                init += f'init(board[{i}][{j}]) := KeeperOnGoal;\n\t\t'
            elif board[i][j] == '$':
                init += f'init(board[{i}][{j}]) := Box;\n\t\t'
            elif board[i][j] == '*':
                init += f'init(board[{i}][{j}]) := BoxOnGoal;\n\t\t'
            elif board[i][j] == '.':
                init += f'init(board[{i}][{j}]) := Goal;\n\t\t'
            elif board[i][j] == '_':
                init += f'init(board[{i}][{j}]) := Floor;\n\t\t'

    return init

def get_transitions(board):
    rows = len(board)
    cols = len(board[0])

    moves_dict = {
        'l': (0, -1),
        'u': (-1, 0),
        'd': (1, 0),
        'r': (0, 1)
    }

    transitions = ''
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == '#': # Wall
                transitions += f'next(board[{i}][{j}]) := Wall;\n\t\t'
            else:
                transitions += f'\n\t\tnext(board[{i}][{j}]) := \n\t\tcase\n'
                
                for move, (dx,dy) in moves_dict.items():
                    ni, nj = i + dx, j + dy
                    transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & board[{ni}][{nj}] = Wall: board[{i}][{j}];\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Floor;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Goal;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{i-dx}][{j-dy}] = Keeper | board[{ni}][{nj}] = KeeperOnGoal): KeeperOnGoal;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{i-dx}][{j-dy}] = Keeper | board[{ni}][{nj}] = KeeperOnGoal): KeeperOnGoal;\n'

                    if 0 <= i + 2 * dx < rows and 0 <= j + 2 * dy < cols:
                        nni, nnj = i + 2 * dx, j + 2 * dy
                        transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Box | board[{nni}][{nnj}] = BoxOnGoal | board[{nni}][{nnj}] = Wall): board[{i}][{j}];\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Floor;\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Goal;\n'

                    transitions += f'\t\t\t(board[{i}][{j}] = Box | board[{i}][{j}] = BoxOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal | board[{ni}][{nj}] = Wall) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): board[{i}][{j}];\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Box & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): Keeper;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = BoxOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): KeeperOnGoal;\n'

                    if 0 <= i - 2 * dx < rows and 0 <= j - 2 * dy < cols:
                        ppi, ppj = i - 2 * dx, j - 2 * dy
                        transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): BoxOnGoal;\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): Box;\n'

                transitions += f'\t\t\tTRUE: board[{i}][{j}];\n'
                transitions += f'\t\tesac;\n\t\t'

    return transitions


def get_winning_condition(board):
    rows = len(board)
    cols = len(board[0])

    Goals_synbols = {'*', '.', '+'}

    winning_pos = [(x, y) for x in range(rows)for y in range(cols) if board[x][y] in Goals_synbols]


    winning_conditions = f'LTLSPEC !(F('
    for w in winning_pos:
        if w == winning_pos[-1]:
            winning_conditions += f'(board[{w[0]}][{w[1]}] = BoxOnGoal)'
            continue
        winning_conditions += f'(board[{w[0]}][{w[1]}] = BoxOnGoal) & '

    winning_conditions += '));'

    return winning_conditions


def createSMVModel(board):
    rows = len(board)
    cols = len(board[0])

    smv = f'''
    MODULE main
    VAR
        board : array 0..{rows-1} of array 0..{cols-1} of {{Keeper, KeeperOnGoal, Box, BoxOnGoal, Wall, Goal, Floor}};
        move : {{l, u, r, d}};

    ASSIGN
        {get_initial_state(board)}
    
        {get_transitions(board)}

    {get_winning_condition(board)}


    '''

    return smv


def run_nuxmv(model_filename, engine=None, k=None):
    start_time = time.time()

    os.chdir(NUXMV_PATH)
    if engine == "SAT":
        output_filename = model_filename.split('.')[0] + 'SAT.out'
    elif engine == "BDD":
        output_filename = model_filename.split('.')[0] + 'BDD.out'
    else:
        nuxmv_process = subprocess.Popen(['.\\nuxmv.exe', model_filename],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        output_filename = model_filename.split('.')[0] + '.out'
    
    stdout, _ = nuxmv_process.communicate()
    with open(output_filename, 'w') as f:
        f.write(stdout)
    print(f"Output written to {output_filename}")

    end_time = time.time()


    return [output_filename, end_time - start_time]


def get_solution(filename):
    current_path = os.getcwd()
    os.chdir(NUXMV_PATH)
    moves = []
    solved = False
    with open(filename, 'r') as f:
        for line in f:
            if 'is false' in line:
                solved = True
                break

        if solved:
            for line in f:
                pass



if __name__ == "__main__":
    board_path = BOARD_PATH

    board = []
    with open(board_path, 'r') as f:
        for line in f:
            board.append(list(line.strip('\n')))

    printBoard(board)

    smv_model = createSMVModel(board)

    model_filename = 'sokoban_model.smv'

    current_path = os.getcwd()
    os.chdir(NUXMV_PATH)

    with open(model_filename, 'w') as f:
        f.write(smv_model)

    os.chdir(current_path)

    output_filename, runnning_time = run_nuxmv(model_filename)


