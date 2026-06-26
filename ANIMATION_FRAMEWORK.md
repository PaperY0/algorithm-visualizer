# 排序动画框架 - 复用指南

> 本文档是 `animation_template.html` 的配套说明。
> 模板经过完整验证，包含修复过的交换动画、循环计数器、暂停/单步控制等全部功能。
> **复制模板 → 替换 4 处必填区 → 即可运行。**

---

## 快速开始

1. 复制 `animation_template.html`，重命名为 `xxx_sort_animation.html`
2. 打开文件，搜索 `【必填】` 标记，共 4 处需要修改
3. 浏览器直接打开即可运行（纯前端，无需构建工具）

---

## 4 处必填区详解

### 必填 ① — 页面标题和描述（HTML 区域）

```html
<!-- 搜索：REPLACE_TITLE -->
<h1 class="title">你的排序名称</h1>
<p class="desc">一句话描述算法核心思想</p>
```

### 必填 ② — 右侧代码展示区（HTML 区域）

```html
<!-- 搜索：REPLACE_FILENAME -->
<span class="code-filename">XxxSort.java</span>

<!-- 搜索：REPLACE_INFO -->
<div class="info-item">⏱ 时间: <span class="info-value">O(n²)</span></div>
<div class="info-item">💾 空间: <span class="info-value">O(1)</span></div>
<div class="info-item">📊 稳定性: <span class="info-value">不稳定</span></div>
```

### 必填 ③ — Java 代码和行号常量（JS 配置区）

```javascript
// 搜索：REPLACE_JAVA_CODE
const JAVA_CODE = [
    'public static void yourSort(int[] a) {',
    '    // ...',
    '}',
];

// 搜索：REPLACE_LINE_NUMBERS
// 行号从 1 开始，对应 JAVA_CODE 数组的索引 + 1
const LINE_COMPARE    = 2;   // 比较操作
const LINE_SWAP       = 3;   // 交换操作
// 按需添加更多行号常量
```

### 必填 ④ — 排序算法生成器（JS 函数区）

```javascript
// 搜索：REPLACE_SORT_GENERATOR
async function* sortGenerator() {
    const n = arr.length;
    comparisons = 0;
    swaps = 0;
    loops = 0;
    updateDivider(0);

    // ★ 在此实现你的排序逻辑 ★
    // 每个步骤的标准流程：
    //   1. loops = 当前轮次; updateStats();    ← 更新循环计数
    //   2. setCircleState(pos, 'active');       ← 高亮参与元素
    //   3. renderCode(LINE_xxx);                ← 高亮代码行
    //   4. setComment('说明文字');               ← 底部提示
    //   5. updateStats();                        ← 更新统计
    //   6. await sleep(getDelay());              ← 等待动画
    //   7. if (isPaused) yield 'paused';         ← 支持暂停
    //   8. 执行交换/移动操作
    //   9. setCircleState(pos, 'normal');        ← 取消高亮
}
```

---

## 小球状态系统（5 种状态，直接用）

| 状态名 | 用途 | 视觉效果 | 使用场景 |
|--------|------|----------|----------|
| `normal` | 默认/未选中 | 蓝色描边 + 深色填充 | 元素空闲时 |
| `active` | 正在比较 | 橙色填充 + 发光 | 比较操作高亮 |
| `pivot` | 基准值/最小值 | 紫色填充 + 发光 | 标记当前关键元素 |
| `sorted` | 已排序 | 绿色描边 + 深绿填充 | 标记已就位元素 |
| `swap-a` / `swap-b` | 交换动画 | 蓝色描边 + 上浮交叉动画 | **仅由 animSwap 内部使用，不要手动设置** |

### 状态切换 API

```javascript
// 设置位置 pos 上的小球为指定状态
setCircleState(pos, 'active');   // 橙色高亮
setCircleState(pos, 'pivot');    // 紫色标记
setCircleState(pos, 'normal');   // 恢复默认
setCircleState(pos, 'sorted');   // 标记已排序

// ⚠️ setCircleState 会完全替换 className，不要连续设置同一元素的不同状态
//    正确：先 setCircleState(pos, 'normal')，再做其他操作
//    错误：同时给同一元素设两个状态
```

---

## 交换动画系统（三段式：上浮 → 交叉 → 下落）

### 调用方式

```javascript
// 交换位置 posA 和 posB 上的小球（带动画）
await animSwap(circleOrder[posA], circleOrder[posB], posA, posB);

// 动画结束后，记得同步更新数据
[arr[posA], arr[posB]] = [arr[posB], arr[posA]];
```

### 内部机制（不需要修改，了解即可）

