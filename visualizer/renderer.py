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
