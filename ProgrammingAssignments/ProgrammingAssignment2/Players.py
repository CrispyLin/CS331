'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol)
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
        

    def Min_Max(self, board):
        p1 = board.p1_symbol
        # check if minimax is playing maxmizer
        # if it is a maxmizer, choose the max node
        # otherwise choose the min node
        col = None
        row = None
        if self.symbol == p1:
            (col, row, score) = self.Max(board)
        else:
            (col, row, score) = self.Min(board)
        if col != -1 and row != -1:
            return (col, row)
        else:
            print(col,row)
    

    def generate_successors(self, board, successor_list, symbol):
        for i in range(0,4):
            for j in range(0,4):
                if board.is_legal_move(j,i,symbol):
                    # if (i,j) is a valid move, append successor list with (i,j)
                    coordinate = (j,i)
                    successor_list.append(coordinate)


    def is_game_over(self, board):
        p1 = board.p1_symbol
        p2 = board.p2_symbol
        if board.has_legal_moves_remaining(p1) == False and board.has_legal_moves_remaining(p2) == False:
            return True
        else:
            return False


    def Max(self, board):
        p1 = board.p1_symbol
        p2 = board.p2_symbol

        best_node_col = -1
        best_node_row = -1
        best_node_score = -6666666 # treat this as -infinite

        # using tuple as an node and  stored in this successors list
        successors = []

        # check if it is a terminal node
        if self.is_game_over(board):
            best_node_score = board.count_score(p1) - board.count_score(p2) # utility here
            return (best_node_col, best_node_row, best_node_score) # terminal node will return (-1, -1, best_node_value)
        
        # only add valid moves/nodes of player 1 into successors
        self.generate_successors(board, successors, p1)

        if len(successors) == 0:
            best_node_score = board.count_score(p1) - board.count_score(p2)
            return (best_node_col, best_node_row, best_node_score)
            
        # expand nodes in successors one by one
        for node in successors:
            temp_board = board.cloneOBoard()
            temp_board.play_move(node[0], node[1], p1)
            # saving the result from min() to a tuple
            (temp_node_col, temp_node_row, temp_node_score) = self.Min(temp_board)

            # if temp node's value is greater than the best value we have so far, as a maximizer, choose to use temp's value
            if temp_node_score > best_node_score:
                best_node_score = temp_node_score
                best_node_col = node[0]
                best_node_row = node[1]
        # return a tuple
        return (best_node_col, best_node_row, best_node_score)


    def Min(self, board):
        p1 = board.p1_symbol
        p2 = board.p2_symbol

        best_node_col = -1
        best_node_row = -1
        best_node_score = 6666666 # treat this as infinite
        

        # using tuple as an node and stored in this successors list
        successors = []
        
        # check if it is a terminal node
        if self.is_game_over(board):
            best_node_score = board.count_score(p1) - board.count_score(p2)
            return (best_node_col, best_node_row, best_node_score)
        
        # only add valid moves/nodes of player 2 into successors
        self.generate_successors(board, successors, p2)


        if len(successors) == 0:
            best_node_score = board.count_score(p1) - board.count_score(p2)
            return (best_node_col, best_node_row, best_node_score)

        # expand nodes in successors one by one
        for node in successors:
            temp_board = board.cloneOBoard()
            temp_board.play_move(node[0], node[1], p2)
            # saving the result from max() to a tuple
            (temp_node_col, temp_node_row, temp_node_score) = self.Max(temp_board)

            # if temp node's value is less than the best value we have so far, as a minimizer, choose to use temp's value
            if temp_node_score < best_node_score:
                best_node_score = temp_node_score
                best_node_col = node[0]
                best_node_row = node[1]
        # return a tuple
        return (best_node_col, best_node_row, best_node_score)
    

    def get_move(self, board):
        return self.Min_Max(board)
