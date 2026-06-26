from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Step:
    """排序算法每一步的状态"""

    array: List[int]                    # 当前数组状态
    highlight_line: int                 # 高亮的Java代码行号
    comparing: List[int] = field(default_factory=list)  # 正在比较的元素索引
    swapping: List[int] = field(default_factory=list)   # 正在交换的元素索引
    sorted_indices: List[int] = field(default_factory=list)  # 已排序的元素索引
    comment: str = ""                   # 当前行的注释说明
    stats: Dict[str, int] = field(default_factory=dict)  # 统计信息


@dataclass
class AlgorithmInfo:
    """算法元信息"""

    name: str                           # 算法名称
    time_complexity: str                # 时间复杂度
    space_complexity: str               # 空间复杂度
    stable: bool                        # 是否稳定
    description: str                    # 算法描述
