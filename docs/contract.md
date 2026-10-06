# 内部契约（前端与题库共同遵守）

服务：`python server/app.py` → `http://127.0.0.1:8000`（只监听本机）

## 页面路由（服务端直接返回 `web/` 下的文件）

| 路径 | 文件 | 说明 |
|---|---|---|
| `/` | `web/index.html` | 首页：统计卡片 + 题库速览 + 快速开始 |
| `/problems` | `web/problems.html` | 题库列表（可筛选类型/难度/考点/状态） |
| `/problem?id=xxx` | `web/problem.html` | 题目详情：左题干右代码，判题结果、测试点、提交历史、题解 |
| `/submissions` | `web/submissions.html` | 全部提交记录 |
| `/contest` | `web/contest.html` | 模拟赛：选题开考、倒计时、成绩单 |

静态资源放 `web/assets/`（`oj.css`、`oj.js`，可再加）。前端只允许引用本地文件，不得引 CDN。

## API

```
GET  /api/problems
  → {items:[{id,title,type,difficulty,score,tags,chapter,test_count,solved,tries,best_score}],
     stats:{problems,solved,submissions,ac_submissions,ac_rate,tags:[{tag,total,solved,tries,rate}]}}

GET  /api/problem?id=<pid>
  → {problem:{...题目公开字段...}, best:{solved,score,full,tries,...}, history:[提交记录], solution_unlocked:bool}
  隐藏测试点只含 {name,score,hidden:true}，不含 input/expected。

POST /api/submit   {problem_id, code, contest_id?}
  → {id,result,passed,total,score,full_score,max_ms,wall_ms,
     cases:[{name,status,ms,hidden,expected,got,detail}],
     error?:{status,detail,line,excerpt}, labels:{AC:"通过",...}}
  result ∈ AC|WA|TLE|RE|CE|OLE|IE

POST /api/answer   {problem_id, answer, contest_id?}   // 填空题
  → {id,result,ok,score,full_score,passed,total,detail}

GET  /api/solution?id=<pid>     // 调用即记录"已看题解"
  → {idea,code,output,answer,reference,chapter}

GET  /api/submissions?limit=100&problem=<pid>
  → {items:[{id,problem_id,kind,result,score,full_score,passed,total,ms,answer,code,detail,created_at}]}

GET  /api/stats
POST /api/star          {problem_id, on?}   // on 省略=切换；返回 {ok, starred, starred_total}
POST /api/contest/start   {title?, duration_min, problem_ids?}  → {id,problem_ids,duration_s,started_at}
GET  /api/contest                    → {items:[比赛], problems:[{id,title,score}]}
GET  /api/contest?id=<cid>           → {board:{contest,rows,total,full,solved,elapsed}, now}
POST /api/contest/finish  {id}       → 同上传 board
POST /api/reset                      → {ok:true}   // 清空全部记录
```

## 题目 JSON（`problems/<file>.json`，一题一文件）

```json
{
  "id": "p01_year_string",
  "order": 1,
  "title": "年号字串",
  "type": "fill",                     // fill=结果填空 / prog=编程题
  "difficulty": "入门",               // 入门 | 提高 | 较难
  "score": 10,
  "tags": ["进制", "字符串"],
  "chapter": "第 13 章 01 / 第 9 章",
  "source": "蓝桥杯省赛真题（题意整理）",
  "statement": "<p>题干 HTML，可用 <code>...</code> <pre>...</pre> <ul><li>，禁止 script/style 属性</p>",
  "input_format": "一行一个整数 n（1 ≤ n ≤ 100000）",
  "output_format": "输出对应字母串",
  "examples": [{"input": "2026", "output": "BYX"}],
  "limits": {"time_ms": 2000},
  "answer": "BYX",                    // 仅 fill
  "answer_hint": "注意 26 进制没有 0 这一位",   // 仅 fill，答错时提示
  "tests": [                          // 仅 prog
    {"name": "样例", "input": "2026\n", "expected": "BYX\n", "score": 10, "hidden": false},
    {"name": "测试点 2", "input": "52\n", "expected": "AZ\n", "score": 15, "hidden": true}
  ],
  "solution": {
    "idea": "<p>思路 HTML</p>",
    "code": "参考实现源码（真实运行过的）",
    "output": "参考实现的实际输出",
    "reference": "code/ch13-real-problems/01_year_string.py",
    "answer": "BYX"
  }
}
```

## 视觉要求（仿蓝桥杯官网风格）

- 顶部深蓝渐变导航条（`#1c4f9c → #2a6fc4`），左侧站名"蓝桥杯 Python 模拟训练平台"，右侧导航：首页 / 题库 / 我的提交 / 模拟赛，最右显示"已解 x/y"
- 内容区白底卡片 + 浅灰背景 `#f0f2f5`，正文宽上限 1180px
- 题库页：表格式列表（编号、标题、类型、难度、分值、考点、状态、操作），难度用色块徽章（入门绿 / 提高橙 / 较难红），状态显示"已解 / 尝试 n 次 / 未做"
- 题目页：左右分栏（左 58% 题干，右 42% 代码区），题干区含"题目描述 / 输入格式 / 输出格式 / 样例 / 数据范围"分节标题；代码区是深色 textarea，等宽字体，Tab 插入 4 空格，`Ctrl+Enter` 提交，下方显示判题结果卡
- 判题结果：大号状态字（AC 绿、WA 红、TLE 橙、RE/CE 紫），下面测试点表格（状态、用时、可见用例的输入/期望/实际）
- 移动端：分栏在窄屏改为上下堆叠
- 不出现"AI 生成"之类字样，不引用外部 CDN/字体
