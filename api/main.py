import asyncio
import csv
import json
import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, StrictInt, model_validator


ROOT = Path(__file__).resolve().parent.parent
PARAMETERS = ["计划开始时刻", "计划结束时刻", "同时服务数量"]
CAR_FIELDS = ["汽车类型", "汽车数量", "装货时间", "卸货时间", "去程时间", "返程时间", "服务时间", "维修时间", "最大工作时间"]
app = FastAPI(title="Double Rostering · 多车型轮转优化 API", version="1.0.0")
gate = asyncio.Semaphore(1)
logger = logging.getLogger(__name__)


class SolveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parameters: dict[str, StrictInt]
    car_types: list[dict[str, StrictInt | str]]

    @model_validator(mode="after")
    def validate_input(self):
        if set(self.parameters) != set(PARAMETERS):
            raise ValueError("必须提供计划起止时刻和同时服务数量")
        values = self.parameters
        if values["计划开始时刻"] < 0 or not 1 <= values["计划结束时刻"] - values["计划开始时刻"] <= 1440:
            raise ValueError("计划跨度必须为 1–1440 小时")
        if not 1 <= values["同时服务数量"] <= 20:
            raise ValueError("同时服务数量必须为 1–20")
        if not 1 <= len(self.car_types) <= 8:
            raise ValueError("汽车类型数量必须为 1–8")
        names = set()
        for car in self.car_types:
            if set(car) != set(CAR_FIELDS) or car["汽车类型"] in names:
                raise ValueError("每种车型必须包含完整字段，且名称不能重复")
            names.add(car["汽车类型"])
            if not 1 <= car["汽车数量"] <= 100 or any(car[field] < 0 or car[field] > 336 for field in CAR_FIELDS[2:]):
                raise ValueError("车型数量或时长超出允许范围")
            if car["服务时间"] < 1 or car["最大工作时间"] < car["装货时间"] + car["去程时间"] + car["服务时间"] + car["返程时间"] + car["卸货时间"]:
                raise ValueError(f"车型 {car['汽车类型']} 的任务周期不可行")
        return self


@app.get("/api/health")
def health():
    return {"status": "ok", "solver": "ALNS multi-type rostering", "max_concurrent_solves": 1, "timeout_seconds": 25}


@app.get("/api/example")
def example():
    with (ROOT / "input/参数表.csv").open(encoding="utf-8-sig", newline="") as source:
        parameters = {row["参数名称"]: int(row["参数值"]) for row in csv.DictReader(source)}
    with (ROOT / "input/汽车信息.csv").open(encoding="utf-8-sig", newline="") as source:
        car_types = [{key: int(value) if key != "汽车类型" else value for key, value in row.items()} for row in csv.DictReader(source)]
    return {"parameters": parameters, "car_types": car_types}


@app.post("/api/solve")
async def solve(payload: SolveRequest):
    try:
        await asyncio.wait_for(gate.acquire(), timeout=0.1)
    except TimeoutError:
        raise HTTPException(429, "求解器正忙，请稍后重试")
    process = None
    try:
        process = await asyncio.create_subprocess_exec(sys.executable, "-m", "api.worker", cwd=ROOT,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        output, errors = await asyncio.wait_for(process.communicate(payload.model_dump_json().encode()), timeout=25)
        if process.returncode:
            logger.error("ALNS failed: %s", errors.decode(errors="replace")[-2000:])
            raise HTTPException(422, "当前车型组合无法生成可行排班，请检查车辆数量和工时约束")
        result = json.loads(output)
        result["warnings"] = [warning for warning in result["warnings"] if warning]
        return result
    except TimeoutError:
        raise HTTPException(504, "求解超过 25 秒，请缩小计划跨度或减少车型规模")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected ALNS error")
        raise HTTPException(500, "算法内部异常，请稍后重试")
    finally:
        if process is not None and process.returncode is None:
            process.kill()
            await process.wait()
        gate.release()


app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
