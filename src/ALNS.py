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

