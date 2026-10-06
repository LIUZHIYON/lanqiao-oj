/* 蓝桥杯 Python 模拟训练平台 —— 公共脚本（只用浏览器原生能力，无任何外部依赖）
 *
 * 约定：
 *   1. 所有接口都用同源相对路径 api/xxx，不写死端口；
 *   2. 除了题干 statement、题解 idea 这两个后端自己写的静态 HTML 片段，
 *      其它内容一律走 textContent，避免代码内容被当成网页标签解析。
 */
(function () {
  'use strict';

  var RESULT_LABEL = {
    AC: '通过', WA: '答案错误', TLE: '超时', RE: '运行错误',
    CE: '编译错误', OLE: '输出过长', IE: '判题异常'
  };

  /* ---------------- 请求 ---------------- */

  function apiUrl(path, params) {
    var qs = [];
    Object.keys(params || {}).forEach(function (k) {
      var v = params[k];
      if (v === null || v === undefined || v === '') { return; }
      qs.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
    });
    var base = 'api/' + path;
    return qs.length ? base + '?' + qs.join('&') : base;
  }

  function isFileUrl() {
    return location.protocol === 'file:';
  }

  function downError() {
    var e = new Error('连不上后端服务');
    e.offline = true;
    e.hint = isFileUrl()
      ? '这个页面需要用本地服务打开：先运行 python server/app.py，再访问 http://127.0.0.1:8000'
      : '后端服务没有启动或已经停止。';
    return e;
  }

  function request(method, path, opts) {
    opts = opts || {};
    var u = apiUrl(path, opts.params);
    var init = { method: method, cache: 'no-store', headers: {} };
    if (opts.body !== undefined) {
      init.headers['Content-Type'] = 'application/json';
      init.body = JSON.stringify(opts.body);
    }
    return fetch(u, init).then(function (resp) {
      return resp.text().then(function (text) {
        var data = null;
        if (text) {
          try { data = JSON.parse(text); } catch (err) { data = null; }
        }
        if (data === null) {
          if (isFileUrl()) { throw downError(); }
          if (!resp.ok) {
            var e = new Error('服务返回异常（HTTP ' + resp.status + '）');
            e.hint = '请确认用 python server/app.py 启动服务，并通过服务地址访问本页。';
            throw e;
          }
          return null;
        }
        if (!resp.ok) {
          var er = new Error(data.error || ('请求失败（HTTP ' + resp.status + '）'));
          er.status = resp.status;
          er.detail = data.trace || data.error || '';
          er.data = data;
          throw er;
        }
        return data;
      });
    }, function () {
      throw downError();
    });
  }

  var api = {
    get: function (path, params) { return request('GET', path, { params: params }); },
    post: function (path, body) { return request('POST', path, { body: body || {} }); }
  };

  /* ---------------- DOM 小工具 ---------------- */

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) { return; }
        if (k === 'class') { n.className = v; }
        else if (k === 'text') { n.textContent = String(v); }
        else if (k === 'html') { n.innerHTML = String(v); }
        else if (k === 'dataset') { Object.keys(v).forEach(function (d) { n.dataset[d] = v[d]; }); }
        else if (k.indexOf('on') === 0 && typeof v === 'function') { n.addEventListener(k.slice(2), v); }
        else if (v === true) { n.setAttribute(k, ''); }
        else { n.setAttribute(k, v); }
      });
    }
    append(n, kids);
    return n;
  }

  function append(node, kids) {
    if (kids === null || kids === undefined) { return node; }
    if (Array.isArray(kids)) {
      kids.forEach(function (k) { append(node, k); });
    } else if (kids instanceof Node) {
      node.appendChild(kids);
    } else {
      node.appendChild(document.createTextNode(String(kids)));
    }
    return node;
  }

  function clear(node) {
    while (node && node.firstChild) { node.removeChild(node.firstChild); }
    return node;
  }

  function qs(name) {
    var m = new RegExp('[?&]' + name + '=([^&#]*)').exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
  }

  function linkProblem(pid, contestId) {
    var u = 'problem?id=' + encodeURIComponent(pid);
    if (contestId) { u += '&contest_id=' + encodeURIComponent(contestId); }
    return u;
  }

  function linkProblems(params) {
    var parts = [];
    Object.keys(params || {}).forEach(function (k) {
      if (params[k]) { parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k])); }
    });
    return parts.length ? 'problems?' + parts.join('&') : 'problems';
  }

  /* ---------------- 格式化 ---------------- */

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function fmtTime(ts) {
    if (!ts) { return '—'; }
    var d = new Date(ts * 1000);
    if (isNaN(d.getTime())) { return '—'; }
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) +
      ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
  }

  function fmtClock(totalSec) {
    var s = Math.max(0, Math.floor(totalSec));
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
    return pad(h) + ':' + pad(m) + ':' + pad(s % 60);
  }

  function fmtMs(ms) {
    if (ms === null || ms === undefined) { return '—'; }
    if (ms < 1000) { return Math.round(ms) + ' ms'; }
    return (ms / 1000).toFixed(2) + ' 秒';
  }

  function fmtDur(sec) {
    if (sec === null || sec === undefined) { return '—'; }
    var s = Math.round(sec);
    if (s < 60) { return s + ' 秒'; }
    if (s < 3600) { return Math.floor(s / 60) + ' 分 ' + pad(s % 60) + ' 秒'; }
    return Math.floor(s / 3600) + ' 时 ' + pad(Math.floor((s % 3600) / 60)) + ' 分';
  }

  function fmtScore(v) {
    if (v === null || v === undefined) { return '—'; }
    var n = Number(v);
    if (isNaN(n)) { return String(v); }
    return (Math.abs(n - Math.round(n)) < 1e-9) ? String(Math.round(n)) : n.toFixed(1);
  }

  function typeLabel(t) { return t === 'fill' ? '填空' : (t === 'prog' ? '编程' : (t || '—')); }

  function diffClass(d) {
    if (d === '入门') { return 'd-ru'; }
    if (d === '提高') { return 'd-gao'; }
    if (d === '较难') { return 'd-nan'; }
    return 'd-unknown';
  }

  /* result -> 大字配色 / 小色块 */
  function verdictClass(result) {
    if (result === 'AC') { return 'v-ok'; }
    if (result === 'WA') { return 'v-bad'; }
    if (result === 'TLE') { return 'v-slow'; }
    if (result === 'RE' || result === 'CE' || result === 'OLE') { return 'v-err'; }
    return 'v-mute';
  }

  function pillClass(result) {
    if (result === 'AC') { return 'ok'; }
    if (result === 'WA') { return 'bad'; }
    if (result === 'TLE') { return 'slow'; }
    if (result === 'RE' || result === 'CE' || result === 'OLE' || result === 'IE') { return 'err'; }
    return 'mute';
  }

  function dotClass(result, hidden) {
    if (hidden) { return 'cd-hidden'; }
    if (result === 'AC') { return 'cd-ok'; }
    if (result === 'WA') { return 'cd-bad'; }
    if (result === 'TLE') { return 'cd-slow'; }
    if (result === 'RE' || result === 'CE' || result === 'OLE') { return 'cd-err'; }
    return '';
  }

  function resultLabel(result, labels) {
    if (labels && labels[result]) { return labels[result]; }
    return RESULT_LABEL[result] || result || '—';
  }

  function statusNode(result, labels) {
    return el('span', { class: 'pill ' + pillClass(result), text: (result || '—') + ' ' + resultLabel(result, labels) });
  }

  /* ---------------- 复制 ---------------- */

  function fallbackCopy(text) {
    var ta = el('textarea', { style: 'position:fixed;left:-9999px;top:0' });
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function copyText(text, btn) {
    function done(ok) {
      if (!btn) { return; }
      var old = btn.textContent;
      btn.textContent = ok ? '已复制' : '复制失败';
      btn.classList.add('done');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('done'); }, 1600);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); },
        function () { done(fallbackCopy(text)); });
    } else {
      done(fallbackCopy(text));
    }
  }

  function copyBlock(text, extra) {
    var btn = el('button', {
      class: 'copy-btn', type: 'button', text: '复制',
      onclick: function () { copyText(text, btn); }
    });
    return el('span', { class: 'row' }, [btn].concat(extra || []));
  }

  /* ---------------- 提示 ---------------- */

  function failBox(err) {
    var box = el('div', { class: 'fail-box' }, [
      el('h3', { text: err && err.offline ? '后端未启动，请先运行 python server/app.py' : '操作没有成功' }),
      el('p', { text: (err && err.message) || '未知错误' })
    ]);
    var hint = (err && err.hint) || '';
    if (!hint && err && err.offline) {
      hint = '在项目根目录打开命令行，执行下面这行，然后刷新页面：';
    }
    if (hint) { box.appendChild(el('p', { text: hint })); }
    if (err && err.offline) {
      box.appendChild(el('p', {}, [el('code', { text: 'python server/app.py' }),
        el('span', { class: 'muted small', text: '　启动后浏览器访问 http://127.0.0.1:8000' })]));
    }
    if (err && err.detail) {
      box.appendChild(el('pre', { class: 'code-view small', text: String(err.detail).slice(0, 1200) }));
    }
    return box;
  }

  function notice(text, kind) {
    return el('div', { class: 'notice' + (kind ? ' ' + kind : ''), text: text });
  }

  function loading(text) {
    return el('div', { class: 'card loading', html: '<span class="spin"></span>' +
      '<span>' + (text || '正在读取本机数据…') + '</span>' });
  }

  /* ---------------- 顶部导航 ---------------- */

  var NAV = [
    { key: 'index', text: '首页', href: '.' },
    { key: 'problems', text: '题库', href: 'problems' },
    { key: 'submissions', text: '我的提交', href: 'submissions' },
    { key: 'contest', text: '模拟赛', href: 'contest' }
  ];

  function initChrome(active) {
    var bar = document.getElementById('topbar');
    if (!bar) { return; }
    clear(bar);
    bar.className = 'topbar';
    var nav = el('nav', { class: 'nav' }, NAV.map(function (n) {
      return el('a', { href: n.href, text: n.text, class: n.key === active ? 'on' : '' });
    }));
    var stat = el('span', { class: 'nav-stat', id: 'navStat', text: '已解 —/—' });
    bar.appendChild(el('div', { class: 'topbar-in' }, [
      el('a', { class: 'brand', href: '.', text: '' }, [
        document.createTextNode('蓝桥杯 Python 模拟训练平台'),
        el('small', { text: '本机 · 离线可用' })
      ]),
      nav, stat
    ]));
    var ft = document.getElementById('foot');
    if (ft) {
      clear(ft);
      ft.className = 'footer';
      ft.textContent = '练习记录只保存在本机 data/oj.db，不上传任何地方。服务启动命令：python server/app.py';
    }
  }

  function setNavStat(solved, total) {
    var s = document.getElementById('navStat');
    if (s) { s.textContent = '已解 ' + (solved === null || solved === undefined ? '—' : solved) +
      '/' + (total === null || total === undefined ? '—' : total); }
  }

  /* ---------------- 草稿 ---------------- */

  function draftKey(pid) { return 'oj.draft.' + pid; }

  function saveDraft(pid, text) {
    try { localStorage.setItem(draftKey(pid), text); } catch (e) { /* 隐私模式下忽略 */ }
  }

  function loadDraft(pid) {
    try { return localStorage.getItem(draftKey(pid)) || ''; } catch (e) { return ''; }
  }

  function dropDraft(pid) {
    try { localStorage.removeItem(draftKey(pid)); } catch (e) { /* ignore */ }
  }

  /* ---------------- 其它 ---------------- */

  function store(key, val) {
    try {
      if (val === undefined) { return localStorage.getItem(key); }
      if (val === null) { localStorage.removeItem(key); }
      else { localStorage.setItem(key, val); }
    } catch (e) { /* ignore */ }
    return null;
  }

  function pySkeleton(problem) {
    var ex = (problem && problem.examples && problem.examples[0]) || null;
    var lines = [
      '# 本题骨架：从标准输入读数据，把答案打印到标准输出',
      '# 提交前记得删掉本行注释外的示例说明',
      'import sys',
      '',
      '',
      'def solve(data):',
      '    # TODO: 在这里写你的处理逻辑',
      '    return ""',
      '',
      '',
      'if __name__ == "__main__":',
      '    print(solve(sys.stdin.read()))',
      ''
    ];
    if (ex && ex.input) {
      lines.splice(5, 0, '样例输入：' + String(ex.input).trim().split('\n')[0],
        '样例输出：' + String(ex.output || '').trim().split('\n')[0], '');
    }
    return lines.join('\n');
  }

  window.OJ = {
    api: api, el: el, clear: clear, append: append, qs: qs,
    apiUrl: apiUrl, linkProblem: linkProblem, linkProblems: linkProblems,
    fmtTime: fmtTime, fmtClock: fmtClock, fmtMs: fmtMs, fmtDur: fmtDur, fmtScore: fmtScore,
    typeLabel: typeLabel, diffClass: diffClass, RESULT_LABEL: RESULT_LABEL,
    verdictClass: verdictClass, pillClass: pillClass, dotClass: dotClass,
    resultLabel: resultLabel, statusNode: statusNode,
    copyText: copyText, copyBlock: copyBlock, copyBtn: copyBlock,
    failBox: failBox, notice: notice, loading: loading,
    initChrome: initChrome, setNavStat: setNavStat,
    saveDraft: saveDraft, loadDraft: loadDraft, dropDraft: dropDraft, store: store,
    pySkeleton: pySkeleton
  };
})();
