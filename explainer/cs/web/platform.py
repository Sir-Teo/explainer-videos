"""The rest of the web platform (Part 42): WCAG contrast from sRGB, the same-origin policy and CORS decisions, an HTTP
cache with freshness and revalidation, the critical rendering path as a dependency graph, and Cumulative Layout
Shift."""

from __future__ import annotations

from urllib.parse import urlsplit


# ---------------------------------------------------------------- contrast

def _lin(c8: int) -> float:
    c = c8 / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcol: str) -> float:
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def wcag(ratio: float):
    return {"AA text": ratio >= 4.5, "AA large": ratio >= 3.0, "AAA text": ratio >= 7.0}


def grey_threshold(bg="#ffffff", need=4.5):
    """The lightest grey text that still passes on bg."""
    best = None
    for v in range(256):
        c = f"#{v:02x}{v:02x}{v:02x}"
        if contrast(c, bg) >= need:
            best = c
    return best


# ---------------------------------------------------------------- origins

def origin(url: str):
    """Tuple origins for HTTP(S)/WebSocket URLs; None for this model's opaque origins."""
    u = urlsplit(url)
    defaults = {"http": 80, "https": 443, "ws": 80, "wss": 443}
    if u.scheme not in defaults or u.hostname is None:
        return None
    port = u.port if u.port is not None else defaults[u.scheme]
    return (u.scheme, u.hostname, port)


def same_origin(a: str, b: str) -> bool:
    oa = origin(a)
    return oa is not None and oa == origin(b)


def _serialized_origin(url: str) -> str:
    o = origin(url)
    if o is None:
        return "null"
    scheme, host, port = o
    host = f"[{host}]" if ":" in host else host
    default = 443 if scheme in ("https", "wss") else 80
    return f"{scheme}://{host}" + (f":{port}" if port != default else "")


def site(url: str):
    """Registrable domain, simplified to the last two labels (the real rule uses the Public Suffix List)."""
    u = urlsplit(url)
    return (u.scheme, ".".join(u.hostname.split(".")[-2:]))


def cors(page: str, target: str, method="GET", headers=(), allow_origin=None, allow_methods=(),
         allow_headers=(), credentials=False, allow_credentials=False):
    """What the browser does with a fetch from page to target: send it simply, send a preflight, and whether the
    script may read the response."""
    if same_origin(page, target):
        return {"preflight": False, "readable": True, "why": "same origin"}
    simple = method in ("GET", "HEAD", "POST") and all(h.lower() in ("accept", "accept-language", "content-language",
                                                                      "content-type") for h in headers)
    o = _serialized_origin(page)
    origin_allowed = allow_origin == o or (allow_origin == "*" and not credentials)
    if not simple:
        if not origin_allowed or (credentials and not allow_credentials) or (method not in allow_methods and
                                                                          method not in ("GET", "HEAD", "POST")):
            return {"preflight": True, "readable": False, "why": "preflight refused; the request is never sent"}
        if any(h.lower() not in [x.lower() for x in allow_headers] for h in headers):
            return {"preflight": True, "readable": False, "why": "a header was not allowed"}
    ok = origin_allowed
    if credentials and not allow_credentials:
        ok = False
    return {"preflight": not simple, "readable": ok,
            "why": "allowed" if ok else "sent, but the response is withheld from the script"}


# ---------------------------------------------------------------- HTTP cache

def cache_sim(requests, max_age=60, swr=0, etag_changes=()):
    """requests: times (s) at which the page asks for one resource.  Cache-Control: max-age (and optionally
    stale-while-revalidate); revalidation with If-None-Match returns 304 unless the content changed."""
    stored = None             # (time stored, etag)
    version = 0
    out = []
    for t in requests:
        while version < len(etag_changes) and etag_changes[version] <= t:
            version += 1
        if stored is None:
            out.append((t, "miss: 200, full body"))
            stored = (t, version)
            continue
        age = t - stored[0]
        if age < max_age:
            out.append((t, "fresh: served from cache, no request"))
        elif age < max_age + swr:
            out.append((t, "stale: served from cache, revalidated in the background"))
            stored = (t, version)
        elif stored[1] == version:
            out.append((t, "revalidate: 304 Not Modified, headers only"))
            stored = (t, version)
        else:
            out.append((t, "revalidate: 200, changed body"))
            stored = (t, version)
    return out


# ---------------------------------------------------------------- critical rendering path

def critical_path(resources):
    """resources: name -> (fetch ms, parse/exec ms, blocking dependencies).  First paint waits for every
    render-blocking resource; the critical path is the longest chain."""
    done = {}

    def fin(n):
        if n not in done:
            f, e, deps = resources[n]
            start = max([fin(d) for d in deps] or [0.0])
            done[n] = start + f + e
        return done[n]
    for n in resources:
        fin(n)
    path, n = [], max(done, key=done.get)
    while True:
        path.append(n)
        deps = resources[n][2]
        if not deps:
            break
        n = max(deps, key=lambda d: done[d])
    return {"finish": done, "path": path[::-1], "first_paint": max(done.values())}


def cls(shifts):
    """Cumulative Layout Shift: each shift scores impact fraction times distance fraction; shifts are grouped in
    session windows (gap under 1 s, window under 5 s) and the worst window is the score."""
    windows, cur, start, last = [], 0.0, None, None
    for t, impact, dist in shifts:
        if start is None or t - last >= 1.0 or t - start >= 5.0:
            if start is not None:
                windows.append(cur)
            cur, start = 0.0, t
        cur += impact * dist
        last = t
    if start is not None:
        windows.append(cur)
    return {"windows": windows, "score": max(windows) if windows else 0.0}


# ---------------------------------------------------------------- mobile radio energy

LTE = {"promotion_s": 0.26, "promotion_w": 1.2, "active_w": 1.3, "tail_s": 11.6, "tail_w": 1.06}
"""Parameters of the LTE radio-state model, rounded from Huang et al., MobiSys 2012 (promotion about 0.26 s, a tail
of about 11.6 s at about 1.06 W before the radio returns to idle)."""


def radio_energy(times, transfer_s=0.3, p=LTE):
    """Energy (J) for transfers starting at the given times: each burst pays a promotion if the radio is idle, then
    transfer time at active power, then the tail, which a later transfer can cut short."""
    times = sorted(times)
    e, end_tail = 0.0, -1e9
    timeline = []
    for k, t in enumerate(times):
        if t >= end_tail:
            e += p["promotion_s"] * p["promotion_w"]
            start = t + p["promotion_s"]
            timeline.append(("promote", t, start))
        else:
            start = t
        e += transfer_s * p["active_w"]
        fin = start + transfer_s
        nxt = times[k + 1] if k + 1 < len(times) else None
        tail_end = fin + p["tail_s"]
        if nxt is not None and nxt < tail_end:
            e += max(0.0, nxt - fin) * p["tail_w"]
            timeline.append(("active", start, fin))
            timeline.append(("tail", fin, max(fin, nxt)))
        else:
            e += p["tail_s"] * p["tail_w"]
            timeline.append(("active", start, fin))
            timeline.append(("tail", fin, tail_end))
        end_tail = tail_end
    return {"joules": e, "timeline": timeline}


def batching(n=10, period=20.0):
    spread = radio_energy([k * period for k in range(n)])
    batched = radio_energy([0.0 + 0.01 * k for k in range(n)])
    return {"spread_J": spread["joules"], "batched_J": batched["joules"], "ratio": spread["joules"] /
            batched["joules"], "spread": spread["timeline"], "batched": batched["timeline"]}
