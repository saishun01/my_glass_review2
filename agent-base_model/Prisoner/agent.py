import random as rnd
import numpy as np

class Agent:
    def __init__(self):
        self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.neighbors_id = []
    
    def decide_next_strategy(self,agents):
        #Pairwise-Fermiモデルで次のゲームでの戦略を決定する
        opponent_id = rnd.choice(self.neighbors_id) #参照する隣人はランダム
        opponent = agents[opponent_id]

        if opponent.strategy != self.strategy and rnd.random() < np.exp((self.point - opponent.point)/0.1): #温度係数0.1
            self.next_strategy = opponent.strategy #戦略を真似る

    def updata_strategy(self):
        self.strategy = self.next_strategy
