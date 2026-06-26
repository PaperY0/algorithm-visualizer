from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


RADIX_SORT_INFO = AlgorithmInfo(
    name="基数排序",
    time_complexity="O(n × k)",
    space_complexity="O(n + k)",
    stable=True,
    description="按位排序，从最低位到最高位，每位使用计数排序。"
)


def radix_sort(arr: List[int]) -> Generator[Step, None, None]:
    """基数排序生成器"""
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
    exp = 1

    while max_val // exp > 0:
        output = [0] * n
        count = [0] * 10

        # 统计当前位的频率
        for i in range(n):
            digit = (a[i] // exp) % 10
            count[digit] += 1

        # 累加
        for i in range(1, 10):
            count[i] += count[i - 1]

        # 构建输出
        for i in range(n - 1, -1, -1):
            digit = (a[i] // exp) % 10
            output[count[digit] - 1] = a[i]
            count[digit] -= 1
            swaps += 1

        for i in range(n):
            a[i] = output[i]

        yield Step(
            array=a.copy(),
            highlight_line=6,
            comparing=[],
            swapping=list(range(n)),
            sorted_indices=[],
            comment=f"按第 {exp} 位排序完成",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

        exp *= 10

    yield Step(
        array=a.copy(),
        highlight_line=0,
        comparing=[],
        swapping=[],
        sorted_indices=list(range(n)),
        comment="排序完成！",
        stats={"comparisons": comparisons, "swaps": swaps}
    )
