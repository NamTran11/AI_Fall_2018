from random import randint
INFINITY = 9999

def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board

# hàm đếm số quân cờ
def count_num_chess(current_state,i_playerNum):
    if i_playerNum == 1 : 
        current_player = 'b'
        competitor = 'r'
    elif i_playerNum == -1: 
        current_player = 'r'
        competitor = 'b'
    num = 0
    for i in range(5):
        for j in range(5):
            if current_state[i][j]== current_player:
                num += 1
    return num

# hàm đếm số quân cờ có thể di chuyển 
def count_num_chess_can_move(current_state,i_playerNum):
    l =  generate_all_next_steps_can_move(board_copy(current_state),i_playerNum)
    if len(l)==0: return 0
    return sum([len(x) for x in l]) - len(l)

# hàm đếm số quân cờ có thể di chuyển 
# đếm và trả về tọa độ các quân cờ gần quân mình nhất
def findCandidateElement(board,i_playerNum,num_get = 4):
    if i_playerNum == 1 : 
        current_player = 'b'
        competitor = 'r'
    elif i_playerNum == -1: 
        current_player = 'r'
        competitor = 'b'

    list_element_of_player = []
    list_element_of_competitor = []
    for i in range(0,5):
        for j in range(0,5):
            if board[i][j]== current_player:
                list_element_of_player.append([i,j])
            if board[i][j]== competitor:
                list_element_of_competitor.append([i,j])

    num_of_element = len(list_element_of_player)
    list_to_sort = []
    # loại dần dần
    for post in list_element_of_player:
        i,j = post
        d = 100
        for p in list_element_of_competitor:
            x,y = p
            d = min(d,(x-i)**2+(y-j)**2)
        list_to_sort.append([d,(i,j)])
    list_to_sort = sorted(list_to_sort)
    return list_to_sort,num_of_element,num_get

#dinh nghia buoc chuyen hop le
def move_valid(current_state,x,y,max_step=8,CHET=False):
    ret = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)] if max_step == 8 else [(x,y-1),(x-1,y),(x+1,y),(x,y+1)]
    i = 0
    while i < len(ret):
        if ret[i][0]<0 or ret[i][0]>4 or ret[i][1]<0 or ret[i][1]>4 :
            ret.remove(ret[i])
            continue
        if not CHET and not current_state[ret[i][0]][ret[i][1]] is '.':
            ret.remove(ret[i])
            continue
        i+=1
    return ret
    #[ret.remove(it) for it in ret if it[0]<0 or it[0]>4 or it[1]<0 or it[1]>4 or not Initial_Board[it[0]][it[1]] is '.']
    
# sinh ra các bước đi tiếp theo (chưa tính trường hợp bắt buộc vào bẫy)
def generate_list_element_CanMove(current_state,i_playerNum):
    #current_player is 'b' or 'r' (1 is 'b' -1 is 'r')
    if i_playerNum == 1 : current_player = 'b'
    elif i_playerNum == -1: current_player = 'r'
    list_element = []
    num_element_of_player = 0
    # count number of elements of player
    for i in range(0,5):
        for j in range(0,5):
            if current_state[i][j] == current_player:
                num_element_of_player+=1
    if(num_element_of_player<=4):
        for i in range(0,5):
            for j in range(0,5):
                if current_state[i][j] == current_player:
                    temp = move_valid(current_state,i,j,8) if (i+j)%2==0 else move_valid(current_state,i,j,4)
                    if len(temp)>0:list_element.append([(i,j)]+temp)
        return list_element


    #return list coordinate of element can move and its next move
    
    list_to_sort,num_of_element,num_get = findCandidateElement(current_state,i_playerNum)
    candidate = list_to_sort[:3] # get four candidate
    for c in candidate:
        d,(i,j) = c
        temp = move_valid(current_state,i,j,8) if (i+j)%2==0 else move_valid(current_state,i,j,4)
        if len(temp)>0:list_element.append([(i,j)]+temp)
    if(len(list_element)==0):
        candidate = list_to_sort[3:]
        for c in candidate:
            d,(i,j) = c
            temp = move_valid(current_state,i,j,8) if (i+j)%2==0 else move_valid(current_state,i,j,4)
            if len(temp)>0:list_element.append([(i,j)]+temp)
            
    return list_element


