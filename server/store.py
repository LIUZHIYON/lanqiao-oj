"""数据层：题库加载（problems/*.json）+ 本地 sqlite 记录。

删掉 data/oj.db 就等于清空全部练习进度。
"""
import json
import os
import sqlite3
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB_DIR = os.path.join(BASE, "problems")
DATA_DIR = os.path.join(BASE, "data")
DB = os.path.join(DATA_DIR, "oj.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  problem_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  result TEXT NOT NULL,
  score REAL NOT NULL DEFAULT 0,
  full_score REAL NOT NULL DEFAULT 0,
  passed INTEGER NOT NULL DEFAULT 0,
  total INTEGER NOT NULL DEFAULT 0,
  ms INTEGER NOT NULL DEFAULT 0,
  code TEXT,
  answer TEXT,
  detail TEXT,
  contest_id INTEGER,
  created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS viewed(
  problem_id TEXT PRIMARY KEY,
  created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS contests(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  problem_ids TEXT NOT NULL,
  duration_s INTEGER NOT NULL,
  started_at REAL NOT NULL,
  finished_at REAL
);
CREATE TABLE IF NOT EXISTS starred(
  problem_id TEXT PRIMARY KEY,
  created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sub_prob ON submissions(problem_id);
"""

_cache = {"mtime": 0, "list": [], "map": {}}


def problems_fingerprint():
    if not os.path.isdir(PROB_DIR):
        return 0
    return max([os.path.getmtime(os.path.join(PROB_DIR, f)) for f in os.listdir(PROB_DIR)
                if f.endswith(".json")] or [0])


def load_problems():
    fp = problems_fingerprint()
    if _cache["mtime"] == fp and _cache["list"]:
        return _cache["list"]
    items = []
    for fn in sorted(os.listdir(PROB_DIR)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        with open(os.path.join(PROB_DIR, fn), encoding="utf-8") as f:
            p = json.load(f)
        p.setdefault("difficulty", "未标注")
        p.setdefault("tags", [])
        p.setdefault("tests", [])
        p.setdefault("type", "prog")
        p["_file"] = fn
        items.append(p)
    items.sort(key=lambda p: p.get("order", 999))
    _cache["mtime"] = fp
    _cache["list"] = items
    _cache["map"] = {p["id"]: p for p in items}
    return items


def get_problem(pid):
    load_problems()
    return _cache["map"].get(pid)


def db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def record_submission(pid, kind, result, score, full, passed, total, ms,
                      code=None, answer=None, detail="", contest_id=None):
    with db() as c:
        cur = c.execute(
            "INSERT INTO submissions(problem_id,kind,result,score,full_score,passed,total,ms,"
            "code,answer,detail,contest_id,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid, kind, result, score, full, passed, total, ms, code, answer, detail,
             contest_id, time.time()))
        c.commit()
        return cur.lastrowid


def best_map():
    """每题的历史最好成绩：{pid: {result, score, full, at}}"""
    sql = """SELECT problem_id, MAX(score) AS score, full_score, result, MIN(created_at) AS ac_at,
                    COUNT(*) AS tries, MAX(created_at) AS last_at
             FROM submissions GROUP BY problem_id"""
    out = {}
    with db() as c:
        for r in c.execute(sql):
            solved = r["score"] >= (r["full_score"] or 1) - 1e-9
            out[r["problem_id"]] = {
                "score": r["score"], "full": r["full_score"], "best_result": r["result"],
                "tries": r["tries"], "last_at": r["last_at"], "solved": bool(solved),
            }
    return out


def submissions(limit=100, pid=None):
    sql = "SELECT * FROM submissions"
    args = []
    if pid:
        sql += " WHERE problem_id=?"
        args.append(pid)
    sql += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with db() as c:
        return [dict(r) for r in c.execute(sql, args)]


def mark_viewed(pid):
    with db() as c:
        c.execute("INSERT OR IGNORE INTO viewed(problem_id, created_at) VALUES(?,?)", (pid, time.time()))
        c.commit()


def viewed():
    with db() as c:
        return {r["problem_id"] for r in c.execute("SELECT problem_id FROM viewed")}


def stats():
    """总体与按考点的刷题统计，用于指出薄弱项。"""
    probs = load_problems()
    best = best_map()
    tags = {}
    for p in probs:
        b = best.get(p["id"], {})
        solved = bool(b.get("solved"))
        for t in p.get("tags", []) or ["未分类"]:
            g = tags.setdefault(t, {"total": 0, "solved": 0, "tries": 0})
            g["total"] += 1
            g["solved"] += 1 if solved else 0
            g["tries"] += b.get("tries", 0)
    total = len(probs)
    done = sum(1 for p in probs if best.get(p["id"], {}).get("solved"))
    stars = set(starred())
    star_todo = sum(1 for p in probs if p["id"] in stars and not best.get(p["id"], {}).get("solved"))
    with db() as c:
        n_sub = c.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
        n_ac = c.execute("SELECT COUNT(*) FROM submissions WHERE result='AC'").fetchone()[0]
    return {
        "problems": total, "solved": done, "submissions": n_sub, "ac_submissions": n_ac,
        "starred": len(stars), "starred_todo": star_todo,
        "ac_rate": round(n_ac / n_sub * 100, 1) if n_sub else 0,
        "tags": [{"tag": k, **v, "rate": round(v["solved"] / v["total"] * 100)}
                 for k, v in sorted(tags.items(), key=lambda kv: (kv[1]["solved"] / kv[1]["total"]))],
    }


def start_contest(title, pids, duration_s):
    with db() as c:
        cur = c.execute("INSERT INTO contests(title,problem_ids,duration_s,started_at) VALUES(?,?,?,?)",
                        (title, json.dumps(pids), duration_s, time.time()))
        c.commit()
        return cur.lastrowid


def list_contests():
    with db() as c:
        rows = []
        for r in c.execute("SELECT * FROM contests ORDER BY id DESC LIMIT 20"):
            d = dict(r)
            d["problem_ids"] = json.loads(d["problem_ids"])
            rows.append(d)
        return rows


def get_contest(cid):
    with db() as c:
        r = c.execute("SELECT * FROM contests WHERE id=?", (cid,)).fetchone()
        if not r:
            return None
        d = dict(r)
        d["problem_ids"] = json.loads(d["problem_ids"])
        return d


def finish_contest(cid):
    with db() as c:
        c.execute("UPDATE contests SET finished_at=? WHERE id=? AND finished_at IS NULL",
                  (time.time(), cid))
        c.commit()


def contest_scoreboard(cid):
    """比赛成绩单：每题最好成绩 + 用时 + 尝试次数。"""
    ct = get_contest(cid)
    if not ct:
        return None
    with db() as c:
        rows = [dict(r) for r in c.execute(
            "SELECT problem_id, MAX(score) score, full_score, COUNT(*) tries, "
            "MIN(created_at) first_at, MAX(created_at) last_at "
            "FROM submissions WHERE contest_id=? GROUP BY problem_id", (cid,))]
    base = ct["started_at"]
    out = []
    for r in rows:
        p = get_problem(r["problem_id"])
        solved = r["score"] >= (r["full_score"] or 1) - 1e-9
        out.append({
            "problem_id": r["problem_id"],
            "title": (p or {}).get("title", r["problem_id"]),
            "score": r["score"], "full": r["full_score"], "tries": r["tries"],
            "solved": solved,
            "cost_s": int(r["last_at"] - base) if solved else None,
        })
    total = sum(x["score"] for x in out)
    full = sum(x["full"] or 0 for x in out)
    return {"contest": ct, "rows": out, "total": total, "full": full,
            "solved": sum(1 for x in out if x["solved"]),
            "elapsed": int((ct.get("finished_at") or time.time()) - base)}


def toggle_star(pid, on=None):
    """收藏/取消收藏。on 为 None 表示切换。返回切换后的状态。"""
    now = set(starred())
    want = (pid not in now) if on is None else bool(on)
    with db() as c:
        if want:
            c.execute("INSERT OR IGNORE INTO starred(problem_id, created_at) VALUES(?,?)", (pid, time.time()))
        else:
            c.execute("DELETE FROM starred WHERE problem_id=?", (pid,))
        c.commit()
    return want


def starred():
    with db() as c:
        return [r["problem_id"] for r in c.execute(
            "SELECT problem_id FROM starred ORDER BY created_at DESC")]


def reset():
    with db() as c:
        c.executescript("DELETE FROM submissions; DELETE FROM viewed; DELETE FROM contests;"
                        " DELETE FROM starred;")
        c.commit()
