
# ======================== Class Player =======================================
class Player:
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

        # từ 1 bàn cờ hiện tại , quyết định bước đi nào
        # kiểm tra nếu đối phương bẫy mình thì phải đi vào bẫy
            # ưu thế là khi bẫy thì biết trước được chắc chắn bước đi tiếp theo của đối phương là gì
            # từ đó rút bớt được cây giải thuật mininax
        # dùng 1 hàm lượng giá để quyết định bước đi kế tiếp 
        # kết hợp 2 cần anpha beta của giải thuật minimax

        #TODO

        #---- kiểm tra nước đi tiếp theo của đối thủ tạo ra bẫy 
        #---- và bẫy đó mình có thể vào được thì phải vào

        # kiểm tra bàn cờ
        
        for row in state:
            for col in row:



        result = [(2, 0), (3, 1)]
        return result