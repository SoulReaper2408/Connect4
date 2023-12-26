#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import time

class GameTreePlayer:

    def __init__(self):
        self.recursions=0
        pass
    
    def FindBestAction(self, currentState):
        bestAction = self.minimax(currentState, 5, 2, float('-inf'), float('inf'))[1]
        return bestAction

    # def minimax(self, game_state, depth, current_player):
    #     if depth == 0 or self.is_game_over(game_state):
    #         return self.evaluate_state(game_state), None

    #     best_score = float('-inf') if current_player == 2 else float('inf')
    #     best_action = None

    #     available_actions = self.get_all_available_actions(game_state)

    #     for action in available_actions:
    #         new_state = self.apply_action(game_state, action, current_player)
    #         child_score, _ = self.minimax(new_state, depth - 1, 3 - current_player)

    #         self.recursions += 1

    #         if (current_player == 2 and child_score > best_score) or (current_player == 1 and child_score < best_score):
    #             best_score = child_score
    #             best_action = action

    #     return best_score, best_action
    # def minimax(self, game_state, depth, current_player, alpha=float('-inf'), beta=float('inf')):
    #     if depth == 0 or self.is_game_over(game_state):
    #         return self.evaluate_state(game_state), None

    #     best_score = float('-inf') if current_player == 2 else float('inf')
    #     best_action = None

    #     available_actions = self.get_all_available_actions(game_state)

    #     for action in available_actions:
    #         new_state = self.apply_action(game_state, action, current_player)
    #         child_score, _ = self.minimax(new_state, depth - 1, 3 - current_player, alpha, beta)

    #         self.recursions += 1

    #         if current_player == 2 and child_score > best_score:
    #             best_score = child_score
    #             best_action = action
    #             alpha = max(alpha, best_score)
    #         elif current_player == 1 and child_score < best_score:
    #             best_score = child_score
    #             best_action = action
    #             beta = min(beta, best_score)

    #         if beta <= alpha:
    #             break

    #     return best_score, best_action
    def minimax(self, game_state, depth, current_player, alpha, beta):
        if depth == 0 or self.is_game_over(game_state):
            return self.evaluate_state(game_state), None

        best_score = float('-inf') if current_player == 2 else float('inf')
        best_action = None

        ordered_actions = self.get_best_action_order(game_state)

        for action in ordered_actions:
            new_state = self.apply_action(game_state, action, current_player)
            child_score, _ = self.minimax(new_state, depth - 1, 3 - current_player, alpha, beta)

            self.recursions += 1

            if (current_player == 2 and child_score > best_score) or (current_player == 1 and child_score < best_score):
                best_score = child_score
                best_action = action

            if current_player == 2:
                alpha = max(alpha, child_score)
            else:
                beta = min(beta, child_score)

            if beta <= alpha:
                break

        return best_score, best_action


    def get_best_action_order(self, game_state):
        available_actions = self.get_all_available_actions(game_state)
        ordered_actions = sorted(available_actions, key=lambda action: self.calculate_state_value(game_state, action, 2), reverse=True)
        return ordered_actions

    def calculate_state_value(self, game_state, action, player):
        # Returns a heuristic value indicating how good the state would be after the specified action
        new_state = self.apply_action(game_state, action, player)
        return self.evaluate_state(new_state)

    def evaluate_state(self, game_board):
        def calculate_rewards(window, current_player, opponent):
            current_player_count = sum(1 for cell in window if cell == current_player)
            opponent_count = sum(1 for cell in window if cell == opponent)

            if current_player_count == 4:
                return 2000
            elif current_player_count == 3 and opponent_count == 0:
                return 100
            elif current_player_count == 2 and opponent_count == 0:
                return 10
            elif opponent_count == 3 and current_player_count == 0:
                return -100
            elif opponent_count == 4:
                return -2000

            # Default case if none of the above conditions are met
            return 0

        def generate_windows(board):
            # Helper function to generate all possible windows
            windows = []
            for row in board:
                for col in range(len(row) - 3):
                    windows.append(row[col:col + 4])

            for col in range(len(board[0])):
                for row in range(len(board) - 3):
                    windows.append([board[row + i][col] for i in range(4)])

            for row in range(len(board) - 3):
                for col in range(len(board[0]) - 3):
                    windows.append([board[row + i][col + i] for i in range(4)])

            for row in range(len(board) - 3):
                for col in range(3, len(board[0])):
                    windows.append([board[row + i][col - i] for i in range(4)])

            return windows

        total_score = 0

        # Generate all possible windows
        all_windows = generate_windows(game_board)

        # Check each window
        for window in all_windows:
            total_score += calculate_rewards(window, 2, 1)  # Player 2 is maximizing
            
        center_array = [int(row[len(row) // 2]) for row in game_board]
        center_count = center_array.count(2)  # Assuming 2 represents the player's piece

        # Add score based on the count
        total_score += center_count * 10

        return total_score

    def is_game_over(self, game_state):
        def is_winning_window(window, player):
            return window.count(player) == 4

        def check_windows(player):
            # Helper function to check for winning windows for a specific player

            # Check horizontal windows
            for row in game_state:
                for col in range(len(row) - 3):
                    if is_winning_window(row[col:col + 4], player):
                        return True

            # Check vertical windows
            for col in range(len(game_state[0])):
                for row in range(len(game_state) - 3):
                    if is_winning_window([game_state[row + i][col] for i in range(4)], player):
                        return True

            # Check diagonal windows (from top-left to bottom-right)
            for row in range(len(game_state) - 3):
                for col in range(len(game_state[0]) - 3):
                    if is_winning_window([game_state[row + i][col + i] for i in range(4)], player):
                        return True

            # Check diagonal windows (from top-right to bottom-left)
            for row in range(len(game_state) - 3):
                for col in range(3, len(game_state[0])):
                    if is_winning_window([game_state[row + i][col - i] for i in range(4)], player):
                        return True

            return False  # If no winning windows are found, return False

        # Check if either player 1 or player 2 has won
        return check_windows(1) or check_windows(2)

    def get_all_available_actions(self, game_state):
        # Get a list of all available actions
        available_actions = []

        for col in range(len(game_state[0])):
            if game_state[0][col] == 0:
                available_actions.append(col)

        return available_actions

    def apply_action(self, game_state, action, player):
        # Apply the action to the state and return the new state
        new_state = [row[:] for row in game_state]

        for row in reversed(new_state):
            if row[action] == 0:
                row[action] = player
                break

        return new_state




def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame(iterations=1):
    total_moves = 0
    total_recursions = 0
    total_wins = 0
    total_losses = 0
    total_draws = 0

    for _ in range(iterations):
        fourConnect = FourConnect()
        fourConnect.PrintGameState()
        gameTree = GameTreePlayer()

        move = 0
        while move < 42:  # At most 42 moves are possible
            if move % 2 == 0:  # Myopic player always moves first
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner is not None:
                break

        if fourConnect.winner is None:
            print("Game is drawn.")
            total_draws += 1
        else:
            print("Winner: Player {0}\n".format(fourConnect.winner))
            if fourConnect.winner == 2:
                total_wins += 1
                total_moves += move
                total_recursions += gameTree.recursions
            else :
                total_losses += 1

    avg_moves = total_moves / total_wins if total_wins > 0 else 0
    avg_recursions = total_recursions / total_wins if total_wins > 0 else 0

    print("Wins:", total_wins, " Losses:", total_losses, " Draws:", total_draws)
    print("Average moves taken to beat the myopic player:", avg_moves)
    print("Average recursive calls to beat the myopic player:", avg_recursions)
        

def RunTestCase():
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2020B1A71960G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    # Initialize counters for wins, losses, and draws
    # start_time = time.time()
    #PlayGame(50)
    # end_time = time.time()

    # print("Time taken: {0} seconds".format(end_time - start_time))

    
    RunTestCase()


if __name__=='__main__':
    main()