import streamlit as st
from src.Rostering.web import function

if __name__ == '__main__':
    # 渲染语言栏
    function.render_language_selector()
    lang, T = function.get_language_dict("app")

    st.set_page_config(
        page_title=T["page_title"],
        page_icon="📦",
        layout="wide"
    )

    st.title(T["page_title"])
    st.markdown(T["welcome_message"])

    st.markdown(T["navigation_guide"])

    function.render_footer()

