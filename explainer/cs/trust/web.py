"""The web layer of Part 55: injection, and the parsing fix that closes it.

Two confusions of *code* and *data*, both run against the series' own instruments:

* **SQL injection** on Part 35's database (``explainer.cs.db.engine``).  A login query built by pasting the user's
  strings into SQL text lets the input reach the *parser* as code: a lone quote derails the tokenizer, and an
  unquoted field (``WHERE id = <input>``) lets ``id = id`` dissolve the filter so the whole table spills out.  The
  fix is Part 12's lesson: parse the query *template* once, then bind the user's values into the finished parse tree
  as literals, so data never reaches the parser at all.  The engine ships no placeholder syntax, so the binding
  (``prepare`` / ``bind``) lives here and never edits ``engine.py``.
* **XSS** on a tiny HTML templater: without escaping, a ``<script>`` in the data becomes a *script element* when the
  page is parsed; with ``html.escape`` the same bytes stay a text node.  We parse both outputs and count the live
  elements to show the trees differ.

After Saltzer & Schroeder (1975) and the OWASP injection canon; the parsing-fix framing follows the series' Part 12.
"""

from __future__ import annotations

import copy
import html
from html.parser import HTMLParser

from explainer.cs.db.engine import Database, parse, plan_query

# --------------------------------------------------------------------------------- the demo database

USERS = [
    (1, "alice", "pw-alice", "alice's diary"),
    (2, "admin", "hunter2-admin", "the root key"),
    (3, "bob", "pw-bob", "bob's diary"),
]


def demo_db() -> Database:
    """A three-row ``users`` table: ``(id, username, password, secret)``."""
    db = Database()
    db.create("users", ["id", "username", "password", "secret"], USERS)
    return db


# --------------------------------------------------------------------------------- vulnerable: string concatenation

def login_concat(db: Database, username: str, password: str) -> dict:
    """The classic mistake: build the SQL by pasting the strings in, then run it.

    Returns ``{"sql", "rows"}`` on a successful parse, or ``{"sql", "error"}`` when the input derails the
    tokenizer -- that error *is* the vulnerability's signature: the user's bytes were read as query syntax."""
    sql = ("SELECT id, username, secret FROM users "
           f"WHERE username = '{username}' AND password = '{password}'")
    try:
        rows = db.query(sql)
    except Exception as exc:                                   # the input reached the parser as code
        return {"sql": sql, "error": f"{type(exc).__name__}: {exc}", "rows": None}
    return {"sql": sql, "error": None, "rows": [list(r) for r in rows]}


def fetch_by_id_concat(db: Database, uid) -> dict:
    """An *unquoted* field pasted into the query -- the most dangerous context, since there is no quote to balance.

    ``uid = 2`` reads one row; ``uid = "id"`` turns the filter into ``WHERE id = id``, which the engine reads as a
    (self-)join condition and drops from the row filter, so every row's secret spills out."""
    sql = f"SELECT id, username, secret FROM users WHERE id = {uid}"
    try:
        rows = db.query(sql)
    except Exception as exc:
        return {"sql": sql, "error": f"{type(exc).__name__}: {exc}", "rows": None}
    return {"sql": sql, "error": None, "rows": [list(r) for r in rows]}


# --------------------------------------------------------------------------------- the fix: bind after parsing

# Placeholder sentinels.  A template is ordinary SQL with these in the value positions; ``prepare`` parses it once,
# ``bind`` drops the caller's values into the finished parse tree.  The sentinels are chosen never to collide with
# real data (NUL-delimited); binding matches them by position, not by re-parsing.
_STR_SENTINELS = ["\x00p0\x00", "\x00p1\x00", "\x00p2\x00", "\x00p3\x00"]
_NUM_SENTINELS = [999_000_001, 999_000_002, 999_000_003, 999_000_004]


def prepare(template: str):
    """Parse a query *template* once, into a fixed parse tree (an ``engine.Query``).  Value positions hold the
    sentinels above; the tree's shape is now frozen and no later input can change it."""
    return parse(template)


def _placeholders_in(query):
    """The sentinels appearing in ``query.where``, in left-to-right order -- the positional parameter order."""
    found = []
    for L, _op, R in query.where:
        for side in (L, R):
            if isinstance(side, tuple) and side[0] == "lit" and side[1] in _ALL_SENTINELS:
                found.append(side[1])
    return found


_ALL_SENTINELS = set(_STR_SENTINELS) | set(_NUM_SENTINELS)