# kiểm tra và trả về tất cả trạng thái người chơi phải đi nếu đối thủ có tạo bẫy, nếu ko có bẫy thì danh sách rỗng
### ý tưởng giải thuật :xet 1 quân cờ của đối thủ , sinh ra tất cả vị trí mà quân cờ đó có thể đi được
### tại mỗi vị trí có thể đi được(CANMOVE) ,xét tiếp vị trí CANDIDATE là vị trí đối xứng với ban đầu qua vị trí CANMOVE
### nếu CANDIDATE == quân cờ của đối thủ thì xem như vị trí CANMOVE là 1 bẫy
### chưa xét tới việc ta có đi vào bấy của quân địch được hay không 
def Is_Trap(current_state,i_playerNum):
    #i_playerNum ở đây thường đóng vai trò người chơi
    list_trap = []
    # bước này sinh để phục vụ giải thuật chứ ko phải tìm đường đi thật sự
    list_element = generate_list_element_CanMove(current_state,-1*i_playerNum)
    
    if i_playerNum == 1 : 
        current_player = 'b'
        competitor = 'r'
    elif i_playerNum == -1: 
        current_player = 'r'
        competitor = 'b'

    for e in list_element:
        (x,y) = e[0] # tọa độ hiện tại
        list_coodinate = e[1:]
        for c in list_coodinate:
            if c in list_trap:
                continue
            # neu la hang ngang
            candidate_position = None
            if(c[0]==x):
                if(y<c[1] and c[1]+1<=4):
                    if(current_state[x][c[1]+1]==competitor):
                        candidate_position = c

                elif(y>c[1] and c[1]-1>=0):
                    if(current_state[x][c[1]-1]==competitor):
                        candidate_position = c

            elif(c[1]==y):
                if(x<c[0] and c[0]+1<=4):
                    if(current_state[c[0]+1][y]==competitor):
                        candidate_position = c

                elif(x>c[0] and c[0]-1>=0):
                    if(current_state[c[0]-1][y]==competitor):
                        candidate_position = c
            else:
                if(c[0]>x and c[1]>y) and (c[0]+1<=4 and c[1]+1<=4):
                    if(current_state[c[0]+1][c[1]+1]==competitor):
                        candidate_position = c
                if(c[0]<x and c[1]<y) and (c[0]-1>=0 and c[1]-1>=0):
                    if(current_state[c[0]-1][c[1]-1]==competitor):
                        candidate_position = c
                if(c[0]<x and c[1]>x) and (c[0]-1>=0 and c[1]+1<=4):
                    if(current_state[c[0]-1][c[1]+1]==competitor):
                        candidate_position = c
                if(c[0]>x and c[1]<x) and (c[0]+1<=4 and c[1]-1>=0):
                    if(current_state[c[0]+1][c[1]-1]==competitor):
                        candidate_position = c

            if not candidate_position is None:
                list_trap.append(candidate_position)

    list_element = generate_list_element_CanMove(board_copy(current_state),i_playerNum)

    if len(list_trap)==0: return []

    list_steps_trap = []
    for e in list_element:
        for trap in list_trap:
            if trap in e[1:]:
                list_steps_trap.append([e[0],trap])

    return list_steps_trap
    # trả về danh sách các bước đi chắc chắn phải đi của người chơi

# sinh ra các bước đi tiếp theo (tính cả trường hợp đối thủ tạo bẫy thì ta phải vào)
def generate_all_next_steps_can_move(current_state,i_playerNum):

    list_trap = Is_Trap(board_copy(current_state),i_playerNum) # kiểm tra có bị đối phương gài bẫy hay ko

    if len(list_trap) > 0: return list_trap
    
    return generate_list_element_CanMove(board_copy(current_state),i_playerNum)

# ứng với mỗi bước di chuyển thì sinh ra trạng thái bàn cờ tiếp theo
# TODO nên xét trường hợp ăn quân trong đây luôn
def generate_next_Board_states(current_Board,steps,i_playerNum):
    
    if i_playerNum == 1 : 
        current_player = 'b'
        competitor = 'r'
    elif i_playerNum == -1: 
        current_player = 'r'
        competitor = 'b'

    list_next_Board_states = []
    # step similar [(0,2) ,(1, 1), (1, 2), (1, 3)]
    # the first tuple is curent position of this element and another is valid move

    curent_position = steps[0]
    next_position = steps[1:]

    for t in next_position:
        new_Board = board_copy(current_Board)
        new_Board[curent_position[0]][curent_position[1]] = '.'
        new_Board[t[0]][t[1]] = current_player

        # kiểm tra gánh được bao nhiêu quân, và trạng thái mới của bàn cờ sau khi gánh
        new_Board,num_eat_more = get_more_chess(new_Board,t[0],t[1],i_playerNum)

        # kiểm tra chẹt bao nhiêu quân và trạng thái mới của bản cờ sau khi chẹt
        new_Board,num_chet = CHET_state(new_Board,current_player,competitor)

        list_next_Board_states.append([[curent_position,t],new_Board,num_eat_more+num_chet])
        # có thể add thêm số quân ăn được ở đây
    return list_next_Board_states

