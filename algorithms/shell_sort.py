from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


SHELL_SORT_INFO = AlgorithmInfo(
    name="希尔排序",
    time_complexity="O(n log²n)",
    space_complexity="O(1)",
    stable=False,
    description="插入排序的改进版，通过间隔分组逐步缩小间隔进行排序。"
)


def shell_sort(arr: List[int]) -> Generator[Step, None, None]:
    """希尔排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i

            yield Step(
                array=a.copy(),
                highlight_line=4,
                comparing=[i],
                swapping=[],
                sorted_indices=[],
                comment=f"间隔={gap}，取出 a[{i}]={temp}",
                stats={"comparisons": comparisons, "swaps": swaps}
            )

            while j >= gap and a[j - gap] > temp:
                comparisons += 1
                a[j] = a[j - gap]
                swaps += 1

                yield Step(
                    array=a.copy(),
                    highlight_line=7,
                    comparing=[j, j - gap],
                    swapping=[j, j - gap],
                    sorted_indices=[],
                    comment=f"将 a[{j-gap}]={a[j-gap]} 右移到 a[{j}]",
                    stats={"comparisons": comparisons, "swaps": swaps}
                )
                j -= gap

            a[j] = temp

        gap //= 2

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
