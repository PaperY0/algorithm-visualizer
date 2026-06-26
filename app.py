import streamlit as st
import time
import random

from algorithms.bubble_sort import bubble_sort, BUBBLE_SORT_INFO
from algorithms.selection_sort import selection_sort, SELECTION_SORT_INFO
from algorithms.insertion_sort import insertion_sort, INSERTION_SORT_INFO
from algorithms.shell_sort import shell_sort, SHELL_SORT_INFO
from algorithms.merge_sort import merge_sort, MERGE_SORT_INFO
from algorithms.quick_sort import quick_sort, QUICK_SORT_INFO
from algorithms.heap_sort import heap_sort, HEAP_SORT_INFO
from algorithms.counting_sort import counting_sort, COUNTING_SORT_INFO
from algorithms.bucket_sort import bucket_sort, BUCKET_SORT_INFO
from algorithms.radix_sort import radix_sort, RADIX_SORT_INFO
from algorithms.base import Step
from visualizer.code_highlight import render_code

# 算法映射
ALGORITHMS = {
    "冒泡排序": (bubble_sort, BUBBLE_SORT_INFO, "java_code/bubble_sort.java"),
    "选择排序": (selection_sort, SELECTION_SORT_INFO, "java_code/selection_sort.java"),
    "插入排序": (insertion_sort, INSERTION_SORT_INFO, "java_code/insertion_sort.java"),
    "希尔排序": (shell_sort, SHELL_SORT_INFO, "java_code/shell_sort.java"),
    "归并排序": (merge_sort, MERGE_SORT_INFO, "java_code/merge_sort.java"),
    "快速排序": (quick_sort, QUICK_SORT_INFO, "java_code/quick_sort.java"),
    "堆排序": (heap_sort, HEAP_SORT_INFO, "java_code/heap_sort.java"),
    "计数排序": (counting_sort, COUNTING_SORT_INFO, "java_code/counting_sort.java"),
    "桶排序": (bucket_sort, BUCKET_SORT_INFO, "java_code/bucket_sort.java"),
    "基数排序": (radix_sort, RADIX_SORT_INFO, "java_code/radix_sort.java"),
}

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="排序算法可视化",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 全局CSS ====================
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background-color: #0a0a10 !important;
}

/* 隐藏默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 全局字体 */
* {
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif !important;
}

/* 主容器 */
.main .block-container {
    max-width: 100%;
    padding: 2rem 3rem;
}

/* ========== 卡片样式 ========== */
.card {
    background: rgba(20, 22, 30, 0.95);
    border: 1px solid rgba(100, 140, 255, 0.15);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 0 30px rgba(100, 140, 255, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.03);
    min-height: 500px;
}

/* ========== 左侧标题 ========== */
.algo-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
}

.algo-subtitle {
    text-align: center;
    font-size: 1rem;
    color: #7a8ba8;
    margin-bottom: 2.5rem;
    font-weight: 400;
}

/* ========== 数字圆圈 ========== */
.circles-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 28px;
    margin: 2rem 0;
    flex-wrap: wrap;
}

.circle-item {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    transition: all 0.3s ease;
    position: relative;
}

/* 普通状态 - 冰蓝色 */
.circle-default {
    background: rgba(20, 30, 60, 0.8);
    border: 2px solid rgba(100, 160, 255, 0.5);
    box-shadow: 0 0 15px rgba(100, 160, 255, 0.15),
                inset 0 0 10px rgba(100, 160, 255, 0.05);
}

/* 比较中 - 橙色高亮 */
.circle-comparing {
    background: rgba(255, 140, 20, 0.9);
    border: 2px solid rgba(255, 180, 60, 0.9);
    box-shadow: 0 0 25px rgba(255, 140, 20, 0.4),
                0 0 50px rgba(255, 140, 20, 0.15),
                inset 0 0 15px rgba(255, 200, 100, 0.1);
    transform: scale(1.08);
}

/* 交换中 - 黄色 */
.circle-swapping {
    background: rgba(255, 200, 20, 0.9);
    border: 2px solid rgba(255, 220, 80, 0.9);
    box-shadow: 0 0 25px rgba(255, 200, 20, 0.4),
                0 0 50px rgba(255, 200, 20, 0.15);
    transform: scale(1.08);
}