#kiểm tra bước đi này có ăn được quân cờ nào không (gánh và chẹt) #chưa kiểm tra chẹt
#trả về trạng thái bàn cờ mới và số quân cờ ăn được từ bước đi này
# HÀM NÀY SAI Ở CHỔ SỐ QUÂN CỜ ĂN ĐƯỢC TRẢ VỀ CHƯA ĐÚNG
def get_more_chess(current_Board,x,y,i_playerNum):
    if i_playerNum == 1 : 
        current_player = 'b'
        competitor = 'r'
    elif i_playerNum == -1: 
        current_player = 'r'
        competitor = 'b'
    #kiểm tra gánh
    ret = sub_get_chess(current_Board,x,y,competitor)
    #TODO : kiểm tra chẹt
    if len(ret) == 0: return current_Board,0

    for pair in ret:
        current_Board[pair[0][0]][pair[0][1]] = current_player
        current_Board[pair[1][0]][pair[1][1]] = current_player
    return current_Board,2*len(ret)
    #quân hiện tại là quân current_player , xét xem có ăn được thêm quân nào nữa ko

def sub_get_chess(current_state,x,y,competitor):

    # xét các cặp đối xứng
    ret = [[(x-1,y-1),(x+1,y+1)],[(x,y-1),(x,y+1)],[(x-1,y),(x+1,y)],[(x-1,y+1),(x+1,y-1)]] if (x+y)%2==0 else [[(x,y-1),(x,y+1)],[(x-1,y),(x+1,y)]]

    i = 0
    while i < len(ret):
        if ret[i][0][0]<0 or ret[i][0][0]>4 or ret[i][0][1]<0 or ret[i][0][1]>4 \
            or ret[i][1][0]<0 or ret[i][1][0]>4 or ret[i][1][1]<0 or ret[i][1][1]>4 :
            ret.remove(ret[i])
            continue
        if current_state[ret[i][0][0]][ret[i][0][1]] != competitor or current_state[ret[i][1][0]][ret[i][1][1]]!=competitor:
            ret.remove(ret[i])
            continue
        i+=1
    return ret

# def CHET_state(current_state,current_player,competitor):
#     ret = []
#     for i in range(0,5):
#         for j in range(0,5):
#             if current_state[i][j]==competitor:
#                 maxstep = 8 if (i+j)%2==0 else 4
#                 CHET = move_valid(current_state,i,j,maxstep,True)
#                 l = [current_state[x[0]][x[1]] for x in CHET]
#                 if l == [current_player]*len(l):
#                     ret.append((i,j))
#     if len(ret)==0:
#         return current_state,0
#     for pair in ret:
#         current_state[pair[0]][pair[1]] = current_player

#     return current_state,len(ret)

def Connected_component(current_state,current_player,x,y,list_points):
    # list_points : tập các điêm thuộc CC đã biết
    # trả về l: tập hợp các điểm của CC
    #       b: bouding box của CC
    list_points_of_CC = list_points

    maxstep = 8 if (x+y)%2==0 else 4
    move_steps = move_valid(current_state,x,y,maxstep,True)
    bouding = move_steps
    
    #print(bouding)
    for point in bouding:
        (x1,y1)= point
        if current_state[x1][y1] == current_player and not [x1,y1] in list_points_of_CC:
            
            list_points_of_CC.append([x1,y1])
            list_points_of_CC,b = Connected_component(current_state,current_player,x1,y1,list_points_of_CC)
            [bouding.append(x) for x in b if not x in bouding]

    [bouding.remove((x[0],x[1])) for x in list_points_of_CC if (x[0],x[1]) in bouding]
    return list_points_of_CC,bouding

def FindAllCC(current_state,current_player):
    cluster = []
    point_clusted = []
    for i in range(0,5):
        for j in range(0,5):
            if current_state[i][j] == current_player and not [i,j] in point_clusted:
               list_points_of_CC,bouding = Connected_component(current_state,current_player,i,j,[[i,j]]) 
               point_clusted+= list_points_of_CC
               cluster.append([list_points_of_CC,bouding])
    return cluster

