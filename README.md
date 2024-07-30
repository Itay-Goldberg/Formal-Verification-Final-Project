# Formal-Verification-Final-Project
# Introduction
This program performs analysis on board configurations using nuXmv. The process involves setting paths, selecting a computer owner, choosing a board number, and running the analysis either normally or with specific mechanisms.

# Requirements
nuXmv installed
Board files in the format "board[i].txt" where i is an integer
# Setup
Change the paths in the program to the locations of the nuXmv bin folder (NUXMV_PATH) and the board files folder (BOARD_PATH).
# Usage
* Run the program (python main.py).
* When prompted, specify the computer you are using to run the software:
Don't enter "i" unless you are using Itays computer. Enter any other character for your computer.
* Input the board number you wish to analyze when prompted.
* Choose the type of run: Normal run or run according to one of the mechanisms tested in the assignment and select whether to create a new SMV file or use an existing one from the specified path.
# Notes
Ensure the board files are correctly named in the format board[i].txt where i is an integer.
Ensure the paths (NUXMV_PATH and BOARD_PATH) are correctly set before running the program.
