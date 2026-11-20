import json
import logging
import os
import random
import sys
import tempfile
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from src.alns import ALNSEnv
from src.data import Input
from src.dump import Dump


LABELS = ["装货", "去程", "服务", "返程", "卸货", "备货", "维修", "空闲"]


def solve(payload):
    started = perf_counter()
    random.seed(7)
    np.random.seed(7)
    with tempfile.TemporaryDirectory(prefix="double-rostering-") as directory:
        workspace = Path(directory)
        input_folder = workspace / "input"
        output_folder = workspace / "output"
        input_folder.mkdir()
        output_folder.mkdir()
        pd.DataFrame(payload["parameters"].items(), columns=["参数名称", "参数值"]).to_csv(input_folder / "参数表.csv", index=False)
        pd.DataFrame(payload["car_types"]).to_csv(input_folder / "汽车信息.csv", index=False)
        previous_directory = Path.cwd()
        try:
            os.chdir(workspace)
            data = Input(input_folder="input", output_folder="output")
            data.generate_data()
            method = ALNSEnv(input=data)
            method.run()
            matrix = Dump(data=data).generate_output_df()
        finally:
            os.chdir(previous_directory)
            logging.shutdown()

    hours = [int(value) for value in matrix.index]
    vehicles = []
    segments = []
    for identifier, column in enumerate(matrix.columns, 1):
        states = [int(value) for value in matrix[column]]
        vehicle_type = str(column).split("_", 1)[-1]
        vehicles.append({"id": identifier, "label": str(column), "type": vehicle_type,
                         "states": states, "work_hours": sum(state < 6 for state in states),
                         "service_hours": states.count(2), "maintenance_hours": states.count(6)})
        begin = 0
        for offset in range(1, len(states) + 1):
            if offset == len(states) or states[offset] != states[begin]:
                segments.append({"vehicle": identifier, "label": str(column), "type": vehicle_type,
                                 "start": hours[begin], "end": hours[begin] + offset - begin,
                                 "state": states[begin], "activity": LABELS[states[begin]]})
                begin = offset
    coverage = [sum(vehicle["states"][offset] == 2 for vehicle in vehicles) for offset in range(len(hours))]
    required = payload["parameters"]["同时服务数量"]
    shortage = sum(max(0, required - value) for value in coverage)
    type_summary = []
    for car_type in payload["car_types"]:
        name = car_type["汽车类型"]
        typed = [vehicle for vehicle in vehicles if vehicle["type"] == name]
        type_summary.append({"type": name, "available": car_type["汽车数量"], "used": len(typed),
                             "service_hours": sum(vehicle["service_hours"] for vehicle in typed)})
    work_values = [vehicle["work_hours"] for vehicle in vehicles] or [0]
    return {"status": "completed", "algorithm": "ALNS multi-type rostering + single-type rotation",
            "runtime_seconds": round(perf_counter() - started, 4), "hours": hours, "vehicles": vehicles,
            "segments": segments, "coverage": coverage, "labels": LABELS, "type_summary": type_summary,
            "allocation": method.best_sol, "kpis": {"vehicles": len(vehicles),
                "coverage_percent": round(100 * (1 - shortage / (len(hours) * required)), 2),
                "shortage_vehicle_hours": shortage, "service_hours": sum(coverage),
                "work_hours": sum(work_values), "maintenance_hours": sum(v["maintenance_hours"] for v in vehicles),
                "work_spread_hours": max(work_values) - min(work_values)},
            "warnings": [f"计划启动阶段存在 {shortage} 车·小时服务缺口。" if shortage else ""]}


if __name__ == "__main__":
    try:
        print(json.dumps(solve(json.loads(sys.stdin.read())), ensure_ascii=False, allow_nan=False))
    except BaseException as error:
        print(json.dumps({"error": type(error).__name__, "message": str(error)}, ensure_ascii=False))
        sys.exit(1)
