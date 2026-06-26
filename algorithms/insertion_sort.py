from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


INSERTION_SORT_INFO = AlgorithmInfo(
    name="插入排序",
    time_complexity="O(n²)",
    space_complexity="O(1)",
    stable=True,
    description="将未排序元素插入到已排序部分的正确位置。"
)


def insertion_sort(arr: List[int]) -> Generator[Step, None, None]:
    """插入排序生成器"""
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(1, n):
        key = a[i]
        j = i - 1

        yield Step(
            array=a.copy(),
            highlight_line=3,
            comparing=[i],
            swapping=[],
            sorted_indices=list(range(i)),
            comment=f"取出 a[{i}]={key} 准备插入",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j + 1] = a[j]
            swaps += 1

            yield Step(
                array=a.copy(),
                highlight_line=6,
                comparing=[j, j + 1],
                swapping=[j, j + 1],
                sorted_indices=list(range(i)),
                comment=f"将 a[{j}]={a[j]} 右移",
                stats={"comparisons": comparisons, "swaps": swaps}
            )
            j -= 1

        a[j + 1] = key

        yield Step(
            array=a.copy(),
            highlight_line=8,
            comparing=[],
            swapping=[j + 1],
            sorted_indices=list(range(i + 1)),
            comment=f"将 {key} 插入到位置 {j + 1}",
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
