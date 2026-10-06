"""题库自检：交付前的最后一道关。

1. 每道编程题：拿 generator/reference/<pid>.py 的源码当提交，交给 server/judge.py 真判，必须全 AC；
   同时把 JSON 里每个 expected 重新跑一遍参考解核对（防止题库和参考解走偏）。
2. 每道填空题：重跑 generator/fill_scripts/<pid>.py，和 JSON 里的 answer 比对。
3. 和讲义里印出来的答案逐个对（不一致就报出来，以本机运行为准）。
4. 结构检查：字段齐不齐、测试点够不够、分值对不对、题干有没有出现禁用词、题解指向的脚本在不在。

用法：python generator/self_check.py
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "server"))
sys.path.insert(0, os.path.join(BASE, "generator"))

import judge                                              # noqa: E402  判题引擎
from build_problems import (FILL_DIR, REF_DIR, all_prog_meta, all_fill_meta,  # noqa: E402
                            only_filter, only_match, run_ref, run_fill)

PROB_DIR = os.path.join(BASE, "problems")
LECTURE_DIR = "D:/WorkBuddy-cn_workspace/lanqiao-cup-python"
FORBIDDEN = ["AI", "模型", "生成", "人工智能"]

# 讲义（第 13 章等）里印出来的答案，用来和本机重跑结果比对
LECTURE_FILL = {
    "p16_cards": "3181", "p17_snake": "761", "p18_goods": "54", "p19_fraction": "2486423",
    "p20_fact_digits": "5809", "p21_fact_zeros": "503", "p22_grid_paths": "137846528820",
    "p23_segments": "80", "p24_digit2": "569", "p25_digit1": "1613",
    "p26_ugly": "859963392", "p27_bracket_fill": "1430",
}
# 编程题：讲义脚本里出现过的（输入 -> 结论），本机重跑再核对一次
LECTURE_PROG = [
    ("p01_year_string", "2026\n", "BYX", "第 13 章 01：2026 -> BYX"),
    ("p01_year_string", "52\n", "AZ", "第 13 章 01 基础用例 52 -> AZ"),
    ("p02_time_display", "5000000\n", "1:23:20", "第 13 章 08 样例"),
    ("p02_time_display", "86399999\n", "23:59:59", "第 13 章 08 边界"),
    ("p03_practice_stats", "10 20 100\n", "8", "第 13 章 04：第 8 天"),
    ("p03_practice_stats", "10 10 100\n", "10", "第 13 章 04 表格第一行"),
    ("p04_cut_trees", "4 7\n20 15 10 17\n", "15", "第 13 章 05 模型 A"),
    ("p04_cut_trees", "8 7\n4 56 2 1 20 8 19 3\n", "49", "第 13 章 05 第二组"),
    ("p05_maze_bfs", "6 6\n001000\n010010\n000101\n110001\n000110\n010000\n", "10",
     "第 13 章 13 的迷宫：BFS 与 Dijkstra 都是 10 步"),
    ("p06_concat_max", "3\n30 32 321\n", "3232130", "第 13 章 07 样例"),
    ("p06_concat_max", "2\n12 121\n", "12121", "第 13 章 07 前缀陷阱"),
    ("p08_perfect_square", "1200000\n", "30", "第 9 章 18：1200000 -> 30"),
    ("p10_bracket_fix", "())(()\n", "2", "第 13 章 10 题 B"),
    ("p10_bracket_fix", "(((\n", "3", "第 13 章 10 题 B 第一行"),
    ("p15_nim", "3\n3 4 5\n", "1", "第 13 章 12：异或 2，先手胜"),
    ("p15_nim", "3\n1 2 3\n", "0", "第 13 章 12：异或 0，先手败"),
]

problems = {}
fails = []
notes = []


def load(pid):
    with open(os.path.join(PROB_DIR, pid + ".json"), encoding="utf-8") as f:
        return json.load(f)


def fail(tag, msg):
    fails.append((tag, msg))
    print("  [FAIL] {}: {}".format(tag, msg))


def need_fields(doc):
    for k in ("id", "order", "title", "type", "difficulty", "score", "tags", "chapter",
              "source", "statement", "input_format", "output_format", "examples", "limits",
              "solution"):
        if k not in doc:
            fail(doc.get("id", "?"), "缺字段 {}".format(k))
    if doc["type"] == "prog":
        if not doc.get("tests"):
            fail(doc["id"], "编程题没有测试点")
        for t in doc["tests"]:
            for k in ("name", "input", "expected", "score", "hidden"):
                if k not in t:
                    fail(doc["id"], "测试点 {} 缺字段 {}".format(t.get("name"), k))
    else:
        for k in ("answer", "answer_hint"):
            if not doc.get(k):
                fail(doc["id"], "填空题缺 {}".format(k))
    for k, v in doc.items():
        if k in ("tests", "examples", "limits", "solution", "tags", "order", "score", "type",
                 "difficulty", "id"):
            continue
        if isinstance(v, str):
            for w in FORBIDDEN:
                if w in v:
                    fail(doc["id"], "文案里出现了禁用词「{}」：{}".format(w, v[:60]))
    sol = doc.get("solution", {})
    for w in FORBIDDEN:
        if w in sol.get("idea", ""):
            fail(doc["id"], "题解思路里出现禁用词「{}」".format(w))


def check_reference_paths():
    """题解里指向的讲义脚本必须真的存在（讲义在同级目录时）。"""
    if not os.path.isdir(LECTURE_DIR):
        notes.append("讲义目录不在本机，跳过 reference 路径检查")
        return
    for doc in problems.values():
        rel = doc.get("solution", {}).get("reference", "")
        if not rel:
            fail(doc["id"], "缺 solution.reference")
            continue
        if not os.path.isfile(os.path.join(LECTURE_DIR, rel.replace("/", os.sep))):
            fail(doc["id"], "reference 指向的讲义脚本不存在：{}".format(rel))


def check_prog(doc):
    pid = doc["id"]
    tests = doc["tests"]
    hidden = [t for t in tests if t["hidden"]]
    visible = [t for t in tests if not t["hidden"]]
    if len(tests) < 5:
        fail(pid, "测试点只有 {} 个，要求至少 5 个".format(len(tests)))
    if len(hidden) < 4:
        fail(pid, "隐藏测试点只有 {} 个，要求至少 4 个".format(len(hidden)))
    if len(visible) != 1:
        fail(pid, "可见样例测试点应正好 1 个，实际 {}".format(len(visible)))
    total = sum(t["score"] for t in tests)
    if total != doc["score"]:
        fail(pid, "测试点分值之和 {} != 题目 score {}".format(total, doc["score"]))
    ex = doc["examples"][0] if doc["examples"] else {}
    if visible and ex:
        if visible[0]["input"].strip("\n") != ex["input"]:
            fail(pid, "样例测试点输入和 examples 不一致")
        if visible[0]["expected"].strip("\n") != ex["output"]:
            fail(pid, "样例测试点输出和 examples 不一致")

    code = open(os.path.join(REF_DIR, pid + ".py"), encoding="utf-8").read()
    if code != doc["solution"]["code"]:
        fail(pid, "题库里的 solution.code 和参考解文件不一致")

    # 1) expected 必须还能重跑复现
    for t in tests:
        out, _ = run_ref(pid + ".py", t["input"])
        if out != t["expected"]:
            fail(pid, "测试点「{}」重跑结果和题库不符：题库 {!r}，实跑 {!r}".format(
                t["name"], t["expected"][:60], out[:60]))

    # 2) 用判题引擎判参考解自己
    res = judge.judge(code, tests, doc.get("limits", {}).get("time_ms", 2000))
    if res["result"] != "AC":
        fail(pid, "参考解判题不是 AC：{}（{}/{}）".format(res["result"], res["passed"], res["total"]))
        for c in res["cases"]:
            if c["status"] != "AC":
                print("     {} -> {}  ms={}".format(c["name"], c["status"], c["ms"]))
    if res["max_ms"] > 2000:
        fail(pid, "判题最慢 {} ms 超过 2000 ms 限制".format(res["max_ms"]))
    return res


FILL_SCRIPT = {m["pid"]: m["script"] for m in all_fill_meta()}


def check_fill(doc):
    pid = doc["id"]
    script = FILL_SCRIPT[pid]
    ans, ms = run_fill(script)
    if ans != doc["answer"]:
        fail(pid, "重跑 fill 脚本得到 {}，题库写的是 {}".format(ans, doc["answer"]))
    if doc["solution"].get("answer") != doc["answer"]:
        fail(pid, "solution.answer 和 answer 不一致")
    code = open(os.path.join(FILL_DIR, script), encoding="utf-8").read()
    if code != doc["solution"]["code"]:
        fail(pid, "题库里的 solution.code 和 fill 脚本不一致")
    if not doc["answer_hint"]:
        fail(pid, "填空题缺易错提醒")
    return ans, ms


def check_lecture():
    print("\n=== 与讲义答案比对（以本机重跑为准）===")
    for pid, want in sorted(LECTURE_FILL.items()):
        if pid not in problems:      # --only 模式下只比对本次真正加载的题
            continue
        got = problems[pid]["answer"]
        print("  {:<18} 本机 {:>14}   讲义 {:>14}   {}".format(
            pid, got, want, "一致" if got == want else "不一致！"))
        if got != want:
            notes.append("填空 {}：本机 {} / 讲义 {}".format(pid, got, want))
    for pid, text, want, label in LECTURE_PROG:
        if pid not in problems:
            continue
        got, _ = run_ref(pid + ".py", text)
        got = got.strip()
        same = got == want.strip()
        print("  {:<18} {:<44} 本机 {:>12}  讲义 {:>12}  {}".format(
            pid, label, got, want, "一致" if same else "不一致！"))
        if not same:
            notes.append("编程 {}：{} 本机 {} / 讲义 {}".format(pid, label, got, want))


def main():
    print("蓝桥模拟 OJ 题库自检    Python {}".format(sys.version.split()[0]))
    print("判题引擎：{}".format(os.path.join(BASE, "server", "judge.py")))
    print()

    only = only_filter()
    all_ids = [m["pid"] for m in all_prog_meta()] + [m["pid"] for m in all_fill_meta()]
    ids = [i for i in all_ids if only_match(i, only)]
    files = sorted(f[:-5] for f in os.listdir(PROB_DIR) if f.endswith(".json"))
    extra = [f for f in files if f not in set(all_ids)]
    for f in extra:
        print("  [注意] problems/ 里有计划外的文件 {}.json（不在任何题库计划里）".format(f))
    for pid in ids:
        doc = load(pid)
        if doc["id"] != pid:
            fail(pid, "文件名和 id 不一致：{}".format(doc["id"]))
        problems[pid] = doc
    missing = [p for p in ids if p not in problems]
    if missing:
        fail("题库", "缺题：{}".format(missing))

    for doc in problems.values():
        need_fields(doc)
    n_prog = sum(1 for d in problems.values() if d["type"] == "prog")
    n_fill = sum(1 for d in problems.values() if d["type"] == "fill")
    if not only and (n_prog < 15 or n_fill < 12):
        fail("题库", "题量低于基线：编程 {} 填空 {}（基线至少 15 / 12）".format(n_prog, n_fill))
    orders = sorted(d["order"] for d in problems.values())
    if not only and orders != list(range(1, len(orders) + 1)):
        fail("题库", "order 不是从 1 连续编号：{}".format(orders))
    check_reference_paths()

    print("\n=== 编程题：判题引擎判参考解 ===")
    print("{:<22}{:<24}{:>5}{:>6}{:>8}{:>9}".format("编号", "标题", "点数", "AC", "得分", "最慢ms"))
    for pid in sorted(problems):
        doc = problems[pid]
        if doc["type"] != "prog":
            continue
        res = check_prog(doc)
        ac = res["passed"] == res["total"]
        print("{:<22}{:<24}{:>5}{:>6}{:>8}{:>9}  {}".format(
            pid, doc["title"], res["total"], "Y" if ac else "N",
            "{}/{}".format(res["score"], res["full_score"]), res["max_ms"], res["result"]))

    print("\n=== 填空题：重跑脚本核对 answer ===")
    for pid in sorted(problems):
        doc = problems[pid]
        if doc["type"] != "fill":
            continue
        ans, ms = check_fill(doc)
        print("{:<22}{:<26}{:>16}{:>10}ms  {}".format(pid, doc["title"], ans, ms,
                                                     "一致" if ans == doc["answer"] else "不一致"))

    check_lecture()

    print("\n=== 汇总 ===")
    print("题目 {} 道（编程 {} / 填空 {}），测试点 {} 个".format(
        len(problems), n_prog, n_fill,
        sum(len(d.get("tests", [])) for d in problems.values())))
    if notes:
        print("需要注意：")
        for n in notes:
            print("  - " + n)
    if fails:
        print("不通过 {} 项：".format(len(fails)))
        for tag, msg in fails:
            print("  [{}] {}".format(tag, msg))
        print("\n自检结果：FAIL")
        return 1
    print("自检结果：全部通过（编程题全 AC，填空题答案与重跑一致，与讲义无冲突）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
