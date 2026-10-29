"""独立研究③：分支限界（branch and bound）解 0-1 背包，并统计搜索节点数。

一句话：分支限界 = 回溯 + 上界剪枝 + 优先扩展最有希望的节点。
- 分支：每件物品“带 / 不带”两路。
- 限界：用“剩余容量按性价比装满”的小数解算出一个上界；若这个上界都超不过
  当前已找到的最好解，整条分支直接砍掉，不再往下搜。
- 比回溯好在哪：回溯只检查“可行不可行”并盲目深度优先，分支限界带着“最多还能
  值多少”的判断做最优性剪枝，通常要访问的节点更少；代价是要维护上界和优先队列。

运行：python branch_bound.py
预期：最优 315，访问节点数明显少于 2^5 = 32 个叶子的全枚举。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 让脚本能找到上一级的 knapsack.py
from knapsack import ITEMS


def branch_and_bound(items, cap):
    """按性价比排序后深度优先搜索，用小数背包上界剪枝。返回 (最优值, 组合, 访问节点数)。"""
    order = sorted(range(len(items)), key=lambda k: -items[k][2] / items[k][1])
    n = len(items)
    best_value, best_set = 0, []
    nodes = 0

    def bound(i, remain):
        """把剩余物品按性价比装满（最后一件可切分）得到上界。"""
        total = 0
        for k in order[i:]:
            _, weight, value = items[k]
            if weight <= remain:
                remain -= weight
                total += value
            else:
                total += value * remain / weight   # 切分最后一件，放大上界
                break
        return total

    def dfs(i, remain, value, chosen):
        nonlocal best_value, best_set, nodes
        nodes += 1
        if value > best_value:                     # 找到一个更好的可行解
            best_value, best_set = value, chosen[:]
        if i == n:
            return
        # 剪枝：当前值 + 剩余上界 <= 已知最优，整条分支没有希望
        if value + bound(i, remain) <= best_value:
            return
        k = order[i]
        _, weight, val = items[k]
        if weight <= remain:                       # 分支1：带
            chosen.append(k)
            dfs(i + 1, remain - weight, value + val, chosen)
            chosen.pop()
        dfs(i + 1, remain, value, chosen)           # 分支2：不带

    dfs(0, cap, 0, [])
    return best_value, sorted(best_set), nodes


def main():
    cap = 1000
    best, chosen, nodes = branch_and_bound(ITEMS, cap)
    names = [ITEMS[k][0] for k in chosen]
    weight = sum(ITEMS[k][1] for k in chosen)
    print(f"分支限界：最优 {best}（{' + '.join(names)}，{weight}g），访问节点 {nodes} 个")
    print(f"全枚举叶子数：2^{len(ITEMS)} = {2 ** len(ITEMS)} 个")
    print(f"说明：分支限界用上界砍掉了大量不可能更优的分支，因此节点数远少于全枚举；")
    print(f"回溯法只判可行性、不做上界剪枝，最坏仍要搜遍整棵解空间树。")
    ok = best == 315 and nodes < 32
    print(f"自查（最优 315 且节点数 < 32）：{'通过' if ok else '未通过'}")


if __name__ == "__main__":
    main()
