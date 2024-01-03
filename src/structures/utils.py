CAR_INFO_FILE = '/飞机信息.csv'
PLAN_FILE = '/参数表.csv'


class CarInfoHeader:
    carType = '飞机类型'
    carNum = '飞机数量'
    packDur = '装货时间'
    unpackDur = '卸货时间'
    goDur = '去程时间'
    returnDur = '返程时间'
    serveDur = '服务时间'
    restDur = '维修时间'
    maxWorkDur = '最大工作时间'


class ParamHeader:
    paramName = '参数名称'
    paramVal = '参数值'


class Params:
    stTime = '计划开始时刻'
    edTime = '计划结束时刻'
    serveNum = '同时服务数量'
