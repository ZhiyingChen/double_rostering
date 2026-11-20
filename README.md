# Double Rostering Lab

多车型车辆轮转优化应用。系统使用两层真实算法：外层 ALNS 在车型之间分配同时服务需求，内层复用 `src/Rostering/singleRoster` 为每种车型生成车辆任务与维修轮转。

## 本地运行

```powershell
git submodule update --init --recursive
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-api.txt
.\.venv\Scripts\python -m uvicorn api.main:app --reload --port 8093
```

打开 `http://127.0.0.1:8093/`，API 文档为 `/docs`。

## 输入

- 全局参数：计划开始、计划结束、同时服务数量。
- 车型参数：车型名称、可用数量、装卸时间、往返时间、服务时间、维修时间、最大工作时间。
- 示例数据来自 `input/参数表.csv` 和 `input/汽车信息.csv`。

每次 API 求解都在独立临时目录中运行，不共享可变模型对象，也不会覆盖项目输入或输出。单实例限制为一个并发求解，超时为 25 秒。

## 输出

API 返回总用车数、车型服务分配、车型启用数量、覆盖率、服务和维修工时、车辆任务矩阵及可导出的任务片段。

原有 Streamlit 页面保留兼容；公开入口使用 `frontend/` 与 `api/`。
