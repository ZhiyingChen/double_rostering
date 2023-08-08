from .Rostering.singleRoster import config as cg
from . import utils as ul
from . import structures as st
from .log_setup import setup_log
from .read_data import Input
import pandas as pd
import numpy as np
import random
import logging
from copy import deepcopy
from collections import defaultdict
from pyomo.environ import Set, ConcreteModel, Var, Constraint, Objective, minimize, maximize
from pyomo.environ import Binary, NonNegativeIntegers, NonNegativeReals
from pyomo.kernel import SolverFactory, value, SolverStatus

class Model4GOODS:
    def __init__(self, input: Input):
        self.data_input = input
        self.use_api_mode = True
        if self.use_api_mode:
            self.opt = SolverFactory('cplex_persistent')
        else:
            self.opt = SolverFactory('cplex_direct')
        # self.opt = SolverFactory('gurobi_persistent')
        self.model = ConcreteModel('Model4GOODS')
        self.task_dict = dict()
        self.goods_maximum = dict()


    def preprocess_data(self):
        self.generate_task_dict()

    def generate_task_dict(self):
        task_dict = defaultdict(dict)
        for car_type_id, car_dict in self.data_input.ALNS_solution.car_act4best_sol.items():
            for car_id, act_dict in car_dict.items():
                for t, act in act_dict.items():
                    if act == cg.actionName.serve:
                        task_dict[t][car_type_id] = task_dict[t].get(car_type_id, 0) + 1
        task_dict = dict(sorted(task_dict.items(), key=lambda x: x[0]))
        self.task_dict = task_dict
        logging.info("Generate task dict.")

    def generate_goods_maximum(self):
        for g_id, good in self.data_input.goods.items():
            pass

    def build_model(self):
        pass