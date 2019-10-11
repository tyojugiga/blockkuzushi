import tkinter as tk

win_width=600
win_height=480
win_center_x=win_width/2
win_center_y=win_height/2
tick=40
game_over=False
game_clear=False

win=tk.Tk()
win.title(u'ブロック崩し')
win.geometry('600x480')
cv=tk.Canvas(win,width=win_width,height=win_height)
cv.pack()

class Ball:
    x=250 #ボールの中心のX座標(初期値）
    y=250 #ボールの中心のY座標(初期値)
    w=10 #ボールの幅

    dx=dy=5 #移動量(X),移動量(Y)
    color='green'

    def draw(self):
        cv.create_oval(self.x-self.w,self.y-self.w,self.x+self.w,self.y+self.w,fill=self.color,tag='ball')


    def move(self):
        # 移動
        bx=self.x+self.dx
        by=self.y+self.dy

        # ボールVS壁
        if bx-self.w<0 or bx+self.w>win_width:
            self.dx*= -1
        if by-self.w<0 or by+self.w>win_height:
            self.dy*= -1
        if self.w<=bx<=win_width-self.w:
            self.x=bx
        if self.w<=by<=win_height-self.w:
            self.y=by




    def delete(self):
        cv.delete('ball')

class Paddle:
    x=win_center_x #パドルの初期値(x座標)
    y=30 #パドルの初期値(y座標)
    wx=45 #パドルの幅(x座標)
    wy=8 #パドルの幅(y座標)
    dx=20 #パドルの移動量(x成分)
    color='blue'

    def draw(self):
        cv.create_rectangle(self.x-self.wx,win_height-self.y+self.wy,self.x+self.wx,win_height-self.y-self.wy,fill=self.color,tag='paddle')


    def right(self):
        cv.delete('paddle')
        self.x+=self.dx
        self.draw()

    def left(self):
        cv.delete('paddle')
        self.x-=self.dx
        self.draw()

    def move(self,action):
        if action==0:
            pass
        elif action==1:
            self.right()
        elif action==2:
            self.left()

    def reflect(self):
        if (ball.y+ball.w>=win_height-self.y-self.wy
        and self.x-self.wx<=ball.x<=self.x+self.wx
        and ball.y+ball.w<=win_height-self.y+self.wy
        ):

            ball.dy*=-1

        elif ((ball.x+ball.w>=self.x-self.wx and win_width-self.y-self.wy<=ball.y<=win_height-self.y+self.wy)
                or (ball.x-ball.w<=self.x+self.wx and win_height-self.y-self.wy<=ball.y<=win_height-self.y+self.wy)):

            ball.dx*=-1



class Block:
    w_x=50 #ブロックの幅(x座標)
    w_y=30 #ブロックの幅(y座標)

    global dx,dy,score #衝突の際にボールのクラスの移動量およびスコアを変更したいので、グローバル宣言を行う。

    # ブロックのスイッチ。1がON,0がOFF
    block_list = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 0 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 1 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # j = 2 , i = 0 ~ 11 行・列の順番

    def draw(self):
        for i in range(12):
            for j in range(3):
                cv.create_rectangle(
                    i*self.w_x,self.w_y+j*self.w_y,
                    (i+1)*self.w_x,self.w_y+(j+1)*self.w_y,
                    fill='orange',tag='block'+str(j)+str(i)
                )


    def reflect(self):
        for i in range(12):
            for j in range(3):
                if (ball.y-ball.w<self.w_y+(j+1)*self.w_y
                        and ball.y+ball.w>j*self.w_y
                        and i*self.w_x<ball.x<(i+1)*self.w_x
                        and self.block_list[j][i]==1
                ):
                    ball.dy*= -1


                    cv.delete('block'+str(j)+str(i))
                    self.block_list[j][i]=0
                    score.score+=1
                    score.delete()
                    score.draw()

class Score:
    score=0
    def draw(self):
        cv.create_text(win_width-50,50,text='Score='+str(self.score),font=('FixedSys',16),tag='score')

    def delete(self):
        cv.delete('score')

def gameover():
    global w,dx,dy,game_over
    if ((ball.y+ball.w>=win_height)
    or (win_height-paddle.y-paddle.wy<ball.y<win_height-paddle.y+paddle.wy
        and paddle.x-paddle.wx<ball.x<paddle.x+paddle.wx)):
        cv.delete('paddle')
        cv.delete('ball')
        ball.w=0
        ball.dx=0
        ball.dy=0
        game_over=True

