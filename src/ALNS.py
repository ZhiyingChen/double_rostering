from . import utils as ul
from . import structures as st
from .log_setup import setup_log
from .read_data import Input
import pandas as pd
import logging

class ALNSEnv:
    def __init__(self, input: Input):
        self.data_input = input
        self.best_sol = dict()

        self.iterMax = 100
        self.temperature = 100
        self.cooling_gradient = 0.97
        self.update_coef = 0.5

        self.wDestroy = [1 for i in range(2)]  # 摧毁算子的初始权重，[1,1]
        self.wRepair = [1 for i in range(2)]  # 修复算子的初始权重
        self.destroyUseTimes = [0 for i in range(2)]  # 摧毁初始次数，0
        self.repairUseTimes = [0 for i in range(2)]  # 修复初始次数
        self.destroyScore = [1 for i in range(2)]  # 摧毁算子初始得分，1
        self.repairScore = [1 for i in range(2)]  # 修复算子初始得分

    def calMinCar(self, curr_sol: dict):
        total_min_car_num = 0
        for c_id, serve_num in curr_sol.items():
            carType = self.data_input.cars[c_id]
            minCar = carType.get_car_num4specified_serve(stTime=self.data_input.start_time, edTime=self.data_input.end_time, specified_serve_num=serve_num)
            total_min_car_num += minCar
        return total_min_car_num

    def randomDelete(self):
        pass

    def randomPickandCut(self):
        pass

    def repairSequentially(self):
        pass

    def repairRandomly(self):
        pass

    def selectAndUseDestroyOperator(self):
        pass

    def selectAndUseRepairOperator(self):
        pass