```
时间线：
0ms     添加 swap-a / swap-b 类（classList.add，保留已有状态类）
        设置 left 目标位置（CSS transition 延迟 0.3s 开始）

0~300ms   小球上浮（A 向上 80px，B 向下 80px）
300~700ms left 过渡生效，两球水平交叉互换
700~800ms 小球下落归位

850ms   移除 swap-a / swap-b 类（classList.remove）
        小球恢复为之前的 normal / sorted 状态
```

### ⚠️ 交换动画关键约束

1. **调用 animSwap 前，必须先将两个小球设为 `normal` 状态**
   ```javascript
   setCircleState(posA, 'normal');
   setCircleState(posB, 'normal');
   await animSwap(...);
   ```

2. **不要手动设置 `swap-a` / `swap-b` 类**，它们由 animSwap 内部管理

3. **swap-a/swap-b 的 CSS 必须包含 border/background/box-shadow**，否则动画期间边框会消失（已修复，模板已包含）

---

## 移动动画系统（用于插入排序等需要位移的算法）

```javascript
// 将 fromPos 位置的小球移动到 toPos
// 中间的小球会自动依次平移腾出位置
moveCircleTo(fromPos, toPos);

// moveCircleTo 内部已处理：
//   - 目标元素的 left 设置
//   - 中间元素的 left 同步更新
//   - circleOrder 数组的重新排列
```

---

## 分隔线系统

分隔线是一条垂直虚线，用于划分「未排序区」和「已排序区」。

### 调用方式

```javascript
updateDivider(position);   // 分隔线放在指定位置的左边界
updateDivider(0);          // 隐藏分隔线（初始状态）
updateDivider(arr.length); // 隐藏分隔线（全部排序完成）
```

### ⚠️ 分隔线方向规则（核心）

分隔线始终位于**已排序区的左边界**，参数不是 `i + 1` 就是 `n - i - 1`，取决于已排序区从哪一端扩展：

```
【已排序区从左侧扩展】（选择排序、插入排序）

  [已排序] | [未排序]
  ■ ■ ■ ■ | □ □ □ □ □
  pos 0,1,2,3  pos 4,5,6,7,8
           ↑
       分隔线在此

  每轮后分隔线右移 → 用 updateDivider(i + 1)
  i=0 → pos 1, i=1 → pos 2, i=2 → pos 3 ...

【已排序区从右侧扩展】（冒泡排序）

  [未排序] | [已排序]
  □ □ □ □ | ■ ■ ■ ■
  pos 0,1,2,3  pos 4,5,6,7
           ↑
       分隔线在此

  每轮后分隔线左移 ← 用 updateDivider(n - i - 1)
  i=0 → pos 7, i=1 → pos 6, i=2 → pos 5 ...
```

### 判断方法

问自己一个问题：**每轮排序结束后，已排序的元素在数组的哪一端？**

- 左端（pos 0, 1, 2...） → `updateDivider(i + 1)`
- 右端（pos n-1, n-2...） → `updateDivider(n - i - 1)`

### 分隔线标签

HTML 中默认标签是 `已排序 ↑`，表示分隔线下方是已排序区。如果方向不同，可按需修改标签文字。

---

## 统计计数器

模板内置 3 个计数器，布局在 stats-row 中：

| 计数器 | DOM id | 变量名 | 含义 |
|--------|--------|--------|------|
| 循环次数 | `loopCount` | `loops` | 外层循环第几轮 |
| 比较次数 | `compCount` | `comparisons` | 元素比较操作次数 |
| 交换次数 | `swapCount` | `swaps` | 元素交换操作次数 |

### 在生成器中使用

```javascript
async function* sortGenerator() {
    // ...
    for (let i = 0; i < n - 1; i++) {
        loops = i + 1;       // ← 更新循环计数
        updateStats();        // ← 刷新 DOM 显示

        // 比较时
        comparisons++;
        updateStats();

        // 交换时
        swaps++;
        updateStats();
    }
}
```

### 如果不需要循环计数器

删除 HTML 中的 loopCount stat-item，删除 JS 中的 `loops` 变量和 `updateStats` 中的对应行即可。

---

## 控制逻辑（已内置，不需要修改）

| 功能 | 函数 | 说明 |
|------|------|------|
| 开始排序 | `startSort()` | 重置数据 → 启动生成器 → 自动播放 |
| 暂停/继续 | `togglePause()` | 生成器内通过 `if (isPaused) yield 'paused'` 响应 |
| 单步执行 | `stepOnce()` | 不运行时可用，每次调用执行生成器的下一个 yield |
| 重置 | `resetAll()` | 停止动画 → 重置所有数据 → 恢复初始状态 |
| 速度调节 | 拖动滑块 | 1~10 档，5 为默认，越大越快 |

---

## 代码高亮系统

右侧代码区自动根据 `JAVA_CODE` 数组渲染，支持 Java 语法高亮。

