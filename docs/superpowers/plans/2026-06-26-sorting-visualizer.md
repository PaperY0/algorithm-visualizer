# 算法可视化学习工具 - 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Streamlit 的 Web 应用，可视化学习十大排序算法，左边数字方块可视化，右边 Java 代码高亮同步。

**Architecture:** Python 生成器模式，每个排序算法实现为 yield 逐步产出 Step 状态，Streamlit 前端消费步骤并渲染可视化和代码高亮。

**Tech Stack:** Python 3.8+, Streamlit, matplotlib, dataclasses

## Global Constraints

- Python 3.8+ 兼容
- Streamlit 使用 session_state 管理状态
- 每个算法独立文件，遵循统一接口
- Java 代码只展示核心方法，带行号
- 可视化颜色：蓝色(默认)、红色(比较)、绿色(已排序)、黄色(交换)

---

## 阶段1：项目骨架 + 冒泡排序 MVP

### Task 1: 项目初始化

**Files:**
- Create: `requirements.txt`
- Create: `algorithms/__init__.py`
- Create: `visualizer/__init__.py`
- Create: `java_code/` (目录)

**Interfaces:**
- Produces: 项目目录结构，依赖可安装

- [ ] **Step 1: 创建 requirements.txt**

```
streamlit>=1.28.0
matplotlib>=3.7.0
```

- [ ] **Step 2: 创建目录结构**

```bash
mkdir -p algorithms visualizer java_code
touch algorithms/__init__.py visualizer/__init__.py
```

- [ ] **Step 3: 安装依赖**

```bash
pip install -r requirements.txt
```

- [ ] **Step 4: 验证 Streamlit 可运行**

```bash
streamlit --version
```

Expected: 显示版本号

- [ ] **Step 5: Commit**

```bash
git init
git add .
git commit -m "chore: initialize project structure"
```

---

### Task 2: Step 数据类

**Files:**
- Create: `algorithms/base.py`

**Interfaces:**
- Produces: `Step` dataclass，所有算法生成器 yield 的统一类型

- [ ] **Step 1: 创建 base.py**

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Step:
    """排序算法每一步的状态"""

    array: List[int]                    # 当前数组状态
    highlight_line: int                 # 高亮的Java代码行号
    comparing: List[int] = field(default_factory=list)  # 正在比较的元素索引
    swapping: List[int] = field(default_factory=list)   # 正在交换的元素索引
    sorted_indices: List[int] = field(default_factory=list)  # 已排序的元素索引
    comment: str = ""                   # 当前行的注释说明
    stats: Dict[str, int] = field(default_factory=dict)  # 统计信息


@dataclass
class AlgorithmInfo:
    """算法元信息"""

    name: str                           # 算法名称
    time_complexity: str                # 时间复杂度
    space_complexity: str               # 空间复杂度
    stable: bool                        # 是否稳定
    description: str                    # 算法描述
```

- [ ] **Step 2: 验证导入**

```bash
python -c "from algorithms.base import Step, AlgorithmInfo; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add algorithms/base.py
git commit -m "feat: add Step and AlgorithmInfo dataclasses"
```

---

### Task 3: 冒泡排序生成器

**Files:**
- Create: `algorithms/bubble_sort.py`

**Interfaces:**
- Consumes: `Step` from `algorithms.base`
- Produces: `bubble_sort(arr: List[int]) -> Generator[Step, None, None]`
- Produces: `BUBBLE_SORT_INFO: AlgorithmInfo`

- [ ] **Step 1: 创建 bubble_sort.py**

```python
from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


BUBBLE_SORT_INFO = AlgorithmInfo(
    name="冒泡排序",
    time_complexity="O(n²)",
    space_complexity="O(1)",
    stable=True,
    description="重复遍历数组，比较相邻元素并交换，直到无需交换。"
)


