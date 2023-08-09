class GoodsType:
    def __init__(self, type, frozen_dur):

        self.type = type
        self.frozen_dur = frozen_dur

        self.capable_cars = set()

    def __repr__(self):
        return "goodsType(type={}, frozen_dur={})".format(self.type, self.frozen_dur)