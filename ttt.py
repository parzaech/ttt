import random
import numpy as np

#DEFINE PROBLEM
#No. of states != 3^9
#Only max X's = 5/4 and same with O's, therefore it nicely reduce the count(set)<3^9
#Count(set)=around 5.5k

class ticmactoe:
    def __init__(self, starting_player = 1):
        #initialised the starting move for 1 = X
        self.starting_player = starting_player
        self.board = np.zeros((3,3), dtype=int) #3x3 empty board
        
        self.current_player = starting_player #current chance at any state

    def reset(self):
        #for restarting the play and emptying the board
        self.board = np.zeros((3,3), dtype=int)
        self.current_player = self.starting_player

        #using a flattened matrix - tuple for every state will be helpful for making a hashtable for aquiring a particular state from Q-table
        return tuple(self.board.flatten())

    def check_terminal(self, state_tuple):
        board = np.array(state_tuple, dtype=int).reshape(3, 3)
        check = np.concatenate([np.sum(board, axis = 0), np.sum(board, axis = 1)
                                ,[np.trace(board), np.trace(np.fliplr(board))]]) # its a 1d array, np.sum throws a (1x3) and np.trace throws a scalar - needs to be converted
        if np.any(check == 3):
            return True, 1 # Player 1 wins
        if np.any(check == -3):
            return True, -1 # Player -1 wins
        if not np.any(board == 0):
            return True, 0   # Draw (Game over, zero reward)
        return False, 0
        
    def get_valid_action(self):
        #to know the legal moves
        return np.where(self.board.flatten() == 0)[0].tolist()

    def step(self, action):
        row = action//3
        col = action%3

        #penalty for wrong action selection
        if(self.board[row,col]!=0):
            reward = -10
            done = True
            return tuple(self.board.flatten()), reward, done

        #reward
        self.board[row, col] = self.current_player


        is_done, term_reward = self.check_terminal(tuple(self.board.flatten()))
        
        if is_done:
            #winner
            if term_reward != 0:
                reward = 1
            else:
            #draw
                reward = 0
            done = True
            return tuple(self.board.flatten()), reward, done

        #intermediate move
        reward = 0
        done = False
        
        self.current_player *= -1
        return tuple(self.board.flatten()), reward, done
    
    def get_space_state(self,state_tuple):
        valid_states = set()
        def dfs(state_tuple, current_player):
            #base case:
            if state_tuple in valid_states:
                return
            valid_states.add(state_tuple)
            is_terminal, _ = self.check_terminal(state_tuple)
            if is_terminal:
                return

            for action in range(9):
                if state_tuple[action] == 0: #empty place = new state
                    new_state = list(state_tuple)
                    new_state[action] = current_player
                    dfs(tuple(new_state),current_player * -1)

        dfs(state_tuple, 1)
        return valid_states
    


def render_board(state_tuple):
    representation = {1:'X', 0:' ', -1:'O'}
    print("\n-------------------\n")
    for row in range(3):
        row_state = state_tuple[row*3 : (row+1)*3]
        row_str = " | ".join([representation[val] for val in row_state])
        print(f"| {row_str} |")
        print("-------------")

def random_vs_human(env):
    state = env.reset()
    done = False

    while not done:
        render_board(state)

        if env.current_player == 1 :
            action = int(input("\nEnter valid action : "))
        else :
            valid_actions = env.get_valid_action()
            action = random.choice(valid_actions)
            print("\nBOT selected :",action)

        state, reward, done = env.step(action)
    render_board(state)



# if(__name__ == "__main__"):
#     env_1 = ticmactoe(starting_player=1)
#     random_vs_human(env_1)

if(__name__ == "__main__"):
    env_1 = ticmactoe(starting_player=1)
    s = env_1.get_space_state(tuple([0]*9))
    print(s)
    print(len(s))

              
#COUNT
#If we start with X, then at every step if its O's turn, x = o + 1 && if its X's turn, x = o
#Vice versa

#To get the number of states, its also possible to start dfs or bfs, start from 1Xs and then go deepdown


#ACTION
#0|1|2
#3|4|5
#6|7|8
#scalar action = {0,1,2,3,4,5,6,7,8}
#row = A//3 && col = A%3 ex. A = 5; row = 1 && col = 2
#


#State machine ---> X = 1, O = -1 and 'empty' = 0
#because of this if a diagnol/row/column achieves the winning state, either it will 3 or -3


#CHECK_WIN
#np.sum(board,axis=1/0) col/rows
#(edge-case-1)for diagonal, check the trace(matrix) = 3
#(edge-case-2)for anti-diagonal, flip the matric L->R and calc tr(fliplr(matrix)) = 3

# def check_win(board, player):
#     check = 3 * player #-3,3

#     if(np.sum(board, axis = 0) == check):
#         return True
#     elif(np.sum(board, axis = 1) == check):
#         return True
#     elif(np.trace(board) == check):
#         return True
#     elif(np.trace(np.fliplr(board)) == check):
#         return True

    #if np.any(all_sums == 3): # Player 1 wins
    #if np.any(all_sums == -3): # Player -1 wins


#Generate the State Space
#dfs - around 5.5k states


#Value iteration
#initialise everything poorly and run iterations

# def value_function(state_tuple):
    
#     return np.argmax((step(state_tuple))+d_factor*value_function(step(state_tuple)))









    