/* 已排序 - 绿色 */
.circle-sorted {
    background: rgba(30, 180, 80, 0.8);
    border: 2px solid rgba(60, 220, 100, 0.7);
    box-shadow: 0 0 15px rgba(60, 220, 100, 0.2);
}

/* ========== 注释区域 ========== */
.comment-box {
    text-align: center;
    margin-top: 2rem;
    padding: 0.8rem 1.2rem;
    background: rgba(100, 140, 255, 0.08);
    border-radius: 10px;
    border: 1px solid rgba(100, 140, 255, 0.12);
    color: #8aa0c0;
    font-size: 0.95rem;
}

/* ========== 统计信息 ========== */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1.5rem;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ff9040;
}

.stat-label {
    font-size: 0.8rem;
    color: #6a7a90;
    margin-top: 0.2rem;
}

/* ========== 控制按钮 ========== */
.controls-row {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 1.5rem;
}

.ctrl-btn {
    background: rgba(100, 140, 255, 0.1);
    border: 1px solid rgba(100, 140, 255, 0.25);
    color: #c0d0f0;
    padding: 8px 20px;
    border-radius: 8px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}

.ctrl-btn:hover {
    background: rgba(100, 140, 255, 0.2);
    border-color: rgba(100, 140, 255, 0.4);
}

/* ========== 代码区域 ========== */
.code-card {
    background: rgba(16, 18, 26, 0.98);
    border: 1px solid rgba(100, 140, 255, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 0 30px rgba(100, 140, 255, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.03);
    min-height: 500px;
}

.code-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(100, 140, 255, 0.1);
}

