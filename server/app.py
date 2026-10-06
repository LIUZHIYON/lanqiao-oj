"""蓝桥杯风格模拟 OJ —— 本地服务入口（只用标准库）

启动：python server/app.py  [--port 8000] [--no-browser]
然后浏览器打开 http://127.0.0.1:8000
"""
import json
import mimetypes
import os
import sys
import time
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge  # noqa: E402
import store  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(BASE, "web")

PAGES = {
    "/": "index.html",
    "/problems": "problems.html",
    "/problem": "problem.html",
    "/submissions": "submissions.html",
    "/contest": "contest.html",
}


def public_problem(p, with_examples=True):
    """对外输出版本：隐藏测试点只留名字和分值，不给输入输出。"""
    tests = []
    for i, t in enumerate(p.get("tests", [])):
        item = {
            "name": t.get("name") or f"测试点 {i + 1}",
            "score": t.get("score", 1),
            "hidden": bool(t.get("hidden")),
        }
        if not t.get("hidden"):
            item["input"] = t.get("input", "")
            item["expected"] = t.get("expected", "")
        tests.append(item)
    out = {k: v for k, v in p.items() if k not in ("tests", "_file", "answer", "solution")}
    out["tests"] = tests
    out["test_count"] = len(tests)
    if not with_examples:
        out.pop("examples", None)
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "LanQiaoOJ/1.0"

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    # ---------- 基础响应 ----------
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    def _file(self, path):
        full = os.path.normpath(os.path.join(WEB, path.lstrip("/")))
        if not full.startswith(WEB) or not os.path.isfile(full):
            return self._send(404, "找不到文件", "text/plain; charset=utf-8")
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"
        with open(full, "rb") as f:
            self._send(200, f.read(), ctype)

    # ---------- GET ----------
    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path in PAGES:
                return self._file("/" + PAGES[u.path])
            if u.path.startswith("/assets/"):
                return self._file(u.path)
            if u.path == "/api/problems":
                best = store.best_map()
                stars = set(store.starred())
                items = []
                for p in store.load_problems():
                    b = best.get(p["id"], {})
                    items.append({
                        "id": p["id"], "title": p["title"], "type": p["type"],
                        "difficulty": p["difficulty"], "score": p.get("score", 0),
                        "tags": p.get("tags", []), "chapter": p.get("chapter", ""),
                        "test_count": len(p.get("tests", [])),
                        "solved": bool(b.get("solved")), "tries": b.get("tries", 0),
                        "best_score": b.get("score", 0),
                        "starred": p["id"] in stars,
                    })
                return self._json({"items": items, "stats": store.stats()})
            if u.path == "/api/problem":
                p = store.get_problem(q.get("id", ""))
                if not p:
                    return self._json({"error": "题目不存在"}, 404)
                best = store.best_map().get(p["id"], {})
                return self._json({"problem": public_problem(p),
                                   "best": best,
                                   "history": store.submissions(20, p["id"]),
                                   "starred": p["id"] in set(store.starred()),
                                   "solution_unlocked": p["id"] in store.viewed()})
            if u.path == "/api/solution":
                p = store.get_problem(q.get("id", ""))
                if not p:
                    return self._json({"error": "题目不存在"}, 404)
                store.mark_viewed(p["id"])
                sol = p.get("solution", {})
                return self._json({
                    "idea": sol.get("idea", ""),
                    "code": sol.get("code", ""),
                    "output": sol.get("output", ""),
                    "answer": p.get("answer") or sol.get("answer", ""),
                    "reference": sol.get("reference", ""),
                    "chapter": p.get("chapter", ""),
                })
            if u.path == "/api/submissions":
                return self._json({"items": store.submissions(int(q.get("limit") or 100),
                                                              q.get("problem") or None)})
            if u.path == "/api/stats":
                return self._json(store.stats())
            if u.path == "/api/contest":
                cid = q.get("id")
                if cid:
                    return self._json({"board": store.contest_scoreboard(int(cid)),
                                       "now": time.time()})
                return self._json({"items": store.list_contests(),
                                   "problems": [{"id": p["id"], "title": p["title"],
                                                 "score": p.get("score", 0)}
                                                for p in store.load_problems()]})
            return self._send(404, "没有这个地址", "text/plain; charset=utf-8")
        except Exception:
            return self._json({"error": "服务端异常", "trace": traceback.format_exc()[-1500:]}, 500)

    # ---------- POST ----------
    def do_POST(self):
        u = urlparse(self.path)
        b = self._body()
        try:
            if u.path == "/api/submit":
                return self._submit(b)
            if u.path == "/api/answer":
                return self._answer(b)
            if u.path == "/api/star":
                pid = (b.get("problem_id") or "").strip()
                if not store.get_problem(pid):
                    return self._json({"error": "题目不存在"}, 404)
                on = b.get("on")
                on = store.toggle_star(pid, None if on is None else bool(on))
                return self._json({"ok": True, "problem_id": pid, "starred": on,
                                   "starred_total": len(store.starred())})
            if u.path == "/api/contest/start":
                pids = b.get("problem_ids")
                if not pids:
                    pids = [p["id"] for p in store.load_problems()]
                mins = int(b.get("duration_min") or 240)
                cid = store.start_contest(b.get("title") or "模拟赛", pids, mins * 60)
                return self._json({"id": cid, "problem_ids": pids, "duration_s": mins * 60,
                                   "started_at": time.time()})
            if u.path == "/api/contest/finish":
                cid = int(b.get("id") or 0)
                store.finish_contest(cid)
                return self._json(store.contest_scoreboard(cid) or {"error": "比赛不存在"})
            if u.path == "/api/reset":
                store.reset()
                return self._json({"ok": True})
            return self._send(404, "没有这个接口", "text/plain; charset=utf-8")
        except Exception:
            return self._json({"error": "服务端异常", "trace": traceback.format_exc()[-1500:]}, 500)

    def _submit(self, b):
        p = store.get_problem((b.get("problem_id") or "").strip())
        code = b.get("code") or ""
        if not p:
            return self._json({"error": "题目不存在"}, 404)
        if p["type"] != "prog":
            return self._json({"error": "这是结果填空题，请在答题区提交答案"}, 400)
        if not code.strip():
            return self._json({"error": "代码是空的"}, 400)
        tests = p.get("tests") or []
        limit = p.get("limits", {}).get("time_ms", judge.TIME_LIMIT_DEFAULT_MS)
        t0 = time.time()
        res = judge.judge(code, tests, limit)
        res["wall_ms"] = int((time.time() - t0) * 1000)
        sid = store.record_submission(p["id"], "code", res["result"], res["score"],
                                      res.get("full_score", 0), res["passed"], res["total"],
                                      res.get("max_ms", 0), code=code,
                                      detail=res.get("error", {}).get("detail", ""),
                                      contest_id=b.get("contest_id"))
        return self._json({"id": sid, **res, "labels": judge.RESULT_LABEL})

    def _answer(self, b):
        p = store.get_problem((b.get("problem_id") or "").strip())
        if not p:
            return self._json({"error": "题目不存在"}, 404)
        if p["type"] != "fill":
            return self._json({"error": "这是编程题，请提交代码"}, 400)
        got = str(b.get("answer") or "").strip()
        want = str(p.get("answer") or "").strip()
        hint = p.get("answer_hint", "")
        ok = bool(got) and got.replace(",", "").replace(" ", "") == \
            want.replace(",", "").replace(" ", "")
        score = p.get("score", 10) if ok else 0
        result = "AC" if ok else "WA"
        detail = "" if ok else (hint or "答案不一致。填空题不要手算，写个几行的枚举程序跑一遍。")
        sid = store.record_submission(p["id"], "answer", result, score, p.get("score", 10),
                                      int(ok), 1, 0, answer=got, detail=detail,
                                      contest_id=b.get("contest_id"))
        return self._json({"id": sid, "result": result, "ok": ok, "score": score,
                           "full_score": p.get("score", 10), "passed": int(ok), "total": 1,
                           "cases": [], "detail": detail})


