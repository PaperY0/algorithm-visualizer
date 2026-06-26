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

## 项目结构

```
algorithm-visualizer/
├── app.py                    # Streamlit主入口
├── requirements.txt          # 依赖
├── algorithms/               # 算法生成器模块
│   ├── base.py               # Step数据类
│   ├── bubble_sort.py        # 冒泡排序
│   ├── selection_sort.py     # 选择排序
│   └── ...
├── java_code/                # Java代码模板
│   ├── bubble_sort.java
│   └── ...
├── visualizer/               # 可视化渲染模块
│   ├── renderer.py           # 数字方块渲染
│   └── code_highlight.py     # 代码高亮
└── docs/                     # 设计文档
```

## 颜色说明

- 🔵 蓝色：未处理
- 🔴 红色：正在比较
- 🟡 黄色：正在交换
- 🟢 绿色：已排序