def CHET_state(current_state,current_player,competitor):
    
    # find all connected component
    cluster = FindAllCC(current_state,competitor)
    num_CHET = 0
    list_point_CHET = []
    for c in cluster:
        l_p,bouding = c
        l = [current_state[x[0]][x[1]] == current_player for x in bouding]
        if l == [True]*len(l):  ## if all is True
            num_CHET+= len(l_p)
            list_point_CHET += l_p

    if len(list_point_CHET)==0:
        return current_state,0
    for pair in list_point_CHET:
        current_state[pair[0]][pair[1]] = current_player

    return current_state,num_CHET

class Node(object):
    def __init__(self,i_depth,i_playerNum,current_board,i_value=0,move_step_to_current_board=None):
        self.i_depth = i_depth
        self.i_playerNum = i_playerNum # 1 is player -1 is competitor
        self.current_board = current_board
        self.i_value = i_value
        self.children = []
        self.move_step_to_current_board = move_step_to_current_board
        self.CreateChildren()
        # một node chỉ chứa các 1 bàn cờ,và có cần chứa bước chuyển để đến bàn cờ hiện tại hay không

    def CreateChildren(self):
        #trạng thái đầu tiên là trạng thái khởi đầu , tầng tiếp theo là tầng của người chơi đi trước
        if self.i_depth >= 0:

            all_element = generate_all_next_steps_can_move(self.current_board,self.i_playerNum)
            #### với mỗi quân cờ sẽ có nhiều bước đi tiếp theo,chọn 1 trong số các quân cờ
            for element_next_steps in all_element:

                new_states = generate_next_Board_states(self.current_board,element_next_steps,self.i_playerNum)

                for state in new_states:
                    self.children.append(Node(self.i_depth-1,-self.i_playerNum,state[1],self.RealVal(state[1],state[2]),state[0]))

    #COST-FUNCTION
    def RealVal(self,value,eating):
        # số bước đi tiếp theo của đối thủ là ít nhất
        # trạng thái hiện tại đã ăn được bao nhiêu quân cờ(càng nhiều càng tốt)
        #m = count_num_chess_can_move(value,-1*self.i_playerNum)
        l = Is_Trap(value,-self.i_playerNum)
        #if len(l)>0: return (0.7*eating - 0.3*len(l)-0.04*m)*self.i_playerNum
        if len(l)>0: return (0.7*eating - 0.3*len(l))*self.i_playerNum
        # trạng thái hiện tại đã để cho quân địch bao nhiêu bẫy (số bẫy càng ít càng tốt) 
        return eating*self.i_playerNum


def minimax(node, depth, i_playerNum, alpha, beta):

    if len(node.children) == 0:
        return node.i_value , node.move_step_to_current_board
    ret_move = None

    if i_playerNum == 1 :
         
        bestVal = -INFINITY 
        for child in node.children:
            value,move_step = minimax(child, depth-1, -i_playerNum, alpha, beta)
            
            if value >= bestVal: # >=
                #ret_move = child.move_step_to_current_board
                if value == bestVal:
                    if randint(0,9)<4:
                        ret_move = child.move_step_to_current_board
                else: ret_move = child.move_step_to_current_board
            
            bestVal = max( bestVal, value) 
            alpha = max( alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal,ret_move

    elif i_playerNum == -1 :

        bestVal = +INFINITY 
        for child in node.children:
            value,move_step  = minimax(child, depth-1, -i_playerNum, alpha, beta)
            
            if value <= bestVal: #<=
                #ret_move = child.move_step_to_current_board
                if value == bestVal:
                    if randint(0,9)<4:
                        ret_move = child.move_step_to_current_board
                else:
                    ret_move = child.move_step_to_current_board

            bestVal = min( bestVal, value) 
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
        return bestVal,ret_move



# node = Node(4,1,Test_Board,0)
# print(minimax(node,4,1,-INFINITY,+INFINITY))
# print(st)


# ======================== Class Player =======================================

class Player:
    inum = 0
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):
        self.inum+=1
        i_playerNum = 1 if self.str == 'b' else -1
        i_depth = 2 if self.inum <15 else 3
        node = Node(i_depth,i_playerNum,current_board=state,i_value = 0)
        result = minimax(node,node.i_depth,node.i_playerNum,-INFINITY,+INFINITY)[1]
        return result