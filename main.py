import re
import os
import time
import subprocess
import shutil

NUXMV_PATH = r'C:\Users\ykupfer\Personal\nuXmv-2.0.0-win64\bin'
BOARD_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project\boards"
TEMP_PATH = r"C:\Users\ykupfer\Personal\foraml verification final project\FVS final project\temp"
LURD_PATH = r"C:\Users\ykupfer\Personal\foraml verification tfinal project\FVS final project\LURD"

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
        print(' '.join(row))
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
            elif board[i][j] == '-':
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
            if board[i][j] == '#':  # Wall
                transitions += f'next(board[{i}][{j}]) := Wall;\n\t\t'
            else:
                transitions += f'\n\t\tnext(board[{i}][{j}]) := \n\t\tcase\n'
                for move, (dx, dy) in moves_dict.items():
                    ni, nj = i + dx, j + dy
                    nni, nnj = i + 2 * dx, j + 2 * dy
                    transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & board[{ni}][{nj}] = Wall: board[{i}][{j}];\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Floor;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal): Goal;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{i - dx}][{j - dy}] = Keeper | board[{i - dx}][{j - dy}] = KeeperOnGoal): KeeperOnGoal;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{i - dx}][{j - dy}] = Keeper | board[{i - dx}][{j - dy}] = KeeperOnGoal): Keeper;\n'
                    if 0 <= nni < rows and 0 <= nnj < cols:
                        transitions += f'\t\t\t(board[{i}][{j}] = Keeper | board[{i}][{j}] = KeeperOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Box | board[{nni}][{nnj}] = BoxOnGoal | board[{nni}][{nnj}] = Wall): board[{i}][{j}];\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = Keeper & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Floor;\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = KeeperOnGoal & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal) & (board[{nni}][{nnj}] = Floor | board[{nni}][{nnj}] = Goal): Goal;\n'
                    if 0 <= i - 2 * dx < rows and 0 <= j - 2 * dy < cols:
                        ppi, ppj = i - 2 * dx, j - 2 * dy
                        transitions += f'\t\t\tboard[{i}][{j}] = Goal & move = {move} & (board[{i - dx}][{j - dy}] = Box | board[{i - dx}][{j - dy}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): BoxOnGoal;\n'
                        transitions += f'\t\t\tboard[{i}][{j}] = Floor & move = {move} & (board[{i - dx}][{j - dy}] = Box | board[{i - dx}][{j - dy}] = BoxOnGoal) & (board[{ppi}][{ppj}] = Keeper | board[{ppi}][{ppj}] = KeeperOnGoal): Box;\n'
                    transitions += f'\t\t\t(board[{i}][{j}] = Box | board[{i}][{j}] = BoxOnGoal) & move = {move} & (board[{ni}][{nj}] = Box | board[{ni}][{nj}] = BoxOnGoal | board[{ni}][{nj}] = Wall) & (board[{i - dx}][{j - dy}] = Keeper | board[{i - dx}][{j - dy}] = KeeperOnGoal): board[{i}][{j}];\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = Box & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i - dx}][{j - dy}] = Keeper | board[{i - dx}][{j - dy}] = KeeperOnGoal): Keeper;\n'
                    transitions += f'\t\t\tboard[{i}][{j}] = BoxOnGoal & move = {move} & (board[{ni}][{nj}] = Floor | board[{ni}][{nj}] = Goal) & (board[{i - dx}][{j - dy}] = Keeper | board[{i - dx}][{j - dy}] = KeeperOnGoal): KeeperOnGoal;\n'
                transitions += f'\t\t\tTRUE: board[{i}][{j}];\n'
                transitions += f'\t\tesac;\n\t\t'
    return transitions


