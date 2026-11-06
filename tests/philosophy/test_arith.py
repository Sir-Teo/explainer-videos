from explainer.philosophy.reasoner import arith as A


def test_q_computes_numerals():
    for a in range(4):
        for b in range(4):
            for op in "+*":
                steps = A.q_steps((op, A.numeral(a), A.numeral(b)))
                assert steps[-1][0] == A.numeral(a + b if op == "+" else a * b)
                assert all(ax in A.Q_AXIOMS for _, ax in steps[1:])
    assert [ax for _, ax in A.q_steps(("+", A.numeral(2), A.numeral(2)))[1:]] == ["Q5", "Q5", "Q4"]


def test_primitive_recursion_and_ackermann():
    assert A.PR_ADD(3, 4) == 7 and A.PR_MUL(3, 4) == 12 and A.PR_EXP(2, 10) == 1024
    assert A.PR_PRED(0) == 0 and A.PR_PRED(9) == 8 and A.PR_FACT(6) == 720
    for m in range(4):
        for n in range(5):
            assert A.ackermann(m, n) == A.ackermann_small(m, n)
    assert A.ackermann(4, 1) == 65533 and A.ackermann(4, 2) == ("tower", 5)


def test_beta_and_sunzi():
    assert A.crt(A.SUNZI) == (23, 105)
    for seq in ([2, 3, 5], [0, 0, 1], [4, 1, 4, 1]):
        c, d = A.beta_code(seq)
        assert [A.beta(c, d, i) for i in range(len(seq))] == seq


def test_godel_numbering_round_trip():
    assert A.godel_number("0=0") == 2 ** 21 * 3 ** 15 * 5 ** 21
    for f in ("0=0", "∀x(x+0=x)", "¬(S0=0)", "∃y(x=Sy)"):
        assert A.godel_decode(A.godel_number(f)) == f


def test_self_reference():
    assert A.quine_check()
    s = A.quine_sentence()
    assert A.quine_subject(s) == s
    g = A.diag(A.GODEL_TEMPLATE)
    assert A.diag_subject(g) == g


def test_miu_invariant():
    ts = {t for level in A.miu_theorems(6) for t in level}
    assert "MU" not in ts and all(t.count("I") % 3 for t in ts)


def test_busy_beavers():
    expected = {2: (6, 4), 3: (21, 5), 4: (107, 13)}
    for n, (steps, ones) in expected.items():
        r = A.run_tm(A.parse_tm(A.CHAMPIONS[n]))
        assert r["halted"] and (r["steps"], r["ones"]) == (steps, ones)
    s = A.busy_beaver_search(2, 50)
    assert s["machines"] == 12 ** 4 and s["max_steps"] == 6 and s["max_ones"] == 4


def test_ramsey_and_berry():
    assert A.mono_triangle_free(5) == 12 and A.mono_triangle_free(6) == 0
    assert A.berry(3) == 19


def test_provability_logic():
    for k in ("second", "godel_fixed", "henkin_fixed", "lob"):
        assert A.gl_valid(A.GL_FACTS[k], 3)[0], k
    assert not A.gl_valid(A.GL_FACTS["reflection"], 3)[0]


def test_bounded_truth():
    verdicts = [A.delta0_eval(s) for s, _ in A.DELTA0_EXAMPLES]
    assert verdicts == [True, False, True, True]
    assert not A.delta0_eval("∃p<97 (90<p ∧ ∀a<p ∀b<p ¬(a×b=p))")      # 91..96 are all composite
    assert A.delta0_eval("(1+1)×3=6") and A.delta0_eval("¬(SS0=S0)")
