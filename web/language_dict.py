# 中英字典
APP_LANG = {
    "中文": {
        "page_title": "📦 多类型车辆轮转算法平台",
        "welcome_message": "欢迎使用！请通过左侧导航栏选择功能页面：",
        "navigation_guide": """
### 📘 页面导航说明：
- **项目背景**：了解问题背景
- **执行算法**：了解输入输出文件格式，编辑输入文件，运行算法并查看结果
"""
    },
    "English": {
        "page_title": "📦 Multi-Type Vehicle Rotation Algorithm Platform",
        "welcome_message": "Welcome! Please select a feature page via the left navigation bar:",
        "navigation_guide": """
### 📘 Page Navigation Guide:
- **Project Background**: Understand the problem background
- **Execute Algorithm**: Learn about input/output file formats, edit input files, run the algorithm, and view results
"""
    }
}

# 中英字典
PROJECT_DOC_LANG = {
    "中文": {
        "page_title": "📦 多类型 汽车轮转与维修调度优化系统",
        "project_background_header": "🧩 项目背景简介",
        "project_background_text": """
在大型园区、后勤保障单位或国防工业中，常配备多类型作业车辆以执行不同等级的运输与服务任务。这些车辆需按时轮转执行任务，同时满足维修、安全、工时等现实约束。

本项目基于实际后勤运维需求，构建了一个多类型车、有限维修周期、小时级任务需求的最小车辆数优化模型。通过将经典的“菱形错峰轮转算法”封装为子模块，并引入启发式的“大自然领域搜索（ALNS）”策略，成功提升模型泛化能力与求解效率。
""",
        "problem_description_subheader": "📋 问题描述",
        "problem_description_image_caption": "问题描述图",
        "problem_description_details": """
车站有A种类型的车，每种类型的车数量为Bi ,i=1,2...A；
每种车到目的地执行任务的流程分为：装货，去往目的地，在目的地执行任务，返回车站，卸货。
每项工作所需时间见约束条件。
核心业务需求是在轮转好车执行任务的班次，用最少的车，满足任务要求。
""",
        "constraints_header": "#### 约束条件：",
        "constraint_1": "- 目的地要求同时有P（P为整数）辆车同时执行任务。",
        "constraint_2": "- 每种车装货时间ni,  i=1...A",
        "constraint_3": "- 每种车去往目的地时间ri,  i=1...A",
        "constraint_4": "- 每种车执行任务的时间si,   i=1...A",
        "constraint_5": "- 每种车返回目的地时间r’i,  i=1...A",
        "constraint_6": "- 每种车的卸货时间mi，i=1...A",
        "constraint_7": "- 每种车的最大连续运转周期Ui,  i=1...A；指车（ri+si+r’i）*累计出动架次 >=Ui时，需要维修保障",
        "constraint_8": "- 每种车维修保障时长Di，i=1...A",
        "constraint_9": "- 目的地执行任务的总时间跨度T",
        "objective_header": "#### 🎯 目标：",
        "objective": "- 制定轮转排班方案，用最少的车满足每小时任务需求，并符合车辆维修、出勤等约束"
    },
    "English": {
        "page_title": "📦 Multi-Type Vehicle Rotation and Maintenance Scheduling Optimization System",
        "project_background_header": "🧩 Project Background Overview",
        "project_background_text": """
In large parks, logistics support units, or defense industries, multiple types of operation vehicles are often equipped to perform different levels of transportation and service tasks. These vehicles need to rotate and execute tasks on schedule while meeting constraints such as maintenance, safety, and working hours.

This project constructs a multi-type vehicle, limited maintenance cycle, hourly task demand optimization model based on actual logistics operations needs. By encapsulating the classic “Diamond Peak Shifting Algorithm” into sub-modules and introducing heuristic “Adaptive Large Neighborhood Search (ALNS)” strategies, the model's generalization ability and solution efficiency have been significantly improved.
""",
        "problem_description_subheader": "📋 Problem Description",
        "problem_description_image_caption": "Problem Description Image",
        "problem_description_details": """
There are A types of vehicles, with Bi units of each type, i=1,2,...,A;
Each vehicle goes through the following process to perform tasks at the destination: loading, going to the destination, performing tasks at the destination, returning to the station, and unloading.
The time required for each task is detailed in the constraints below.
The core business requirement is to develop a rotation schedule using the minimum number of vehicles to meet task demands.
""",
        "constraints_header": "#### Constraints:",
        "constraint_1": "- The destination requires P (an integer) vehicles to perform tasks simultaneously.",
        "constraint_2": "- Loading time for each type of vehicle ni,  i=1...A",
        "constraint_3": "- Travel time to the destination for each type of vehicle ri,  i=1...A",
        "constraint_4": "- Task execution time for each type of vehicle si,   i=1...A",
        "constraint_5": "- Return travel time from the destination for each type of vehicle r’i,  i=1...A",
        "constraint_6": "- Unloading time for each type of vehicle mi, i=1...A",
        "constraint_7": "- Maximum continuous operating cycle Ui for each type of vehicle,  i=1...A; indicating that when the sum of (ri + si + r’i) * cumulative trips >= Ui, maintenance is required.",
        "constraint_8": "- Maintenance duration Di for each type of vehicle, i=1...A",
        "constraint_9": "- Total time span T for task execution at the destination",
        "objective_header": "#### 🎯 Objective:",
        "objective": "- Develop a rotation scheduling plan using the minimum number of vehicles to meet hourly task demands and comply with vehicle maintenance and attendance constraints."
    }
}

