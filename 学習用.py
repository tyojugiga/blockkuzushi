import tkinter as tk
from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.models import Model
from keras.optimizers import RMSprop
from collections import deque
import numpy as np
import random
import copy
import time

win_width=600
win_height=480
win_center_x=win_width/2
win_center_y=win_height/2
tick=40


win=tk.Tk()
win.title(u'ブロック崩し')
win.geometry('600x480')
cv=tk.Canvas(win,width=win_width,height=win_height)
cv.pack()

class Ball:
    x=250 #ボールの中心のX座標(初期値）
    y=250 #ボールの中心のY座標(初期値)
    w=5 #ボールの幅

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
        if (ball.y+ball.w>win_height-self.y-self.wy
        and self.x-self.wx<ball.x<self.x+self.wx
        ):
            ball.dy*=-1


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
    if ball.y+ball.w>=win_height:
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
    ball.w = 5  # ボールの幅
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



class DQN:
    def __init__(self):
        self.memory = deque(maxlen=100000)
        self.epsilon = 1.0
        model = Sequential()
        model.add(Dense(128, input_shape=(21,)))
        model.add(Dropout(0.25))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer=RMSprop(lr=0.0001))
        self.model = model

    def choice_action(self, state0, actionable):
        if self.epsilon >= random.random():
            return random.choice(actionable)
        else:
            return self.choice_best_action(state0, actionable)

    def choice_best_action(self, state0, actionables):
        best_actions = []
        max_action_value = -999
        for actionable in actionables:
            state0.append(actionable)
            action_value = self.model.predict(np.array([state0]))
            state0.pop()
            if action_value > max_action_value:
                best_actions.append(actionable)
                if len(best_actions)>1:
                    del best_actions[0]
                max_action_value = action_value
            elif action_value == max_action_value:
                best_actions.append(actionable)
        if len(best_actions)==0:
            return 0
        return random.choice(best_actions)

    def remember_memory(self, state0, action0, next_state0, reward0, next_actionables0, is_completed0):
        if len(self.memory)>=10000:
            del self.memory[0]
        self.memory.append((state0, action0, next_state0, reward0, next_actionables0, is_completed0))

    def replay_experience(self, batch_size):
        batch_size = min(batch_size, len(self.memory))
        minibatch = random.sample(self.memory, batch_size)

        for i in range(batch_size):
            X = []
            Y = []
            state1, action1, next_state1, reward1, next_actionables1, is_completed1 = minibatch[i]
            state1.append(action1)
            if is_completed1:
                target = reward1
            else:
                next_rewards = []
                if len(next_state1)==21:
                    next_state1.pop()
                for actionable in next_actionables1:
                    next_state1.append(actionable)
                    next_rewards.append(self.model.predict(np.array([next_state1])))
                    next_state1.pop()

                target = reward + 0.9 * np.amax(np.array(next_rewards))
            if len(state1)==22:
                state1.pop()
            X.append(state1)
            Y.append(target)
            n_X = np.array(X)
            n_Y = np.array([Y])
            self.model.fit(n_X, n_Y, epochs=1, verbose=0)
        if self.epsilon > 0.01:
            self.epsilon *= 0.99995

dqn=DQN()
t1=time.time()
episode=50000
a=[0]
for e in range(episode):

    game_over = False
    game_clear = False
    reset()
    is_completed=False
    state=[]
    next_state=[]
    k=0
    s0=[ball.x,ball.y,ball.dx,ball.dy,paddle.x]
    a0=0
    reward=0
    a.clear()
    while not game_over:
        if k == 0:
            state.extend(s0)
            s1 = copy.copy(s0)
            state.extend(s1)
            s2 = copy.copy(s0)
            state.extend(s2)
            s3 = copy.copy(s0)
            state.extend(s3)
        actions=[0,1,2]
        action=dqn.choice_action(state,actions)
        a.append(action)
        ball.delete()
        ball.move()
        paddle.move(action)
        if paddle.x + paddle.wx > win_width:
            paddle.x = win_width - paddle.wx
        elif paddle.x - paddle.wx < 0:
            paddle.x = paddle.wx
        paddle.reflect()
        block.reflect()
        ball.draw()
        s4=[ball.x,ball.y,ball.dx,ball.dy,paddle.x]
        next_state=copy.copy(state)
        next_state.extend(s4)
        del next_state[0]
        del next_state[0]
        del next_state[0]
        del next_state[0]
        del next_state[0]
        gameover()
        gameclear()
        if game_over:
            is_completed=game_over
            reward-=100
        elif game_clear:
            is_completed=game_clear
            reward+=10000
        elif score.score>0:
            reward+=10
        elif paddle.x>ball.x:
            if action==2:
                reward+=2
        elif paddle.x<ball.x:
            if action==1:
                reward+=2
        else:
            reward=0
        next_actionables=[0,1,2]
        dqn.remember_memory(state, action, next_state, reward, next_actionables, is_completed)
        state = next_state
        k+=1
        if game_over or game_clear:
            if e % 250==0:
                t2=time.time()
                print("episode: {}".format(e))
                print('time:{}'.format(t2-t1))
            if score.score>=3:
                print("episode: {}".format(e))
                print(score.score)
                print(a)
            break

    dqn.replay_experience(32)

win.mainloop()

