Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
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

print(generate_next_move(2,0))