### 高亮指定行

```javascript
renderCode(LINE_COMPARE);   // 高亮比较操作对应的行
renderCode(LINE_SWAP);      // 高亮交换操作对应的行
renderCode(0);               // 取消所有高亮
```

### 行号常量命名建议

```javascript
const LINE_COMPARE    = 6;   // 比较
const LINE_UPDATE_MIN = 7;   // 更新最小值索引
const LINE_SWAP_TEMP  = 10;  // 交换临时变量
const LINE_SWAP_A     = 11;  // 交换赋值 a
const LINE_SWAP_B     = 12;  // 交换赋值 b
const LINE_INSERT     = 5;   // 插入操作（插入排序用）
const LINE_MERGE      = 8;   // 合并操作（归并排序用）
```

---

## 分隔线（已排序/未排序）

```javascript
// 更新分隔线位置，sortedCount 为已排序元素个数
updateDivider(0);              // 隐藏分隔线
updateDivider(i + 1);          // 分隔线在第 i+1 个元素左侧
updateDivider(arr.length);     // 排序完成，隐藏分隔线
```

---

## 常见复用陷阱

### ❌ 陷阱 1：交换后忘记更新数据

```javascript
// 错误：只有动画，没有数据交换
await animSwap(circleOrder[i], circleOrder[j], i, j);
// arr 没变！下次比较还是旧数据

// 正确：
await animSwap(circleOrder[i], circleOrder[j], i, j);
[arr[i], arr[j]] = [arr[j], arr[i]];  // ← 必须同步更新
```

### ❌ 陷阱 2：animSwap 前没有设为 normal

```javascript
// 错误：元素还是 active/pivot 状态就执行交换
setCircleState(i, 'active');
await animSwap(...);  // active 的 border:none 会残留

// 正确：先恢复 normal，再交换
setCircleState(i, 'normal');
setCircleState(j, 'normal');
await animSwap(...);
```

### ❌ 陷阱 3：循环计数器没有重置

```javascript
// 错误：第二次点开始，循环次数从上次的值继续
// 因为 loops 没有归零

// 正确：startSort() 中已包含 loops = 0，自定义时注意
```

### ❌ 陷阱 4：生成器中忘记 yield

```javascript
// 错误：暂停功能不生效
if (isPaused) return;  // ← 直接 return 会终止生成器

// 正确：
if (isPaused) yield 'paused';  // ← yield 暂停，下次调用 .next() 继续
```

### ❌ 陷阱 5：手动修改 circleOrder

```javascript
// 错误：直接操作 circleOrder 数组
circleOrder[0] = circleOrder[1];  // 会破坏位置映射

// 正确：使用 animSwap 或 moveCircleTo，它们内部已处理 circleOrder
await animSwap(circleOrder[posA], circleOrder[posB], posA, posB);
// 或
moveCircleTo(fromPos, toPos);
```

### ❌ 陷阱 6：分隔线方向搞反

```javascript
// 错误：冒泡排序用 updateDivider(i + 1)
// 结果：分隔线从左侧开始右移，方向完全反了

// 正确：冒泡排序的已排序区在右侧，分隔线应从右往左移
updateDivider(n - i - 1);  // 冒泡排序
updateDivider(i + 1);      // 选择排序、插入排序
```

> 💡 判断规则：看每轮排序结束后已排序元素在数组的哪一端。左端用 `i+1`，右端用 `n-i-1`。
> 详见「分隔线系统」章节。

---

## 10 个算法的配置参考

### 1. 冒泡排序 (bubble_sort)

```
JAVA_FILENAME: BubbleSort.java
TIME: O(n²)  SPACE: O(1)  稳定性: 稳定
LINE_COMPARE=5, LINE_SWAP=7
逻辑：相邻比较，大的往后冒泡
分隔线：已排序区在右侧，用 updateDivider(n - i - 1)
```

### 2. 选择排序 (selection_sort) ✅ 已完成

```
JAVA_FILENAME: SelectionSort.java
TIME: O(n²)  SPACE: O(1)  稳定性: 不稳定
LINE_INIT_MIN=4, LINE_COMPARE=6, LINE_UPDATE_MIN=7, LINE_SWAP_TEMP=10
逻辑：找 minIdx → 交换 a[i] 和 a[minIdx]
分隔线：已排序区在左侧，用 updateDivider(i + 1)
```

### 3. 插入排序 (insertion_sort)

```
JAVA_FILENAME: InsertionSort.java
TIME: O(n²)  SPACE: O(1)  稳定性: 稳定
LINE_EXTRACT=3, LINE_SHIFT=6, LINE_INSERT=8
逻辑：取出 key → 右移元素 → 插入 key
特殊：使用 moveCircleTo() 做位移动画
分隔线：已排序区在左侧，用 updateDivider(i + 1)
```