def bubble_sort(arr: List[int]) -> Generator[Step, None, None]:
    """冒泡排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(n - i - 1):
            comparisons += 1
            yield Step(
                array=a.copy(),
                highlight_line=5,
                comparing=[j, j + 1],
                swapping=[],
                sorted_indices=list(range(n - i, n)),
                comment=f"比较 a[{j}]={a[j]} 和 a[{j+1}]={a[j+1]}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )

            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                yield Step(
                    array=a.copy(),
                    highlight_line=6,
                    comparing=[],
                    swapping=[j, j + 1],
                    sorted_indices=list(range(n - i, n)),
                    comment=f"交换 a[{j}] 和 a[{j+1}]",
                    stats={"comparisons": comparisons, "swaps": swaps}
                )

    # 最终状态
    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
```

- [ ] **Step 2: 测试冒泡排序生成器**

```bash
python -c "
from algorithms.bubble_sort import bubble_sort
steps = list(bubble_sort([3, 1, 4, 2]))
print(f'Total steps: {len(steps)}')
print(f'Final array: {steps[-1].array}')
print(f'Sorted: {steps[-1].sorted_indices}')
"
```

Expected:
```
Total steps: (若干步)
Final array: [1, 2, 3, 4]
Sorted: [0, 1, 2, 3]
```

- [ ] **Step 3: Commit**

```bash
git add algorithms/bubble_sort.py
git commit -m "feat: implement bubble sort generator"
```

---

### Task 4: 冒泡排序 Java 代码模板

**Files:**
- Create: `java_code/bubble_sort.java`

**Interfaces:**
- Produces: Java 代码字符串，带行号，供右侧显示

- [ ] **Step 1: 创建 bubble_sort.java**

```java
public static void bubbleSort(int[] a) {
    int n = a.length;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                int temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
}
```

- [ ] **Step 2: 验证文件可读取**

```bash
python -c "
with open('java_code/bubble_sort.java') as f:
    lines = f.readlines()
print(f'Lines: {len(lines)}')
print(lines[4].strip())  # 第5行
"
```

Expected: 显示第5行代码 `if (a[j] > a[j + 1]) {`

- [ ] **Step 3: Commit**

```bash
git add java_code/bubble_sort.java
git commit -m "feat: add bubble sort Java code template"
```

---

### Task 5: 数字方块可视化渲染器

**Files:**
- Create: `visualizer/renderer.py`

**Interfaces:**
- Consumes: `Step` from `algorithms.base`
- Produces: `render_array(step: Step) -> matplotlib.figure.Figure`

- [ ] **Step 1: 创建 renderer.py**

```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from algorithms.base import Step


# 颜色方案
COLORS = {
    'default': '#4A90D9',    # 蓝色
    'comparing': '#E74C3C',  # 红色
    'sorted': '#2ECC71',     # 绿色
    'swapping': '#F39C12',   # 黄色
}


def render_array(step: Step) -> plt.Figure:
    """渲染数字方块可视化"""
    fig, ax = plt.subplots(figsize=(8, 3))

    n = len(step.array)
    max_val = max(step.array) if step.array else 1
    bar_width = 0.6

    for i, val in enumerate(step.array):
        # 确定颜色
        if i in step.swapping:
            color = COLORS['swapping']
        elif i in step.comparing:
            color = COLORS['comparing']
        elif i in step.sorted_indices:
            color = COLORS['sorted']
        else:
            color = COLORS['default']

        # 绘制方块
        rect = patches.Rectangle(
            (i - bar_width / 2, 0),
            bar_width,
            val,
            linewidth=1,
            edgecolor='black',
            facecolor=color
        )
        ax.add_patch(rect)

        # 显示数字
        ax.text(i, val + 0.1, str(val),
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max_val * 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('排序可视化', fontsize=14)

    return fig
```

- [ ] **Step 2: 测试渲染器**

```bash
python -c "
from algorithms.base import Step
from visualizer.renderer import render_array
import matplotlib
matplotlib.use('Agg')

step = Step(
    array=[3, 1, 4, 2],
    highlight_line=5,
    comparing=[0, 1],
    swapping=[],
    sorted_indices=[3],
    comment='比较 a[0]=3 和 a[1]=1',
    stats={'comparisons': 1, 'swaps': 0}
)
fig = render_array(step)
fig.savefig('test_render.png')
print('Render OK')
"
```

Expected: 生成 `test_render.png` 文件

- [ ] **Step 3: Commit**

```bash
git add visualizer/renderer.py
git commit -m "feat: implement array visualization renderer"
```

---

### Task 6: 代码高亮模块

**Files:**
- Create: `visualizer/code_highlight.py`

**Interfaces:**
- Consumes: Java 代码文件路径，高亮行号
- Produces: `render_code(code_path: str, highlight_line: int) -> str` 返回带样式的 HTML

- [ ] **Step 1: 创建 code_highlight.py**

```python
def render_code(code_path: str, highlight_line: int) -> str:
    """渲染带行号高亮的Java代码"""
    with open(code_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_lines = []
    for i, line in enumerate(lines, 1):
        # HTML转义
        escaped = (line
                   .replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace(' ', '&nbsp;')
                   .replace('\n', ''))

        if i == highlight_line:
            html_lines.append(
                f'<div style="background-color: #FFF3CD; padding: 2px 8px;">'
                f'<span style="color: #666; margin-right: 12px;">{i:2d}</span>'
                f'<span style="color: #333; font-weight: bold;">{escaped}</span>'
                f'</div>'
            )
        else:
            html_lines.append(
                f'<div style="padding: 2px 8px;">'
                f'<span style="color: #999; margin-right: 12px;">{i:2d}</span>'
                f'<span style="color: #333;">{escaped}</span>'
                f'</div>'
            )

    return (
        '<div style="background-color: #1E1E1E; color: #D4D4D4; '
        'font-family: Consolas, monospace; font-size: 14px; '
        'padding: 12px; border-radius: 8px; overflow-x: auto;">'
        + '\n'.join(html_lines)
        + '</div>'
    )
```

- [ ] **Step 2: 测试代码高亮**

```bash
python -c "
from visualizer.code_highlight import render_code
html = render_code('java_code/bubble_sort.java', 5)
print('HTML generated:', len(html), 'chars')
print('Contains highlight:', '#FFF3CD' in html)
"
```

Expected: HTML 包含高亮样式

- [ ] **Step 3: Commit**

```bash
git add visualizer/code_highlight.py
git commit -m "feat: implement code highlight renderer"
```

---

### Task 7: Streamlit 主应用

**Files:**
- Create: `app.py`

**Interfaces:**
- Consumes: 所有算法模块、可视化模块
- Produces: 可运行的 Streamlit Web 应用

- [ ] **Step 1: 创建 app.py**

```python
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
```

- [ ] **Step 2: 启动 Streamlit 应用**

```bash
streamlit run app.py
```

Expected: 浏览器打开，显示应用界面

- [ ] **Step 3: 测试完整流程**

1. 在侧边栏点击 "生成随机数组"
2. 点击 "▶ 开始"
3. 观察左侧可视化和右侧代码高亮同步变化
4. 点击 "⏸ 暂停" 暂停播放
5. 点击 "⏭ 单步" 单步执行
6. 点击 "🔄 重置" 重置状态

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: implement main Streamlit app with bubble sort"
```

---

## 阶段2：补齐其余排序算法

### Task 8: 选择排序

**Files:**
- Create: `algorithms/selection_sort.py`
- Create: `java_code/selection_sort.java`
- Modify: `app.py` (添加选择排序选项)

- [ ] **Step 1: 创建 selection_sort.py**

```python
from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


SELECTION_SORT_INFO = AlgorithmInfo(
    name="选择排序",
    time_complexity="O(n²)",
    space_complexity="O(1)",
    stable=False,
    description="每次从未排序部分选择最小元素，放到已排序部分末尾。"
)


def selection_sort(arr: List[int]) -> Generator[Step, None, None]:
    """选择排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            yield Step(
                array=a.copy(),
                highlight_line=5,
                comparing=[min_idx, j],
                swapping=[],
                sorted_indices=list(range(i)),
                comment=f"比较 a[{min_idx}]={a[min_idx]} 和 a[{j}]={a[j]}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )

            if a[j] < a[min_idx]:
                min_idx = j

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            yield Step(
                array=a.copy(),
                highlight_line=7,
                comparing=[],
                swapping=[i, min_idx],
                sorted_indices=list(range(i + 1)),
                comment=f"交换 a[{i}] 和 a[{min_idx}]",
                stats={"comparisons": comparisons, "swaps": swaps}
            )

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
```

- [ ] **Step 2: 创建 selection_sort.java**

```java
public static void selectionSort(int[] a) {
    int n = a.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[minIdx]) {
                minIdx = j;
            }
        }
        int temp = a[i];
        a[i] = a[minIdx];
        a[minIdx] = temp;
    }
}
```

- [ ] **Step 3: 测试选择排序**

```bash
python -c "
from algorithms.selection_sort import selection_sort
steps = list(selection_sort([64, 25, 12, 22, 11]))
print(f'Final array: {steps[-1].array}')
"
```

Expected: `Final array: [11, 12, 22, 25, 64]`

- [ ] **Step 4: Commit**

```bash
git add algorithms/selection_sort.py java_code/selection_sort.java
git commit -m "feat: implement selection sort"
```

---

### Task 9: 插入排序

**Files:**
- Create: `algorithms/insertion_sort.py`
- Create: `java_code/insertion_sort.java`

- [ ] **Step 1: 创建 insertion_sort.py**

```python
from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


