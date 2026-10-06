"""判题引擎：用本机 Python 真实执行提交的代码。

只依赖标准库。判题在 data/runs/<编号>/ 的隔离目录里进行，跑完即删。
子进程环境用白名单构造，不继承用户机器上的其它环境变量。
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

TIME_LIMIT_DEFAULT_MS = 2000
OUTPUT_LIMIT_BYTES = 1_000_000
STDERR_KEEP = 4000

RESULT_LABEL = {
    "AC": "通过",
    "WA": "答案错误",
    "TLE": "超时",
    "RE": "运行错误",
    "CE": "编译错误",
    "OLE": "输出过长",
    "IE": "判题异常",
}


def _env(run_dir):
    tmp = os.path.join(run_dir, "tmp")
    os.makedirs(tmp, exist_ok=True)
    keep = ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "SYSTEMDRIVE", "PROGRAMFILES")
    e = {k: os.environ[k] for k in keep if k in os.environ}
    e["TEMP"] = e["TMP"] = tmp
    e["PYTHONIOENCODING"] = "utf-8"
    e["PYTHONUTF8"] = "1"
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    return e


def _kill_tree(pid):
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)],
                       capture_output=True)
    else:
        try:
            os.killpg(os.getpgid(pid), 9)
        except OSError:
            pass


def normalize(text):
    """比对前的规范化：统一换行、去掉行尾空白、去掉尾部空行。"""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines = [ln.rstrip() for ln in lines]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def check_syntax(code):
    """先做语法检查，把编译错误和运行错误分开报。"""
    try:
        compile(code, "submission.py", "exec")
        return None
    except SyntaxError as e:
        line = e.lineno or 0
        seg = (e.text or "").rstrip()
        return {
            "status": "CE",
            "detail": f"SyntaxError: {e.msg}",
            "line": line,
            "excerpt": f'第 {line} 行: {seg}' if seg else f"第 {line} 行",
        }
    except Exception as e:  # ValueError 之类（含 null 字节）
        return {"status": "CE", "detail": f"{type(e).__name__}: {e}", "line": 0, "excerpt": ""}


def run_one(code, stdin_text, time_ms, run_dir):
    """执行一次，返回 status / stdout / stderr / 耗时。"""
    src = os.path.join(run_dir, "submission.py")
    with open(src, "w", encoding="utf-8") as f:
        f.write(code)

    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            [sys.executable, "submission.py"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=run_dir, env=_env(run_dir),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
    except OSError as e:
        return {"status": "IE", "detail": f"无法启动 Python：{e}", "stdout": "", "stderr": "", "ms": 0}

    try:
        out, err = proc.communicate(input=stdin_text.encode("utf-8"), timeout=time_ms / 1000.0)
    except subprocess.TimeoutExpired:
        _kill_tree(proc.pid)
        try:
            proc.communicate(timeout=3)
        except Exception:
            proc.kill()
        spent = int((time.perf_counter() - t0) * 1000)
        return {"status": "TLE", "detail": f"超过时间限制 {time_ms} ms", "stdout": "", "stderr": "", "ms": spent}

    spent = int((time.perf_counter() - t0) * 1000)
    stdout = out.decode("utf-8", "replace")
    stderr = err.decode("utf-8", "replace")

    if len(stdout.encode("utf-8")) > OUTPUT_LIMIT_BYTES:
        return {"status": "OLE", "detail": "输出超过 1 MB", "stdout": stdout[:2000], "stderr": "", "ms": spent}
    if proc.returncode != 0:
        tail = stderr.strip().splitlines()[-6:] if stderr.strip() else [f"退出码 {proc.returncode}"]
        return {"status": "RE", "detail": "\n".join(tail)[:STDERR_KEEP],
                "stdout": stdout, "stderr": stderr[-STDERR_KEEP:], "ms": spent}
    return {"status": "AC", "detail": "", "stdout": stdout, "stderr": "", "ms": spent}


def judge(code, tests, time_ms=TIME_LIMIT_DEFAULT_MS):
    """逐测试点评判。tests: [{name, input, expected, score, hidden}]"""
    ce = check_syntax(code)
    if ce:
        return {"result": "CE", "passed": 0, "total": len(tests), "score": 0,
                "cases": [], "error": ce, "max_ms": 0}

    run_dir = tempfile.mkdtemp(prefix="run_", dir=_runs_root())
    try:
        cases = []
        passed = 0
        score = 0
        worst = "AC"
        max_ms = 0
        for i, t in enumerate(tests):
            name = t.get("name") or f"测试点 {i + 1}"
            r = run_one(code, t.get("input", ""), t.get("time_ms") or time_ms, run_dir)
            max_ms = max(max_ms, r["ms"])
            if r["status"] == "AC":
                got, want = normalize(r["stdout"]), normalize(t["expected"])
                if got == want:
                    passed += 1
                    score += t.get("score", 1)
                    case_status = "AC"
                else:
                    case_status = "WA"
                    worst = "WA" if worst == "AC" else worst
            else:
                case_status = r["status"]
                order = {"RE": 3, "TLE": 2, "OLE": 4, "IE": 5}
                if worst == "AC" or order.get(case_status, 0) > order.get(worst, 0):
                    worst = case_status if case_status != "AC" else worst
            cases.append({
                "name": name,
                "status": case_status,
                "ms": r["ms"],
                "hidden": bool(t.get("hidden")),
                "expected": "" if t.get("hidden") else t["expected"],
                "got": "" if t.get("hidden") else r["stdout"][:2000],
                "detail": r["detail"],
            })
        result = "AC" if passed == len(tests) else worst
        return {"result": result, "passed": passed, "total": len(tests), "score": score,
                "cases": cases, "max_ms": max_ms,
                "full_score": sum(t.get("score", 1) for t in tests)}
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def _runs_root():
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "runs")
    os.makedirs(root, exist_ok=True)
    return root
