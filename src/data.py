from src.structures import utils as ul
from src.structures.car_type import CarType
from src.structures.log import setup_log
import pandas as pd
import logging


class Input:
    def __init__(self, input_folder, output_folder):
        setup_log(output_folder, section_name=input_folder)
        self.input_folder = input_folder
        self.cars = dict()
        self.start_time = None
        self.end_time = None
        self.serve_num = None
        self.ALNS_solution = None
        logging.info('start reading data from {}'.format(self.input_folder))

    def load_params(self):
        from src.structures.utils import ParamHeader as ph
        from src.structures.utils import Params as p

        param_df = pd.read_csv(self.input_folder + ul.PLAN_FILE, dtype={ph.paramName: str, ph.paramVal: int})
        param_dict = dict(zip(param_df[ph.paramName], param_df[ph.paramVal]))
        self.start_time = param_dict[p.stTime]
        self.end_time = param_dict[p.edTime]
        self.serve_num = param_dict[p.serveNum]
        logging.info("Finish loading params.")

    def load_car_info(self):
        from src.structures.utils import CarInfoHeader as pih

        car_df = pd.read_csv(self.input_folder + ul.CAR_INFO_FILE, dtype={
            pih.carType: str,
            pih.carNum: int,
            pih.packDur: int,
            pih.unpackDur: int,
            pih.goDur: int,
            pih.returnDur: int,
            pih.serveDur: int,
            pih.restDur: int,
            pih.maxWorkDur: int
        })

        cars = dict()
        for idx, row in car_df.iterrows():
            car_type = CarType(
                type=row[pih.carType],
                total_num=row[pih.carNum],
                upload_dur=row[pih.packDur],
                leave_dur=row[pih.goDur],
                serve_dur=row[pih.serveDur],
                return_dur=row[pih.returnDur],
                unpack_dur=row[pih.unpackDur],
                rest_dur=row[pih.restDur],
                full_dur=row[pih.maxWorkDur]
            )
            cars[car_type.type] = car_type

        logging.info("Finish loading car type info: {}".format(len(cars)))
        return cars

    def load_data(self):
        self.load_params()
        self.cars = self.load_car_info()
        logging.info("Finish loading data.")

    def generate_max_serves4cars(self):
        for p, car_type in self.cars.items():
            car_type.generate_max_serve_num(stTime=self.start_time, edTime=self.end_time)

    def check_feasibility(self):
        max_serve_num = sum(car_type.max_serves for c_id, car_type in self.cars.items())
        if max_serve_num < self.serve_num:
            logging.error("Total serving num {} is smaller than required {}.".format(max_serve_num, self.serve_num))
            raise BaseException
        else:
            logging.info(
                "Total serving num {} is equal to or larger than required {}.".format(max_serve_num, self.serve_num))

    def generate_data(self):
        self.load_data()
        # Finish loading data
        self.generate_max_serves4cars()
        self.check_feasibility()
        # self.generate_min_serves4cars()
