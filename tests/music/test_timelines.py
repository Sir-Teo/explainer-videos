"""Monochord's timelines (Part 37): the measures against hand counts and Toussaint's published values.

    python -m pytest -q tests/music/test_timelines.py
"""

import numpy as np

from explainer.music.monochord import mathmusic as MM
from explainer.music.monochord import timelines as T

STD = T.TIMELINES["standard pattern (12)"]


def test_standard_pattern_is_the_major_scale_in_time():
    assert T.steps(STD) == [2, 2, 1, 2, 2, 2, 1]
    assert [r["steps"] for r in T.rotations(STD)][1] == [2, 1, 2, 2, 2, 1, 2]          # Dorian
    assert T.metrics(STD)["euclidean"] and MM.is_rotation([1 if c == "x" else 0 for c in STD], MM.euclid(7, 12))
    # the interval content of the diatonic scale, <2 5 4 3 6 1>: every distance with its own count (a deep set)
    ic = T.interval_content(STD)
    assert [ic[d] for d in range(1, 7)] == [2, 5, 4, 3, 6, 1] and len(set(ic.values())) == 6
    major = "x.x.xx.x.x.x"                                                           # C D E F G A B as pitch classes
    assert T.interval_content(major) == ic


def test_offbeatness_against_toussaint():
    assert T.offbeat_positions(12) == [1, 5, 7, 11] and T.offbeat_positions(16) == list(range(1, 16, 2))
    m = {k: T.metrics(v) for k, v in T.TIMELINES.items()}
    assert m["standard pattern (12)"]["offbeat"] == 3
    assert m["son clave (16)"]["offbeat"] == 1 and m["rumba clave (16)"]["offbeat"] == 2 and m["shiko (16)"]["offbeat"] == 0


def test_oddity_by_hand():
    m = {k: T.metrics(v) for k, v in T.TIMELINES.items()}
    assert m["son clave (16)"]["oddity"] and m["bossa nova (16)"]["oddity"]
    assert not m["standard pattern (12)"]["oddity"]           # strokes on pulses 5 and 11 face each other
    assert not m["gahu (16)"]["oddity"]


def test_evenness_order():
    m = {k: T.metrics(v)["evenness"] for k, v in T.TIMELINES.items() if k.endswith("(16)")}
    assert min(m, key=m.get) == "bossa nova (16)" and max(m, key=m.get) == "soukous (16)"
    assert T.metrics("x...x...x...x...")["evenness"] < 1e-9


def test_swap_distance_and_centrality():
    assert T.swap_distance(T.TIMELINES["son clave (16)"], T.TIMELINES["rumba clave (16)"]) == 1
    c = T.centrality()
    assert min(c, key=c.get) == "son clave (16)" and c["son clave (16)"] == 6
    # brute force: the swap distance is the fewest adjacent swaps, found by breadth-first search
    from collections import deque

    def bfs(a, b):
        seen, q = {a: 0}, deque([a])
        while q:
            x = q.popleft()
            if x == b:
                return seen[x]
            for i in range(len(x) - 1):
                if x[i] != x[i + 1]:
                    y = x[:i] + x[i + 1] + x[i] + x[i + 2:]
                    if y not in seen:
                        seen[y] = seen[x] + 1
                        q.append(y)
    for a in T.CLAVES[:3]:
        for b in T.CLAVES[3:]:
            assert bfs(T.TIMELINES[a], T.TIMELINES[b]) == T.swap_distance(T.TIMELINES[a], T.TIMELINES[b])


def test_hocket_and_interlock():
    mel = [72, 74, 76, 72]
    a, b = T.hocket(mel, [{72, 76}, {74}])
    assert a == [72, None, 76, 72] and b == [None, 74, None, None]
    A, B = T.interlock_melody([(0, 80), (3, 81)], 6, [50, 51])
    assert [i for i, _ in A] == [0, 2, 4] and [i for i, _ in B] == [1, 3, 5] and (3, 81) in B


def test_inherent_pattern_is_in_neither_part():
    target = [72, 74, 76, 79, 76, 74]
    a, b, t = T.design_inherent(target, [55, 59, 62, 57], 3)
    assert [p for _, p in T.inherent([a, b], 66)] == target
    assert [p for _, p in a if p > 66] != target and [p for _, p in b if p > 66] != target
    hi, lo = T.streams([(0, 70), (1, 50), (2, 71)], 60)
    assert hi == [(0, 70), (2, 71)] and lo == [(1, 50)]


def test_mbira_tine():
    assert abs(T.TINE[1] - (4.694 / 1.875) ** 2) < 0.01 and abs(T.TINE[2] - (7.855 / 1.875) ** 2) < 0.05
    y = T.mbira(392.0, 1.0, buzz=0.0)
    f = np.fft.rfftfreq(len(y), 1 / 48000)
    spec = np.abs(np.fft.rfft(y))
    assert abs(f[np.argmax(spec)] - 392.0) < 3.0
