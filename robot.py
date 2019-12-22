# -*- coding: utf-8 -*-
"""
実装すべきもの:
    荷物オブジェクトを作成
    アニメーション
    ＧＡを適用
    
    
注意事項:
    オブジェクトの描画はareaからしなければならない
    plt.figure()で初期化されるため

"""
import matplotlib.pyplot as plt
import random 

# オブジェクト
class My_object():
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y
# エリア
class Area(My_object):
    def __init__(self, x, y, width, height):# エリア設定
        super(Area, self).__init__(x, y)
        self.x2 = x + width
        self.y2 = y + height
        
    def draw(self):# 描画
        plt.figure()
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width
             ]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width
             ]

        plt.plot(x, y, color='#1f77b4')
        margin_width = 5
        plt.ylim(self.x1 - margin_width, 
                 self.x2 + margin_width)
        plt.xlim(self.y1 - margin_width, 
                 self.y2 + margin_width)
# 障害物
class Obstacle(My_object):
    def __init__(self, x, y, width, height):# エリア設定
        super(Obstacle, self).__init__(x, y)
        self.x2 = x + width
        self.y2 = y + height
    
    def draw(self):# 描画
        width = 0.9
        x = [self.x1 - width, 
             self.x1 - width, 
             self.x2 + width, 
             self.x2 + width, 
             self.x1 - width
             ]
        
        y = [self.y1 - width, 
             self.y2 + width, 
             self.y2 + width, 
             self.y1 - width, 
             self.y1 - width
             ]

        plt.plot(x, y, color='#FF0000')
# エージェント
class Agent(My_object):
    def __init__(self, x, y):# 初期設定
        super(Agent, self).__init__(x, y)
    
    def area_collision(self, area):# エリアの衝突判定
        # エリアの範囲に出たら，エリア内の戻す
        if self.x1 < area.x1:
            self.x1 = area.x1
        if self.y1 < area.y1:
            self.y1 = area.y1
        if self.x1 > area.x2:
            self.x1 = area.x2
        if self.y1 > area.y2:
            self.y1 = area.y2
    
    def obstacle_collision(self, obstacle, x, y):# 障害物との衝突判定
        if self.x1 >= obstacle.x1 \
            and self.x1 <= obstacle.x2 \
            and self.y1 >= obstacle.y1 \
            and self.y1 <= obstacle.y2:# 障害物に侵入した時
            self.x1 = x
            self.y1 = y
    
    def draw(self):# 描画
        plt.plot(self.x1, 
                 self.y1,
                 marker='.', 
                 markersize = 20, 
                 color='#1f77b4')
    
    def up(self):# 上へ移動
        self.y1 += 1
    def down(self):# 下へ移動
        self.y1 -= 1
    def right(self):# 右へ移動
        self.x1 += 1
    def left(self):# 左へ移動
        self.x1 -= 1
# main関数
def main():
    max_t = 10# 最大ステップ数
    fig_interval = 1
    
    area = Area(0, 0, 30, 30)# Area 生成
    agent = Agent(5, 5)# agent 生成
    bstacle1 = Obstacle(15, 5, 2, 5)# 障害物1 生成
    bstacle2 = Obstacle(5, 15, 5, 3)# 障害物2 生成
    
    bstacle_list = [bstacle1, bstacle2]
    object_list = [area, agent] + bstacle_list
    #　描画
    for oject in object_list:
            oject.draw()
    
    for t in range(max_t):
        x_before = agent.x1#移動前のx座標
        y_before = agent.y1#移動前のy座標
        #--移動--
        if random.random() < 1/4:
            agent.up()
        elif random.random() < 2/4:
            agent.down()
        elif random.random() < 3/4:
            agent.right()
        else:
            agent.left()
        #agent.right()
        # 衝突判定
        agent.area_collision(area)# エリア
        for bstacle in bstacle_list:
            agent.obstacle_collision(bstacle, 
                                     x_before, 
                                     y_before)# 障害物
        #　描画
        if t % fig_interval ==0:
            for oject in object_list:
                oject.draw()



main()