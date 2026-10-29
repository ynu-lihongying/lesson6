"""自主实践①：背包容量从 1000g 改成 800g，对比动规与按性价比贪心的结果。

运行：python step3_budget_compare.py
要点：对比 1000 → 800 的动规最优值变化，并检查贪心在 800g 是否仍然最优。
"""

from knapsack import ITEMS, knapsack_dp, knapsack_greedy_ratio


def show(cap):
    best, chosen, _ = knapsack_dp(ITEMS, cap)
    gval, gchosen, gused = knapsack_greedy_ratio(ITEMS, cap)
    names = [ITEMS[k][0] for k in chosen]
    gnames = [ITEMS[k][0] for k in gchosen]
    weight = sum(ITEMS[k][1] for k in chosen)
    print(f"容量 {cap}g：")
    print(f"  动规：{best}（{' + '.join(names)}，{weight}g，1基 {[k + 1 for k in chosen]}）")
    print(f"  贪心（性价比）：{gval}（{' + '.join(gnames)}，{gused}g，1基 {[k + 1 for k in gchosen]}）")
    print(f"  贪心是否等于动规最优：{gval == best}")
    return best, gval


def main():
    best1000, greedy1000 = show(1000)
    print()
    best800, greedy800 = show(800)

    print("\n===== 对比与解释 =====")
    print(f"容量 1000 → 800：动规最优 {best1000} → {best800}，下降 {best1000 - best800}")
    print(f"下降原因：原来 睡袋350 + 食物400 + 水具250 恰好占满 1000g；")
    print(f"容量只剩 800g 时，400g 的食物无法再与 350g 的睡袋同时放下，")
    print(f"只能换成 炉具200 + 睡袋350 + 水具250 = 800g，重要度 60+115+80 = {best800}。")
    print(f"贪心在 800g 刚好也得到 {greedy800}，与最优相同；")
    print(f"但把容量放回 1000g，贪心只有 {greedy1000}，低于动规 {best1000}——")
    print(f"这说明贪心“这次碰巧对”不等于“永远对”，仍要看问题结构、持证上岗。")
    ok = best1000 == 315 and best800 == 255 and greedy800 == 255 and greedy1000 == 255
    print(f"\n自查（1000:315、800:255、贪心800=255、贪心1000=255）：{'通过' if ok else '未通过'}")


if __name__ == "__main__":
    main()
