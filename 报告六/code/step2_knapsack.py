"""Step2 0-1 背包：限重 1000g，五件物品，每件要么带要么不带（至多装满）。

运行：python step2_knapsack.py
检查点：最优重要度 315，组合 睡袋 + 食物 + 水具（350+400+250 = 1000g）。
"""

from knapsack import ITEMS, UNIT, brute_force, knapsack_dp


def print_table(items, dp, unit):
    """打印完整 dp 表：行=前 i 件，列=容量（每 50g 一档）。"""
    cap_labels = [f"{c * unit}" for c in range(len(dp[0]))]
    row_head = "前i件\\容量g"
    print(f"{row_head:<12}" + "".join(f"{lab:>5}" for lab in cap_labels))
    for i, row in enumerate(dp):
        name = "无物品" if i == 0 else f"{i}.{items[i - 1][0]}"
        print(f"{name:<12}" + "".join(f"{val:>5}" for val in row))


def trace_path(items, dp, unit):
    """从右下角回溯，返回 (选中下标, 经过的格子列表)。"""
    n = len(items)
    w = [it[1] // unit for it in items]
    i, c = n, len(dp[0]) - 1
    chosen, cells = [], []
    while i > 0:
        if dp[i][c] == dp[i - 1][c]:
            cells.append((i, c, f"跳过 {items[i - 1][0]}", dp[i][c]))
            i -= 1
        else:
            cells.append((i, c, f"带上 {items[i - 1][0]}", dp[i][c]))
            chosen.append(i - 1)
            c -= w[i - 1]
            i -= 1
    cells.append((0, c, "到达地基", dp[0][c]))
    chosen.sort()
    return chosen, cells


def main():
    cap = 1000
    best, chosen, dp = knapsack_dp(ITEMS, cap)

    print(f"背包限重 {cap}g；容量按 {UNIT}g 一档，共 {len(dp[0]) - 1} 档（至多装满）")
    print("\n===== 完整 dp 表（行=前 i 件，列=容量 g）=====")
    print_table(ITEMS, dp, UNIT)

    print("\n===== dp 表最后一行（前 5 件、各容量下的最优重要度）=====")
    print("容量g : " + "".join(f"{c * UNIT:>5}" for c in range(len(dp[0]))))
    print("最优值: " + "".join(f"{val:>5}" for val in dp[5]))
    print(f"dp[5][1000] = {dp[5][-1]}")

    _, cells = trace_path(ITEMS, dp, UNIT)
    print("\n===== 回溯路径（从 dp[5][1000] 往左上走）=====")
    for i, c, action, val in cells:
        print(f"  dp[{i}][{c * UNIT:>4}g] = {val:>3}  {action}")

    names = [ITEMS[k][0] for k in chosen]
    weight = sum(ITEMS[k][1] for k in chosen)
    value = sum(ITEMS[k][2] for k in chosen)
    print(f"\n最优组合（0基）：{chosen}；1基：{[k + 1 for k in chosen]}")
    print(f"物品：{' + '.join(names)}")
    print(f"重量：{weight}g，重要度：{value}")
    print(f"是否恰好装满：{weight == cap}")

    bf_value, bf_set = brute_force(ITEMS, cap)
    print(f"\n穷举核对：最优 {bf_value}，组合 {bf_set}（1基 {[k + 1 for k in bf_set]}）")
    ok = (value, chosen) == (315, [2, 3, 4]) and bf_value == 315 and bf_set == [2, 3, 4]
    print(f"检查点（315 + 睡袋/食物/水具，且与穷举一致）：{'通过' if ok else '未通过'}")


if __name__ == "__main__":
    main()
