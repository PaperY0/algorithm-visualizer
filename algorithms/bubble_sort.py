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

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
