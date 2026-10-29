"""独立研究①：n-皇后问题（回溯法）。

n-皇后问题：在 n×n 棋盘上放 n 个皇后，使任意两个皇后都不在同一行、同一列、
同一条斜线上，求方案数（并打印一种方案）。

与“动规式穷举”的区别：
- n-皇后是“可行性/计数”搜索，没有可最大化的目标值，也不存在重叠子问题；
  第 i 行的可行位置依赖前面所有皇后的具体摆法，状态无法压缩成一张 dp 表，
  所以不能用动规。
- 回溯法仍是穷举，但“边走边判”：某一行放不下时立即退回上一行换位置，
  提前砍掉整棵不可能成活的分支（剪枝），比“先枚举全部 n^n 种摆法再检查”少走很多路。

运行：python n_queens.py
预期：n=4 有 2 解，n=8 有 92 解。
"""


def solve_n_queens(n, want_one=False):
    """回溯求 n-皇后方案；返回 (方案数, 第一个方案或 None)。"""
    cols = set()          # 已占用的列
    diag1 = set()         # 主对角线：行-列 相同
    diag2 = set()         # 副对角线：行+列 相同
    queen_col = [-1] * n  # queen_col[r] = 第 r 行皇后所在列
    count = 0
    first = None

    def backtrack(r):
        nonlocal count, first
        if r == n:                       # 第 n 行也放好了，得到一个完整方案
            count += 1
            if first is None:
                first = queen_col[:]
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue                 # 冲突，这一格不能放，直接换下一列
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            queen_col[r] = c
            backtrack(r + 1)             # 递归放下一行
            cols.remove(c)               # 撤销选择 → 回溯
            diag1.remove(r - c)
            diag2.remove(r + c)

    backtrack(0)
    return count, first


def print_board(queen_col):
    n = len(queen_col)
    for r in range(n):
        print(" ".join("Q" if c == queen_col[r] else "." for c in range(n)))


def main():
    for n in (4, 8):
        count, first = solve_n_queens(n)
        print(f"n={n}：共 {count} 种方案")
        if n == 4 and first is not None:
            print("其中一种方案（Q 为皇后）：")
            print_board(first)
        print()

    count4, _ = solve_n_queens(4)
    count8, _ = solve_n_queens(8)
    print(f"检查点（n=4 → 2，n=8 → 92）：{'通过' if (count4, count8) == (2, 92) else '未通过'}")


if __name__ == "__main__":
    main()
