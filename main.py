import os
import time
import subprocess

NUXMV_PATH = r'C:\Users\ykupfer\Personal\nuXmv-2.0.0-win64\bin'
BOARD_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project\boards\board1.txt"
TEMP_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project"
LURD_PATH r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project"

NUXMV_PATH_ITAY = r'C:\Users\05ita\OneDrive - Bar-Ilan University - Students\לימודים\שנה ד\סמסטר א\אימות פורמלי\nuXmv-2.0.0-win64.tar\nuXmv-2.0.0-win64\nuXmv-2.0.0-win64\bin'
BOARD_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\boards\board1.txt"
TEMP_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\temp"
LURD_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\LURD"


def printBoard(board):
    print("**** SOKOBAN ****")
    for row in board:
        print(row)
    print("******************")


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


def run_nuxmv(model_filename, smv_path, temp_path, engine=None, k=None):
    start_time = time.time()

    full_path = os.path.join(temp_path, model_filename)

    if engine == "SAT":
        output_filename = model_filename.split('.')[0] + 'SAT.out'
    elif engine == "BDD":
        output_filename = model_filename.split('.')[0] + 'BDD.out'
    else:
        nuxmv_process = subprocess.Popen(["nuXmv.exe", full_path],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        output_filename = model_filename.split('.')[0] + '.out'
    os.chdir(temp_path)
    stdout, _ = nuxmv_process.communicate()
    with open(output_filename, 'w') as f:
        f.write(stdout)
    print(f"Output written to {output_filename}")

    end_time = time.time()


    return [output_filename, end_time - start_time]


def get_solution(output_filename, temp_path):
    current_path = os.getcwd()
    os.chdir(smv_path)
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

    # get current directory
    cwd = os.getcwd()

    #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
    os.chdir(temp_path)
    ###############################################################

    # a list to store the movements
    steps = []
    # a variable to store the last movement in case it doesn't change between State
    last_step = None

    # Open the file and iterate over the lines
    with open(output_filename, 'r') as file:
        for line in file:
            # If we find a line with 'State' we add the last movement to the list
            if 'State' in line:
                if last_step is not None:
                    steps.append(last_movement)
            # If we find a line with 'movement =' we extract the movement
            elif 'movement =' in line:
                last_movement = line.split('=')[-1].strip()
            elif 'Loop starts here' in line:
                break

    #change directory back to the original directory
    os.chdir(cwd)

    # Add the last movement if there is one
    if last_movement is not None:
        movements.append(last_movement)

    return movements[:-1]




if __name__ == "__main__":
    user_input = input("Does this computer belong to Itay (i) or Yonatan (y) ? ")
    if user_input == "y":
        board_path = BOARD_PATH
        smv_path = NUXMV_PATH
        temp_path = TEMP_PATH
        report_path = LURD_PATH
    else:
        board_path = BOARD_PATH_ITAY
        smv_path = NUXMV_PATH_ITAY
        temp_path = TEMP_PATH_ITAY
        report_path = LURD_PATH_ITAY

    board = []
    with open(board_path, 'r') as f:
        for line in f:
            board.append(list(line.strip('\n')))

    printBoard(board)

    smv_model = createSMVModel(board)

    model_filename = 'sokoban_model.smv'

    current_path = os.getcwd()
    os.chdir(temp_path)

    with open(model_filename, 'w') as f:
        f.write(smv_model)

    os.chdir(current_path)

    output_filename, runnning_time = run_nuxmv(model_filename, smv_path, temp_path)


