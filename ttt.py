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

# if(__name__ == "__main__"):
#     env_1 = ticmactoe(starting_player=1)
#     s = env_1.get_space_state(tuple([0]*9))
#     print(s)
#     print(len(s))

              
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


def next_state(state_tuple, action, player):
    new_state = list(state_tuple)
    new_state[action] = player
    return tuple(new_state)

#Value iteration
def value_function(env, gamma=1.0, epsilon=1e-6, max_iter=100,
                   track_history=False):
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be between 0 and 1")
    if epsilon <= 0:
        raise ValueError("epsilon must be greater than 0")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")

    all_states = env.get_space_state(tuple([0]*9))
    V = {state: 0.0 for state in all_states}
    history = []

    def get_player(state):
        count_x = sum(1 for v in state if v == 1)
        count_o = sum(1 for v in state if v == -1)
        return 1 if count_x == count_o else -1

    for i in range(max_iter):
        max_diff = 0.0
        new_V = {}
        for state, v_old in V.items():
            is_terminal, winner = env.check_terminal(state)
            if is_terminal:
                if winner == 1:
                    v_new = 1.0
                elif winner == -1:
                    v_new = -1.0
                else:
                    v_new = 0.0
            else:
                valid = [a for a in range(9) if state[a] == 0]
                player = get_player(state)
                if player == 1:
                    v_new = max(gamma * V[next_state(state, a, player)] for a in valid)
                else:
                    v_new = sum(gamma * V[next_state(state, a, player)] for a in valid) / len(valid)
            new_V[state] = v_new
            diff = abs(v_new - v_old)
            if diff > max_diff:
                max_diff = diff
        V = new_V
        history.append(max_diff)
        if max_diff < epsilon:
            print(f"Converged in {i+1} iterations")
            break

    if track_history:
        return V, history
    return V


def plot_gamma_convergence(env, gamma_values=(0.5, 0.8, 0.9, 0.99, 1.0),
                           epsilon=1e-6, max_iter=100):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "plot_gamma_convergence requires matplotlib; "
            "install it with 'python3 -m pip install matplotlib'"
        ) from exc

    if not gamma_values:
        raise ValueError("gamma_values must contain at least one value")

    fig, ax = plt.subplots()
    for gamma in gamma_values:
        _, history = value_function(
            env,
            gamma=gamma,
            epsilon=epsilon,
            max_iter=max_iter,
            track_history=True,
        )
        iterations = range(1, len(history) + 1)
        ax.plot(iterations, history, marker="o", label=f"gamma={gamma}")

    ax.axhline(
        epsilon,
        color="black",
        linestyle="--",
        linewidth=1,
        label=f"epsilon={epsilon:g}",
    )
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Maximum value change")
    ax.set_title("Value-iteration convergence for different gamma values")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    plt.show()
    return fig, ax


def extract_policy(env, V):
    policy = {}
    for state in V:
        count_x = sum(1 for v in state if v == 1)
        count_o = sum(1 for v in state if v == -1)
        if count_x != count_o:
            continue
        is_terminal, _ = env.check_terminal(state)
        if is_terminal:
            continue
        valid = [a for a in range(9) if state[a] == 0]
        values = [V[next_state(state, a, 1)] for a in valid]
        policy[state] = valid[np.argmax(values)]
    return policy


if __name__ == "__main__":
    env = ticmactoe(starting_player=1)
    plot_gamma_convergence(env)
