import streamlit as st
import pandas as pd
import time
import sys
from src.Rostering.web import function as rostering_function
from src import gantt
from src.data import Input
from src.alns import ALNSEnv
from src.dump import Dump
from web import function

# 渲染语言栏
function.render_language_selector()
lang, T = function.get_language_dict("algo")

st.title(T["page_title"])
st.markdown(T["description"])

# 输入接口文档
st.header(T["input_interface_header"])

with st.expander(T["global_params_expander"]):
    df_global_params = pd.DataFrame(T["global_params_table"], columns=T["global_field"])
    st.table(df_global_params)

    st.markdown(T["global_params_description"])

with st.expander(T["car_info_expander"]):
    df_car_info = pd.DataFrame(T["car_info_table"], columns=T["global_field"])
    st.table(df_car_info)

st.header(T["output_interface_header"])
with st.expander(T["vehicle_result_expander"]):
    st.markdown(T["vehicle_result_details"])

st.markdown("---")
# 示例数据展示
st.header(T["example_data_header"])


@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# 加载示例数据
global_df = load_csv("input/参数表.csv")
car_df = load_csv("input/汽车信息.csv")

# 可编辑的 DataFrame
with st.expander(T["edit_global_params"]):
    edited_global_df = st.data_editor(global_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label=T["download_global_params"],
        data=edited_global_df.to_csv(index=False).encode('utf-8'),
        file_name="全局参数.csv",
        mime="text/csv"
    )

with st.expander(T["edit_car_info"]):
    edited_car_df = st.data_editor(car_df, num_rows="dynamic")
    # 下载按钮
    st.download_button(
        label=T["download_car_info"],
        data=edited_car_df.to_csv(index=False).encode('utf-8'),
        file_name="汽车信息.csv",
        mime="text/csv"
    )

# 显示运行按钮
if st.button(T["run_algorithm"]):
    with st.spinner(T["running_algorithm"]):
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
            st.success(T["algorithm_success"].format(round(time.time() - st_time)))
        except Exception as e:
            st.error(T["algorithm_error"].format(e))

        st.markdown("---")
        st.header(T["output_results"].format(len(result_df.columns)))

        with st.expander(T["vehicle_execution_results"]):
            st.dataframe(result_df)
            st.download_button(
                label=T["download_vehicle_results"],
                data=result_df.to_csv(index=False),
                file_name="车辆和执行结果.csv",
                mime="text/csv"
            )
        with st.spinner(T["drawing_gantt_chart"]):
            gantt.plot_gantt_bar(result_df)

rostering_function.render_footer()