class Server(ThreadingHTTPServer):
    # Windows 下 SO_REUSEADDR 允许两个程序绑同一端口：绑定不报错，但请求全被
    # 先占端口的程序接走，表现为"服务起来了却打不开"。这里关掉它，让冲突真的报错。
    allow_reuse_address = False
    daemon_threads = True


def bind(preferred):
    """端口被占用就自动往后找，避免和其它本地服务冲突。"""
    tried = []
    for p in [preferred] + [x for x in (8000, 8010, 8020, 8030, 8050, 8080, 8123, 8888)
                            if x != preferred]:
        try:
            return Server(("127.0.0.1", p), Handler), p, tried
        except OSError:
            tried.append(p)
    return None, None, tried


def say(msg=""):
    print(msg, flush=True)


def main():
    port = 8000
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    httpd, port, tried = bind(port)
    probs = store.load_problems()
    if httpd is None:
        say("[启动失败] 这些端口都被占用了： " + ", ".join(map(str, tried)))
        say("请换个端口启动：python server\\app.py --port 9000")
        input("按回车退出")
        return
    if tried:
        say(f"[提示] 端口 {', '.join(map(str, tried))} 已被其它程序占用，自动改用 {port}")
    say("=" * 62)
    say(" 蓝桥杯 Python 模拟 OJ（本地）")
    say(f" 地址：http://127.0.0.1:{port}    判题：本机 Python {sys.version.split()[0]}")
    if probs:
        say(f" 题库：{len(probs)} 道题（编程题 {sum(1 for p in probs if p['type'] == 'prog')}"
            f" / 填空题 {sum(1 for p in probs if p['type'] == 'fill')}）")
    else:
        say(" 题库：空 —— 先运行  python generator/build_problems.py")
    say(" 停止：按 Ctrl + C 或直接关闭本窗口")
    say("=" * 62)
    if "--no-browser" not in sys.argv:
        webbrowser.open(f"http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        say("\n已停止。")


if __name__ == "__main__":
    main()
