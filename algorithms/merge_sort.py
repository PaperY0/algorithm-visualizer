from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


MERGE_SORT_INFO = AlgorithmInfo(
    name="归并排序",
    time_complexity="O(n log n)",
    space_complexity="O(n)",
    stable=True,
    description="分治法，将数组分成两半分别排序，再合并。"
)


def merge_sort(arr: List[int]) -> Generator[Step, None, None]:
    """归并排序生成器"""
    a = arr.copy()
    comparisons = [0]
    swaps = [0]

    def _merge_sort(start: int, end: int):
        if end - start <= 1:
            return

        mid = (start + end) // 2
        yield from _merge_sort(start, mid)
        yield from _merge_sort(mid, end)
        yield from _merge(start, mid, end)

    def _merge(start: int, mid: int, end: int):
        left = a[start:mid]
        right = a[mid:end]
        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            comparisons[0] += 1
            yield Step(
                array=a.copy(),
                highlight_line=6,
                comparing=[start + i, mid + j],
                swapping=[],
                sorted_indices=[],
                comment=f"比较 left[{i}]={left[i]} 和 right[{j}]={right[j]}",
                stats={"comparisons": comparisons[0], "swaps": swaps[0]}
            )

            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
            swaps[0] += 1
            k += 1

        while i < len(left):
            a[k] = left[i]
            i += 1
            k += 1
            swaps[0] += 1

        while j < len(right):
            a[k] = right[j]
            j += 1
            k += 1
            swaps[0] += 1

        yield Step(
            array=a.copy(),
            highlight_line=10,
            comparing=[],
            swapping=list(range(start, end)),
            sorted_indices=[],
            comment=f"合并区间 [{start}, {end})",
            stats={"comparisons": comparisons[0], "swaps": swaps[0]}
        )

    yield from _merge_sort(0, len(a))

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(len(a))),
        comment="排序完成！",
        stats={"comparisons": comparisons[0], "swaps": swaps[0]}
    )
