import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="冒泡排序 - 滚动交换动画",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏 Streamlit 默认元素
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background-color: #05070f !important; }
</style>
""", unsafe_allow_html=True)

# 读取 HTML 文件
html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bubble_sort_animation.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# 嵌入动画组件
components.html(html_content, height=900, scrolling=False)
