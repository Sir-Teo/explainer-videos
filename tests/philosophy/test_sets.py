"""The set-theory Reasoner against known facts: Ackermann's bijection, the cumulative hierarchy, ordinal arithmetic,
Goodstein's sequences, Cantor's theorem, and the paradoxical decomposition of the free group."""

from explainer.philosophy.reasoner import sets as S


def test_ackermann_is_a_bijection():
    seen = set()
    for n in range(4096):
        s = S.ackermann_decode(n)
        assert S.ackermann_code(s) == n
        seen.add(s)
    assert len(seen) == 4096
    assert S.ackermann_code(S.von_neumann(3)) == 11


def test_hierarchy_and_ordinals():
    assert [len(S.V(k)) for k in range(5)] == [0, 1, 2, 4, 16]
    assert S.V_size(5) == 65536
    for n in range(6):
        o = S.von_neumann(n)
        assert len(o) == n and S.transitive(o) and S.rank(o) == n
    assert all(S.rank(x) < 4 for x in S.V(4))


def test_cantor():
    for n in (1, 2, 3):
        r = S.cantor_check(n)
        assert r["all_miss"] and r["functions"] == (2 ** n) ** n
    rows = [[0, 1, 1], [1, 1, 0], [0, 0, 0]]
    d = S.diagonal(rows)
    assert all(d[i] != rows[i][i] for i in range(3))
    assert all(S.cantor_unpair(S.cantor_pair(x, y)) == (x, y) for x in range(30) for y in range(30))
    q = S.calkin_wilf(200)
    assert len(set(q)) == 200 and all(__import__("math").gcd(a, b) == 1 for a, b in q)


def test_ordinal_arithmetic():
    w, one, two = S.OMEGA, S.ONE, S.Ord.nat(2)
    assert one + w == w and w < w + one
    assert two * w == w and w * two == w + w
    assert w * w == S.Ord.omega_power(two)
    assert S.Ord.nat(1000) < w < w * w < S.Ord.omega_power(w) < S.Ord.omega_tower(3)
    a = S.Ord.omega_power(two, 3) + w + S.Ord.nat(5)
    assert (a + S.Ord.omega_power(two)) == S.Ord.omega_power(two, 4)


def test_goodstein():
    g3 = S.goodstein(3, 10)
    assert [t["value"] for t in g3] == [3, 3, 3, 2, 1, 0]
    g4 = S.goodstein(4, 8)
    assert [t["value"] for t in g4] == [4, 26, 41, 60, 83, 109, 139, 173]
    for g in (g3, g4, S.goodstein(5, 12)):
        ords = [t["ordinal"] for t in g if t["value"] is not None]
        assert all(b < a for a, b in zip(ords, ords[1:]))


def test_free_group_paradox():
    r = S.paradoxical_check(6)
    assert r["W(a) + aW(A)"] and r["W(b) + bW(B)"]
    assert len(set(r["counts"].values())) == 1
    assert S.reduce_word("abBA") == ""


def test_generic_real():
    ground = [[0] * 8, [1] * 8, [0, 1] * 4, [1, 0] * 4, [0, 0, 1, 1] * 2]
    r = S.generic_real(ground, 10)
    assert r["differs"]
