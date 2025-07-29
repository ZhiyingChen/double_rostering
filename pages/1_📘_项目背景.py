import streamlit as st
from src.Rostering.web import function as rostering_function
from web import function


function.render_language_selector()
lang, T = function.get_language_dict("doc")

st.title(T["page_title"])

# 项目背景介绍
st.header(T["project_background_header"])
st.markdown(T["project_background_text"])

st.subheader(T["problem_description_subheader"])
# 插入问题描述图片
st.image("src/Rostering/image/Question.png", caption=T["problem_description_image_caption"], width=800)
st.markdown(T["problem_description_details"])

st.markdown(T["constraints_header"])
st.markdown(T["constraint_1"])
st.markdown(T["constraint_2"])
st.markdown(T["constraint_3"])
st.markdown(T["constraint_4"])
st.markdown(T["constraint_5"])
st.markdown(T["constraint_6"])
st.markdown(T["constraint_7"])
st.markdown(T["constraint_8"])
st.markdown(T["constraint_9"])

st.markdown(T["objective_header"])
st.markdown(T["objective"])

rostering_function.render_footer()



