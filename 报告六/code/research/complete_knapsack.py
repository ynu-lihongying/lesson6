"""独立研究②：完全背包（每件物品可以重复取无限次）与 0-1 背包差在哪一行。

0-1 背包：dp[i][c] = max(dp[i-1][c], dp[i-1][c-w[i]] + v[i])
完全背包：dp[i][c] = max(dp[i-1][c], dp[i][c-w[i]] + v[i])
                                    ^^^^^^^^^ 从“本行”而不是“上一行”取

为什么：完全背包在决定“再拿一件第 i 种物品”时，之前的决策里第 i 种物品
仍然可以继续拿，所以参考的是同一行（已经允许重复拿第 i 种）的格子；
0-1 背包每件只能用一次，拿第 i 件后必须回到“前 i-1 件”的世界，故看上一行。

一维写法更常见的记法：
- 0-1 背包：容量 for c 从 C 递减到 w[i]（保证本件只用一次）
- 完全背包：容量 for c 从 w[i] 递增到 C（允许本件反复使用）

运行：python complete_knapsack.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 让脚本能找到上一级的 knapsack.py
from knapsack import ITEMS, UNIT


def knapsack_01(items, cap, unit=UNIT):
    """0-1 背包的一维写法：容量从大到小遍历。"""
    C = cap // unit
    dp = [0] * (C + 1)
    for _, weight, value in items:
        w = weight // unit
        for c in range(C, w - 1, -1):        # ← 递减，防止同一件被重复使用
            dp[c] = max(dp[c], dp[c - w] + value)
    return dp[C]


def knapsack_complete(items, cap, unit=UNIT):
    """完全背包的一维写法：容量从小到大遍历，并记录选了哪些。"""
    C = cap // unit
    dp = [0] * (C + 1)
    choice = [-1] * (C + 1)
    for c in range(1, C + 1):
        for k, (_, weight, value) in enumerate(items):
            w = weight // unit
            if c >= w and dp[c - w] + value > dp[c]:
                dp[c] = dp[c - w] + value    # ← 本行反复使用，即“完全背包”
                choice[c] = k
    combo, c = [], C
    while c > 0:
        k = choice[c]
        if k < 0:
            break
        combo.append(k)
        c -= items[k][1] // unit
    combo.sort()
    return dp[C], combo


def main():
    cap = 1000
    v01 = knapsack_01(ITEMS, cap)
    vc, combo = knapsack_complete(ITEMS, cap)
    names = [ITEMS[k][0] for k in combo]
    weight = sum(ITEMS[k][1] for k in combo)

    print(f"同一组物品、限重 {cap}g：")
    print(f"  0-1 背包（每件最多 1 次）：最优 {v01}")
    print(f"  完全背包（物品可重复）：最优 {vc}，组合 {names}，{weight}g")
    print(f"\n差别一行：0-1 用 dp[i-1][c-w]（上一行），完全用 dp[i][c-w]（本行）；")
    print(f"一维写法对应“容量递减”与“容量递增”。")
    print(f"在本题里，完全背包可以拿 2 个睡袋 + 1 个帐篷 = 2×115+90 = 320，")
    print(f"比 0-1 背包的 315 更高，正是“可重复”带来的差别。")

    ok = v01 == 315 and vc == 320
    print(f"\n自查（0-1 = 315，完全 = 320）：{'通过' if ok else '未通过'}")


if __name__ == "__main__":
    main()
