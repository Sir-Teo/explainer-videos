"""Modal logic: parser, Kripke semantics, frame correspondence, bisimulation and the Peterson model checker."""

from explainer.philosophy.reasoner import modal as m


def test_parse_show():
    for s in ["[]p -> p", "<>p -> []<>p", "[]([]p -> p) -> []p", "~[]~p <-> <>p", "G p -> F p"]:
        f = m.parse(s)
        assert m.parse(m.show(f)) == f, m.show(f)


def test_duality_and_K_valid_everywhere():
    for R in m.all_frames(2):
        assert m.valid_on_frame(m.parse("[](p -> q) -> ([]p -> []q)"), R, 2)
        assert m.valid_on_frame(m.parse("<>p <-> ~[]~p"), R, 2)


def test_correspondence_on_three_worlds():
    counts = {"T": 64, "D": 343, "B": 64, "4": 171, "L": 19}
    for ax, n_valid in counts.items():
        r = m.correspondence(ax, 3)
        assert r["agree"] == r["frames"] == 512 and r["valid"] == n_valid, (ax, r)


def test_countermodel_and_model_finder():
    f = m.parse("[]p -> p")
    assert m.frame_countermodel(f, set(), 1) is not None          # the empty frame: []p holds, p need not
    assert m.find_model([m.parse("[]p"), m.parse("~p")], 2, m.reflexive) is None
    assert m.find_model([m.parse("[]p"), m.parse("~p")], 2) is not None


def test_bisimulation_minimize():
    # a 3-cycle of p-worlds is bisimilar to a single p-world with a loop
    M = m.Model([0, 1, 2], {(0, 1), (1, 2), (2, 0)}, {"p": {0, 1, 2}})
    blocks, Q = m.minimize(M)
    assert len(blocks) == 1 and Q.R == {(0, 0)}


def test_peterson():
    ok, trace, n = m.mutual_exclusion(m.peterson())
    assert ok and trace is None
    ok, trace, n = m.mutual_exclusion(m.peterson(broken=True))
    assert not ok and trace[-1][0] == 4 and trace[-1][1] == 4
    assert not m.fair_eg(m.peterson(), lambda s: s[0] in (1, 2, 3))     # no fair starvation
    st, ed = m.peterson().graph()
    assert m.ctl_eg(st, ed, {s for s in st if s[0] in (1, 2, 3)})        # unfair starvation exists


def test_tableau_against_frames():
    # the tableau's verdict for K agrees with brute-force validity on all frames of up to 2 worlds (a sanity check;
    # K's finite model property makes small frames representative for these formulas)
    for s in ["[](p -> q) -> ([]p -> []q)", "[]p -> p", "<>p & <>q -> <>(p & q)", "[]p -> [][]p",
              "[](p & q) <-> ([]p & []q)", "<>(p | q) <-> (<>p | <>q)", "[]p | []~p"]:
        f = m.parse(s)
        valid, _, M = m.tableau(f)
        brute = all(m.valid_on_frame(f, R, n) for n in (1, 2) for R in m.all_frames(n))
        if valid:
            assert brute, s
        else:
            assert not m.holds(f, M, 0), s
    assert m.tableau(m.parse("[]p -> p"), reflexive_=True)[0]
