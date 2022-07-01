import copy
from typing import List
from winsound import Beep

# 定义一个围棋类
class Go:
    """ 新开始一局棋 """
    def __init__(self, size=19) -> None:
        self.size = size  # 棋盘路数
        self.board = {(x,y):None for x in range(size) for y in range(size)}      # 用字典记录当前棋盘状态
        self.boards = []  # 纪录每一步落下之后的状态，用于判断全局同型
        self.steps = []   # 用列表记录每一步棋所下的位置及棋子颜色
    
    def get_opposed_color(self,color):  # 计算对手方棋子颜色
        if color == 0:
            return 1
        elif color == 1:
            return 0
        else:
            raise ValueError("color只能是int类的0或者1")
            
    def get_neighbours(self,x,y):
        """返回围棋盘上某个点的周围的点的集合
        Return: set
        """
        return {(x-1,y),(x+1,y),(x,y-1),(x,y+1)} & set(self.board)
    
    def clear_deads(self,x,y,color) -> None|set:   # 清理掉某点周围对手方死子
        deads = []
        op_color = self.get_opposed_color(color)
        ns = self.get_neighbours(x,y)
        for p in ns:
            if (self.board[p] == op_color and
               (temp := self.is_dead([],p[0],p[1],op_color)) != False):
                deads += temp
        if len(deads) > 0:
            tmp_set = set(deads)
            for dead in set(deads):
                self.board[dead] = None
            return tmp_set
            
    
    def move(self,x,y,color) -> None|set:
        self.steps.append(((x,y),color))
        self.board[(x,y)] = color
        deads = self.clear_deads(x,y,color)     # 提子,UI更新
        self.boards.append(copy.deepcopy(self.board))
        return deads
        
    def cancel_move(self, n = 1) -> None:
        """悔棋——即恢复到上n步的棋局状态"""
        nl = len(self.boards)
        if n > nl:  # 悔棋步数不能超过实际步数
            n = nl
        self.steps = self.steps[:-n]
        self.boards = self.boards[:-n]
        if n == nl:
            self.board = {(x,y):None for x in range(self.size) for y in range(self.size)}
        else:
            self.board = copy.deepcopy(self.boards[-1])

            
    def get_neighbours(self,x,y) -> set:
            return {(x-1,y),(x+1,y),(x,y-1),(x,y+1)} & set(self.board)
        
           
    def is_dead(self,dead_list,x,y,color):
        """判断一个棋子是不是没气, 先判断它自身，如果是则递归判断与它相连的一块棋是否也都没气"""
        ns = self.get_neighbours(x,y)
        # 只要周围的点的值有一个为空（有气），返回False
        if any(self.board[point] == None for point in ns):
            return False
        dead_list.append((x,y))
        for point in ns:
            if (self.board[point] == color and
                   point not in dead_list and
                   not self.is_dead(dead_list,point[0],point[1],color)):
                return False  
        return dead_list  # 如果的确都没气，返回死子列表供给UI模块
    
    def is_checked(self,x,y,color) -> bool:
        """判断落子是否符合围棋规则(这里用应氏规则)"""
        if self.board[(x,y)] != None:   # 如果一个位置已经有棋子，返回False
            Beep(1000,500)
            return False
        ns = self.get_neighbours(x,y)
        for point in ns:
            if self.board[point] == None:   # 如果这点还有气，返回True
                return True
        
        self.move(x,y,color)
        
        if (self.is_dead([],x,y,color) == False and    # 自己有气
            self.boards[-1] not in self.boards[:-1]):  # 并且不全局同型
                self.cancel_move()  # 返回之前，恢复
                return True
        else:
            self.cancel_move()  # 返回之前，恢复
            Beep(1000,500)
            return False 
        
            
            