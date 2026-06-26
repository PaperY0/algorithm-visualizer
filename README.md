# 排序算法可视化学习工具

一个排序算法可视化项目，包含两种可视化方式：

- **HTML 动画版**：独立的 HTML 页面，带小球交换动画、代码高亮、暂停/单步控制
- **Streamlit 版**：基于 Streamlit 的 Web 应用，方块式可视化

---

## 项目结构

```
algorithm-visualizer/
│
├── sort/                              # 🔥 HTML 动画版排序算法
│   ├── bubble_sort_animation.html     #   冒泡排序
│   ├── selection_sort_animation.html  #   选择排序
│   └── insertion_sort_animation.html  #   插入排序
│
├── animation_template.html            # 动画模板（创建新算法用）
├── ANIMATION_FRAMEWORK.md             # 复用指南和框架文档
│
├── app.py                             # Streamlit 版入口
├── requirements.txt                   # Python 依赖
│
├── algorithms/                        # Streamlit 版算法生成器
│   ├── base.py                        #   Step 数据类
│   ├── bubble_sort.py                 #   冒泡排序
│   ├── selection_sort.py              #   选择排序
│   ├── insertion_sort.py              #   插入排序
│   ├── shell_sort.py                  #   希尔排序
│   ├── merge_sort.py                  #   归并排序
│   ├── quick_sort.py                  #   快速排序
│   ├── heap_sort.py                   #   堆排序
│   ├── counting_sort.py               #   计数排序
│   ├── bucket_sort.py                 #   桶排序
│   └── radix_sort.py                  #   基数排序
│
├── java_code/                         # 各算法的 Java 代码（右侧展示用）
│   ├── bubble_sort.java
│   └── ...
│
├── visualizer/                        # Streamlit 版渲染模块
│   ├── renderer.py                    #   数字方块渲染
│   └── code_highlight.py             #   代码高亮
│
└── docs/                              # 设计文档
```

---

## HTML 动画版

独立的 HTML 文件，浏览器直接打开即可运行，无需安装任何依赖。

### 运行方式

直接在浏览器中打开 `sort/` 目录下的 HTML 文件：

```bash
# Windows
start sort/bubble_sort_animation.html

# macOS
open sort/bubble_sort_animation.html

# Linux
xdg-open sort/bubble_sort_animation.html
```

### 功能特性

- 🎯 **小球动画**：数字以圆形小球展示，支持上浮、交叉、下落三段式交换动画
- 📝 **代码高亮**：右侧同步展示 Java 代码，当前执行行高亮
- 🎮 **播放控制**：开始 / 暂停 / 单步 / 重置
- ⚡ **速度调节**：10 档速度可调
- 📊 **实时统计**：循环次数、比较次数、交换次数
- 📏 **分隔线**：动态标记已排序区域和未排序区域的边界
- 🎨 **暗色主题**：赛博朋克风格的 UI 设计

### 小球状态

| 状态 | 颜色 | 用途 |
|------|------|------|
| `normal` | 🔵 蓝色描边 | 默认状态 |
| `active` | 🟠 橙色 | 正在比较的元素 |
| `pivot` | 🟣 紫色 | 当前最小值 / 基准值 |
| `sorted` | 🟢 绿色 | 已排序 |
| `moving` | 🔵 青色 | 正在右移（插入排序） |
| `swap-a` / `swap-b` | 🔵 蓝色 | 交换动画中 |

### 支持的算法（HTML 版）

| 算法 | 时间复杂度 | 空间复杂度 | 稳定性 |
|------|-----------|-----------|--------|
| 冒泡排序 | O(n²) | O(1) | ✅ 稳定 |
| 选择排序 | O(n²) | O(1) | ❌ 不稳定 |
| 插入排序 | O(n²) | O(1) | ✅ 稳定 |

> 更多算法持续添加中...

---

## Streamlit 版

基于 Streamlit 的 Web 应用，支持 10 种排序算法。

### 安装运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 支持的算法（Streamlit 版）

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

---

## 扩展新算法（HTML 版）

1. 复制 `animation_template.html` 到 `sort/` 目录
2. 搜索并替换以下标记：
   - `REPLACE_TITLE` — 算法名称
   - `REPLACE_DESC` — 算法描述
   - `REPLACE_FILENAME` — Java 文件名
   - `REPLACE_TIME` / `REPLACE_SPACE` / `REPLACE_STABILITY` — 复杂度
   - `REPLACE_JAVA_CODE` — Java 代码数组
   - `REPLACE_LINE_NUMBERS` — 行号常量
   - `REPLACE_SORT_GENERATOR` — 排序逻辑生成器
3. 详细指南见 `ANIMATION_FRAMEWORK.md`

### ⚠️ 分隔线方向规则

分隔线位置必须根据算法特性设置：

- **已排序区从左侧扩展**（选择排序、插入排序）→ `updateDivider(i + 1)`
- **已排序区从右侧扩展**（冒泡排序）→ `updateDivider(n - i - 1)`

---

## 技术栈

- **HTML 动画版**：纯 HTML + CSS + JavaScript，零依赖
- **Streamlit 版**：Python + Streamlit + Pillow
- **代码展示**：Java（语法高亮展示用）
