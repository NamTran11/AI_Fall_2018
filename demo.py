def board_print(board, move=[], num=0):

    print("====== The current board(", num, ")is (after move): ======")
    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")
def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board

Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]
Test_Board = [
                  ['.', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', 'b', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]
# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
#======================================================================

#dinh nghia buoc chuyen hop le
def move_valid(x,y,max_step=8):
    global Initial_Board
    ret = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)] if max_step == 8 else [(x,y-1),(x-1,y),(x+1,y),(x,y+1)]
    i = 0
    while i < len(ret):
        if ret[i][0]<0 or ret[i][0]>4 or ret[i][1]<0 or ret[i][1]>4 :
            ret.remove(ret[i])
            continue
        if not Initial_Board[ret[i][0]][ret[i][1]] is '.':
            ret.remove(ret[i])
            continue
        i+=1
    return ret
    #[ret.remove(it) for it in ret if it[0]<0 or it[0]>4 or it[1]<0 or it[1]>4 or not Initial_Board[it[0]][it[1]] is '.']
    
def generate_next_move(x,y):
    if x%2 == 0:
        if y%2 ==0:
            return move_valid(x,y,8)
        else : return move_valid(x,y,4)
    else:
        if y%2==0:
            return move_valid(x,y,4)
        else:return move_valid(x,y,8)
def generate_list_element_CanMove(current_state,current_player):
    #current_player is 'b' or 'r'
    #return list coordinate of element can move and its next move
    list_element = []

    #travel in all posible position
    for i in range(0,5):
        for j in range(0,5):
            if current_state[i][j] is current_player:
                temp = generate_next_move(i,j)
                if len(temp)>0:list_element.append([(i,j)]+temp)

    return list_element

# from given list of (tuple)coodinate generate next states of chess board
def generate_next_Board_states(current_state,element_stat,current_player):

    list_next_Board_states = []
    # element_stat similar [(0,2) ,(1, 1), (1, 2), (1, 3)]
    # the first tuple is curent position of this element and another is valid move

    curent_position = element_stat[0]
    next_position = element_stat[1:]

    for t in next_position:
        new_Board = board_copy(current_state)
        new_Board[curent_position[0]][curent_position[1]] = '.'
        new_Board[t[0]][t[1]] = str(current_player)
        list_next_Board_states.append([[curent_position,t],new_Board])
    return list_next_Board_states
    # có nên cho thêm cái [(x_old,y_old),(x_new,y_new)] hay không

def generate_state_tree(current_state,current_player):
    l = generate_list_element_CanMove(board_copy(current_state),current_player)
    for state in l:
        for board in generate_next_Board_states(board_copy(current_state),state,current_player):
            board_print(board[1],board[0])
        print("********************************************************")
generate_state_tree(Test_Board,'b')
#generate_next_Board_states(Initial_Board,[(0,2) ,(1, 1), (1, 2), (1, 3)],'b')
#print(generate_list_element_CanMove(Initial_Board,'b'))

#print(generate_next_move(2,0))

