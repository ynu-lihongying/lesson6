"""Step1 凑硬币：贪心 vs 动态规划（面额 1、5、11，金额 15）。

运行：python step1_coin.py
检查点：贪心 5 枚（11+1+1+1+1） vs 动规 3 枚（5+5+5）。
"""

INF = float("inf")


def coin_greedy(coins, amount):
    """贪心：每一步都取“不超过余额的最大面额”，拿到拿不动为止，不回头。"""
    remain = amount
    combo = []
    for c in sorted(coins, reverse=True):      # 从大到小依次尝试
        while remain >= c:                     # 当前面额还能拿就继续拿
            combo.append(c)
            remain -= c
    if remain != 0:                            # 面额表凑不出余额
        return None, None
    return len(combo), combo


def coin_dp(coins, amount):
    """动规：dp[c] = 凑出 c 元的最少枚数。

    递推（本题的心脏一行）：
        dp[c] = 1 + min(dp[c - coin])          # 对每个 c >= coin 的面额取最小
    地基：dp[0] = 0。choice[c] 记录“最后一枚用了哪张面额”，供回溯组合。
    """
    dp = [INF] * (amount + 1)
    dp[0] = 0
    choice = [-1] * (amount + 1)
    for c in range(1, amount + 1):
        for coin in coins:
            if c >= coin and dp[c - coin] + 1 < dp[c]:
                dp[c] = dp[c - coin] + 1        # ← 能指认的填表那一行
                choice[c] = coin
    if dp[amount] == INF:
        return None, None, dp
    combo = []
    c = amount
    while c > 0:                                # 顺着 choice 回溯出具体组合
        combo.append(choice[c])
        c -= choice[c]
    return dp[amount], combo, dp


def main():
    coins = [1, 5, 11]
    amount = 15

    gc, gcombo = coin_greedy(coins, amount)
    dc, dcombo, dp = coin_dp(coins, amount)

    print(f"面额 {coins}，金额 {amount}")
    print(f"贪心：{gc} 枚  →  {'+'.join(map(str, gcombo))} = {amount}")
    print(f"动规：{dc} 枚  →  {'+'.join(map(str, dcombo))} = {amount}")
    print(f"dp[c] 填表（c=0..{amount}）：{dp}")
    print(f"检查点（贪心 5 枚、动规 3 枚）：{'通过' if (gc, dc) == (5, 3) else '未通过'}")


if __name__ == "__main__":
    main()
