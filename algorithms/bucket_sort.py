from typing import List, Generator
from algorithms.base import Step, AlgorithmInfo


BUCKET_SORT_INFO = AlgorithmInfo(
    name="桶排序",
    time_complexity="O(n + k)",
    space_complexity="O(n + k)",
    stable=True,
    description="将元素分到不同的桶中，每个桶单独排序，再合并。"
)


def bucket_sort(arr: List[int]) -> Generator[Step, None, None]:
    """桶排序生成器"""
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
    bucket_count = (max_val - min_val) // n + 1
    buckets = [[] for _ in range(bucket_count)]

    # 分配到桶
    for i in range(n):
        idx = (a[i] - min_val) // n
        buckets[idx].append(a[i])
        yield Step(
            array=a.copy(),
            highlight_line=3,
            comparing=[i],
            swapping=[],
            sorted_indices=[],
            comment=f"将 a[{i}]={a[i]} 放入桶 {idx}",
            stats={"comparisons": comparisons, "swaps": swaps}
        )

    # 每个桶排序并合并
    result = []
    for i, bucket in enumerate(buckets):
        bucket.sort()
        result.extend(bucket)
        comparisons += len(bucket) * max(0, len(bucket) - 1)

    for i in range(n):
        a[i] = result[i]
        swaps += 1

    yield Step(
        array=a.copy(),
        highlight_line=8,
        comparing=[],
        swapping=list(range(n)),
        sorted_indices=list(range(n)),
        comment="合并所有桶",
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
