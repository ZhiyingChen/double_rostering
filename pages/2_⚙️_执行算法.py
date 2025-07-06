import streamlit as st
import pandas as pd
import time
import sys
from src.Rostering.web import function
from src import gantt
from src.data import Input
from src.alns import ALNSEnv
from src.dump import Dump


st.title("⚙️ 多车型 汽车轮转与维修调度算法")

st.markdown(
    """
    请在“执行算法”页面将示例输入文件改成你需要的数据。
    """
)

# 输入接口文档
# 输入接口文档
st.header("📥 输入接口文档")

with st.expander("📥 输入文件说明：全局参数.csv"):
    df_global_params = pd.DataFrame([
        ["参数名称", "str", "各类参数的名称"],
        ["参数值", "double", "参数值"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_global_params)

    st.markdown("""
        **参数枚举说明：**
        以下是各个参数的定义和含义：

        - **计划开始时间**：小时，整数，例如 0
        - **计划结束时间**：小时，整数，例如 720
        - **同时服务数量**： 整数，例如 2
    
    """)

with st.expander("📥 输入文件说明：汽车信息.csv"):
    df_car_info = pd.DataFrame([
        ["汽车类型", "str", "汽车的类型名称，如 A，B，C"],
        ["汽车数量", "int", "汽车的最多使用的个数"],
        ["装货时间", "int", "该类型汽车装货需要的小时数"],
        ["卸货时间", "int", "该类型汽车卸货需要的小时数"],
        ["去程时间", "int", "该类型汽车去程需要的小时数"],
        ["返程时间", "int", "该类型汽车返程需要的小时数"],
        ["服务时间", "int", "该类型汽车可服务的小时数"],
        ["维修时间", "int", "该类型汽车维修需要的小时数"],
        ["最大工作时间", "int", "该类型汽车最多可服务的小时数，工作满了这个时间就要维修"]
    ], columns=["字段名称", "类型", "描述"])
    st.table(df_car_info)


st.header("📥 输出接口文档")
with st.expander("📥 输出文件说明：车辆和执行结果.csv"):
    st.markdown(
        """
        每一行代表时间（小时），每一列代表每辆车，内容值含义如下
        - 装货： 0
        - 出发： 1
        - 服务： 2
        - 返回： 3
        - 卸货： 4
        - 备货： 5
        - 维修： 6
        - 空闲： 7
        """
    )

st.markdown("---")
# 示例数据展示
st.header("📄 示例输入数据（可编辑）")


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# 加载示例数据
global_df = load_csv("input/参数表.csv")
car_df = load_csv("input/汽车信息.csv")

# 可编辑的 DataFrame
with st.expander("📝 编辑全局参数"):
    edited_global_df = st.data_editor(global_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 全局参数.csv",
        data=edited_global_df.to_csv(index=False).encode('utf-8'),
        file_name="全局参数.csv",
        mime="text/csv"
    )

with st.expander("📝 编辑汽车信息"):
    edited_car_df = st.data_editor(
        car_df, num_rows="dynamic"
    )
    # 下载按钮
    st.download_button(
        label="📥 下载编辑后的 汽车信息.csv",
        data=edited_car_df.to_csv(index=False).encode('utf-8'),
        file_name="汽车信息.csv",
        mime="text/csv"
    )

# 显示运行按钮
if st.button("🚀 运行算法"):
    with st.spinner("算法运行中，请稍候..."):
        try:
            st_time = time.time()

            input_folder = 'input'
            if 'win' in sys.platform:
                output_folder = './output/'
            else:
                output_folder = '/tmp/'

            input_data = Input(
                input_folder=input_folder, output_folder=output_folder
            )
            input_data.generate_data()

            ALNSMethod = ALNSEnv(input=input_data)
            ALNSMethod.run()

            dumper = Dump(data=input_data)
            result_df = dumper.generate_output_df()
            st.success("✅ 算法运行完成！耗时{}秒".format(round(time.time() - st_time)))
        except Exception as e:
            st.error(f"❌ 算法运行出错：{e}")

        st.markdown("---")
        st.header("📊 输出结果: 至少需要{}辆车".format(len(result_df.columns)))

        with st.expander("📄 车辆和执行结果"):
            st.dataframe(result_df)
            st.download_button(
                label=f"📥 下载 车辆和执行结果.csv",
                data=result_df.to_csv(index=False),
                file_name="车辆和执行结果.csv",
                mime="text/csv"
            )
        with st.spinner("正在绘制甘特图..."):
            gantt.plot_gantt_bar(result_df)

function.render_footer()