def get_winning_condition(board):
    rows = len(board)
    cols = len(board[0])
    goal_symbols = {'*', '.', '+'}
    winning_pos = [(x, y) for x in range(rows) for y in range(cols) if board[x][y] in goal_symbols]
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
        board : array 0..{rows - 1} of array 0..{cols - 1} of {{Keeper, KeeperOnGoal, Box, BoxOnGoal, Wall, Goal, Floor}};
        move : {{l, u, r, d}};

    ASSIGN
        {get_initial_state(board)}

        {get_transitions(board)}

    {get_winning_condition(board)}
    '''
    return smv

def run_nuxmv(model_filename, smv_path, temp_path, engine=None, k=None):
    source = os.path.join(temp_path, model_filename)
    dest = os.path.join(smv_path, model_filename)
    shutil.copy(source, dest)

    print(f"Model copied from {source} to {dest}")

    start_time = time.time()
    os.chdir(smv_path)
    base_command = ["./nuXmv"]

    full_path = os.path.join(smv_path, model_filename)
    print(f"Running nuXmv on {full_path} with engine {engine} and bound {k}")

    try:
        if engine == "SAT":
            output_filename = model_filename.split('.')[0] + '_SAT_' + str(k) + '.out'
            args = ["./nuXmv", "-int", model_filename]
            nuxmv_process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, universal_newlines=True)
            nuxmv_process.stdin.write("go_bmc\n")
            nuxmv_process.stdin.write(f"check_ltlspec_bmc -k {k}\n")
            nuxmv_process.stdin.write("quit\n")
        elif engine == "BDD":
            output_filename = model_filename.split('.')[0] + '_BDD.out'
            nuxmv_process = subprocess.Popen(base_command + ["-int"],
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             universal_newlines=True)
            nuxmv_process.stdin.write(f"read_model -i {full_path}\n")
            nuxmv_process.stdin.write("go\n")
            nuxmv_process.stdin.write("check_ltlspec\n")
            nuxmv_process.stdin.write("quit\n")
        else:
            nuxmv_process = subprocess.Popen(base_command + [model_filename],
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             universal_newlines=True)
            output_filename = model_filename.split('.')[0] + '.out'

        stdout, stderr = nuxmv_process.communicate()
        print("nuXmv process completed")
        print("stdout:", stdout)
        print("stderr:", stderr)

        if stderr:
            print("Error encountered while running nuXmv:")
            print(stderr)
            raise RuntimeError("nuXmv process failed")

        os.chdir(temp_path)
        with open(output_filename, 'w') as f:
            f.write(stdout)

        end_time = time.time()

        print(f"Output saved to {output_filename}")
        print(f"Runtime: {end_time - start_time} seconds")

        return output_filename, end_time - start_time

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def get_solution(output_filename, temp_path):
    print(output_filename)
    current_path = os.getcwd()
    os.chdir(temp_path)

    steps = []
    last_move = None  # Track the last known move
    state_counter = 0
    move_counter = 0
    skip_first_move = False
    is_loop = False
    without_move = False

    try:
        with open(output_filename, 'r') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                line = lines[i].strip()

                if '-- Loop starts here' in line:
                    # Stop processing moves once a loop is detected
                    is_loop = True
                    break

                if '-> State:' in line:
                    state_counter += 1  # Increment state counter
                    without_move = True

                    if state_counter == 2 and i + 1 < len(lines) and 'move =' in lines[i + 1]:
                        skip_first_move = True  # Set flag to skip the first move

                    # Only append the last move if there has been a state change without a new move
                    if state_counter > move_counter and last_move is not None:
                        print(f"step1: {state_counter}")
                        print(f"move_c1: {move_counter}")
                        print(f"last_move1: {last_move}")
                        steps.append(last_move)
                        move_counter += 1

                elif 'move =' in line:
                    # Update the last known move when a move is explicitly specified
                    last_move = line.split('=')[-1].strip()
                    without_move = False

                    # Append the move and increment the move counter
                    if state_counter >= move_counter and move_counter:
                        print(f"step2: {state_counter}")
                        print(f"move_c2: {move_counter}")
                        print(f"last_move2: {last_move}")
                        steps.append(last_move)
                    move_counter += 1

                elif 'is true' in line:
                    # Handle unsolvable case
                    return ['Not solvable']

    except FileNotFoundError:
        return ['The run results cannot be analyzed because the SMV file has not been run before']

    os.chdir(current_path)

    if skip_first_move:
        steps = steps[1:]

    if is_loop or not without_move:
        return steps[:-1]
    else:
        return steps









def iterative_solver(board, model_filename, k):
    state_to_symbol, goal_symbols, goals = prepare_solver(board)

    solution = []
    total_time = 0
    original_board = [row[:] for row in board]  # Backup original board

    for iteration, goal in enumerate(goals, 1):
        print(f"\nIteration number {iteration}: Targeting goal at {goal}")

        # Reset board to its original configuration
        board = [row[:] for row in original_board]

        # Prepare the board for the current iteration's goal
        setup_board_for_goal(board, goals, goal)

        print("Current board setup:")
        printBoard(board)

        # Generate and run the model
        iter_model_filename = f'{model_filename.split(".")[0]}_iter{iteration}.smv'
        smv_model = createSMVModel(board)
        write_model_to_file(smv_model, iter_model_filename)

        output_filename, iteration_time = run_nuxmv(iter_model_filename, smv_path, temp_path, "SAT", k)
        total_time += iteration_time
        current_moves = get_solution(output_filename, temp_path)
        solution.append(current_moves)

        print(f"Solution for iteration {iteration}: {current_moves}")
        update_board_from_model_output(board, output_filename, state_to_symbol)
        printBoard(board)

    print(f"\n\nThe final solution is: {solution} \nTotal number of iterations: {iteration} \nTotal time for the given board: {total_time}")

def reintegrate_keeper(board):
    # Ensure there is only one keeper on the board at any time
    keeper_found = False
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell in {'@', '+'}:
                if keeper_found:
                    board[i][j] = '-' if cell == '@' else '.'
                keeper_found = True

def prepare_solver(board):
    # Mapping of states to symbols used on the board
    state_to_symbol = {
        'Keeper': '@',
        'KeeperOnGoal': '+',
        'Box': '$',
        'BoxOnGoal': '*',
        'Wall': '#',
        'Goal': '.',
        'Floor': '-'
    }

    # Define goal symbols for quick reference
    goal_symbols = {'+', '.'}  # Goal positions can be empty goals or keeper on goal

    # Identify all goals on the board
    goals = [(x, y) for x in range(len(board)) for y in range(len(board[0])) if board[x][y] in goal_symbols]

    return state_to_symbol, goal_symbols, goals


def setup_board_for_goal(board, goals, current_goal):
    # Clear goals and set the current goal
    for x, y in goals:
        if board[x][y] == '*':
            board[x][y] = '$'  # Revert box on goal to just box
        elif board[x][y] == '+':
            board[x][y] = '@'  # Revert keeper on goal to just keeper
        elif board[x][y] == '.':
            board[x][y] = '-'  # Revert goal to floor

    # Set current goal
    if board[current_goal[0]][current_goal[1]] == '@':
        board[current_goal[0]][current_goal[1]] = '+'
    elif board[current_goal[0]][current_goal[1]] == '$':
        board[current_goal[0]][current_goal[1]] = '*'
    else:
        board[current_goal[0]][current_goal[1]] = '.'

def write_model_to_file(smv_model, filename):
    with open(os.path.join(temp_path, filename), 'w') as f:
        f.write(smv_model)


def update_board_from_model_output(board, output_filename, state_to_symbol):
    with open(output_filename, 'r') as file:
        model_output = file.readlines()
    for line in model_output:
        match = re.search(r'board\[(\d+)\]\[(\d+)\] = (\w+)', line)
        if match:
            i, j, state = int(match.group(1)), int(match.group(2)), match.group(3)
            board[i][j] = state_to_symbol[state]


def reintroduce_goals(board, goal_statuses):
    for (x, y), achieved in goal_statuses.items():
        if not achieved:
            if board[x][y] == '@':
                board[x][y] = '+'
            elif board[x][y] == '-':
                board[x][y] = '.'
            elif board[x][y] == '$':
                board[x][y] = '*'


def update_goal_statuses(board, goals, goal_statuses):
    for x, y in goals:
        if board[x][y] == '*':
            goal_statuses[(x, y)] = True  # Goal achieved if a box is on it
        else:
            goal_statuses[(x, y)] = False  # Goal not achieved

if __name__ == "__main__":
    user_input = input("Does this computer belong to Itay (i) or Yonatan (y) ?\n")
    board_num = input("Select the board number you would like to examine (1-8)\n")
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

    with open(os.path.join(temp_path, model_filename), 'w') as f:
        f.write(smv_model)

    board_analyzing = input(
        "What would you like to do?\n(1) run " + model_filename + "\n(2) run " + model_filename + " in BDD mode\n(3) run " + model_filename + " in SAT mode\n(4) run iterative mode\n(5) receive the analysis of the results\n(6) run full test\n")
    if board_analyzing == "1":
        print(model_filename + " is running normal...")
        output_filename, runnning_time1 = run_nuxmv(model_filename, smv_path, temp_path)
        print("The runnning time is " + str(runnning_time1))
    elif board_analyzing == "2":
        print(model_filename + " is running BDD...")
        output_filename, runnning_time2 = run_nuxmv(model_filename, smv_path, temp_path, "BDD")
        print("The runnning time is " + str(runnning_time2))
    elif board_analyzing == "3":
        k = input("k = ")
        print(model_filename + f" is running SAT with k={k}...")
        output_filename, runnning_time3 = run_nuxmv(model_filename, smv_path, temp_path, "SAT", k)
        print("The runnning time is " + str(runnning_time3))
    elif board_analyzing == "4":
        k = input("k = ")
        print(model_filename + f" iterative solver with k={k}...")
        iterative_solver(board, model_filename, k)
    elif board_analyzing == "5":
        output_filename = model_filename.split('.')[0] + '.out'
    else:
        k = input("k = ")
        print(model_filename + " is running normal...")
        output_filename1, runnning_time1 = run_nuxmv(model_filename, smv_path, temp_path)
        steps = get_solution(output_filename1, temp_path)
        print("This is the solution for the tested board")
        print(steps)

        print(model_filename + " is running BDD...")
        output_filename2, runnning_time2 = run_nuxmv(model_filename, smv_path, temp_path, "BDD")
        print("The runnning time is " + str(runnning_time2))
        steps = get_solution(output_filename2, temp_path)
        print("This is the solution for the tested board")
        print(steps)

        print(model_filename + f" is running SAT with k={k}...")
        output_filename3, runnning_time3 = run_nuxmv(model_filename, smv_path, temp_path, "SAT", k)
        print("The runnning time is " + str(runnning_time3))
        steps = get_solution(output_filename3, temp_path)
        print("This is the solution for the tested board")
        print(steps)

        print(f"time comparing:\nnormal run: {runnning_time1}.\nBDD run: {runnning_time2}.\nSAT run: {runnning_time3}.")

    if int(board_analyzing) <= 5 and int(board_analyzing) != 4:
        steps = get_solution(output_filename, temp_path)
        print("This is the solution for the tested board")
        print(steps)
