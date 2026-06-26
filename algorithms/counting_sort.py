from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


COUNTING_SORT_INFO = AlgorithmInfo(
    name="计数排序",
    time_complexity="O(n + k)",
    space_complexity="O(k)",
    stable=True,
    description="统计每个值出现的次数，按顺序输出。适用于范围不大的整数。"
)


def counting_sort(arr: List[int]) -> Generator[Step, None, None]:
    """计数排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    if n == 0:
        yield Step(
            array=a.copy(),
            highlight_line=0,
            comparing=[],
            swapping=[],
            sorted_indices=[],
            comment="排序完成！",
            stats={"comparisons": 0, "swaps": 0}
        )
        return

    max_val = max(a)
    min_val = min(a)
    range_val = max_val - min_val + 1
    count = [0] * range_val
    output = [0] * n

    # 统计频率
    for i in range(n):
        count[a[i] - min_val] += 1
        yield Step(
            array=a.copy(),
            highlight_line=3,
            comparing=[i],
            swapping=[],
            sorted_indices=[],
            comment=f"统计 a[{i}]={a[i]}，计数={count[a[i] - min_val]}",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

    # 累加计数
    for i in range(1, range_val):
        count[i] += count[i - 1]

    # 构建输出
    for i in range(n - 1, -1, -1):
        output[count[a[i] - min_val] - 1] = a[i]
        count[a[i] - min_val] -= 1
        swaps += 1
        yield Step(
            array=output.copy(),
            highlight_line=8,
            comparing=[i],
            swapping=[count[a[i] - min_val]],
            sorted_indices=[],
            comment=f"将 a[{i}]={a[i]} 放到输出位置 {count[a[i] - min_val]}",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

    for i in range(n):
        a[i] = output[i]

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
