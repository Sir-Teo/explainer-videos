from explainer.philosophy.reasoner import truth as Tr


def test_least_fixed_point_and_grounding():
    lfp = Tr.least_fixed_point(Tr.WORLD)
    assert lfp["s5"] == "t" and lfp["s4"] == "t" and lfp["s9"] == "t"
    assert lfp["L"] == lfp["H"] == lfp["s8"] == lfp["s10"] == "n"
    assert len(Tr.kripke_stages(Tr.WORLD)) == 4          # three jumps, then nothing changes


def test_fixed_points_and_classification():
    fps = Tr.fixed_points(Tr.WORLD)
    assert len(fps) == 3                                  # the truth-teller may be t, f or n
    assert all(fp["L"] == "n" and fp["A"] == "n" for fp in fps)
    c = Tr.classify(Tr.WORLD)
    assert c["L"] == c["A"] == c["B"] == c["s8"] == "paradoxical"
    assert c["H"] == c["s13"] == "ungrounded" and c["s5"] == "grounded"


def test_revision():
    v = Tr.revision_verdicts(Tr.WORLD)
    assert v["L"] == "unstable" and v["H"] == "depends"
    assert v["s8"] == "stably true"                       # 'the liar is true or not' is categorically true
    seq = Tr.revision(Tr.WORLD, {n: False for n in Tr.WORLD}, 4)
    assert [h["L"] for h in seq] == [False, True, False, True, False]


def test_yablo_and_exam():
    for n in range(1, 7):
        sols = Tr.yablo_solutions(n)
        assert len(sols) == 1 and sols[0][f"Y{n}"] and not any(sols[0][f"Y{k}"] for k in range(1, n))
    assert Tr.surprise_exam(5) == [5, 4, 3, 2, 1]


def test_revenge_grelling_moore():
    assert Tr.all_fixed_points(Tr.REVENGE) == []                   # the exclusion liar has no fixed point
    assert [h["R"] for h in Tr.iterate(Tr.REVENGE, 4)] == ["n", "t", "f", "t", "f"]
    g = Tr.grelling()
    assert g["table"]["short"] == "autological" and g["table"]["long"] == "heterological"
    assert g["heterological_consistent"] == []
    m = Tr.moore()
    assert m["said_satisfiable"] and not m["believed_satisfiable"]


def test_tarski_st_exam_programs():
    ss = Tr.tarski_sentences(2)
    assert Tr.tarski_true(("some", "x", ("White", "x"))) and not Tr.tarski_true(("all", "x", ("White", "x")))
    assert all(Tr.tarski_true(f) != Tr.tarski_true(("not", f)) for f in ss)        # bivalent, as Tarski's is
    st = Tr.st_demo()
    assert st["proves_L"] and st["L_entails_q"] and not st["proves_q"]              # cut fails in ST
    assert Tr.exam_announcements(5) == [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3], [1, 2], [1], []]
    assert Tr.surprise_holds(3, {1, 2, 3, 4})                                       # Wednesday is still a surprise
    runs = Tr.run_definitions()
    lfp = Tr.least_fixed_point(Tr.WORLD)
    assert all((runs[n] == "never returns") == (lfp[n] == "n") for n in Tr.WORLD)
