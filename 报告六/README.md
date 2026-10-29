# lesson06-dp · 贪心与动态规划（第 6 次课作业）

- 课程：《人工智能程序设计与实践》2026 秋
- 学号／姓名：20251030168 李红颖
- 对应实践指南六《贪心与动态规划 × 用 AI 开发程序》与课堂作业六
- 本仓库所有代码均为 Python 标准库实现，不依赖第三方包

## 目录结构

```text
报告六/
├── README.md                       # 本文件
├── progress.md                     # 进度报告（按课件站模板）
├── 20251030168_李红颖_贪心与动态规划实验报告.md
├── code/
│   ├── step1_coin.py               # 案例复现 Step1：凑硬币 贪心 vs 动规
│   ├── knapsack.py                 # 0-1 背包核心函数（dp、回溯、贪心、穷举核对）
│   ├── step2_knapsack.py           # 案例复现 Step2：0-1 背包 + 回溯组合
│   ├── step3_budget_compare.py     # 自主实践①：容量 1000→800 对比
│   ├── step4_required_item.py      # 自主实践②：必投项目约束
│   └── research/
│       ├── n_queens.py             # 独立研究①：n-皇后回溯
│       ├── complete_knapsack.py    # 独立研究②：完全背包
│       └── branch_bound.py         # 独立研究③：分支限界
├── results/                        # 各脚本的真实运行输出
└── images/dp_heatmap.svg           # dp 表热力图（选做留档）
```

## 运行方法

在 `code/` 目录下执行：

```sh
python step1_coin.py
python step2_knapsack.py
python step3_budget_compare.py
python step4_required_item.py
python research/n_queens.py
python research/complete_knapsack.py
python research/branch_bound.py
```

## 检查点

| 检查点 | 程序输出 | 是否通过 |
|---|---|---|
| 凑硬币：贪心 5 枚 vs 动规 3 枚 | 贪心 `11+1+1+1+1`，动规 `5+5+5` | 通过 |
| 背包最优 315，组合 [3,4,5] | `睡袋 + 食物 + 水具`，350+400+250=1000g | 通过 |
| 至多装满变体 | dp 初值全 0（不是恰好装满的 −inf） | 已在报告中写明 |

## 提交说明

- 代码、报告与运行输出已整理完毕，可直接纳入本人仓库 `lesson06-dp`；
- Git 初始化与远程 push 由本人自行完成，示例命令：
  `git init && git add . && git commit -m "lesson06-dp: 贪心与动态规划作业" && git remote add origin <仓库地址> && git push -u origin main`。