def bind(query, params):
    """Return a copy of the parsed ``query`` with its placeholder literals replaced, in order, by ``params``.

    The values enter as finished ``("lit", value)`` nodes; they are never tokenized, so a value like
    ``' OR '1'='1`` is just a 12-character username string, not syntax."""
    q = copy.deepcopy(query)
    order = _placeholders_in(q)
    if len(order) != len(params):
        raise ValueError(f"template has {len(order)} placeholders, got {len(params)} params")
    repl = dict(zip(order, params))

    def sub(side):
        if isinstance(side, tuple) and side[0] == "lit" and side[1] in repl:
            return ("lit", repl[side[1]])
        return side

    q.where = [(sub(L), op, sub(R)) for (L, op, R) in q.where]
    return q


def login_param(db: Database, username: str, password: str) -> dict:
    """The same login, done safely: one fixed template, values bound after parsing."""
    tmpl = ("SELECT id, username, secret FROM users "
            f"WHERE username = '{_STR_SENTINELS[0]}' AND password = '{_STR_SENTINELS[1]}'")
    q = bind(prepare(tmpl), [username, password])
    rows = db.run(plan_query(db, q))
    return {"template": tmpl, "rows": [list(r) for r in rows]}


def fetch_by_id_param(db: Database, uid: int) -> dict:
    """The id lookup, done safely: the unquoted position is a bound parameter, so ``"id"`` would be a *value*."""
    tmpl = f"SELECT id, username, secret FROM users WHERE id = {_NUM_SENTINELS[0]}"
    q = bind(prepare(tmpl), [uid])
    rows = db.run(plan_query(db, q))
    return {"template": tmpl, "rows": [list(r) for r in rows]}


# --------------------------------------------------------------------------------- the report

def injection_report() -> dict:
    """Run the standard payloads through both the concatenation login and the bound login, and the ``id`` leak
    through both, reporting what each returns.  Keys: ``login`` (list of trials) and ``id_leak``."""
    db = demo_db()
    trials = []
    cases = [
        ("honest, correct", "admin", "hunter2-admin"),
        ("honest, wrong password", "admin", "nope"),
        ("tautology payload", "' OR '1'='1", "anything"),
        ("comment payload", "admin'--", "anything"),
    ]
    for label, u, p in cases:
        vuln = login_concat(db, u, p)
        safe = login_param(db, u, p)
        trials.append({
            "label": label, "username": u, "password": p,
            "concat_rows": vuln["rows"], "concat_error": vuln["error"],
            "param_rows": safe["rows"],
        })

    id_leak = {
        "concat_id_2": fetch_by_id_concat(db, 2),               # one row, as intended
        "concat_id_eq_id": fetch_by_id_concat(db, "id"),        # WHERE id = id -> the whole table leaks
        "param_value_id": _param_id_value(db),                  # "id" bound as data -> no leak
    }
    return {"login": trials, "id_leak": id_leak}


def _param_id_value(db: Database) -> dict:
    """Bind the literal value ``"id"`` into the id lookup: it is compared as data (no rows), nothing leaks."""
    tmpl = f"SELECT id, username, secret FROM users WHERE id = '{_STR_SENTINELS[0]}'"
    q = bind(prepare(tmpl), ["id"])
    rows = db.run(plan_query(db, q))
    return {"template": tmpl, "bound_value": "id", "rows": [list(r) for r in rows]}


# --------------------------------------------------------------------------------- XSS

class _Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def handle_data(self, data):
        self.text.append(data)


def _scan(doc: str) -> dict:
    s = _Scan()
    s.feed(doc)
    return {"tags": s.tags, "text": "".join(s.text)}


def render_comment(body: str, escape: bool) -> str:
    """A one-field HTML template.  With ``escape`` the body is ``html.escape``d; without, it is pasted raw."""
    value = html.escape(body) if escape else body
    return f"<div class=comment>{value}</div>"


def xss_report(payload: str = "<script>steal()</script>") -> dict:
    """Render the payload both ways and parse each result.  Unescaped, the ``<script>`` becomes a live element;
    escaped, it stays text.  Keys: ``payload``, ``raw``/``safe`` (each ``{html, tags, text}``), ``script_injected``."""
    raw = render_comment(payload, escape=False)
    safe = render_comment(payload, escape=True)
    raw_scan, safe_scan = _scan(raw), _scan(safe)
    return {
        "payload": payload,
        "raw": {"html": raw, **raw_scan},
        "safe": {"html": safe, **safe_scan},
        "script_injected": {"raw": "script" in raw_scan["tags"], "safe": "script" in safe_scan["tags"]},
    }
