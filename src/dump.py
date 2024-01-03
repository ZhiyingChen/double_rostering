from src.Rostering.singleRoster.car import Car
from .data import Input
import pandas as pd
class Dump:
    def __init__(self, data: Input):
        self.data = data

    def generate_car_record(self, car: Car):
        from src.Rostering.singleRoster import config as cg

        record = {k: cg.Sign.spare for k in range(self.data.start_time, self.data.end_time + 1)}

        for t, event in car.schedule.items():
            if cg.actionName.serve in event.keys():
                serve_dur = event[
                                cg.actionName.serve] - car.upload_dur - car.leave_dur - car.return_dur - car.unpack_dur - car.prepare_dur
                curr_t = t

                for i in range(car.upload_dur):
                    record[curr_t] = cg.Sign.upload
                    curr_t += 1

                for i in range(car.leave_dur):
                    record[curr_t] = cg.Sign.leave
                    curr_t += 1

                for i in range(serve_dur):
                    record[curr_t] = cg.Sign.serve
                    curr_t += 1

                for i in range(car.return_dur):
                    record[curr_t] = cg.Sign.back
                    curr_t += 1
                for i in range(car.unpack_dur):
                    record[curr_t] = cg.Sign.unpack
                    curr_t += 1
                for i in range(car.prepare_dur):
                    record[curr_t] = cg.Sign.prepare
                    curr_t += 1

            elif cg.actionName.rest in event.keys():
                curr_t = t
                for i in range(car.rest_dur):
                    record[curr_t] = cg.Sign.fix
                    curr_t += 1
        return record

    def generate_output_df(self):

        record_dict = dict()

        car_num = 1
        for car_type, car_dict in self.data.ALNS_solution.items():
            for c_id, car in car_dict.items():
                car_record = self.generate_car_record(car=car)
                record_dict.update({'{}_{}'.format(car_num, car_type):car_record})
                car_num += 1

        out_df = pd.DataFrame(record_dict, dtype=object)
        out_df = out_df.loc[self.data.start_time:self.data.end_time]
        out_df.to_csv('{}/result.csv'.format(self.data.output_folder))
