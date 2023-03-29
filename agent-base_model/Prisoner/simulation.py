import numpy as np
import random as rnd
import networkx as nx #ターミナルで走らせないとうまくいかない
import pandas as pd
from agent import Agent

class Simulation:
    def __init__(self, population, average_degree):
        self.agents = self.__generate_agents(population, average_degree) #下で説明
        self.initial_cooperators = self.__choose_initial_cooperators() #さらに下で説明

    def __generate_agents(self, population, average_degree):
        #エージェントをリストに詰め、隣人エージェントのIDをリセットする

        rearange_edges = average_degree//2
        network = nx.barabasi_albert_graph(population, rearange_edges) #SNSで似た構造が見られるnetworkを実装

        agents = [Agent() for id in range(population)]
        for index, focal in enumerate(agents):
            neighbors_id = list(network[index])
            for agent_id in neighbors_id:
                focal.neighbors_id.append(agent_id)
        
        return agents
    
    def __choose_initial_cooperators(self):
        #最初のゲームでC戦略をとるエージェントをランダムに選ぶ

        population = len(self.agents)
        initial_cooperators = rnd.sample(range(population), k=int(population/2))

        return initial_cooperators
    
    #続きは初期化から

