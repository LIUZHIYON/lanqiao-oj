"""题库构建脚本：把 problems/ 下的 27 道题（15 道编程 + 12 道填空）写出来。

铁律：编程题每个测试点的 expected 一律来自真实运行 generator/reference/<pid>.py，
填空题的 answer 一律来自真实运行 generator/fill_scripts/<pid>.py。
本脚本里不手写任何答案，只手写输入数据。

用法：python generator/build_problems.py
"""
import importlib.util
import json
import os
import random
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_DIR = os.path.join(BASE, "generator", "reference")
FILL_DIR = os.path.join(BASE, "generator", "fill_scripts")
EXTRA_DIR = os.path.join(BASE, "generator", "extra")      # 追加题库放这里，一文件一批
OUT_DIR = os.path.join(BASE, "problems")
SEED = 20261007
TIME_MS = 2000
SLOW_MS = 1500          # 单个测试点超过这个数就提示（判题限制 2000 ms）

_EXTRA = None


def _extra():
    """加载 generator/extra/*.py。每个文件可选暴露 PROG_META / FILL_META / prog_cases()。
    单个文件报错只跳过它并警告，不会拖垮整个构建。"""
    global _EXTRA
    if _EXTRA is not None:
        return _EXTRA
    pm, fm, cs = [], [], {}
    want = only_filter()
    if os.path.isdir(EXTRA_DIR):
        for fn in sorted(os.listdir(EXTRA_DIR)):
            if not fn.endswith(".py") or fn.startswith("_"):
                continue
            path = os.path.join(EXTRA_DIR, fn)
            spec = importlib.util.spec_from_file_location("extra_" + fn[:-3], path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                m_pm = list(getattr(mod, "PROG_META", []))
                m_fm = list(getattr(mod, "FILL_META", []))
                m_cs = dict(mod.prog_cases()) if hasattr(mod, "prog_cases") else {}
            except Exception as e:
                print("  [跳过] extra/{} 加载失败：{}".format(fn, e))
                continue
            if want:
                keep = [x["pid"] for x in m_pm] + [x["pid"] for x in m_fm]
                if not any(only_match(p, want) for p in keep):
                    continue
            pm += m_pm
            fm += m_fm
            cs.update(m_cs)
    _EXTRA = (pm, fm, cs)
    return _EXTRA


def only_filter():
    """命令行 --only p28 p48_xxx ... 或环境变量 OJ_ONLY='p28,p48'，用于只构建某一批题。
    支持只写短编号（p28 会匹配 p28_arithmetic_bundle），避免传错时静默构建 0 题。"""
    vals = []
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        for a in sys.argv[i + 1:]:
            if a.startswith("--"):
                break
            vals += a.split(",")
    env = os.environ.get("OJ_ONLY", "").strip()
    if env:
        vals += env.split(",")
    vals = {v.strip() for v in vals if v.strip()}
    return vals or None


def only_match(pid, only):
    if not only:
        return True
    return any(pid == v or pid.startswith(v + "_") for v in only)


def all_prog_meta():
    return PROG_META + _extra()[0]


def all_fill_meta():
    return FILL_META + _extra()[1]

RUN_ENV = {
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
    "PATH": os.environ.get("PATH", ""),
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUTF8": "1",
    "PYTHONDONTWRITEBYTECODE": "1",
}


# ---------------------------------------------------------------- 跑脚本
def run_ref(script, stdin_text, timeout=120):
    """真实运行参考解，返回（标准输出全文，用时毫秒）。"""
    t0 = time.perf_counter()
    p = subprocess.run([sys.executable, script], cwd=REF_DIR,
                       input=stdin_text.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=timeout, env=RUN_ENV)
    ms = int((time.perf_counter() - t0) * 1000)
    if p.returncode != 0:
        raise RuntimeError(script + " 运行失败：\n" + p.stderr.decode("utf-8", "replace")[-1500:])
    return p.stdout.decode("utf-8"), ms


def run_fill(script, timeout=600):
    t0 = time.perf_counter()
    p = subprocess.run([sys.executable, script], cwd=FILL_DIR,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=timeout, env=RUN_ENV)
    ms = int((time.perf_counter() - t0) * 1000)
    if p.returncode != 0:
        raise RuntimeError(script + " 运行失败：\n" + p.stderr.decode("utf-8", "replace")[-1500:])
    return p.stdout.decode("utf-8").strip(), ms


# ---------------------------------------------------------------- 造输入
def rand_ints(rnd, n, lo, hi):
    return [rnd.randint(lo, hi) for _ in range(n)]


def rand_grid_text(rnd, n, m, wall_p, force_open=()):
    """n 行 m 列的 01 网格文本；force_open 位置的格子强制是通路。"""
    lines = []
    for i in range(n):
        line = ""
        for j in range(m):
            if (i, j) in force_open:
                line += "0"
            else:
                line += "1" if rnd.random() < wall_p else "0"
        lines.append(line)
    return "".join(ln + "\n" for ln in lines)


def open_grid_text(n, m):
    return ("0" * m + "\n") * n


def maze_text(rnd, n, m, wall_p, carve_path=True):
    """随机 01 网格。carve_path=True 时再沿一条只向右/向下走的路线把沿途清成通路，
    保证右下角一定能走到 —— 大随机点要考的是真的广度优先搜索，而不是一眼看出走不到。"""
    rows = [[1 if rnd.random() < wall_p else 0 for _ in range(m)] for _ in range(n)]
    i = j = 0
    rows[i][j] = 0
    while i < n - 1 or j < m - 1:
        if i == n - 1:
            j += 1
        elif j == m - 1:
            i += 1
        elif rnd.random() < 0.5:
            i += 1
        else:
            j += 1
        rows[i][j] = 0
    return "".join("".join(str(v) for v in r) + "\n" for r in rows)


# ---------------------------------------------------------------- 分值分配
def attach_scores(cases, total):
    """cases 是 [(测试点名字, 输入文本)]，第一条是可见样例，其余全是隐藏点。"""
    h = len(cases) - 1
    base = (total - 5) // h
    scores = [5] + [base] * h
    scores[-1] += (total - 5) - base * h
    return [{"name": name, "input": text, "expected": "", "score": sc, "hidden": idx > 0}
            for idx, ((name, text), sc) in enumerate(zip(cases, scores))]


# ---------------------------------------------------------------- 编程题输入表
def prog_cases():
    rnd = random.Random(SEED)
    cs = {}

    cs["p01_year_string"] = [
        ("样例 2026", "2026\n"),
        ("最小 n=1", "1\n"),
        ("一位字母的尽头 26", "26\n"),
        ("刚出现两个字母 27", "27\n"),
        ("两位含 Z", "52\n"),
        ("两位最大 702", "702\n"),
        ("随机中间值", "{}\n".format(rnd.randint(1000, 20000))),
        ("最大 n=100000", "100000\n"),
    ]

    cs["p02_time_display"] = [
        ("样例 5000000 毫秒", "5000000\n"),
        ("最小 0 毫秒", "0\n"),
        ("不足一秒", "999\n"),
        ("刚过一秒", "1000\n"),
        ("整点", "3600000\n"),
        ("分秒要补零", "43200000\n"),
        ("最大 86399999", "86399999\n"),
        ("随机", "{}\n".format(rnd.randint(0, 86399999))),
    ]

    cs["p03_practice_stats"] = [
        ("样例 a=10 b=20 n=100", "10 20 100\n"),
        ("最小 a b n", "1 1 1\n"),
        ("工作日和周末一样多", "10 10 100\n"),
        ("周末刷得多", "1 100 100\n"),
        ("刚好一周做完", "10 10 70\n"),
        ("差一题要跨周", "5 3 47\n"),
        ("随机中等", "{} {} {}\n".format(rnd.randint(1, 100), rnd.randint(1, 100),
                                        rnd.randint(1000, 10 ** 8))),
        ("最大 n=1e15", "100 1 1000000000000000\n"),
    ]

    n4 = 50000
    h4 = rand_ints(rnd, n4, 1, 10 ** 9)
    cs["p04_cut_trees"] = [
        ("样例 四棵树要 7 米", "4 7\n20 15 10 17\n"),
        ("最小 n=1", "1 1\n1000000000\n"),
        ("M=0 一点也不用砍", "3 0\n5 9 2\n"),
        ("刚好砍到 3", "3 9\n5 4 9\n"),
        ("全部等高", "5 10\n7 7 7 7 7\n"),
        ("凑不够 M 要输出 0", "3 30\n5 9 2\n"),
        ("只有一棵超高树", "8 7\n4 56 2 1 20 8 19 3\n"),
        ("大随机 n=50000", "{} {}\n".format(n4, sum(h4) // 3) +
         " ".join(map(str, h4)) + "\n"),
    ]

    r5 = random.Random(SEED + 5)
    cs["p05_maze_bfs"] = [
        ("样例 3x3 全通", "3 3\n000\n000\n000\n"),
        ("最小 1x1 原地不动", "1 1\n0\n"),
        ("起点是墙", "3 3\n100\n000\n000\n"),
        ("终点是墙", "3 3\n000\n000\n001\n"),
        ("中间一堵竖墙不可达", "3 3\n010\n010\n010\n"),
        ("要先往上绕再往下绕", "5 5\n00001\n11101\n10001\n10111\n10000\n"),
        ("沿走廊绕到右下角", "5 5\n00001\n11101\n11101\n11101\n00000\n"),
        ("讲义第 13 章 13 那张图", "6 6\n001000\n010010\n000101\n110001\n000110\n010000\n"),
        ("20x20 无障碍", "20 20\n" + open_grid_text(20, 20)),
        ("大随机 250x250 一定可达",
         "250 250\n" + maze_text(r5, 250, 250, 0.30)),
    ]

    cs["p06_concat_max"] = [
        ("样例 30 32 321", "3\n30 32 321\n"),
        ("最小 n=1", "1\n7\n"),
        ("全是 0", "3\n0 0 0\n"),
        ("前缀陷阱 12 与 121", "2\n12 121\n"),
        ("9 与 91", "2\n9 91\n"),
        ("有重复的串", "5\n3 3 34 5 9\n"),
        ("随机 60 个", "60\n" + " ".join(str(rnd.randint(0, 999)) for _ in range(60)) + "\n"),
        ("大随机 n=800", "800\n" + " ".join(str(rnd.randint(1, 99999)) for _ in range(800)) + "\n"),
    ]

    n7, w7 = 100, 10000
    items7 = [(rnd.randint(1, 200), rnd.randint(1, 500)) for _ in range(n7)]
    cs["p07_knapsack_01"] = [
        ("样例 3 件容量 5", "3 5\n2 3\n4 5\n3 6\n"),
        ("容量 W=0", "2 0\n1 5\n2 6\n"),
        ("一件都装不下", "3 1\n5 9\n7 8\n9 10\n"),
        ("最小 n=1 装得下", "1 10\n3 7\n"),
        ("刚好装满", "4 10\n2 3\n3 4\n5 8\n6 9\n"),
        ("随机 8 件", "8 50\n" + "".join(
            "{} {}\n".format(rnd.randint(1, 30), rnd.randint(1, 60)) for _ in range(8))),
        ("大随机 n=100 W=10000", "{} {}\n".format(n7, w7) +
         "".join("{} {}\n".format(w, v) for w, v in items7)),
    ]

    cs["p08_perfect_square"] = [
        ("样例 N=12", "12\n"),
        ("最小 N=1", "1\n"),
        ("本身就是平方数", "36\n"),
        ("N=2022", "2022\n"),
        ("含高次幂 512", "512\n"),
        ("三个不同质因子 4199", "4199\n"),
        ("随机 10 位数", "{}\n".format(rnd.randint(10 ** 9, 10 ** 10 - 1))),
        ("最大 N=1e12", "1000000000000\n"),
    ]

    cs["p09_divisors"] = [
        ("样例 n=36", "36\n"),
        ("最小 n=2", "2\n"),
        ("质数 1000003", "1000003\n"),
        ("平方数 100", "100\n"),
        ("2 的 20 次方", "1048576\n"),
        ("随机 9 位数", "{}\n".format(rnd.randint(10 ** 8, 10 ** 9))),
        ("最大 n=1e12", "1000000000000\n"),
    ]

    cs["p10_bracket_fix"] = [
        ("样例 (）(()", "())(()\n"),
        ("已经合法", "()\n"),
        ("最小长度 只有一个左括号", "(\n"),
        ("最小长度 只有一个右括号", ")\n"),
        ("顺序颠倒", ")(\n"),
        ("十个左括号", "((((((((((\n"),
        ("最大长度 1000 个左括号", "(" * 1000 + "\n"),
        ("随机长串 2000", "".join(rnd.choice("()") for _ in range(2000)) + "\n"),
    ]

    n11 = 60000
    a11 = rand_ints(rnd, n11, -10 ** 6, 10 ** 6)
    cs["p11_max_subarray"] = [
        ("样例 8 个数", "8\n1 -2 3 -1 2 -3 4 -5\n"),
        ("最小 n=1 且是负数", "1\n-9\n"),
        ("全是负数", "5\n-7 -2 -9 -4 -6\n"),
        ("含 0 的全负", "4\n0 -3 -1 -2\n"),
        ("全是正数", "5\n1 2 3 4 5\n"),
        ("两头大中间小", "6\n5 -1 -1 -1 5 -10\n"),
        ("大随机 n=60000", "{}\n".format(n11) + " ".join(map(str, a11)) + "\n"),
    ]

    cs["p12_primes"] = [
        ("样例 n=10", "10\n"),
        ("最小 n=1", "1\n"),
        ("n=2", "2\n"),
        ("n 自己是素数", "5\n"),
        ("小质数 13", "13\n"),
        ("随机中等", "{}\n".format(rnd.randint(1000, 50000))),
        ("最大 n=100000", "100000\n"),
    ]

    cs["p13_combination"] = [
        ("样例 C(5,2)", "5 2\n"),
        ("最小 0 0", "0 0\n"),
        ("k=0", "10 0\n"),
        ("k=n", "10 10\n"),
        ("k 比 n 大要输出 0", "7 9\n"),
        ("利用对称性", "30 28\n"),
        ("随机中等", "{} {}\n".format(rnd.randint(100, 600), rnd.randint(1, 99))),
        ("最大 n=2000", "2000 1000\n"),
    ]

    r14 = random.Random(SEED + 14)
    cs["p14_grid_paths"] = [
        ("样例 中间一堵墙", "3 3\n000\n010\n000\n"),
        ("最小 1x1", "1 1\n0\n"),
        ("起点是墙", "3 3\n100\n000\n000\n"),
        ("终点是墙", "2 2\n00\n01\n"),
        ("一整行墙隔断", "4 4\n0000\n1111\n0000\n0000\n"),
        ("无障碍 10x10", "10 10\n" + open_grid_text(10, 10)),
        ("无障碍 20x20", "20 20\n" + open_grid_text(20, 20)),
        ("大随机 40x40", "40 40\n" + rand_grid_text(r14, 40, 40, 0.2,
                                                   force_open={(0, 0), (39, 39)})),
    ]

    k15 = 50000
    p15 = rand_ints(rnd, k15, 0, 10 ** 9)
    cs["p15_nim"] = [
        ("样例 3 4 5", "3\n3 4 5\n"),
        ("最小 k=1 有石子", "1\n7\n"),
        ("一堆且是空堆", "1\n0\n"),
        ("全是空堆", "4\n0 0 0 0\n"),
        ("两堆相同必败", "2\n12 12\n"),
        ("三堆异或为 0", "3\n1 2 3\n"),
        ("随机 9 堆", "9\n" + " ".join(str(rnd.randint(0, 100)) for _ in range(9)) + "\n"),
        ("大随机 k=50000", "{}\n".format(k15) + " ".join(map(str, p15)) + "\n"),
    ]
    cs.update(_extra()[2])
    return cs


# ---------------------------------------------------------------- 编程题文案
PROG_META = [
    dict(pid="p01_year_string", title="年号字串", difficulty="入门", tags=["进制", "字符串"],
         chapter="第 13 章 01 / 第 9 章 进制", source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/01_year_string.py",
         input_format="一行一个正整数 n（1 ≤ n ≤ 100000）。",
         output_format="一行，对应的字母串，全部大写，中间不空格。",
         statement="<p>比赛用字母给年份编号，规则和表格的列名完全一样："
                   "<code>1=A，2=B，……，25=Y，26=Z，27=AA，28=AB</code>，一直往后排。</p>"
                   "<p>给你一个编号 <code>n</code>，输出它对应的字母串。</p>"
                   "<p>先想清楚它和普通进制差在哪：普通 26 进制每位是 0~25，"
                   "而这里每位是 1~26（A 到 Z），<strong>根本没有 0 这一位</strong>。"
                   "所以每次取余之前要先减 1。</p>",
         idea="<p>把 n 当成 Excel 列名处理：每次 <code>n -= 1</code> 把 1~26 压回 0~25，"
              "取余得到最右边那个字母，再 <code>n //= 26</code> 走到左边一位。</p>"
              "<p>稳妥做法：再写一个反解函数（字母串换回数字），把 1、26、27、52、702 "
              "这几个关键点双向对一遍再交。</p>"),

    dict(pid="p02_time_display", title="时间显示", difficulty="入门", tags=["整除取余", "格式化输出"],
         chapter="第 13 章 08 / 第 1 章 基础语法", source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/08_time_display.py",
         input_format="一行一个整数 t，表示毫秒数（0 ≤ t ≤ 86399999，保证不足一整天）。",
         output_format="一行，格式为 H:MM:SS。小时不补零，分钟和秒都要补足两位。",
         statement="<p>一段程序跑了 <code>t</code> 毫秒，把它显示成 <code>时:分:秒</code> 的样子。</p>"
                   "<p>格式规定：小时该是几就写几，不补零；分钟和秒必须补零到两位，"
                   "比如 1 点 2 分 3 秒要写成 <code>1:02:03</code>。</p>"
                   "<p>这道题没有算法，考的就是整除 <code>//</code> 和取余 <code>%</code> 的先后顺序，"
                   "以及输出格式。毫秒先换成整秒，不满一秒的部分直接丢掉。</p>",
         idea="<p><code>总秒数 = t // 1000</code>；小时 <code>= 总秒数 // 3600</code>，"
              "分钟 <code>= 总秒数 % 3600 // 60</code>，秒 <code>= 总秒数 % 60</code>。</p>"
              "<p>输出用 f-string：<code>f&#34;{h}:{m:02d}:{s:02d}&#34;</code>，"
              "<code>02d</code> 表示不足两位就补零。写完拿 0、999、3600000、86399999 "
              "四个边界各跑一遍。</p>"),

    dict(pid="p03_practice_stats", title="刷题统计", difficulty="入门", tags=["模拟", "周期跳步"],
         chapter="第 13 章 04 / 第 5 章 枚举与模拟", source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/04_practice_stats.py",
         input_format="一行三个整数 a、b、n（1 ≤ a, b ≤ 100，1 ≤ n ≤ 10^15）。",
         output_format="一行一个整数，是第几天。",
         statement="<p>小蓝从周一开始刷题：周一到周五每天做 <code>a</code> 道，周六周日每天做 "
                   "<code>b</code> 道。给定 <code>n</code>，问第几天累计做题数第一次达到或超过 n。</p>"
                   "<p>一天一天加最直观，但 n 最大到 10^15，慢慢循环一定跑不完。"
                   "注意 7 天是一个循环：一整周固定做 <code>5a + 2b</code> 道，"
                   "先把整周成批跳过去，剩下的再逐天补。</p>",
         idea="<p>先算 <code>full = n // (5a + 2b)</code>，直接跳 full 周（此时已做 "
              "<code>full * (5a+2b)</code> 道，一定还没超过 n），再用 while 一天一天补。</p>"
              "<p>判断星期几用 <code>(day - 1) % 7 &lt; 5</code>。"
              "把 n 刚好等于一整周题数的情况单独跑一次，最容易看出有没有多算一天。</p>"),

    dict(pid="p04_cut_trees", title="砍树", difficulty="提高", tags=["二分答案", "贪心"],
         chapter="第 13 章 05 / 第 8 章 二分", source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/05_binary_answer.py",
         input_format="第一行两个整数 n 和 M（1 ≤ n ≤ 50000，0 ≤ M ≤ 10^14）；"
                      "第二行 n 个整数是每棵树的高度（1 ≤ 高度 ≤ 10^9）。",
         output_format="一行一个整数，是锯木高度的最大值。怎么锯都凑不够 M 米时输出 0。",
         statement="<p>山里有 <code>n</code> 棵树，园林局要运走至少 <code>M</code> 米木材。</p>"
                   "<p>统一把锯片设在高度 <code>H</code>：每棵高出 H 的部分被锯下来，"
                   "矮于 H 的那棵一根也不掉。问 H 最高能设多高。</p>"
                   "<p>锯得越高，砍下来的木材越少，所以可行性是有单调性的：能凑够 M 的高度排在前面，"
                   "凑不够的排在后面 —— 这正是<strong>二分答案</strong>的形状。"
                   "不要枚举每棵树的高度，那是 O(n × 最大高度)，太慢。</p>",
         idea="<p>写 <code>check(H)</code>：一次遍历累加 <code>max(0, 高度 - H)</code>，看是否 ≥ M，"
              "复杂度 O(n)。然后对答案 H 二分。</p>"
              "<p>模板用 <code>mid = (lo + hi + 1) // 2</code> 配 <code>lo = mid</code>，"
              "少写那个 +1 就会原地打转死循环。两个边界要单独想：M = 0 时答案是最高那棵树的高度；"
              "全部树加一起都不够 M 时要输出 0。</p>"),

    dict(pid="p05_maze_bfs", title="迷宫最短路", difficulty="提高", tags=["BFS", "网格", "图论"],
         chapter="第 13 章 13 / 第 6 章 搜索", source="蓝桥杯省赛真题（改编：走不到输出 -1）",
         reference="code/ch13-real-problems/13_maze.py",
         input_format="第一行两个整数 n 和 m（1 ≤ n, m ≤ 250）；接下来 n 行，"
                      "每行 m 个字符，只有 0（通路）和 1（墙），中间没有空格。",
         output_format="一行一个整数，是最少步数；右下角走不到时输出 -1。",
         statement="<p>一张 <code>n</code> 行 <code>m</code> 列的地图，<code>0</code> 是路、"
                   "<code>1</code> 是墙。人站在左上角，要走到右下角，"
                   "每步只能上、下、左、右挪一格，不能穿墙。</p>"
                   "<p>问最少走几步（起点就算第 0 步），走不到输出 <code>-1</code>。</p>"
                   "<p>求最少就要一层一层往外扩：BFS 第一次踩到终点时，层数就是最短距离，"
                   "因为比它近的格子一定已经先被访问过了。</p>",
         idea="<p><code>dist</code> 全部初始化成 -1，起点置 0，用 <code>deque</code> 的 "
              "<code>popleft</code> 出队（写成 <code>pop</code> 就变成深度优先，得到的不是最短）。</p>"
              "<p>三个常见坑：起点或终点是墙要直接判 -1；越界判断写成 <code>0 &lt;= nx &lt; n</code>；"
              "入队时就标记距离，别等出队才标记，否则同一格子会排队好几次，大数据直接超时。</p>"),

    dict(pid="p06_concat_max", title="拼数", difficulty="提高", tags=["排序", "自定义比较"],
         chapter="第 13 章 07 / 第 8 章 排序与贪心", source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch13-real-problems/07_concat_max.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 800）；第二行 n 个数字串，用空格隔开"
                      "（每个串长 1~5，只由数字组成）。",
         output_format="一行，拼出的最大数。原样输出，不去掉前导 0。",
         statement="<p>给你 <code>n</code> 个数字串，把它们首尾相接排成一排，拼出一个尽量大的数。</p>"
                   "<p>比如 <code>30 32 321</code>，排成 32、321、30 得到 <code>3232130</code>，"
                   "这就是最大的。</p>"
                   "<p>按字典序从大到小排是<strong>错的</strong>：那样会把 321 排在 32 前面，"
                   "得到 32132，比 32321 小。正确的比较方法是把两个串分别接到对方头上，"
                   "比较 <code>a+b</code> 和 <code>b+a</code> 哪个大。</p>",
         idea="<p>比较规则：<code>a+b &gt; b+a</code> 就让 a 排前面。Python 里用 "
              "<code>functools.cmp_to_key</code> 把比较函数变成 sort 能用的 key。</p>"
              "<p>验证：串数不超过 7 个时用 <code>itertools.permutations</code> 全排列取最大，"
              "和贪心结果逐条对比，一致才敢交。全 0 的输入要按原样输出，不要自作主张去掉。</p>"),

    dict(pid="p07_knapsack_01", title="0-1 背包", difficulty="提高", tags=["动态规划", "背包"],
         chapter="第 7 章 08、09（0-1 背包）", source="蓝桥杯常考题型（题意整理）",
         reference="code/ch07-dp/09_knapsack_1d.py",
         input_format="第一行两个整数 n 和 W（1 ≤ n ≤ 100，0 ≤ W ≤ 10000）；"
                      "接下来 n 行每行两个整数，是这件物品的重量和价值（都介于 1 到 1000）。",
         output_format="一行一个整数，是总重量不超过 W 时能装下的最大价值。",
         statement="<p>背包容量 <code>W</code>，桌上有 <code>n</code> 件物品，每件有重量和价值，"
                   "<strong>每件要么整件拿走，要么不要</strong>。问最多能装多少价值。</p>"
                   "<p>这就是 0-1 背包。状态：<code>dp[c]</code> = 容量为 c 时能拿到的最大价值，"
                   "一件一件物品考虑：装上它会不会更值。</p>",
         idea="<p>一维滚动数组，内层容量必须<strong>从大到小</strong>遍历："
              "<code>for c in range(W, w-1, -1): dp[c] = max(dp[c], dp[c-w] + v)</code>。"
              "从小到大的话，同一件物品会被重复计算，那就变成完全背包了。</p>"
              "<p>重量超过 W 的物品直接跳过；W = 0 时答案是 0，这是最容易漏的边界。</p>"),

    dict(pid="p08_perfect_square", title="完全平方数", difficulty="提高", tags=["质因数分解", "数论"],
         chapter="第 9 章 18 / 第 5 章 13、第 13 章 14",
         source="蓝桥杯省赛真题（题意整理）",
         reference="code/ch09-number-theory/18_real_perfect_square.py",
         input_format="一行一个正整数 N（1 ≤ N ≤ 10^12）。",
         output_format="一行一个正整数 x，是使 N*x 成为完全平方数的最小正整数。",
         statement="<p>给一个正整数 <code>N</code>，找一个最小的正整数 <code>x</code>，"
                   "让 <code>N * x</code> 刚好是完全平方数。</p>"
                   "<p>比如 N = 12：12 × 3 = 36 = 6 的平方，所以 x = 3。</p>"
                   "<p>完全平方数的每个质因子指数都是偶数。把 N 分解质因数，"
                   "指数是奇数的那些质因子各差一个才能配对，把它们乘起来就是答案。"
                   "别从 1 开始一个一个试 x，N 大到 10^12 时试不出来。</p>",
         idea="<p>试除分解：先除干净 2，再从 3 开始只试奇数，直到 <code>d * d &gt; n</code>，"
              "剩下的 n 若大于 1 就是一个质因子。答案 = 所有指数为奇数的质因子之积。</p>"
              "<p>验证用 <code>math.isqrt</code>：算出 r 后判断 <code>r*r == N*x</code>。"
              "千万别用 <code>int((N*x) ** 0.5)</code>，浮点数只有 53 位有效二进制位，"
              "大数上会开错。</p>"),

    dict(pid="p09_divisors", title="约数个数与最大真约数", difficulty="提高",
         tags=["质因数分解", "约数"], chapter="第 9 章 06、04（约数与分解）",
         source="蓝桥杯常考题型（题意整理）",
         reference="code/ch09-number-theory/06_divisors.py",
         input_format="一行一个整数 n（2 ≤ n ≤ 10^12）。",
         output_format="一行两个整数，用空格隔开：n 的约数个数、n 的最大真约数。",
         statement="<p>给一个整数 <code>n</code>，输出两个数：n 的约数个数，以及 n 的最大真约数。</p>"
                   "<p>真约数指的是除开 n 自己以外的约数。比如 12 的约数是 1、2、3、4、6、12，"
                   "一共 6 个，最大真约数是 6，所以这一行输出 <code>6 6</code>。</p>"
                   "<p>从 1 一直试到 n 太慢。用质因数分解：若 "
                   "<code>n = p1^e1 * p2^e2 * ...</code>，约数个数就是 "
                   "<code>(e1+1) * (e2+1) * ...</code>；最大真约数等于 n 除以 n 的最小质因子。</p>",
         idea="<p>先分解质因数，按公式 <code>∏(e+1)</code> 数约数，最大真约数用 "
              "<code>n // 最小质因子</code>。</p>"
              "<p>小数据要用成对枚举核对一遍：<code>for i in range(1, isqrt(n)+1)</code>，"
              "遇到约数就把 i 和 n//i 都记上。完全平方数中间那一格只能算一次，"
              "这是最常见的失分点。</p>"),

    dict(pid="p10_bracket_fix", title="括号补全", difficulty="提高", tags=["贪心", "栈", "字符串"],
         chapter="第 13 章 10 / 第 11 章 30、38", source="蓝桥杯常考题型（题意整理）",
         reference="code/ch13-real-problems/10_brackets.py",
         input_format="一行一个只由 ( 和 ) 组成的字符串，长度 1 到 2000。",
         output_format="一行一个整数，是最少需要插入的括号个数。",
         statement="<p>一串括号，可能配不成对。你可以在任意位置插入 <code>(</code> 或 <code>)</code>，"
                   "问最少插几个能让它变成合法的括号序列。</p>"
                   "<p>合法的意思是：左右数量相等，而且从左往右读时，任何位置上已读到的左括号"
                   "都不少于右括号。<code>()()</code> 和 <code>(())</code> 合法，"
                   "<code>)(</code> 不合法。</p>"
                   "<p>例如 <code>())(()</code>：中间多出一个右括号、末尾少一个右括号，"
                   "最少插 2 个。</p>",
         idea="<p>从左到右扫一遍，用一个计数器攒着还没配对的左括号：遇到 <code>(</code> 加一；"
              "遇到 <code>)</code> 时若有攒着的就抵消一个，没有就说明这里缺一个左括号，记一次插入。"
              "扫完后，还攒着的左括号每个要补一个右括号。</p>"
              "<p>答案 = 补的左括号数 + 收尾时没配对的左括号数。"
              "拿十个连续左括号这种极端串跑一遍，看是不是 10。</p>"),

    dict(pid="p11_max_subarray", title="最大子段和", difficulty="提高",
         tags=["动态规划", "贪心"], chapter="第 7 章 04（最大子段和）",
         source="经典蓝桥题型（题意整理）",
         reference="code/ch07-dp/04_max_subarray.py",
         input_format="第一行一个整数 n（1 ≤ n ≤ 60000）；"
                      "第二行 n 个整数，用空格隔开（每个数的绝对值不超过 10^6）。",
         output_format="一行一个整数，是最大子段和。",
         statement="<p>一列数，有正有负。从中选出<strong>连续的一段</strong>，"
                   "至少也要含一个数，让这一段的和最大，输出这个和。</p>"
                   "<p>例如 <code>1 -2 3 -1 2 -3 4 -5</code>，"
                   "选 <code>3 -1 2 -3 4</code> 这段，和是 5，没有更大的了。</p>"
                   "<p>如果整列都是负数，就只能选其中最大的那一个，不能输出 0 —— "
                   "题目要求至少选一个数。</p>",
         idea="<p>Kadane：设 <code>cur</code> 为以当前数结尾的最大子段和，"
              "<code>cur = max(x, cur + x)</code>，要么接着前面要么另起炉灶，"
              "全程记最大值 <code>ans</code>，O(n) 一次过。</p>"
              "<p>初始化用 <code>cur = ans = 第一个数</code>，别把 ans 设成 0，"
              "否则全负数那个测试点必错。</p>"),

    dict(pid="p12_primes", title="素数", difficulty="提高", tags=["筛法", "数论"],
         chapter="第 9 章 03、05（素数与筛法）", source="蓝桥杯常考题型（题意整理）",
         reference="code/ch09-number-theory/05_sieve.py",
         input_format="一行一个正整数 n（1 ≤ n ≤ 100000）。",
         output_format="一行两个整数，用空格隔开：第 n 个素数、n 以内（含 n）的素数个数。",
         statement="<p>把素数从小到大排：<code>2, 3, 5, 7, 11, ...</code>。"
                   "给定 n，输出两个数：</p>"
                   "<ul><li>第 n 个素数是多少；</li>"
                   "<li>n 以内（包括 n 自己）一共有多少个素数。</li></ul>"
                   "<p>比如 n = 10：第 10 个素数是 29，10 以内的素数是 2、3、5、7 共 4 个，"
                   "输出 <code>29 4</code>。</p>"
                   "<p>两个问题都依赖素数表，所以先把筛法跑一遍：埃氏筛就是拿每个素数去划掉它的倍数，"
                   "剩下的全是素数，一次筛几百万都没问题。</p>",
         idea="<p>先估一个够大的上界（第 6 个之后 <code>p_k &lt; k(ln k + ln ln k)</code>）筛一次，"
              "表里不够 n 个就把上界翻倍重来，这样第 n 个素数一定在表里。</p>"
              "<p>n 以内有多少个素数，直接在表上数 <code>p &lt;= n</code>，不用另开一次筛。"
              "n = 1 时答案是 <code>2 0</code> —— 1 以内一个素数都没有，这个 0 很容易漏。</p>"),

    dict(pid="p13_combination", title="组合计数", difficulty="提高", tags=["组合数", "大整数"],
         chapter="第 12 章 01、02（排列组合）", source="蓝桥杯常考题型（题意整理）",
         reference="code/ch12-math-date/01_perm_comb.py",
         input_format="一行两个整数 n 和 k（0 ≤ n ≤ 2000，0 ≤ k ≤ 2000）。",
         output_format="一行一个整数，是 C(n, k) 的精确值，不要取模，完整写出来。",
         statement="<p>从 <code>n</code> 个不同的东西里挑 <code>k</code> 个，不管顺序，"
                   "一共有多少种挑法？这就是组合数 <code>C(n, k)</code>。</p>"
                   "<p>规定 <code>k &lt; 0</code> 或 <code>k &gt; n</code> 时答案是 0（根本挑不出来），"
                   "<code>C(n, 0) = C(n, n) = 1</code>。</p>"
                   "<p>要输出精确值。C(2000, 1000) 是一个 601 位的数字，"
                   "换成 C++ 早就溢出了，Python 的大整数直接算就行 —— 这就是选 Python 的理由之一。</p>",
         idea="<p>直接用 <code>math.comb(n, k)</code>；想写递推就是杨辉三角 "
              "<code>C(n,k) = C(n-1,k-1) + C(n-1,k)</code>，"
              "先把 k 换成 min(k, n-k) 更省时间。</p>"
              "<p>坑：Python 3.11 起，把超过 4300 位的整数变成字符串会直接报错。"
              "如果哪天题目把 n 放到上万，程序开头要加一行 "
              "<code>import sys; sys.set_int_max_str_digits(0)</code>。</p>"),

    dict(pid="p14_grid_paths", title="网格路径数", difficulty="提高",
         tags=["动态规划", "网格", "大整数"], chapter="第 13 章 09 / 第 7 章 15、23",
         source="蓝桥杯常考题型（题意整理）",
         reference="code/ch13-real-problems/09_paths.py",
         input_format="第一行两个整数 n 和 m（1 ≤ n, m ≤ 40）；接下来 n 行，每行 m 个字符，"
                      "0 是空格、1 是墙，中间没有空格。",
         output_format="一行一个整数，是走法总数（精确值，不取模）。",
         statement="<p>一张 <code>n</code> 行 <code>m</code> 列的方格，左上角是起点、右下角是终点。"
                   "每步只能<strong>向右</strong>或<strong>向下</strong>走一格，墙（字符 1）不能进。</p>"
                   "<p>问一共有多少条不同走法。起点或终点本身就是墙时答案算 0。</p>"
                   "<p>没有墙时答案正好是组合数 <code>C(n+m-2, n-1)</code>，"
                   "可以拿它来检验你的递推写对没有。数字会很大，Python 不会溢出，直接输出。</p>",
         idea="<p><code>dp[i][j] = dp[i-1][j] + dp[i][j-1]</code>，墙的位置保持 0，"
              "起点 <code>dp[0][0] = 1</code>。</p>"
              "<p>先在 3x3 这种小格子上手算一遍和程序对；再把无障碍的情况和 "
              "<code>math.comb(n+m-2, n-1)</code> 对一次，两边都一致才算写对。</p>"),

    dict(pid="p15_nim", title="Nim 取石子", difficulty="较难", tags=["博弈", "异或"],
         chapter="第 13 章 12 / 第 12 章 20", source="蓝桥杯常考题型（题意整理）",
         reference="code/ch13-real-problems/12_game.py",
         input_format="第一行一个整数 k（1 ≤ k ≤ 50000），是堆数；"
                      "第二行 k 个整数是每堆的石子数（0 ≤ 每堆 ≤ 10^9）。",
         output_format="一行一个整数：先手必胜输出 1，先手必败输出 0。",
         statement="<p>桌上有 <code>k</code> 堆石子，两人轮流拿。每次只能选一堆，"
                   "从这一堆里至少拿走一个，全拿走也行。谁把最后一颗石子拿走谁赢。</p>"
                   "<p>两人都绝顶聪明，给定每堆数量，问先手是不是必胜：是就输出 1，不是就输出 0。</p>"
                   "<p>这题不用模拟过程。把每堆数量做<strong>按位异或</strong>（Python 里的 "
                   "<code>^</code>）：结果是 0 说明当前是必败局面，先手输；不是 0 就先手赢。"
                   "所有堆都是 0 时异或和也是 0，输出 0。</p>",
         idea="<p>把所有堆异或起来，非 0 则先手胜。道理是：异或为 0 时无论怎么拿都会变成非 0，"
              "而异或非 0 时总能一步把它拿回 0，所以被逼到 0 局面的人会先拿光最后一颗。</p>"
              "<p>不敢信结论就写个暴力验证：堆数不超过 3、每堆不超过 6 时，"
              "用 <code>lru_cache</code> 递归算 SG 值（或者直接判断谁能赢），"
              "和异或结论逐一对比，全部一致再交。</p>"),
]


# ---------------------------------------------------------------- 填空题文案
FILL_META = [
    dict(pid="p16_cards", title="数字卡片", difficulty="提高", tags=["枚举", "数位统计"],
         chapter="第 13 章 02 / 第 5 章 枚举", source="蓝桥杯省赛真题（题意整理）",
         script="p16_cards.py", reference="code/ch13-real-problems/02_cards.py",
         answer_hint="问的是能完整写到哪个数，不是哪种数字先用完；数字 0 要到 10 才被用到，别从 1 起算。",
         statement="<p>小蓝有 0 到 9 每种数字卡片各 <strong>2021 张</strong>。</p>"
                   "<p>他从 1 开始把正整数一个个写出来：1、2、3、4……"
                   "每写一个数就要用掉对应数字的卡片（写 100 用掉一张 1 和两张 0）。"
                   "某一种卡片用完就写不下去了。</p>"
                   "<p>问最多能<strong>完整地</strong>写到哪个数，把这个数填进来。</p>"
                   "<p>这种题手算必错，写个几行的循环边写边统计、一超限就停，程序比手指快得多。</p>",
         idea="<p>做法 A：一个一个数往上加，用长度 10 的列表统计每个数字用掉几张，"
              "一旦超过 2021 就输出上一个数。</p>"
              "<p>做法 B：写出算 1~n 中数字 d 出现多少次的数位函数，再对 n 二分。</p>"
              "<p>两种做法给出同一个数才敢填，顺便把写到该数时各数字的用量打印出来看一眼。</p>"),

    dict(pid="p17_snake", title="蛇形填数", difficulty="入门", tags=["找规律", "模拟"],
         chapter="第 13 章 03 / 第 5 章 枚举", source="蓝桥杯省赛真题（题意整理）",
         script="p17_snake.py", reference="code/ch13-real-problems/03_snake_grid.py",
         answer_hint="先确认规则：本题是同一条斜线上从最上面那行开始往下填，不是来回交替的之字形。",
         statement="<p>把 1、2、3、…… 沿斜线填进一张很大的方格表：行号加列号相同的格子算同一条斜线，"
                   "每条斜线上从最上面那一行开始往下填。</p>"
                   "<pre>行1:  1  2  4  7 11\n行2:  3  5  8 12\n行3:  6  9 13\n行4: 10 14\n行5: 15</pre>"
                   "<p>问第 20 行第 20 列那个格子里的数是多少。</p>",
         idea="<p>先按规则真的模拟填一遍（用字典记 (行,列) 到数值），再推公式："
              "设 s = 行 + 列，前面 s-2 条斜线一共有 <code>(s-2)(s-1)/2</code> 个数，"
              "本条斜线上它排第行个，所以值 = <code>(s-2)*(s-1)//2 + 行</code>。</p>"
              "<p>把 20x20 范围内每一格的模拟值和公式值逐格比对，全一致才填。</p>"),

    dict(pid="p18_goods", title="货物摆放", difficulty="较难", tags=["质因数分解", "计数"],
         chapter="第 13 章 06 / 首页必做清单第 43 题", source="蓝桥杯省赛真题（题意整理）",
         script="p18_goods.py", reference="code/ch13-real-problems/06_goods.py",
         answer_hint="这里数的是有序三元组，(2,3,5) 和 (3,2,5) 算两种；如果题目改成 a≤b≤c 结果会小很多。",
         statement="<p>仓库里有 <code>2022082731456292</code> 件货物，要正好码成一个长方体，"
                   "三条边的长度分别是 a、b、c 件，也就是 <code>a * b * c = 2022082731456292</code>。</p>"
                   "<p>问满足等式的<strong>有序</strong>三元组 (a, b, c) 有多少种。"
                   "a、b、c 都是正整数，顺序不同算不同方案。</p>"
                   "<p>这个数有 16 位，三重循环枚举到毕业也跑不完。正确思路是先分解质因数。</p>",
         idea="<p>分解得到 <code>2022082731456292 = 2^2 * 47917 * 10549923469</code>，"
              "指数分布是 2、1、1。把某个质因子的 e 次幂分给 a、b、c 三个数（可以分到 0 个）"
              "是可重复组合，方案数 <code>C(e+2, 2)</code>；不同质因子之间相互独立，全部乘起来："
              "<code>C(4,2)*C(3,2)*C(3,2) = 6*3*3</code>。</p>"
              "<p>再用另一种算法核对：枚举 L 的每个约数 a，统计 b*c = L/a 的有序对数（就是 L/a 的约数个数）"
              "并求和。约数要用质因数组合出来，不要从 1 试到 L。</p>"),

    dict(pid="p19_fraction", title="既约分数", difficulty="提高", tags=["最大公约数", "计数"],
         chapter="第 5 章 14 / 第 9 章 19、首页必做清单第 16 题",
         source="蓝桥杯省赛真题（题意整理）",
         script="p19_fraction.py", reference="code/ch05-brute-force/14_reduced_fractions.py",
         answer_hint="1/1 这种分子分母相同的会被两半各数一次，用 2*Σφ 之后要减掉重复的那一次。",
         statement="<p>分子和分母都必须是 1 到 2022 之间的整数（含 2022），"
                   "真分数、假分数、整数都算。</p>"
                   "<p>分子和分母互质（最大公约数是 1）的分数叫既约分数。"
                   "比如 3/4 是；6/35 是；1/1 也是；而 2/4 不是，因为 2 和 4 有公约数 2。</p>"
                   "<p>问一共能组成多少个不同的既约分数（分子或分母不同就算不同的分数）。答案是一个几百万量级的数。</p>",
         idea="<p>固定分母 b，不超过 b 且与 b 互质的分子个数正好是欧拉函数 φ(b)。"
              "先把 a ≤ b 这半个三角形数完（每行 φ(b) 个），乘 2 得到全部，"
              "再减掉被数了两次的 1/1，所以答案是 <code>2 * Σφ(1..2022) - 1</code>。</p>"
              "<p>φ 用筛法一次算完。再写一个双重循环 gcd 的版本在 1~100 的小范围核对公式，"
              "确认没有多算也没有漏算。</p>"),

    dict(pid="p20_fact_digits", title="2022 阶乘的位数", difficulty="提高", tags=["阶乘", "大整数"],
         chapter="第 13 章 11 / 第 9 章 16、首页必做清单第 17 题",
         source="蓝桥杯省赛真题（题意整理）",
         script="p20_factorial_digits.py", reference="code/ch13-real-problems/11_factorial.py",
         answer_hint="位数 = 向下取整(log10) 再加 1，别写成四舍五入；Python 3.11 以后要把整数转字符串的位数上限关掉才能真算。",
         statement="<p>算式 <code>2022! = 1 × 2 × 3 × … × 2022</code>。</p>"
                   "<p>把这个乘出来的大整数写成十进制，一共有多少位十进制数字？</p>"
                   "<p>Python 的大整数不会溢出，可以真把 2022! 乘出来数长度；"
                   "但更该会的是用 log10 估：<code>位数 = floor(log10(N!)) + 1</code>。"
                   "两种办法必须给出同一个数。</p>",
         idea="<p><code>log10(2022!)</code> 就是 <code>lgamma(2023) / ln(10)</code>，"
              "或者把 <code>math.log10(i)</code> 从 2 一路加到 2022，向下取整再加 1。</p>"
              "<p>再用真算出来的 <code>len(str(math.factorial(2022)))</code> 核对。"
              "Python 3.11 起默认禁止把超过约 4300 位的整数变成字符串，"
              "所以程序开头要写 <code>import sys; sys.set_int_max_str_digits(0)</code>。</p>"),

    dict(pid="p21_fact_zeros", title="2022 阶乘末尾的 0", difficulty="入门", tags=["阶乘", "质因子"],
         chapter="第 13 章 11 / 第 9 章 16", source="蓝桥杯省赛真题（题意整理）",
         script="p21_factorial_zeros.py", reference="code/ch13-real-problems/11_factorial.py",
         answer_hint="只数质因子 5 就够（2 多得用不完）；25、125、625 这些含有多个 5 的要重复数。",
         statement="<p>还是 <code>2022!</code> 这个乘积，写成十进制以后，"
                   "<strong>末尾连着有多少个 0</strong>？</p>"
                   "<p>每个 0 都来自一对 <code>2 × 5</code>。乘积里因子 2 比因子 5 多得多，"
                   "所以只要数因子 5 出现了多少次。</p>"
                   "<p>真乘出来数尾巴也能得到答案，但公式只花几微秒，而且能说明道理。</p>",
         idea="<p><code>2022//5 + 2022//25 + 2022//125 + 2022//625</code>，"
              "也就是 404 + 80 + 16 + 3。25 里的两个 5 被数了两次，这正是想要的效果；"
              "写成循环是 <code>while n: n //= 5; s += n</code>。</p>"
              "<p>再用真乘出来的 2022! 数一遍结尾连续的 0 核对（记得先关掉位数限制）。</p>"),

    dict(pid="p22_grid_paths", title="20x20 网格路径数", difficulty="提高",
         tags=["动态规划", "组合数"], chapter="第 13 章 09 / 第 7 章 15",
         source="经典题型（题意整理）",
         script="p22_grid_paths.py", reference="code/ch13-real-problems/09_paths.py",
         answer_hint="20x20 的方格纸沿格线走要走满 40 段、其中 20 段向下，所以是 C(40,20)，不是 C(20,10)，也不是 C(38,19)。",
         statement="<p>一张 20 行 20 列的方格纸，一共有 21 条横线和 21 条竖线，"
                   "它们的交点（格点）排成 21x21 的点阵。</p>"
                   "<p><strong>沿着格线</strong>从最左上角那个格点走到最右下角那个格点，"
                   "每步只能沿格线向右或向下挪一小段（一个小方格的边长）。"
                   "横着必须走满 20 段、竖着也必须走满 20 段，一共 40 段。</p>"
                   "<p>问一共有多少种不同的走法。</p>"
                   "<p>答案是十二位数，直接填数字。写一遍递推，再套一遍组合公式，"
                   "两个对上才动手填。小心别和编程题里格子到格点的算法混了：这里是格点到格点，"
                   "所以是 C(40, 20)。</p>",
         idea="<p>递推 <code>dp[i][j] = dp[i-1][j] + dp[i][j-1]</code>，起点是 1，"
              "本质上就是把杨辉三角铺到二维。</p>"
              "<p>组合角度：一共走 40 步，选定哪 20 步向下就定死了整条路线，所以是 "
              "<code>C(40, 20)</code>。Python 大整数直接算，不会溢出。</p>"),

    dict(pid="p23_segments", title="七段码", difficulty="较难", tags=["并查集", "连通性", "枚举"],
         chapter="第 10 章 08（并查集与七段码）", source="蓝桥杯省赛真题（题意整理）",
         script="p23_segments.py", reference="code/ch10-graph/08_seven_segment_code.py",
         answer_hint="只点亮一个段也算连通；判连通时只能在两端都亮着的段之间连线，没亮的段不能当桥。",
         statement="<p>一个七段数码管有 a 到 g 七个段，位置是：</p>"
                   "<pre> aaa\nf   b\n ggg\ne   c\n ddd</pre>"
                   "<p>点亮其中若干个段就表示一个字符。要求亮着的段必须<strong>首尾相连</strong>"
                   "成一个整体（两个段有公共端点就算相连），散成两块就不算。"
                   "比如只亮 a 和 d 不行，因为它们挨不着。</p>"
                   "<p>问一共能点亮多少种合法的连通字符（至少要亮一个段，全灭不算）。</p>",
         idea="<p>先把公共端点关系写成边：<code>a-b, a-f, b-g, b-c, f-g, f-e, c-g, c-d, g-e, e-d</code>。</p>"
              "<p>非空子集一共 127 个，逐个枚举：只看两端都亮着的边，用并查集合并，"
              "最后检查是不是只剩一个集合；再从任意一段做广度优先搜索看能不能走遍整个子集。"
              "两种做法逐个一致才填。</p>"),

    dict(pid="p24_digit2", title="含数字 2 的数", difficulty="入门", tags=["数位统计", "枚举"],
         chapter="第 13 章 15 / 首页必做清单第 20 题",
         source="蓝桥杯常考填空题（题意整理）",
         script="p24_digit2_count.py", reference="code/ch13-real-problems/15_digit_stats.py",
         answer_hint="问的是多少个数，不是数字 2 出现多少次：222 这样的数只能算一个。",
         statement="<p>把 1 到 2026 这些整数依次写出来。</p>"
                   "<p>问其中<strong>含有数字 2</strong> 的数一共有多少个。"
                   "2 出现一次还是多次都只算一个数，比如 2、12、202、222 各算一个。</p>"
                   "<p>注意看清问法：这一题问几个数，下一题问出现几次，两个数不一样。</p>",
         idea="<p>最稳的做法就是写循环：用 <code>'2' in str(x)</code> 判断再计数，"
              "两千多个数一眨眼就跑完了。填空题就该这么干。</p>"
              "<p>再用整除取余一位一位判断核对一次；想练数位统计就反过来数每一位都不是 2 的数，"
              "用乘法原理算完再拿总数去减，三种办法一致才填。</p>"),

    dict(pid="p25_digit1", title="写了多少个数字 1", difficulty="入门", tags=["数位统计", "枚举"],
         chapter="第 13 章 15 / 首页必做清单第 20 题",
         source="蓝桥杯常考填空题（题意整理）",
         script="p25_digit1_count.py", reference="code/ch13-real-problems/15_digit_stats.py",
         answer_hint="111 要数 3 次；这题问出现次数，不是问有多少个数含 1，别和上一题搞混。",
         statement="<p>还是把 1 到 2026 依次写出来，数一数一共用掉了多少个数字 <code>1</code>。</p>"
                   "<p>写 1 用掉 1 个，写 11 用掉 2 个，写 111 用掉 3 个，写 2026 一个都不用。</p>",
         idea="<p>暴力法一行搞定：<code>sum(str(x).count('1') for x in range(1, 2027))</code>，"
              "一毫秒出结果。</p>"
              "<p>数位公式法：一位一位看，把数拆成高位、当前位、低位三段讨论"
              "（当前位大于 1、等于 1、小于 1 三种情况）再乘上每轮的跨度。"
              "两种办法一致才填。</p>"),

    dict(pid="p26_ugly", title="第 1500 个丑数", difficulty="提高", tags=["动态规划", "堆", "数论"],
         chapter="第 13 章 14 / 首页必做清单第 19 题", source="经典题型（题意整理）",
         script="p26_ugly.py", reference="code/ch13-real-problems/14_ugly.py",
         answer_hint="1 也算丑数、是第 1 个；三指针前进时要用三个并列的 if，写成 elif 会漏掉相等的情况。",
         statement="<p>丑数是<strong>只含质因子 2、3、5</strong> 的正整数，并且规定 1 也是丑数"
                   "（排在第 1 个）。</p>"
                   "<p>把丑数从小到大排：<code>1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, ...</code>。</p>"
                   "<p>问第 1500 个丑数是多少。</p>"
                   "<p>用堆不停弹出最小值、再放进它的 2 倍 3 倍 5 倍，很直观，但要处理重复；"
                   "三指针递推更快也更好写。</p>",
         idea="<p><code>dp[i] = min(dp[p2]*2, dp[p3]*3, dp[p5]*5)</code>，"
              "谁贡献了这个最小值谁的指针就前进一格，三个判断都要写（用 elif 会漏重复值，"
              "序列里就会出现重复或漏数）。第 1500 个不到 1 毫秒。</p>"
              "<p>再用小根堆算一遍核对，并把答案做一次验证：连续除以 2、3、5，最后剩 1 才真是丑数。</p>"),

    dict(pid="p27_bracket_fill", title="长度 16 的合法括号序列", difficulty="提高",
         tags=["卡特兰数", "动态规划"], chapter="第 13 章 10 / 第 12 章 05",
         source="经典题型（题意整理）",
         script="p27_bracket_count.py", reference="code/ch13-real-problems/10_brackets.py",
         answer_hint="长度 16 是 8 对括号，不是 16 对；公式里要除以 (n+1)，只算 C(16,8) 会偏大。",
         statement="<p>用 <code>(</code> 和 <code>)</code> 写长度为 <strong>16</strong> 的串，"
                   "要求它是合法的括号序列：左右括号各 8 个，而且从左往右读时任何位置"
                   "读到的左括号都不少于右括号。</p>"
                   "<p>问这样的串一共有多少个。</p>"
                   "<p>这就是卡特兰数。可以先算小的：长度 2 有 1 个、长度 4 有 2 个、"
                   "长度 6 有 5 个、长度 8 有 14 个，看出规律再上 16。</p>",
         idea="<p>递推：枚举最外面那对括号里面包了多长，"
              "<code>g[i] = Σ g[j] * g[i-2-j]</code>（i 只取偶数，g[0] = 1）。</p>"
              "<p>公式是 <code>C(2n, n) / (n + 1)</code>，这里 n = 8。"
              "长度 16 一共才 2^16 种串，可以直接全枚举暴力验证一遍，"
              "递推、公式、暴力三个一致才填。</p>"),
]


# ---------------------------------------------------------------- 组装
def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    cases = prog_cases()
    only = only_filter()
    rows = []

    for meta in all_prog_meta():
        if not only_match(meta["pid"], only):
            continue
        pid, script = meta["pid"], meta["pid"] + ".py"
        src = open(os.path.join(REF_DIR, script), encoding="utf-8").read()
        tests = attach_scores(cases[pid], 25)
        sample_out = ""
        for t in tests:
            out, ms = run_ref(script, t["input"])
            t["expected"] = out if out.endswith("\n") else out + "\n"
            t["ms"] = ms
            if not t["hidden"]:
                sample_out = t["expected"]
        doc = {
            "id": pid,
            "order": int(pid[1:3]),
            "title": meta["title"],
            "type": "prog",
            "difficulty": meta["difficulty"],
            "score": sum(t["score"] for t in tests),
            "tags": meta["tags"],
            "chapter": meta["chapter"],
            "source": meta["source"],
            "statement": meta["statement"],
            "input_format": meta["input_format"],
            "output_format": meta["output_format"],
            "examples": [{"input": tests[0]["input"].strip("\n"),
                          "output": sample_out.strip("\n")}],
            "limits": {"time_ms": TIME_MS},
            "tests": [{"name": t["name"], "input": t["input"], "expected": t["expected"],
                       "score": t["score"], "hidden": t["hidden"]} for t in tests],
            "solution": {
                "idea": meta["idea"],
                "code": src,
                "output": "$ python {}.py\n输入：{}\n输出：{}".format(pid, tests[0]["input"], sample_out),
                "reference": meta["reference"],
            },
        }
        dump(pid, doc)
        slow = [t["name"] for t in tests if t["ms"] > SLOW_MS]
        rows.append((pid, meta["title"], "prog", len(tests), max(t["ms"] for t in tests), slow))

    for meta in all_fill_meta():
        if not only_match(meta["pid"], only):
            continue
        ans, ms = run_fill(meta["script"])
        code = open(os.path.join(FILL_DIR, meta["script"]), encoding="utf-8").read()
        doc = {
            "id": meta["pid"],
            "order": int(meta["pid"][1:3]),
            "title": meta["title"],
            "type": "fill",
            "difficulty": meta["difficulty"],
            "score": 10,
            "tags": meta["tags"],
            "chapter": meta["chapter"],
            "source": meta["source"],
            "statement": meta["statement"],
            "input_format": "填空题不需要写输入，把最终结果（一个数字或一串字符）填进答题区即可。",
            "output_format": "只要最终结果，过程不记分。",
            "examples": [],
            "limits": {"time_ms": TIME_MS},
            "answer": ans,
            "answer_hint": meta["answer_hint"],
            "tests": [],
            "solution": {
                "idea": meta["idea"],
                "code": code,
                "output": "$ python {}\n{}".format(meta["script"], ans),
                "reference": meta["reference"],
                "answer": ans,
            },
        }
        dump(meta["pid"], doc)
        rows.append((meta["pid"], meta["title"], "fill", 1, ms, []))
    return rows


def dump(pid, doc):
    path = os.path.join(OUT_DIR, pid + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)


def main():
    rows = build()
    n_prog = sum(1 for r in rows if r[2] == "prog")
    n_fill = sum(1 for r in rows if r[2] == "fill")
    print("写出 {} 道题（编程 {} / 填空 {}）-> problems/*.json".format(len(rows), n_prog, n_fill))
    print("{:<22} {:<26} {:>5} {:>9}  超过 {} ms 的测试点".format(
        "编号", "标题", "测试点", "最慢ms", SLOW_MS))
    for pid, title, kind, nt, ms, slow in rows:
        print("{:<22} {:<26} {:>5} {:>9}  {}".format(pid, title, nt, ms, "、".join(slow)))
    print("\n所有 expected 与 answer 都由脚本真实运行得到，未手写任何结果。")


if __name__ == "__main__":
    main()
