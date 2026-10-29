"""自主实践②：给 0-1 背包加“必投项目”约束。

题意：在原有五件物品中指定一件“必投”，它必须被带上，其余物品仍可选可不选，
在 1000g 限重下求最优组合。做法是扣除必投物品的重量与价值，在剩余物品和
剩余容量上照常跑 0-1 背包，最后把必投物品加回组合。

运行：python step4_required_item.py
"""

from knapsack import ITEMS, brute_force, knapsack_required


def show_required(required, cap=1000):
    name = ITEMS[required][0]
    best, chosen = knapsack_required(ITEMS, cap, required)
    if best is None:
        print(f"必投 {name}（{ITEMS[required][1]}g）：限重 {cap}g 时装不下 → 无可行解")
        return None, None
    names = [ITEMS[k][0] for k in chosen]
    weight = sum(ITEMS[k][1] for k in chosen)
    bf_value, bf_set = brute_force(ITEMS, cap, required=required)
    print(f"必投 {name}（{ITEMS[required][1]}g, {ITEMS[required][2]}）：")
    print(f"  最优 {best}（{' + '.join(names)}，{weight}g，1基 {[k + 1 for k in chosen]}）")
    print(f"  穷举核对：{bf_value}，1基 {[k + 1 for k in bf_set]} → "
          f"{'一致' if (best, chosen) == (bf_value, bf_set) else '不一致'}")
    return best, chosen


def main():
    from knapsack import knapsack_dp
    best_free, chosen_free, _ = knapsack_dp(ITEMS, 1000)
    names_free = [ITEMS[k][0] for k in chosen_free]
    print(f"无约束：{best_free}（{' + '.join(names_free)}，1基 {[k + 1 for k in chosen_free]}）\n")

    print("===== 情形一：必投“帐篷”（原最优组合里没有它）=====")
    show_required(0)
    print("\n===== 情形二：必投“睡袋”（原最优组合里已有它）=====")
    show_required(2)
    print("\n===== 情形三：必投“炉具”=====")
    show_required(1)
    print("\n===== 情形四：必投“帐篷”但容量只有 200g（不可行）=====")
    show_required(0, cap=200)

    print("\n===== 解释 =====")
    print("必投约束把“可选题”变成“必选题”：先无条件占用一份重量和重要度，")
    print("剩余容量变小，原最优组合可能被挤掉。必投“帐篷”时，剩余 700g 最多")
    print("再拿 食物+水具（200），总计 90+200 = 290，比无约束的 315 少 25；")
    print("必投“睡袋”时它本来就在原最优组合里，所以最优值仍是 315，组合不变。")


if __name__ == "__main__":
    main()
