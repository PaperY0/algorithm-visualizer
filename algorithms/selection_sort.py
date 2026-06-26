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