### 4. 希尔排序 (shell_sort)

```
JAVA_FILENAME: ShellSort.java
TIME: O(n log²n)  SPACE: O(1)  稳定性: 不稳定
LINE_EXTRACT=4, LINE_SHIFT=7
逻辑：按 gap 分组，每组做插入排序
特殊：gap 逐步缩小
```

### 5. 归并排序 (merge_sort)

```
JAVA_FILENAME: MergeSort.java
TIME: O(n log n)  SPACE: O(n)  稳定性: 稳定
LINE_COMPARE=6, LINE_MERGE=10
逻辑：递归分治，合并两个有序子数组
特殊：需要跟踪递归区间 [start, mid, end)
```

### 6. 快速排序 (quick_sort)

```
JAVA_FILENAME: QuickSort.java
TIME: O(n log n)  SPACE: O(log n)  稳定性: 不稳定
LINE_PIVOT=3, LINE_COMPARE=6, LINE_SWAP=8, LINE_PLACE=10
逻辑：选基准值 → 分区 → 递归
特殊：基准值用 'pivot' 紫色高亮
```

### 7. 堆排序 (heap_sort)

```
JAVA_FILENAME: HeapSort.java
TIME: O(n log n)  SPACE: O(1)  稳定性: 不稳定
LINE_CHILD_L=5, LINE_CHILD_R=8, LINE_SWAP=10, LINE_EXTRACT=14
逻辑：建堆 → 逐步取出堆顶
特殊：需要 heapify 递归
```

### 8. 计数排序 (counting_sort)

```
JAVA_FILENAME: CountingSort.java
TIME: O(n+k)  SPACE: O(k)  稳定性: 稳定
LINE_COUNT=3, LINE_OUTPUT=8
逻辑：统计频率 → 累加 → 构建输出
特殊：无直接交换，用 'active' 高亮表示放入输出
```

### 9. 桶排序 (bucket_sort)

```
JAVA_FILENAME: BucketSort.java
TIME: O(n+k)  SPACE: O(n+k)  稳定性: 稳定
LINE_DISTRIBUTE=3, LINE_MERGE=8
逻辑：分配到桶 → 桶内排序 → 合并
特殊：需要显示桶的概念
```

### 10. 基数排序 (radix_sort)

```
JAVA_FILENAME: RadixSort.java
TIME: O(n×k)  SPACE: O(n+k)  稳定性: 稳定
LINE_DIGIT=6
逻辑：按位排序（个位→十位→...）
特殊：每轮按一位排序，需要显示当前位
```

---

## 扩展：添加新的小球状态

如果算法需要新的高亮状态（如「正在扫描」「已访问」等），按以下步骤：

```css
/* 1. 在 <style> 中添加新状态类 */
/* ⚠️ 必须定义 border 属性，否则边框会消失！ */
.circle.scanning {
    background: linear-gradient(135deg, #06b6d4, #22d3ee);
    color: #fff;
    box-shadow: 0 0 24px rgba(6, 182, 212, 0.6),
                0 0 48px rgba(6, 182, 212, 0.2);
    border: none;    /* ← 不要省略！如果要边框，写具体值 */
    z-index: 5;
    filter: brightness(1.15);
}
```

```javascript
// 2. 在生成器中使用
setCircleState(pos, 'scanning');
```

### ⚠️ 添加新状态的约束

- **必须定义 `border`**：如果不要边框写 `border: none`，要边框写具体的 border 值
- **不要省略 `border` 属性**：否则继承 `.circle` 基类（无 border），边框会消失
- **新状态类放在 `.circle.sorted` 之前**：确保 CSS 优先级正确

---

## 文件结构

```
algorithm-visualizer/
├── animation_template.html        ← 复用模板（复制这个）
├── ANIMATION_FRAMEWORK.md          ← 本文档
├── selection_sort_animation.html   ← 已完成：选择排序
├── bubble_sort_animation.html      ← 已完成：冒泡排序
├── insertion_sort_animation.html   ← 已完成：插入排序
└── ...
```

---

## 调试技巧

1. **动画不同步**: 确保 `await sleep()` 等待时间 ≥ CSS transition 时间 (0.4s)
2. **圆圈位置错乱**: 检查 `circleOrder` 是否正确更新，用 `console.log(circleOrder)` 调试
3. **高亮不消失**: 确保每个步骤结束时调用 `setCircleState(pos, 'normal')`
4. **暂停不生效**: 确保在 `await sleep()` 之后检查 `if (isPaused) yield 'paused'`
5. **边框消失**: 检查状态类是否定义了 `border` 属性，检查 animSwap 是否用 `classList.add` 而非 `className =`
