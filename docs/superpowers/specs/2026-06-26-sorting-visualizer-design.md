# 算法可视化学习工具 - 设计文档

> 创建日期：2026-06-26
> 状态：设计完成，待实现

## 1. 项目概述

一个基于 Streamlit 的 Web 应用，用于可视化学习十大排序算法。

**核心体验**：左边是排序过程的数字方块可视化，右边是 Java 代码。代码执行到某一行时高亮，左边同步显示操作过程。

## 2. 技术选型

| 方面 | 决定 |
|------|------|
| 前端框架 | Python + Streamlit |
| 代码语言 | Java（只展示核心方法，不执行） |
| 可视化 | matplotlib / plotly |
| 算法实现 | Python 生成器（yield 逐步产出状态） |

## 3. 架构设计

```
用户输入数组 → Python生成器算法 → yield步骤状态 → Streamlit渲染
                  ↑                                    │
                  └────── 控制信号（暂停/继续/单步）──────┘
```

### 3.1 Step 数据结构

每个算法生成器 yield 的步骤包含：

```python
@dataclass
class Step:
    array: list           # 当前数组状态
    highlight_line: int   # 高亮的Java代码行号
    comparing: list       # 正在比较的元素索引
    swapping: list        # 正在交换的元素索引
    sorted: list          # 已排序的元素索引
    comment: str          # 当前行的注释说明
    stats: dict           # 统计信息（比较次数、交换次数）
```

### 3.2 生成器示例（冒泡排序）

```python
def bubble_sort(arr):
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
                comparing=[j, j+1],
                swapping=[],
                sorted=list(range(n-i, n)),
                comment=f"比较 a[{j}]={a[j]} 和 a[{j+1}]={a[j+1]}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )

            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1
                yield Step(
                    array=a.copy(),
                    highlight_line=6,
                    comparing=[],
                    swapping=[j, j+1],
                    sorted=list(range(n-i, n)),
                    comment=f"交换 a[{j}] 和 a[{j+1}]",
                    stats={"comparisons": comparisons, "swaps": swaps}
                )
```

## 4. UI 布局

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                      │
│  ┌─────────────────────┬──────────────────────────────┐ │
│  │   左侧：可视化区域    │      右侧：代码区域          │ │
│  │                     │                              │ │
│  │  ┌───┬───┬───┬───┐  │  1│ public static void       │ │
│  │  │ 3 │ 1 │ 4 │ 2 │  │  2│   bubbleSort(int[] a) {  │ │
│  │  └───┴───┴───┴───┘  │  3│   for (int i=0; ...) {   │ │
│  │                     │  4│     for (int j=0; ...) {  │ │
│  │  [比较中] [已排序]   │  5│       if (a[j]>a[j+1]) { │ │
│  │                     │  6│         swap(a,j,j+1);   │ │
│  │                     │  7│       }                   │ │
│  │                     │  8│     }                     │ │
│  │                     │  9│   }                       │ │
│  │                     │ 10│ }                         │ │
│  ├─────────────────────┴──────────────────────────────┤ │
│  │  [开始] [暂停] [单步] [重置]  速度: ━━━━●━━━━       │ │
│  ├────────────────────────────────────────────────────┤ │
│  │  复杂度: O(n²) | 比较: 12 | 交换: 5 | 稳定性: 稳定  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 5. 控制逻辑

使用 `st.session_state` 保存状态：

```python
st.session_state.generator    # 当前算法生成器
st.session_state.current_step # 当前步骤
st.session_state.is_playing   # 是否正在播放
st.session_state.speed        # 速度（秒/步）
st.session_state.mode         # "auto" 或 "step"
```

**播放控制流程**：
1. 用户点击 [开始] → 设置 is_playing = True
2. 循环：从生成器取下一个 step
3. 渲染可视化 + 高亮代码行
4. 等待 speed 秒
5. 检查 [暂停] 或 [结束] → 退出循环

**单步模式**：点击 [下一步] 时，只从生成器取一个 step 并渲染。

**速度控制**：滑块范围 0.1s ~ 2s/步。

## 6. 可视化渲染

### 6.1 数字方块颜色方案

| 状态 | 颜色 | 含义 |
|------|------|------|
| 蓝色 | 默认 | 未处理 |
| 红色 | 正在比较 | 当前正在比较的元素 |
| 绿色 | 已排序 | 已确定最终位置 |
| 黄色 | 正在交换 | 刚发生交换的元素 |

### 6.2 代码高亮

- 使用 `st.code()` 显示 Java 代码
- 通过自定义 CSS 实现当前行高亮（黄色背景）

### 6.3 额外信息

- 算法复杂度信息（时间/空间/稳定性）预存
- 操作计数器实时更新（比较次数、交换次数）
- 代码注释显示当前行在做什么

## 7. 十大排序算法

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

## 8. 项目结构

```
algorithm-visualizer/
├── app.py                    # Streamlit主入口
├── requirements.txt          # 依赖：streamlit, matplotlib
├── algorithms/               # 算法生成器模块
│   ├── __init__.py
│   ├── base.py               # Step数据类 + 基类
│   ├── bubble_sort.py
│   ├── selection_sort.py
│   ├── insertion_sort.py
│   ├── shell_sort.py
│   ├── merge_sort.py
│   ├── quick_sort.py
│   ├── heap_sort.py
│   ├── counting_sort.py
│   ├── bucket_sort.py
│   └── radix_sort.py
├── java_code/                # Java代码模板
│   ├── bubble_sort.java
│   ├── selection_sort.java
│   └── ...
├── visualizer/               # 可视化渲染模块
│   ├── __init__.py
│   ├── renderer.py           # 数字方块渲染逻辑
│   └── code_highlight.py     # 代码高亮逻辑
└── docs/
    └── superpowers/specs/    # 设计文档
```

## 9. 实现顺序

| 阶段 | 内容 | 产出 |
|------|------|------|
| 阶段1 | 项目骨架 + 冒泡排序 | 能跑通一个完整流程 |
| 阶段2 | 补齐其余9个排序算法 | 十大排序全部可用 |
| 阶段3 | 美化UI + 动画优化 | 视觉体验提升 |
| 阶段4 | 测试 + 修复 + 文档 | 可交付使用 |

### 阶段1详细任务

1. 初始化项目，安装依赖
2. 实现 Step 数据类
3. 实现冒泡排序生成器
4. 编写冒泡排序 Java 代码模板
5. 实现 Streamlit 主页面布局
6. 实现数字方块渲染
7. 实现代码高亮显示
8. 实现播放控制（开始/暂停/单步/重置）
9. 实现速度滑块
10. 实现复杂度信息和计数器

## 10. 依赖

```
streamlit
matplotlib
```
