"""追加题库模板：复制本文件改名（如 easy_batch.py），填好三处即可被 build_problems 自动发现。

约定：
  · 参考解放 generator/reference/<pid>.py，读 stdin、print 答案
  · 填空题脚本放 generator/fill_scripts/<pid>.py，print 最终答案
  · pid 用 pNN_xxx，NN 是 order（全局唯一、从 1 连续）
  · prog_cases() 返回 {pid: [(测试点名字, 输入文本), ...]}，第一条必须是可见样例
  · 只手写输入数据，绝不手写 expected —— 那些由 build_problems 跑参考解生成

构建自己这一批（不影响别的题）：
    python generator/build_problems.py --only p28 p29 p30
    python generator/self_check.py    --only p28 p29 p30

渲染规矩（踩过的坑）：
  · statement、solution.idea 前端用 innerHTML —— 里面的 < > & 要写成 &lt; &gt; &amp;；
    想在页面上显示字面 &lt; 就得再转一层写 &amp;lt;
  · input_format、output_format、answer_hint 前端用 textContent —— 不要写 HTML 实体，
    否则页面原样显示 &lt;；要表达"小于"直接用 ≤ 这类纯文本字符

其它坑：判题输出上限 1 MB（注意 OLE）；O(n^2) 参考解要把 n 压到 2 秒内跑得完并在题面写明范围；
禁用词 AI/模型/生成/人工智能（题干和测试点名字都算）；平均数别用 .xx5 这种舍入有歧义的值。
"""

PROG_META = [
    {
        "pid": "p90_example",
        "title": "示例题：求和",
        "difficulty": "入门",
        "tags": ["输入输出", "循环"],
        "chapter": "第 1 章 / 第 2 章",
        "source": "蓝桥杯省赛真题（题意整理）",
        "statement": "<p>读入 n 个整数，输出它们的和。</p>",
        "input_format": "第一行一个整数 n；第二行 n 个整数，空格分隔。",
        "output_format": "一行，一个整数。",
        "idea": "<p>读入后累加即可，注意 <code>input()</code> 拿到的是字符串。</p>",
        "reference": "code/ch02-control/03_sum_template.py",
    },
]

FILL_META = [
    # {
    #     "pid": "p91_example_fill", "title": "示例填空题", "difficulty": "入门",
    #     "tags": ["枚举"], "chapter": "第 5 章", "source": "蓝桥杯省赛真题（题意整理）",
    #     "statement": "<p>……</p>", "script": "p91_example_fill.py",
    #     "idea": "<p>……</p>", "answer_hint": "别手算，写程序跑", "reference": "code/...",
    # },
]


def prog_cases():
    return {
        "p90_example": [
            ("样例", "5\n1 2 3 4 5\n"),
            ("最小 n=1", "1\n7\n"),
            ("含负数", "4\n-1 -2 3 4\n"),
            ("较大规模", "100000\n" + " ".join(["1"] * 100000) + "\n"),
        ],
    }