.code-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.code-dot-red { background: #ff5f57; }
.code-dot-yellow { background: #ffbd2e; }
.code-dot-green { background: #28c840; }

.code-filename {
    color: #6a7a90;
    font-size: 0.85rem;
    margin-left: 12px;
}

/* 代码行 */
.code-line {
    font-family: 'Consolas', 'Fira Code', 'Courier New', monospace !important;
    font-size: 14px;
    line-height: 1.8;
    padding: 0 12px;
    border-radius: 4px;
    white-space: pre;
    display: block;
}

.code-line-highlight {
    background: rgba(180, 160, 50, 0.25);
    border-left: 3px solid #c8a832;
}

.code-line-normal {
    background: transparent;
    border-left: 3px solid transparent;
}

/* 语法高亮 */
.syn-keyword { color: #c678dd; }    /* void, int, for, if - 紫色 */
.syn-type { color: #e5c07b; }       /* 类型名 - 金色 */
.syn-func { color: #61afef; }       /* 函数名 - 蓝色 */
.syn-number { color: #56b6c2; }     /* 数字 - 青色 */
.syn-string { color: #98c379; }     /* 字符串 - 绿色 */
.syn-comment { color: #5c6370; font-style: italic; }  /* 注释 - 灰色 */
.syn-op { color: #abb2bf; }         /* 运算符 - 浅灰 */
.syn-var { color: #e0e0e0; }        /* 变量 - 白色 */

.line-num {
    color: #4a5060;
    display: inline-block;
    width: 28px;
    text-align: right;
    margin-right: 16px;
    user-select: none;
}

/* ========== 复杂度信息栏 ========== */
.info-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1.2rem;
    padding: 0.6rem 1rem;
    background: rgba(100, 140, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(100, 140, 255, 0.08);
}

.info-item {
    color: #7a8ba8;
    font-size: 0.85rem;
}

.info-value {
    color: #c0d0f0;
    font-weight: 600;
}

/* ========== 侧边栏样式 ========== */
[data-testid="stSidebar"] {
    background-color: #0d0d15 !important;
    border-right: 1px solid rgba(100, 140, 255, 0.1);
}

/* Streamlit按钮样式覆盖 */
.stButton > button {
    background: rgba(100, 140, 255, 0.1) !important;
    border: 1px solid rgba(100, 140, 255, 0.25) !important;
    color: #c0d0f0 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: rgba(100, 140, 255, 0.2) !important;
    border-color: rgba(100, 140, 255, 0.4) !important;
}

/* 侧边栏标题 */
.sidebar-title {
    color: #ffffff;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(100, 140, 255, 0.15);
}

/* 选择框样式 */
.stSelectbox > div > div {
    background: rgba(20, 22, 30, 0.95) !important;
    border: 1px solid rgba(100, 140, 255, 0.2) !important;
    color: #c0d0f0 !important;
}

/* 滑块样式 */
.stSlider > div > div > div {
    color: #ff9040 !important;
}

</style>
""", unsafe_allow_html=True)


# ==================== 初始化 session_state ====================
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = None
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'speed' not in st.session_state:
    st.session_state.speed = 0.5
if 'input_array' not in st.session_state:
    st.session_state.input_array = [5, 3, 8, 4, 2]


# ==================== 侧边栏 ====================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ 控制面板</div>', unsafe_allow_html=True)

    # 算法选择
    algorithm = st.selectbox("选择算法", list(ALGORITHMS.keys()))
    sort_func, sort_info, code_path = ALGORITHMS[algorithm]

    st.divider()

    # 数据输入
    data_option = st.radio("数据来源", ["随机生成", "手动输入"])

    if data_option == "随机生成":
        array_size = st.slider("数组大小", 4, 15, 5)
        if st.button("🎲 生成随机数组", use_container_width=True):
            st.session_state.input_array = random.sample(
                range(1, array_size * 3 + 1), array_size
            )
            st.session_state.generator = None
            st.session_state.current_step = None
            st.session_state.is_playing = False
    else:
        input_str = st.text_input(
            "输入数字（逗号分隔）",
            ",".join(map(str, st.session_state.input_array))
        )
        try:
            new_arr = [int(x.strip()) for x in input_str.split(',')]
            if new_arr != st.session_state.input_array:
                st.session_state.input_array = new_arr
                st.session_state.generator = None
                st.session_state.current_step = None
                st.session_state.is_playing = False
        except ValueError:
            pass

    st.divider()

    # 速度控制
    speed = st.slider("播放速度", 0.1, 2.0, 0.5, 0.1,
                       format="%.1f 秒/步")
    st.session_state.speed = speed


# ==================== 渲染函数 ====================
def render_circles(step: Step) -> str:
    """渲染数字圆圈HTML"""
    circles = []
    for i, val in enumerate(step.array):
        if i in step.swapping:
            cls = "circle-swapping"
        elif i in step.comparing:
            cls = "circle-comparing"
        elif i in step.sorted_indices:
            cls = "circle-sorted"
        else:
            cls = "circle-default"

        circles.append(f'<div class="circle-item {cls}">{val}</div>')

    return '<div class="circles-container">' + ''.join(circles) + '</div>'


def render_code_html(code_path: str, highlight_line: int) -> str:
    """渲染带语法高亮的Java代码"""
    with open(code_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_lines = []
    for i, line in enumerate(lines, 1):
        # 简单语法高亮
        escaped = line.rstrip('\n')

        # 替换关键字
        import re
        # 注释
        if '//' in escaped:
            comment_idx = escaped.index('//')
            code_part = escaped[:comment_idx]
            comment_part = escaped[comment_idx:]
            escaped = highlight_java_syntax(code_part) + f'<span class="syn-comment">{comment_part}</span>'
        else:
            escaped = highlight_java_syntax(escaped)

        # 转义空格
        escaped = escaped.replace(' ', '&nbsp;')

        if i == highlight_line:
            html_lines.append(
                f'<span class="code-line code-line-highlight">'
                f'<span class="line-num">{i}</span>{escaped}</span>'
            )
        else:
            html_lines.append(
                f'<span class="code-line code-line-normal">'
                f'<span class="line-num">{i}</span>{escaped}</span>'
            )

    return '<div style="padding: 0.5rem 0;">' + '\n'.join(html_lines) + '</div>'


def highlight_java_syntax(code: str) -> str:
    """Java语法高亮"""
    import re

    # 关键字
    keywords = r'\b(void|int|for|if|while|return|class|public|private|static|new|true|false|null)\b'
    code = re.sub(keywords, r'<span class="syn-keyword">\1</span>', code)

    # 数字
    code = re.sub(r'\b(\d+)\b', r'<span class="syn-number">\1</span>', code)

    # 函数名 (后面跟括号的标识符)
    code = re.sub(r'\b([a-zA-Z_]\w*)\s*(?=\()', r'<span class="syn-func">\1</span>', code)

    return code


# ==================== 主页面 ====================

# 顶部标题
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #ffffff; font-size: 1.8rem; font-weight: 300; letter-spacing: 4px;">
        🔥 算法可视化教学平台
    </h1>
    <p style="color: #4a5060; font-size: 0.9rem; margin-top: 0.3rem;">
        左侧算法演示 · 右侧代码同步 · 交互式学习体验
    </p>
</div>
""", unsafe_allow_html=True)

# 左右分栏
col_left, col_right = st.columns(2, gap="large")

# ==================== 左侧：算法可视化 ====================
with col_left:
    # 卡片开始
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # 标题
    st.markdown(f'<div class="algo-title">{sort_info.name}</div>', unsafe_allow_html=True)

    # 副标题
    st.markdown(f'<div class="algo-subtitle">{sort_info.description}</div>', unsafe_allow_html=True)

    # 数字圆圈
    if st.session_state.current_step:
        circles_html = render_circles(st.session_state.current_step)
        st.markdown(circles_html, unsafe_allow_html=True)

        # 注释
        comment = st.session_state.current_step.comment or "准备开始..."
        st.markdown(f'<div class="comment-box">💡 {comment}</div>', unsafe_allow_html=True)

        # 统计信息
        stats = st.session_state.current_step.stats
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">{stats.get('comparisons', 0)}</div>
                <div class="stat-label">比较次数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{stats.get('swaps', 0)}</div>
                <div class="stat-label">交换次数</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 初始状态显示
        initial_html = '<div class="circles-container">'
        for val in st.session_state.input_array:
            initial_html += f'<div class="circle-default circle-item">{val}</div>'
        initial_html += '</div>'
        st.markdown(initial_html, unsafe_allow_html=True)
        st.markdown('<div class="comment-box">🎮 点击右侧控制按钮开始演示</div>', unsafe_allow_html=True)

    # 卡片结束
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== 右侧：代码区域 ====================
with col_right:
    # 代码卡片开始
    st.markdown('<div class="code-card">', unsafe_allow_html=True)

    # 代码头部（模拟IDE）
    filename = code_path.split('/')[-1]
    st.markdown(f"""
    <div class="code-header">
        <div class="code-dot code-dot-red"></div>
        <div class="code-dot code-dot-yellow"></div>
        <div class="code-dot code-dot-green"></div>
        <span class="code-filename">{filename}</span>
    </div>
    """, unsafe_allow_html=True)

    # 复杂度信息
    st.markdown(f"""
    <div class="info-bar">
        <div class="info-item">⏱ 时间: <span class="info-value">{sort_info.time_complexity}</span></div>
        <div class="info-item">💾 空间: <span class="info-value">{sort_info.space_complexity}</span></div>
        <div class="info-item">📊 稳定性: <span class="info-value">{'稳定' if sort_info.stable else '不稳定'}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # 代码内容
    highlight_line = 0
    if st.session_state.current_step:
        highlight_line = st.session_state.current_step.highlight_line

    code_html = render_code_html(code_path, highlight_line)
    st.markdown(code_html, unsafe_allow_html=True)

    # 代码卡片结束
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== 底部控制栏 ====================
st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

# 控制按钮
col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([1, 1, 1, 1, 2])

with col_ctrl1:
    if st.button("▶ 开始", use_container_width=True):
        st.session_state.generator = sort_func(st.session_state.input_array)
        st.session_state.is_playing = True

with col_ctrl2:
    if st.button("⏸ 暂停", use_container_width=True):
        st.session_state.is_playing = False

with col_ctrl3:
    if st.button("⏭ 单步", use_container_width=True):
        if st.session_state.generator is None:
            st.session_state.generator = sort_func(st.session_state.input_array)
            st.session_state.is_playing = False
        if st.session_state.generator:
            try:
                st.session_state.current_step = next(st.session_state.generator)
            except StopIteration:
                st.session_state.generator = None

with col_ctrl4:
    if st.button("🔄 重置", use_container_width=True):
        st.session_state.generator = None
        st.session_state.current_step = None
        st.session_state.is_playing = False


# ==================== 自动播放逻辑 ====================
if st.session_state.is_playing and st.session_state.generator:
    time.sleep(st.session_state.speed)
    try:
        st.session_state.current_step = next(st.session_state.generator)
        st.rerun()
    except StopIteration:
        st.session_state.is_playing = False
        st.session_state.generator = None
        st.success("🎉 排序完成！")
