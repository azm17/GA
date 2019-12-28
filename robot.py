# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# オブジェクト
class MyObject():
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
# エリア
class Area(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Area, self).__init__(x, y, width, height)
        
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        im = plt.plot(x, y, color='#1f77b4')
        margin_width = 5
        plt.ylim(self.x1 - margin_width, 
                 self.x2 + margin_width)
        plt.xlim(self.y1 - margin_width, 
                 self.y2 + margin_width)
        return im
# 障害物
class Obstacle(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Obstacle, self).__init__(x, y, width, height)
    
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        im = plt.plot(x, y, color='#FF0000')
        return im
# エージェント
class Agent(MyObject):
    def __init__(self, x, y):# 初期設定
        super(Agent, self).__init__(x, y, 0, 0)
    
    def getAgent(self):# 座標を取得
        return (self.x1, self.y1)
    
    def area_collision(self, area):# エリアの衝突判定
        # エリアの範囲に出たら，エリア内に戻す
        if self.x1 <= area.x1:
            self.x1 = area.x1
        if self.y1 <= area.y1:
            self.y1 = area.y1
        if self.x1 >= area.x2:
            self.x1 = area.x2
        if self.y1 >= area.y2:
            self.y1 = area.y2
    
    def obstacle_collision(self, obstacle, x, y):# 障害物との衝突判定
        if self.x1 >= obstacle.x1 \
            and self.x1 <= obstacle.x2 \
            and self.y1 >= obstacle.y1 \
            and self.y1 <= obstacle.y2:# 障害物に侵入した時
            self.x1 = x
            self.y1 = y
    
    def goal_collision(self, obstacle):# 障害物との衝突判定
        if self.x1 >= obstacle.x1 \
            and self.x1 <= obstacle.x2 \
            and self.y1 >= obstacle.y1 \
            and self.y1 <= obstacle.y2:# 障害物に侵入した時
            return True
        return False
        
    def draw(self):# 描画
        im = plt.plot(self.x1, 
                 self.y1,
                 marker='.', 
                 markersize = 20, 
                 color='#1f77b4')
        return im
    
    def up(self):# 上へ移動
        self.y1 += 1
    def down(self):# 下へ移動
        self.y1 -= 1
    def right(self):# 右へ移動
        self.x1 += 1
    def left(self):# 左へ移動
        self.x1 -= 1

class Goal(MyObject):
    def __init__(self, x, y, width, height):# エリア設定
        super(Goal, self).__init__(x, y, width, height)
    
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width]

        im = plt.plot(x, y, color='#008000')
        return im
# mainの関数
def run(goal_xy, move, fig_draw_mode):
    fig_interval = 1 #画像表示間隔
    max_t = 60
    # fig_draw_mode =1
    
    area = Area(0, 0, 30, 30)# Area 生成
    agent = Agent(2, 2)# agent 生成
    goal = Goal(goal_xy[0], goal_xy[1], 2, 2)
    
    # 障害物リスト　
    bstacle_list = [#Obstacle(14, 8, 2, 20), # 障害物１
                    Obstacle(2, 5, 5, 3),  # 障害物2
                    Obstacle(20, 27, 5, 3), # 障害物3
                    Obstacle(24, 20, 5, 3),  # 障害物4
                    #Obstacle(24, 20, 5, 3),  # 障害物5
                    ]
    
    object_list = [area, agent, goal] + bstacle_list# オブジェクトリスト
    #　描画
    if fig_draw_mode == 1:
        # print(type(fig_draw_mode))
        fig = plt.figure(figsize=(5, 5))
        ims = []; tmp = plt.plot()
        for oject in object_list:
                tmp += oject.draw()
        ims.append(tmp)
    # メインの計算
    for t in range(len(move)):
        if t > max_t:
            break
        x_before = agent.x1#移動前のx座標
        y_before = agent.y1#移動前のy座標
        # --移動--
        if move[t] == 'UP':
            agent.up()
        if move[t] == 'DOWN':
            agent.down()
        if move[t] == 'RIGHT':
            agent.right()
        if move[t] == 'LEFT':
            agent.left()
        # --衝突判定--
        agent.area_collision(area)# エリア
        for bstacle in bstacle_list:# 障害物
            agent.obstacle_collision(bstacle, x_before, y_before)
        # --ゴール判定--
        if agent.goal_collision(goal): break# ゴール(計算の終了)
        #　--描画--
        if fig_draw_mode == 1:
            if t % fig_interval == 0:
                tmp = plt.plot()
                for oject in object_list:
                    tmp += oject.draw()
                ims.append(tmp)

    if fig_draw_mode == 1:
        ani = animation.ArtistAnimation(fig, ims)
        ani.save("output.mp4", writer="pillow")
    
    # 計算の終了
    return agent.getAgent()

if __name__ == "__main__":
    move_list = []
    for i in range(20):
         move_list.append('RIGHT')
         
    print(run([28, 28], move_list, 1))