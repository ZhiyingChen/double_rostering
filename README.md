# Rostering

**Problem Description**

机场里有A种类型的车，每种类型的车数量为Bi ,i=1,2...A；

每种车到目的地执行任务的流程分为：装货，去往目的地，在目的地执行任务，返回机场，卸货。

每项工作所需时间见约束条件。

核心业务需求是在轮转好车执行任务的班次，用最少的车，满足任务要求。

    约束条件：
    
    目的地要求同时有P（P为整数）辆车同时执行任务。
    
    每种车装货时间ni,  i=1...A
    
    每种车去往目的地时间ri,  i=1...A
    
    每种车执行任务的时间si,   i=1...A
    
    每种车返回目的地时间r’i,  i=1...A
    
    每种车的卸货时间mi，i=1...A
    
    每种车的最大连续运转周期Ui,  i=1...A；指车（ri+si+r’i）*累计出动架次 >=Ui时，需要维修保障
    
    每种车维修保障时长Di，i=1...A
    
    目的地执行任务的总时间跨度T
    
    优化目标：
    
    飞机数量最少


**Environment Deployment**

 Install Python Executor (version >= 3.7.0), Anaconda IDE is recommended


The required packages are listed in requirements.txt. you can install them using:

    pip install -r requirements.txt
 
 **Run**

To run project:

    1. put your input data in input folder, you can adjust parameters.
    2. execute python main.py, and result.csv will be generated in output folder.

**Result Explanation**

    装货： 0
    
    出发： 1
    
    服务： 2
    
    返回： 3
    
    卸货： 4
    
    备货： 5
    
    维修： 6
    
    空闲： 7




