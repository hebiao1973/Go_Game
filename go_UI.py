import turtle
import go_lib

def getP_in_canvas(x,y):
    """计算围棋点在画布上对应的位置"""
    tmp = (go_size - 1)/2
    return (x-tmp)*gap, -(y-tmp)*gap


def get_point(cx,cy):
    """当鼠标点击时，获取点击时离棋盘上最近的交叉点，
    并计算鼠标点击点距离这个交叉点的位置，如果足够近，
    ——小于四分之一个间隔，就返回这个交叉点"""
    tmp = (go_size-1) / 2
    x = cx / gap + tmp
    y = -cy / gap + tmp
    dis = 0.25  # 代表0.25个间隔
    if (x >= -dis and x <= (go_size-1)+dis 
        and y >= -dis and y <= (go_size-1)+dis):
        tmp_peers = set((px,py) for px in [int(x),int(x+1)] for py in [int(y), int(y+1)] ) 
        peers = tmp_peers & set(my_go.board)
        for peer in peers:
            if abs(x-peer[0]) < dis and abs(y-peer[1]) < dis:
                return peer

      
def draw(x,y,color):
    """画上棋子"""
    tu.penup()
    tu.goto(x,y-gap*0.31)
    tu.pendown()
    if color == 0:
        tu.fillcolor("black")
    else:
        tu.fillcolor("white")
    tu.begin_fill()
    tu.circle(gap*0.31)
    tu.end_fill()

def clean_dead(dead):
    cx,cy = getP_in_canvas(dead[0],dead[1])
    tu.up()
    tu.goto(cx, cy-gap*0.35)
    tu.color("white")
    tu.begin_fill()
    tu.circle(gap*0.35)
    tu.end_fill()
    tu.goto(cx,cy-gap*0.35)
    tu.down()
    tu.color("black")
    tu.goto(cx,cy+gap*0.35)
    tu.up()
    tu.goto(cx-gap*0.35,cy)
    tu.down()
    tu.goto(cx+gap*0.35,cy)
    wn.update()
    
def play(x,y):
    global color
    p = get_point(x,y)
    if p != None:
        if my_go.is_checked(p[0],p[1],color):
            deads = my_go.move(p[0],p[1],color)
            cx,cy = getP_in_canvas(p[0],p[1])
            draw(cx,cy,color)
            if deads:
                for dead in deads:
                    clean_dead(dead)
            color = my_go.get_opposed_color(color)
        
        
wn = turtle.Screen()
wn.tracer(10,1)
my_go = go_lib.Go()
color = 0  # 开始的棋子颜色

tu = turtle.Turtle()
tu.hideturtle()

go_size = my_go.size  # 围棋路数
gap = 25  # 棋盘线之间的间隔
len_line = gap*(go_size-1)   # 棋盘线长

start_x = start_y = -len_line/2

for i in range(go_size): # 画横线
    tu.penup()
    tu.goto(start_x, start_y+gap*i)
    tu.pendown()
    tu.goto(start_x + len_line, start_y+gap*i)    
for i in range(go_size): # 画横线
    tu.penup()
    tu.goto(start_x + gap*i, start_y)
    tu.pendown()
    tu.goto(start_x + gap*i, start_y + len_line)
    
stars = set((x,y) for x in (3,9,15) for y in (3,9,15))
for star in stars:
    tu.up()
    cx,cy = getP_in_canvas(star[0],star[1])
    tu.goto(cx,cy)
    tu.down()
    tu.dot(go_size*0.4,"black")
    wn.update()
    

wn.onclick(play)
wn.update()
wn.mainloop()
