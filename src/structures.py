from .Rostering.singleRoster import data_structure as sds
import math
import logging

class carType:
    def __init__(self, type, total_num,
                 upload_dur, leave_dur, serve_dur, return_dur, unpack_dur, rest_dur, full_dur):

        self.type = type
        self.total_num = total_num

        self.upload_dur = upload_dur
        self.leave_dur = leave_dur
        self.serve_dur = serve_dur
        self.return_dur = return_dur
        self.unpack_dur = unpack_dur
        self.rest_dur = rest_dur
        self.full_dur = full_dur
        self.prepare_dur = 0

        self.capable_goods = set()
        self.max_serves = None

    def __repr__(self):
        return "carType(type={}, total={}, max_serves={})".format(self.type, self.total_num, self.max_serves)

    def generate_max_serve_num(self, stTime, edTime):

        oneServe = sds.Solver(stTime=stTime, edTime=edTime, serveNum=1,
                 upload_dur=self.upload_dur, unpack_dur=self.unpack_dur,
                 prepare_dur=self.prepare_dur, leave_dur=self.leave_dur,
                 return_dur=self.return_dur, serve_dur=self.serve_dur, rest_dur=self.rest_dur,
                    full_dur=self.full_dur)
        car4one = oneServe.generate_min_car_num()
        min_serves = math.ceil(self.total_num / car4one)

        curr_needed_planes = 0
        serve_num = min_serves
        while curr_needed_planes <= self.total_num:
            k = serve_num + 1
            currServe = sds.Solver(stTime=stTime, edTime=edTime, serveNum=k,
                 upload_dur=self.upload_dur, unpack_dur=self.unpack_dur,  prepare_dur=self.prepare_dur,
                leave_dur=self.leave_dur, return_dur=self.return_dur, serve_dur=self.serve_dur, rest_dur=self.rest_dur,
                    full_dur=self.full_dur)
            curr_needed_planes = currServe.generate_min_car_num()
            if curr_needed_planes <= self.total_num:
                serve_num += 1

        self.max_serves = serve_num
        logging.info("Max serving num for plane type {} is {}".format(self.type, self.max_serves))


class goodsType:
    def __init__(self, type, frozen_dur):

        self.type = type
        self.frozen_dur = frozen_dur

        self.capable_cars = set()

    def __repr__(self):
        return "goodsType(type={}, frozen_dur={})".format(self.type, self.frozen_dur)