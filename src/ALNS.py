from . import utils as ul
from . import structures as st
from .log_setup import setup_log
from .read_data import Input
import pandas as pd
import numpy as np
import logging
from copy import deepcopy

class ALNSEnv:
    def __init__(self, input: Input):
        self.data_input = input
        self.best_sol = dict()

        self.iterMax = 100
        self.temperature = 100
        self.cooling_gradient = 0.97
        self.update_coef = 0.5

        self.wDestroy = [1 for i in range(2)]  # 摧毁算子的初始权重，[1,1]
        self.wRepair = [1 for i in range(2)]  # 修复算子的初始权重，[1,1]
        self.destroyUseTimes = [0 for i in range(2)]  # 摧毁初始次数，[0,0]
        self.repairUseTimes = [0 for i in range(2)]  # 修复初始次数，[0,0]
        self.destroyScore = [1 for i in range(2)]  # 摧毁算子初始得分，[1,1]
        self.repairScore = [1 for i in range(2)]  # 修复算子初始得分，[1,1]

    def calMinCar4curr_sol(self, curr_sol: dict):
        total_min_car_num = 0
        for c_id, serve_num in curr_sol.items():
            carType = self.data_input.cars[c_id]
            minCar = carType.get_car_num4specified_serve(stTime=self.data_input.start_time, edTime=self.data_input.end_time, specified_serve_num=serve_num)
            total_min_car_num += minCar
        return total_min_car_num

    def randomDelete(self, curr_sol):
        car_type_lt = list(curr_sol.keys())
        chosen_lt = np.random.choice(car_type_lt, 2)
        destroyed_sol = deepcopy(curr_sol)
        delete_num = 0
        for car_type in chosen_lt:
            delete_num += curr_sol[car_type]
            destroyed_sol[car_type] = 0
        return destroyed_sol, delete_num

    def randomPickandCut(self, curr_sol):
        car_type_lt = list(curr_sol.keys())
        pick_key = np.random.choice(car_type_lt)
        pick_curr_num = curr_sol[pick_key]
        if pick_curr_num == 0:
            return curr_sol, 0
        rand_cut = np.random.randint(0, pick_curr_num)
        destroyed_sol = deepcopy(curr_sol)
        destroyed_sol[pick_key] -= rand_cut
        return destroyed_sol, rand_cut

    def repairSequentially(self, destroyed_sol, remove_num):
        repaired_sol = deepcopy(destroyed_sol)
        for c_id, car_type in self.data_input.cars.items():
            if remove_num == 0:
                break
            gap = car_type.max_serves - destroyed_sol.get(c_id, 0)
            fill_num = min(gap, remove_num)
            repaired_sol[c_id] = repaired_sol.get(c_id, 0) + fill_num
            remove_num -= fill_num

        return repaired_sol

    def repairRandomly(self, destroyed_sol, remove_num):
        repaired_sol = deepcopy(destroyed_sol)
        car_type_lt = list(self.data_input.cars.keys())
        np.random.shuffle(car_type_lt)
        for c_id in car_type_lt:
            car_type = self.data_input.cars[c_id]
            if remove_num == 0:
                break
            gap = car_type.max_serves - destroyed_sol.get(c_id, 0)
            fill_num = min(gap, remove_num)
            repaired_sol[c_id] = repaired_sol.get(c_id, 0) + fill_num
            remove_num -= fill_num

        return repaired_sol

    def selectAndUseDestroyOperator(self):
        pass

    def selectAndUseRepairOperator(self):
        pass

