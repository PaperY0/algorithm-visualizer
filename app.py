import streamlit as st
import time
from algorithms.bubble_sort import bubble_sort, BUBBLE_SORT_INFO
from algorithms.base import Step
from visualizer.renderer import render_array
from visualizer.code_highlight import render_code

# 页面配置
st.set_page_config(
    page_title="排序算法可视化",
    page_icon="📊",
    layout="wide"
)

st.title("📊 排序算法可视化学习工具")

# 初始化 session_state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = None
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'speed' not in st.session_state:
    st.session_state.speed = 0.5

# 侧边栏：数据输入
with st.sidebar:
    st.header("数据设置")

    data_option = st.radio("数据来源", ["随机生成", "手动输入"])

    if data_option == "随机生成":
        array_size = st.slider("数组大小", 5, 20, 8)
        if st.button("生成随机数组"):
            import random
            st.session_state.input_array = random.sample(
                range(1, array_size * 2), array_size
            )
    else:
        input_str = st.text_input("输入数字（逗号分隔）", "5,3,8,1,9,2,7,4")
        st.session_state.input_array = [
            int(x.strip()) for x in input_str.split(',')
        ]

    st.divider()

    # 算法选择（目前只有冒泡排序）
    st.header("算法选择")
    algorithm = st.selectbox("选择排序算法", ["冒泡排序"])

    st.divider()

    # 速度控制
    st.header("播放控制")
    speed = st.slider("速度（秒/步）", 0.1, 2.0, 0.5, 0.1)
    st.session_state.speed = speed

# 主界面
col_viz, col_code = st.columns([1, 1])

# 左侧：可视化区域
with col_viz:
    st.subheader("可视化")

    # 控制按钮
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

    with btn_col1:
        if st.button("▶ 开始", use_container_width=True):
            if 'input_array' in st.session_state:
                st.session_state.generator = bubble_sort(
                    st.session_state.input_array
                )
                st.session_state.is_playing = True

    with btn_col2:
        if st.button("⏸ 暂停", use_container_width=True):
            st.session_state.is_playing = False

    with btn_col3:
        if st.button("⏭ 单步", use_container_width=True):
            if st.session_state.generator is None:
                if 'input_array' in st.session_state:
                    st.session_state.generator = bubble_sort(
                        st.session_state.input_array
                    )
            if st.session_state.generator:
                try:
                    st.session_state.current_step = next(
                        st.session_state.generator
                    )
                except StopIteration:
                    st.session_state.generator = None

    with btn_col4:
        if st.button("🔄 重置", use_container_width=True):
            st.session_state.generator = None
            st.session_state.current_step = None
            st.session_state.is_playing = False

    # 显示可视化
    if st.session_state.current_step:
        fig = render_array(st.session_state.current_step)
        st.pyplot(fig)

        # 注释
        st.info(st.session_state.current_step.comment)
    else:
        st.info("点击 [开始] 或 [单步] 开始排序演示")

# 右侧：代码区域
with col_code:
    st.subheader("Java 代码")

    # 复杂度信息
    info = BUBBLE_SORT_INFO
    st.markdown(f"""
    **{info.name}**
    - 时间复杂度: `{info.time_complexity}`
    - 空间复杂度: `{info.space_complexity}`
    - 稳定性: {'✅ 稳定' if info.stable else '❌ 不稳定'}
    """)

    # 代码显示
    highlight_line = 0
    if st.session_state.current_step:
        highlight_line = st.session_state.current_step.highlight_line

    code_html = render_code('java_code/bubble_sort.java', highlight_line)
    st.markdown(code_html, unsafe_allow_html=True)

# 底部：统计信息
if st.session_state.current_step:
    stats = st.session_state.current_step.stats
    st.divider()
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.metric("比较次数", stats.get('comparisons', 0))
    with stat_col2:
        st.metric("交换次数", stats.get('swaps', 0))
    with stat_col3:
        st.metric("当前状态", st.session_state.current_step.comment)

# 自动播放逻辑
if st.session_state.is_playing and st.session_state.generator:
    time.sleep(st.session_state.speed)
    try:
        st.session_state.current_step = next(st.session_state.generator)
        st.rerun()
    except StopIteration:
        st.session_state.is_playing = False
        st.session_state.generator = None
        st.success("🎉 排序完成！")
