from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


HEAP_SORT_INFO = AlgorithmInfo(
    name="堆排序",
    time_complexity="O(n log n)",
    space_complexity="O(1)",
    stable=False,
    description="利用堆数据结构，先建大顶堆，再逐步取出最大值。"
)


def heap_sort(arr: List[int]) -> Generator[Step, None, None]:
    """堆排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    def heapify(size: int, i: int):
        nonlocal comparisons, swaps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < size:
            comparisons += 1
            yield Step(
                array=a.copy(),
                highlight_line=5,
                comparing=[largest, left],
                swapping=[],
                sorted_indices=list(range(n - size, n)),
                comment=f"比较 a[{largest}]={a[largest]} 和左子 a[{left}]={a[left]}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )
            if a[left] > a[largest]:
                largest = left

        if right < size:
            comparisons += 1
            yield Step(
                array=a.copy(),
                highlight_line=8,
                comparing=[largest, right],
                swapping=[],
                sorted_indices=list(range(n - size, n)),
                comment=f"比较 a[{largest}]={a[largest]} 和右子 a[{right}]={a[right]}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )
            if a[right] > a[largest]:
                largest = right

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            swaps += 1
            yield Step(
                array=a.copy(),
                highlight_line=10,
                comparing=[],
                swapping=[i, largest],
                sorted_indices=list(range(n - size, n)),
                comment=f"交换 a[{i}] 和 a[{largest}]",
                stats={"comparisons": comparisons, "swaps": swaps}
            )
            yield from heapify(size, largest)

    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    # 排序
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        swaps += 1
        yield Step(
            array=a.copy(),
            highlight_line=14,
            comparing=[],
            swapping=[0, i],
            sorted_indices=list(range(i, n)),
            comment=f"将堆顶 a[0] 与 a[{i}] 交换",
            stats={"comparisons": comparisons, "swaps": swaps}
        )
        yield from heapify(i, 0)

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
