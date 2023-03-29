#2次元平面内で動作するエージェント
#結果をグラフ描画

import numpy as np
import matplotlib.pyplot as plt

#定数
TIMELIMIT = 100

#クラス定義
class Agent:
    def __init__(self, cat):
        self.category = cat #カテゴリの指定
        #初期位置・初期速度
        self.x = 0 
        self.y = 0
        self.dx = 0
        self.dy = 1
    def calcnext(self): #次時刻の状態の計算
        if self.category == 0: #カテゴリ0の計算
            self.cat0()
        else:
            print("ERROR カテゴリがありません\n")
    def cat0(self): #カテゴリ0の計算の中身
        self.dx = self.reverse(self.dx)
        self.dy = self.reverse(self.dy)
        self.x += self.dx
        self.y += self.dy
    def reverse(self,i): #0を1に，1を0に
        if i == 0:
            return 1
        else:
            return 0
    def putstate(self): #状態の出力
        print(self.x, self.y)

#クラス定義終了

#下請け関数の定義
def calcn(a): #aというエージェント群の計算
    for i in range(len(a)):
        a[i].calcnext()
        a[i].putstate()

        xlist.append(a[i].x)
        ylist.append(a[i].y)

#メイン実行部
#初期化
a = [Agent(0)]

#グラフデータの初期化
xlist = []
ylist = []

#エージェントシミュレーション
for t in range(TIMELIMIT):
    calcn(a)
    plt.clf()
    plt.axis([0,60,0,60])
    plt.plot(xlist,ylist,".")
    plt.pause(0.01)
    xlist.clear()
    ylist.clear()
plt.show()