EXECUTE_ALGORITHM_LANG = {
    "中文": {
        "page_title": "⚙️ 多车型 汽车轮转与维修调度算法",
        "description": """
请在“执行算法”页面将示例输入文件改成你需要的数据。
""",
        "input_interface_header": "📥 输入接口文档",
        "global_params_expander": "📥 输入文件说明：全局参数.csv",
        "global_field": ["字段名称", "类型", "描述"],
        "global_params_table": [
            ["参数名称", "str", "各类参数的名称"],
            ["参数值", "double", "参数值"]
        ],
        "global_params_description": """
**参数枚举说明：**
以下是各个参数的定义和含义：

- **计划开始时间**：小时，整数，例如 0
- **计划结束时间**：小时，整数，例如 720
- **同时服务数量**： 整数，例如 2
""",
        "car_info_expander": "📥 输入文件说明：汽车信息.csv",
        "car_info_table": [
            ["汽车类型", "str", "汽车的类型名称，如 A，B，C"],
            ["汽车数量", "int", "汽车的最多使用的个数"],
            ["装货时间", "int", "该类型汽车装货需要的小时数"],
            ["卸货时间", "int", "该类型汽车卸货需要的小时数"],
            ["去程时间", "int", "该类型汽车去程需要的小时数"],
            ["返程时间", "int", "该类型汽车返程需要的小时数"],
            ["服务时间", "int", "该类型汽车可服务的小时数"],
            ["维修时间", "int", "该类型汽车维修需要的小时数"],
            ["最大工作时间", "int", "该类型汽车最多可服务的小时数，工作满了这个时间就要维修"]
        ],
        "output_interface_header": "📥 输出接口文档",
        "vehicle_result_expander": "📥 输出文件说明：车辆和执行结果.csv",
        "vehicle_result_details": """
每一行代表时间（小时），每一列代表每辆车，内容值含义如下：
- 装货： 0
- 出发： 1
- 服务： 2
- 返回： 3
- 卸货： 4
- 备货： 5
- 维修： 6
- 空闲： 7
""",
        "example_data_header": "📄 示例输入数据（可编辑）",
        "edit_global_params": "📝 编辑全局参数",
        "download_global_params": "📥 下载编辑后的 全局参数.csv",
        "edit_car_info": "📝 编辑汽车信息",
        "download_car_info": "📥 下载编辑后的 汽车信息.csv",
        "run_algorithm": "🚀 运行算法",
        "running_algorithm": "算法运行中，请稍候...",
        "algorithm_success": "✅ 算法运行完成！耗时{}秒",
        "algorithm_error": "❌ 算法运行出错：{}",
        "output_results": "📊 输出结果: 至少需要{}辆车",
        "vehicle_execution_results": "📄 车辆和执行结果",
        "download_vehicle_results": "📥 下载 车辆和执行结果.csv",
        "drawing_gantt_chart": "正在绘制甘特图..."
    },
    "English": {
        "page_title": "⚙️ Multi-Type Vehicle Rotation and Maintenance Scheduling Algorithm",
        "description": """
Please modify the example input files on the "Execute Algorithm" page to your required data.
""",
        "input_interface_header": "📥 Input Interface Documentation",
        "global_params_expander": "📥 Input File Description: global_params.csv",
        "global_field": ["field", "type", "description"],
        "global_params_table": [
            ["Parameter Name", "str", "Names of various parameters"],
            ["Parameter Value", "double", "Values of parameters"]
        ],
        "global_params_description": """
**Parameter Enumeration Explanation:**
Below are the definitions and meanings of each parameter:

- **Plan Start Time**: Hours, integer, e.g., 0
- **Plan End Time**: Hours, integer, e.g., 720
- **Simultaneous Service Quantity**: Integer, e.g., 2
""",
        "car_info_expander": "📥 Input File Description: car_info.csv",
        "car_info_table": [
            ["Car Type", "str", "Type name of the car, e.g., A, B, C"],
            ["Number of Cars", "int", "Maximum number of cars used"],
            ["Loading Time", "int", "Hours required for loading by this type of car"],
            ["Unloading Time", "int", "Hours required for unloading by this type of car"],
            ["Travel Time", "int", "Hours required for traveling to the destination by this type of car"],
            ["Return Time", "int", "Hours required for returning from the destination by this type of car"],
            ["Service Time", "int", "Hours this type of car can serve"],
            ["Maintenance Time", "int", "Hours required for maintenance by this type of car"],
            ["Max Working Time", "int", "Maximum hours this type of car can work before requiring maintenance"]
        ],
        "output_interface_header": "📥 Output Interface Documentation",
        "vehicle_result_expander": "📥 Output File Description: vehicle_and_execution_results.csv",
        "vehicle_result_details": """
Each row represents an hour, each column represents a vehicle, and the content values represent:
- Loading: 0
- Departure: 1
- Service: 2
- Return: 3
- Unloading: 4
- Preparation: 5
- Maintenance: 6
- Idle: 7
""",
        "example_data_header": "📄 Example Input Data (Editable)",
        "edit_global_params": "📝 Edit Global Parameters",
        "download_global_params": "📥 Download Edited global_params.csv",
        "edit_car_info": "📝 Edit Car Information",
        "download_car_info": "📥 Download Edited car_info.csv",
        "run_algorithm": "🚀 Run Algorithm",
        "running_algorithm": "Algorithm running, please wait...",
        "algorithm_success": "✅ Algorithm run successfully! Took {} seconds",
        "algorithm_error": "❌ Algorithm error: {}",
        "output_results": "📊 Output Results: At least {} vehicles needed",
        "vehicle_execution_results": "📄 Vehicle and Execution Results",
        "download_vehicle_results": "📥 Download vehicle_and_execution_results.csv",
        "drawing_gantt_chart": "Drawing Gantt chart..."
    }
}