def gameclear():
    global w, dx, dy,game_clear
    if score.score == 36:
        cv.delete("paddle")
        cv.delete("ball")
        cv.create_text(win_center_x, win_center_y, text="GAME CLEAR", font=('FixedSys', 40),tag='b')
        ball.w = 0
        ball.dx = 0
        ball.dy = 0
        game_clear=True


paddle=Paddle()
ball=Ball()
score=Score()
block=Block()

#初期描画
ball.draw()
paddle.draw()
block.draw()
score.draw()

def reset():
    cv.delete('score')
    ball.x = 250  # ボールの中心のX座標(初期値）
    ball.y = 250  # ボールの中心のY座標(初期値)
    ball.w = 10  # ボールの幅
    ball.dx = ball.dy = 5  # 移動量(X),移動量(Y)

    paddle.x = win_center_x  # パドルの初期値(x座標)
    paddle.y = 30  # パドルの初期値(y座標)
    paddle.wx = 45  # パドルの幅(x座標)
    paddle.wy = 8  # パドルの幅(y座標)
    paddle.dx = 20  # パドルの移動量(x成分)

    block.block_list = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 0 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # j = 1 , i = 0 ~ 11
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # j = 2 , i = 0 ~ 11 行・列の順番

    score.score=0

    ball.draw()
    paddle.draw()
    block.draw()
    score.draw()



a=[2, 0, 2, 1, 0, 1, 1, 0, 0, 1, 1, 2, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 0, 2, 0, 2, 0, 1, 1, 0, 0, 1, 0, 2, 2, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0, 2, 1, 0, 0, 2, 1, 2, 1, 0, 2, 2, 1, 1, 0, 0, 1, 0, 2, 0, 1, 2, 2, 0, 2, 2, 2, 1, 2, 1, 1, 1, 0, 1, 1, 0, 2, 2, 1, 1, 0, 2, 1, 2, 1, 1, 1, 1, 2, 0, 2, 0, 2, 0, 1, 2, 1, 2, 2, 2, 1, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 1, 2, 1, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 1, 1, 2, 1, 1, 2, 1, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 0, 1, 2, 1, 2, 0, 0, 0, 0, 0, 1, 2, 1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 2, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 2, 0, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 0, 2, 2, 2, 1, 1, 1, 1, 0, 1, 2, 0, 2, 1, 2, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 2, 2, 2, 0, 2, 0, 1, 1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 2, 1, 2, 1, 2, 0, 2, 1, 2, 0, 2, 2, 2, 0, 2, 2, 0, 0, 2, 2, 1, 0, 2, 0, 2, 0, 1, 1, 1, 0, 0, 1, 0, 2, 0, 2, 0, 1, 1, 2, 0, 0, 0, 0, 1, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 0, 1, 2, 1, 0, 2, 1, 1, 2, 0, 0, 0, 2, 0, 0, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, 0, 1, 1, 0, 2, 1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 2, 1, 2, 2, 2, 1, 1, 2, 0, 0, 2, 1, 2, 0, 2, 0, 1, 2, 2, 0, 0, 0, 0, 1, 0, 1, 2, 0, 2, 2, 2, 0, 1, 2, 0, 1, 2, 2, 2, 0, 1, 0, 2, 0, 2, 1, 2, 2, 0, 2, 2, 1, 2, 1, 0, 1, 1, 2, 1, 1, 0, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2, 2, 2, 1, 0, 1, 2, 2, 2, 0, 2, 0, 2, 0, 2, 1, 1, 0, 0, 1, 2, 1, 0, 2, 2, 1, 1, 2, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 2, 0, 0, 1, 0, 1, 0, 1, 2, 2, 0, 0, 1, 0, 1, 0, 2, 0, 0, 2, 2, 0, 1, 0, 1, 2, 0, 0, 1, 0, 2]
k=0

def gameloop():
    global game_over,game_clear,k,a
    ball.delete()
    ball.move()
    action=a[k]
    paddle.move(action)
    if paddle.x+paddle.wx>win_width:
        paddle.x=win_width-paddle.wx
    elif paddle.x-paddle.wx<0:
        paddle.x=paddle.wx
    paddle.reflect()
    block.reflect()
    ball.draw()
    k+=1
    gameover()
    gameclear()
    if game_over:
        cv.delete('a')
        game_over=False
    if game_clear:
        cv.delete('b')
        reset()
        game_clear=False
    win.after(tick,gameloop)

gameloop()
win.mainloop()



