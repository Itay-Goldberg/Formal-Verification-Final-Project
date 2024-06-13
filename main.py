import os
import time
import subprocess

NUXMV_PATH = r'C:\Users\ykupfer\Personal\nuXmv-2.0.0-win64\bin'
BOARD_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project\boards"
TEMP_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project"
LURD_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project"

NUXMV_PATH_ITAY = r'C:\Users\05ita\OneDrive - Bar-Ilan University - Students\לימודים\שנה ד\סמסטר א\אימות פורמלי\nuXmv-2.0.0-win64.tar\nuXmv-2.0.0-win64\nuXmv-2.0.0-win64\bin'
BOARD_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\boards"
TEMP_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\temp"
LURD_PATH_ITAY = r"C:\Users\05ita\Desktop\code_files\py_files\formalVS_files\LURD"


def printBoard(board):
    n = len(board)
    m = len(board[0])
    print("Board Size: " + str(n) + " X " + str(m))
    print("* * * * * * * * * * * * * * * * * * * *")
    for row in board:
        print(row)
    print("* * * * * * * * * * * * * * * * * * * *")


def get_initial_state(board):
    rows = len(board)

    cols = len(board[0])
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
                    nni, nnj = i + 2 * dx, j + 2 * dy

                    # First Order - Effects of Steps
                    # Step towards a wall - standing still
                    transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & board[{ni}][{nj}] = Wall: board[{i}][{j}];\n'
                    # A Keeper's step towards a floor - leaving a square as floor
                    transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Floor;\n'
                    # A KeeperOnGoal's step towards a floor - leaving a square as Goal
                    transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Goal;\n'
                    # A Goal square stped by a Keeper - become a KeeperOnGoal
                    transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): KeeperOnGoal;\n'
                    # A Floor square stped by a Keeper/KeeperOnGoal - become a Keeper
                    transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): Keeper;\n'

                    # Second Order - Effects of Steps
                    # A box/BoxOnGoal square that is blocked in the direction of the step by a box/BoxOnGoal or wall when the Keeper/KeeperOnGoal is facing the direction of the square - unchanged
                    transitions += f'\t\t\t(board[{i}][{j}] = Box | board[{i}][{j}] = BoxOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal | board[{ni}][{nj}] = Wall) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): board[{i}][{j}];\n'
                    # A box square that is'nt blocked in the direction of the step when the Keeper/KeeperOnGoal is facing the direction of the square - become a Keeper
                    transitions += f'\t\t\tboard[{i}][{j}] = Box & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): Keeper;\n'
                    # A BoxOnGoal square that is'nt blocked in the direction of the step when the Keeper/KeeperOnGoal is facing the direction of the square - become a KeeperOnGoal
                    transitions += f'\t\t\tboard[{i}][{j}] = BoxOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i-dx}][{j-dy}] = Keeper | board[{i-dx}][{j-dy}] = KeeperOnGoal): KeeperOnGoal;\n'

                    if 0 <= nni < rows and 0 <= nnj < cols:
                        # A Keeper's/KeeperOnGoal's step towards a Box/BoxOnGoal that is blocked in the direction of the step by Box/BoxOnGoal/wall - standing still
                        transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Box | board[{nni}][{nnj}] = BoxOnGoal | board[{nni}][{nnj}] = Wall): board[{i}][{j}];\n'
                        # A Keeper's step towards a Box/BoxOnGoal that is'nt blocked in the direction of the step (floor/Goal) - become a Floor
                        transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Floor;\n'
                        # A KeeperOnGoal's step towards a Box/BoxOnGoal that is'nt blocked in the direction of the step (floor/Goal) - become a Goal
                        transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Goal;\n'


                    if 0 <= i - 2 * dx < rows and 0 <= j - 2 * dy < cols:
                        ppi, ppj = i - 2 * dx, j - 2 * dy
                        # A Goal square that have a box/BoxOnGoal fron the direction of the step when the Keeper/KeeperOnGoal is facing the direction of the box/BoxOnGoal - become a BoxOnGoal
                        transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{i-dx}][{j-dy}] = Box | board[{i-dx}][{j-dy}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): BoxOnGoal;\n'
                        # A Floor square that have a box/BoxOnGoal fron the direction of the step when the Keeper/KeeperOnGoal is facing the direction of the box/BoxOnGoal - become a Box
                        transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{i-dx}][{j-dy}] = Box | board[{i-dx}][{j-dy}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): Box;\n'

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
        output_filename = model_filename.split('.')[0] + '_SAT_' + str(k) + '.out'
        # Run the command
        nuxmv_process = subprocess.Popen(["nuXmv.exe", "-int", full_path],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        nuxmv_process.stdin.write("go_bmc\n")
        nuxmv_process.stdin.write(f"check_ltlspec_bmc -k " + str(k) + "\n")
        # enter ctrl+c to exit
        nuxmv_process.stdin.write("quit\n")
    elif engine == "BDD":
        output_filename = model_filename.split('.')[0] + '_BDD.out'
        # Run the command
        nuxmv_process = subprocess.Popen(["nuXmv.exe", "-int", full_path],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
        nuxmv_process.stdin.write("go\n")
        nuxmv_process.stdin.write(f"check_ltlspec\n")
        # enter ctrl+c to exit
        nuxmv_process.stdin.write("quit\n")
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
    # print(f"Output written to {output_filename}")

    end_time = time.time()


    return [output_filename, end_time - start_time]


def get_solution(output_filename, temp_path):
    current_path = os.getcwd()
    os.chdir(temp_path)

    steps = []
    Loop_starts_here_counter = 0
    state_counter = 0

    try:
        with open(output_filename, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                line = lines[i]

                if 'Loop starts here' in line:
                    if Loop_starts_here_counter == 1:
                        os.chdir(current_path)
                        return steps
                    else:
                        Loop_starts_here_counter += 1
                elif 'move =' in line:
                    if Loop_starts_here_counter == 1:
                        continue
                    # Check if the line located two lines ahead also contains "move ="
                    if i + 2 < len(lines) and 'move =' in lines[i + 2]:
                        continue
                    else:
                        step = line.split('=')[-1].strip()
                        steps.append(step)
                elif  i > 1 and 'State:' in line and 'move =' not in lines[i-1] and state_counter > 0:
                        steps.append(step)
                elif 'State:' in line:
                    state_counter += 1
                elif 'is true' in line:
                    return ['Not solvable']

    except FileNotFoundError:
        return ['The run results cannot be analyzed because the smv file has not been run before']
    
    os.chdir(current_path)
    return steps[:-1]


if __name__ == "__main__":
    user_input = input("Does this computer belong to Itay (i) or Yonatan (y) ?\n")
    board_num = input("Select the board number you would like to examine (1-7)\n")
    board_name = "board" + board_num + ".txt"
    if user_input == "y":
        board_path = os.path.join(BOARD_PATH, board_name)
        smv_path = NUXMV_PATH
        temp_path = TEMP_PATH
        report_path = LURD_PATH
    else:
        board_path = os.path.join(BOARD_PATH_ITAY, board_name)
        smv_path = NUXMV_PATH_ITAY
        temp_path = TEMP_PATH_ITAY
        report_path = LURD_PATH_ITAY

    board = []
    with open(board_path, 'r') as f:
        for line in f:
            board.append(list(line.strip('\n')))
    
    board_name = board_name.split('.')[0]
    model_filename = 'sokoban_model_' + str(board_name) + '.smv'

    print("This is what the board you chose to examine looks like")
    printBoard(board)

    smv_model = createSMVModel(board)

    current_path = os.getcwd()
    os.chdir(temp_path)

    with open(model_filename, 'w') as f:
        f.write(smv_model)

    os.chdir(current_path)

    board_analyzing = input("What would you like to do?\n(1) run " + model_filename + "\n(2) run " + model_filename + " in BDD mode\n(3) run " + model_filename + " in SAT mode\n(4) receive the analysis of the results\n")
    if board_analyzing == "1":
        print(model_filename + " is running...")
        output_filename, runnning_time = run_nuxmv(model_filename, smv_path, temp_path)
    elif board_analyzing == "2":
        print(model_filename + " is running...")
        output_filename, runnning_time = run_nuxmv(model_filename, smv_path, temp_path, "BDD")
        print("The runnning time is " + str(runnning_time))
    elif board_analyzing == "3":
        k = input("k = ")
        print(model_filename + " is running...")
        output_filename, runnning_time = run_nuxmv(model_filename, smv_path, temp_path, "SAT", k)
        print("The runnning time is " + str(runnning_time))
    else:
        output_filename = model_filename.split('.')[0] + '.out'
    steps = get_solution(output_filename, temp_path)
    print("This is the solution for the tested board")
    print(steps)


