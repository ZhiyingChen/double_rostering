from . import utils as ul
from . import structures as st
from .log_setup import setup_log
from .read_data import Input
import pandas as pd
import numpy as np
import random
import logging
from copy import deepcopy

class ALNSEnv:
    def __init__(self, input: Input):
        self.data_input = input
        self.best_sol = dict()
        self.min_car4best_sol = dict()

        self.iterMax = 1000
        self.init_temprature = 100
        self.temperature = self.init_temprature
        self.end_temperature = 10
        self.cooling_gradient = 0.97
        self.update_coef = 0.8

        self.wDestroy = [1 for i in range(2)]  # 摧毁算子的初始权重，[1,1]
        self.wRepair = [1 for i in range(2)]  # 修复算子的初始权重，[1,1]
        self.destroyUseTimes = [0 for i in range(2)]  # 摧毁初始次数，[0,0]
        self.repairUseTimes = [0 for i in range(2)]  # 修复初始次数，[0,0]
        self.destroyScore = [1 for i in range(2)]  # 摧毁算子初始得分，[1,1]
        self.repairScore = [1 for i in range(2)]  # 修复算子初始得分，[1,1]

    def calMinCar4curr_sol(self, curr_sol: dict):
        total_min_car_num = 0
        for c_id, serve_num in curr_sol.items():
            if serve_num == 0:
                continue
            carType = self.data_input.cars[c_id]
            minCar = carType.get_car_num4specified_serve(stTime=self.data_input.start_time, edTime=self.data_input.end_time, specified_serve_num=serve_num)
            total_min_car_num += minCar
        return total_min_car_num

    def randomDelete(self, curr_sol):
        car_type_lt = list(curr_sol.keys())
        chosen_lt = random.choice(car_type_lt)
        destroyed_sol = deepcopy(curr_sol)
        delete_num = 0
        for car_type in chosen_lt:
            delete_num += curr_sol[car_type]
            destroyed_sol[car_type] = 0
        return destroyed_sol, delete_num

    def randomPickandCut(self, curr_sol):
        car_type_lt = list(curr_sol.keys())
        pick_key = random.choice(car_type_lt)
        pick_curr_num = curr_sol[pick_key]
        if pick_curr_num == 0:
            return curr_sol, 0
        delete_num = random.randint(0, pick_curr_num)
        destroyed_sol = deepcopy(curr_sol)
        destroyed_sol[pick_key] -= delete_num
        return destroyed_sol, delete_num

    def get_destroy_method(self, operator, curr_sol):
        if operator == 0:
            return self.randomDelete(curr_sol)
        elif operator == 1:
            return self.randomPickandCut(curr_sol)
        else:
            raise BaseException('Unrecognized operator: %s' % operator)

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
        random.shuffle(car_type_lt)
        for c_id in car_type_lt:
            car_type = self.data_input.cars[c_id]
            if remove_num == 0:
                break
            gap = car_type.max_serves - destroyed_sol.get(c_id, 0)
            fill_num = min(gap, remove_num)
            repaired_sol[c_id] = repaired_sol.get(c_id, 0) + fill_num
            remove_num -= fill_num

        return repaired_sol

    def get_repair_method(self, operator, destroyed_sol, remove_num):
        if operator == 0:
            return self.repairSequentially(destroyed_sol, remove_num)
        elif operator == 1:
            return self.repairRandomly(destroyed_sol, remove_num)
        else:
            raise BaseException('Unrecognized operator: %s' % operator)

    def selectAndUseDestroyOperator(self, curr_sol):
        destroyOperator = None  # 算子初始值，除0/1外的数
        sol = deepcopy(curr_sol)  # 深拷贝,currentSolution之后的改变不影响sol
        destroyRoulette = np.array(self.wDestroy).cumsum()  #轮盘赌, cumsum()把列表里之前数的和加到当前列，如a=[1,2,3,4]，comsum结果为[1,3,6,10]
        r = random.uniform(0, max(destroyRoulette))  # 随机生成【0，轮盘赌列表最大数】之间的浮点数
        for i in range(len(self.wDestroy)):
            if destroyRoulette[i] >= r:
                destroyOperator = i
                break
        destroyed_sol, delete_num = self.get_destroy_method(operator=destroyOperator, curr_sol=sol)
        self.destroyUseTimes[destroyOperator] += 1
        return destroyed_sol, delete_num, destroyOperator

    def selectAndUseRepairOperator(self, destroyed_sol, delete_num):
        repairOperator = None
        repairRoulette = np.array(self.wRepair).cumsum()
        r = random.uniform(0, max(self.wRepair))
        for i in range(len(self.wRepair)):
            if repairRoulette[i] >= r:
                repairOperator = i
                break
        repaired_sol = self.get_repair_method(operator=repairOperator, destroyed_sol=destroyed_sol, remove_num=delete_num)
        self.repairUseTimes[repairOperator] += 1
        return repaired_sol, repairOperator

    def generate_init_sol(self):
        sol = dict()
        curr_num = self.data_input.serve_num
        car_type_lt = list(self.data_input.cars.keys())
        random.shuffle(car_type_lt)
        for c_id in car_type_lt:
            car_type = self.data_input.cars[c_id]
            if curr_num == 0:
                break
            fill_num = min(car_type.max_serves, curr_num)
            sol[c_id] = sol.get(c_id, 0) + fill_num
            curr_num -= fill_num
        self.best_sol = deepcopy(sol)
        return sol

    def generate_possible_best_sol(self, sol):
        curr_sol = sol
        iterx = 0
        while iterx < self.iterMax:
            while self.temperature > self.end_temperature:
                destroyed_sol, delete_num, destroyOperator = self.selectAndUseDestroyOperator(curr_sol)
                new_sol, repairOperator = self.selectAndUseRepairOperator(destroyed_sol, delete_num)

                if self.calMinCar4curr_sol(new_sol) <= self.calMinCar4curr_sol(curr_sol):
                    curr_sol = new_sol
                    if self.calMinCar4curr_sol(curr_sol) <= self.calMinCar4curr_sol(self.best_sol):
                        self.best_sol = deepcopy(curr_sol)
                        self.destroyScore[destroyOperator] += 1.5
                        self.repairScore[repairOperator] += 1.5
                    else:
                        self.destroyScore[destroyOperator] += 1.2
                        self.repairScore[repairOperator] += 1.2
                else:
                    if random.random() < np.exp((self.calMinCar4curr_sol(curr_sol)-self.calMinCar4curr_sol(new_sol))/self.temperature):
                        curr_sol = new_sol
                        self.destroyScore[destroyOperator] += 0.8
                        self.repairScore[repairOperator] += 0.8
                    else:
                        self.destroyScore[destroyOperator] += 0.6
                        self.repairScore[repairOperator] += 0.6

                # 更新权重，（1-b）应该放前面，这个例子里取b=0.5，无影响
                self.wDestroy[destroyOperator] = self.wDestroy[destroyOperator] * self.update_coef\
                    + (1 - self.update_coef) * (self.destroyScore[destroyOperator] / self.destroyUseTimes[destroyOperator])
                self.wRepair[repairOperator] = self.wRepair[repairOperator] * self.update_coef\
                    + (1 - self.update_coef) * (self.repairScore[repairOperator] / self.repairUseTimes[repairOperator])

                self.temperature = self.cooling_gradient * self.temperature
            iterx += 1
            self.temperature = self.init_temprature



    def generate_min_car4best_sol(self):
        for c_id, serve_num in self.best_sol.items():
            if serve_num == 0:
                continue
            car_type = self.data_input.cars[c_id]
            self.min_car4best_sol[c_id] = car_type.get_car_num4specified_serve(stTime=self.data_input.start_time,
                                                                               edTime=self.data_input.end_time,
                                                                               specified_serve_num=serve_num)

    def run(self):
        init_sol = self.generate_init_sol()
        self.generate_possible_best_sol(sol=init_sol)
        self.generate_min_car4best_sol()

        logging.info("Best serve num for each car is as follows.")
        for c_id, serve_num in self.best_sol.items():
            logging.info("Car: {} \t Serve num: {} \t Needed cars: {}".format(c_id, serve_num,  self.min_car4best_sol.get(c_id, 0)))

        logging.info("Total needed cars: {}".format(self.calMinCar4curr_sol(self.best_sol)))