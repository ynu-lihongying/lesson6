"""0-1 背包核心函数（Step2 / Step3 / Step4 共用）。

两条约定：
1. 容量以 50g 为一档（UNIT = 50）。本课五件物品重量都是 50 的倍数，
   用 50g 一档与逐克计算的结果完全一致，但 dp 表更紧凑、便于贴进报告。
2. 统一使用“至多装满”变体：容量可以不花完，因此 dp 初始值全为 0；
   若用“恰好装满”，初值应为 -inf（除 dp[*][0] = 0），答案可能不同。
"""

UNIT = 50

ITEMS = [
    ("帐篷", 300, 90),
    ("炉具", 200, 60),
    ("睡袋", 350, 115),
    ("食物", 400, 120),
    ("水具", 250, 80),
]


def knapsack_dp(items, cap, unit=UNIT):
    """0-1 背包（至多装满）。返回 (最优重要度, 选中物品的0基下标, dp表)。

    心脏一行：
        dp[i][c] = max(dp[i - 1][c],                       # 不带第 i 件
                       dp[i - 1][c - w[i]] + v[i])          # 带（前提 c >= w[i]）
    dp 的每一行都可以由上一行推出，所以从第 1 行逐行填到第 n 行即可。
    """
    n = len(items)
    C = cap // unit
    w = [it[1] // unit for it in items]
    v = [it[2] for it in items]

    dp = [[0] * (C + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for c in range(C + 1):
            dp[i][c] = dp[i - 1][c]                       # 不带第 i 件
            if c >= w[i - 1] and dp[i - 1][c - w[i - 1]] + v[i - 1] > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w[i - 1]] + v[i - 1]   # 带第 i 件

    # 回溯：从右下角出发，比较“本格”和“正上方”，相等说明没带第 i 件
    chosen = []
    i, c = n, C
    while i > 0:
        if dp[i][c] == dp[i - 1][c]:
            i -= 1                                        # 没带第 i 件，往上走
        else:
            chosen.append(i - 1)                          # 带了第 i 件
            c -= w[i - 1]
            i -= 1
    chosen.sort()
    return dp[n][C], chosen, dp


def knapsack_required(items, cap, required, unit=UNIT):
    """加“必投项目”约束：required 号物品必须带上，其余仍按 0-1 背包求最优。

    做法：先扣除必投物品的重量和价值，再在其余物品、剩余容量上跑普通 0-1 背包。
    若必投物品本身就超重，则无可行解，返回 (None, None)。
    """
    if items[required][1] > cap:
        return None, None
    rest = [k for k in range(len(items)) if k != required]
    rest_items = [items[k] for k in rest]
    best, sub_chosen, _ = knapsack_dp(rest_items, cap - items[required][1], unit)
    chosen = sorted([rest[k] for k in sub_chosen] + [required])
    return items[required][2] + best, chosen


def knapsack_greedy_ratio(items, cap):
    """按性价比（价值/重量）从高到低装，能装就装——这是贪心，不保证全局最优。

    排序规则：性价比降序；性价比相同则轻的优先（便于复现）。
    """
    order = sorted(
        range(len(items)),
        key=lambda k: (-items[k][2] / items[k][1], items[k][1]),
    )
    remain, chosen = cap, []
    for k in order:
        if items[k][1] <= remain:
            chosen.append(k)
            remain -= items[k][1]
    chosen.sort()
    value = sum(items[k][2] for k in chosen)
    used = sum(items[k][1] for k in chosen)
    return value, chosen, used


def brute_force(items, cap, required=None):
    """穷举全部 2^n 种组合，作为 dp 结果的独立核对（n=5 时只有 32 种）。"""
    n = len(items)
    best, best_set = -1, None
    for mask in range(1 << n):
        chosen = [k for k in range(n) if mask >> k & 1]
        if required is not None and required not in chosen:
            continue
        weight = sum(items[k][1] for k in chosen)
        if weight > cap:
            continue
        value = sum(items[k][2] for k in chosen)
        if value > best:
            best, best_set = value, chosen
    return best, best_set