INSERTION_SORT_INFO = AlgorithmInfo(
    name="插入排序",
    time_complexity="O(n²)",
    space_complexity="O(1)",
    stable=True,
    description="将未排序元素插入到已排序部分的正确位置。"
)


def insertion_sort(arr: List[int]) -> Generator[Step, None, None]:
    """插入排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(1, n):
        key = a[i]
        j = i - 1

        yield Step(
            array=a.copy(),
            highlight_line=3,
            comparing=[i],
            swapping=[],
            sorted_indices=list(range(i)),
            comment=f"取出 a[{i}]={key} 准备插入",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j + 1] = a[j]
            swaps += 1

            yield Step(
                array=a.copy(),
                highlight_line=6,
                comparing=[j, j + 1],
                swapping=[j, j + 1],
                sorted_indices=list(range(i)),
                comment=f"将 a[{j}]={a[j]} 右移",
                stats={"comparisons": comparisons, "swaps": swaps}
            )
            j -= 1

        a[j + 1] = key

        yield Step(
            array=a.copy(),
            highlight_line=8,
            comparing=[],
            swapping=[j + 1],
            sorted_indices=list(range(i + 1)),
            comment=f"将 {key} 插入到位置 {j + 1}",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
```

- [ ] **Step 2: 创建 insertion_sort.java**

```java
public static void insertionSort(int[] a) {
    int n = a.length;
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
```

- [ ] **Step 3: 测试并提交**

```bash
python -c "
from algorithms.insertion_sort import insertion_sort
steps = list(insertion_sort([12, 11, 13, 5, 6]))
print(f'Final array: {steps[-1].array}')
"
git add algorithms/insertion_sort.py java_code/insertion_sort.java
git commit -m "feat: implement insertion sort"
```

---

### Task 10-16: 其余排序算法

按照相同模式实现：
- Task 10: 希尔排序 (Shell Sort)
- Task 11: 归并排序 (Merge Sort)
- Task 12: 快速排序 (Quick Sort)
- Task 13: 堆排序 (Heap Sort)
- Task 14: 计数排序 (Counting Sort)
- Task 15: 桶排序 (Bucket Sort)
- Task 16: 基数排序 (Radix Sort)

每个任务包含：
1. 算法生成器 Python 文件
2. Java 代码模板
3. 测试验证
4. Commit

---

## 阶段3：集成所有算法到主应用

### Task 17: 更新 app.py 支持所有算法

**Files:**
- Modify: `app.py`

- [ ] **Step 1: 导入所有算法模块**

在 `app.py` 顶部添加所有算法的导入：

```python
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
```

- [ ] **Step 2: 创建算法映射字典**

```python
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
```

- [ ] **Step 3: 更新算法选择下拉框**

```python
algorithm = st.selectbox("选择排序算法", list(ALGORITHMS.keys()))
sort_func, sort_info, code_path = ALGORITHMS[algorithm]
```

- [ ] **Step 4: 更新开始按钮逻辑**

```python
if st.button("▶ 开始", use_container_width=True):
    if 'input_array' in st.session_state:
        st.session_state.generator = sort_func(
            st.session_state.input_array
        )
        st.session_state.is_playing = True
```

- [ ] **Step 5: 更新代码显示**

```python
code_html = render_code(code_path, highlight_line)
```

- [ ] **Step 6: 更新复杂度信息显示**

```python
st.markdown(f"""
**{sort_info.name}**
- 时间复杂度: `{sort_info.time_complexity}`
- 空间复杂度: `{sort_info.space_complexity}`
- 稳定性: {'✅ 稳定' if sort_info.stable else '❌ 不稳定'}
- {sort_info.description}
""")
```

- [ ] **Step 7: 测试所有算法**

逐一测试每个算法，确保可视化和代码高亮正常工作。

- [ ] **Step 8: Commit**

```bash
git add app.py
git commit -m "feat: integrate all 10 sorting algorithms"
```

---

## 阶段4：UI 美化与优化

### Task 18: 添加算法说明和图例

**Files:**
- Modify: `app.py`

- [ ] **Step 1: 添加颜色图例**

```python
st.markdown("""
**颜色说明：**
- 🔵 蓝色：未处理
- 🔴 红色：正在比较
- 🟡 黄色：正在交换
- 🟢 绿色：已排序
""")
```

- [ ] **Step 2: Commit**

```bash
git add app.py
git commit -m "feat: add color legend and UI improvements"
```

---

### Task 19: 最终测试与文档

**Files:**
- Create: `README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# 排序算法可视化学习工具

一个基于 Streamlit 的 Web 应用，用于可视化学习十大排序算法。

## 功能特性

- 🎯 十大经典排序算法可视化
- 📝 Java 代码同步高亮
- 🎮 播放控制：开始/暂停/单步/重置
- ⚡ 速度调节
- 📊 实时统计：比较次数、交换次数
- 📈 算法复杂度信息

## 安装运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 支持的算法

1. 冒泡排序 (Bubble Sort)
2. 选择排序 (Selection Sort)
3. 插入排序 (Insertion Sort)
4. 希尔排序 (Shell Sort)
5. 归并排序 (Merge Sort)
6. 快速排序 (Quick Sort)
7. 堆排序 (Heap Sort)
8. 计数排序 (Counting Sort)
9. 桶排序 (Bucket Sort)
10. 基数排序 (Radix Sort)
```

- [ ] **Step 2: 最终 Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

## 计划完成

实现计划已保存到 `docs/superpowers/plans/2026-06-26-sorting-visualizer.md`

两种执行方式：

**1. Subagent-Driven (推荐)** - 每个任务分派独立子代理，任务间审查，快速迭代

**2. Inline Execution** - 在当前会话中执行任务，批量执行带检查点

选择哪种方式？
