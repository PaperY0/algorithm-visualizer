from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


QUICK_SORT_INFO = AlgorithmInfo(
    name="快速排序",
    time_complexity="O(n log n)",
    space_complexity="O(log n)",
    stable=False,
    description="分治法，选基准值分区，递归排序。"
)


def quick_sort(arr: List[int]) -> Generator[Step, None, None]:
    """快速排序生成器"""
    a = arr.copy()
    comparisons = [0]
    swaps = [0]

    def _quick_sort(low: int, high: int):
        if low < high:
            pivot_idx = yield from _partition(low, high)
            yield from _quick_sort(low, pivot_idx - 1)
            yield from _quick_sort(pivot_idx + 1, high)

    def _partition(low: int, high: int) -> int:
        pivot = a[high]
        i = low - 1

        yield Step(
            array=a.copy(),
            highlight_line=3,
            comparing=[high],
            swapping=[],
            sorted_indices=[],
            comment=f"选择基准值 a[{high}]={pivot}",
            stats={"comparisons": comparisons[0], "swaps": swaps[0]}
        )

        for j in range(low, high):
            comparisons[0] += 1
            yield Step(
                array=a.copy(),
                highlight_line=6,
                comparing=[j, high],
                swapping=[],
                sorted_indices=[],
                comment=f"比较 a[{j}]={a[j]} 和基准值 {pivot}",
                stats={"comparisons": comparisons[0], "swaps": swaps[0]}
            )

            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps[0] += 1
                yield Step(
                    array=a.copy(),
                    highlight_line=8,
                    comparing=[],
                    swapping=[i, j],
                    sorted_indices=[],
                    comment=f"交换 a[{i}] 和 a[{j}]",
                    stats={"comparisons": comparisons[0], "swaps": swaps[0]}
                )

        a[i + 1], a[high] = a[high], a[i + 1]
        swaps[0] += 1
        yield Step(
            array=a.copy(),
            highlight_line=10,
            comparing=[],
            swapping=[i + 1, high],
            sorted_indices=[i + 1],
            comment=f"将基准值放到位置 {i + 1}",
            stats={"comparisons": comparisons[0], "swaps": swaps[0]}
        )

        return i + 1

    yield from _quick_sort(0, len(a) - 1)

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(len(a))),
        comment="排序完成！",
        stats={"comparisons": comparisons[0], "swaps": swaps[0]}
    )
