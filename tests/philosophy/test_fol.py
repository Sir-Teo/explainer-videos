"""First-order logic: parser, satisfaction, the model finder and the tableau, against known validities."""

from explainer.philosophy.reasoner.fol import (Structure, check_fitch, countermodel, find_model, holds, parse, prove,
                                            show)


def test_parse_show():
    for s in ["forall x exists y L(x, y)", "exists x (D(x) -> forall y D(y))", "~(P(a) & Q(a)) | x = y"]:
        f = parse(s)
        assert parse(show(f)) == f, show(f)


def test_satisfaction():
    M = Structure(range(3), {"L": {(0, 1), (1, 2), (2, 0)}})
    assert holds(parse("forall x exists y L(x, y)"), M)
    assert not holds(parse("exists y forall x L(x, y)"), M)


def test_tableau_validities():
    assert prove([], parse("exists x (D(x) -> forall y D(y))")).closed          # the drinker
    horse = prove([parse("forall x (H(x) -> A(x))")],
                  parse("forall x ((exists y (Hd(x, y) & H(y))) -> exists y (Hd(x, y) & A(y)))"))
    assert horse.closed                                                        # De Morgan's horse heads
    barbara = prove([parse("forall x (M(x) -> P(x))"), parse("forall x (S(x) -> M(x))")],
                    parse("forall x (S(x) -> P(x))"))
    assert barbara.closed


def test_countermodels():
    cm = countermodel([parse("forall x exists y L(x, y)")], parse("exists y forall x L(x, y)"))
    assert cm is not None and len(cm.domain) == 2
    dar = countermodel([parse("forall x (M(x) -> P(x))"), parse("forall x (M(x) -> S(x))")],
                       parse("exists x (S(x) & P(x))"))
    assert dar is not None and not dar.preds.get("M")
    r = prove([parse("forall x (M(x) -> P(x))"), parse("forall x (M(x) -> S(x))")], parse("exists x (S(x) & P(x))"))
    assert not r.closed and (r.countermodel is not None or r.gave_up)


def test_tableau_soundness_fresh_witnesses():
    # an existential witness must be new: these are invalid, so the tableau must not close
    for ps, c in [(["exists x P(x)"], "forall x P(x)"), ([], "exists x P(x) -> P(a)"),
                  (["forall x exists y L(x, y)"], "exists y forall x L(x, y)")]:
        assert not prove([parse(p) for p in ps], parse(c), max_terms=5).closed


def test_fitch_quantifiers():
    # someone loved by all  =>  everyone loves someone
    good = [(0, "exists y forall x L(x, y)", "premise", []),
            (1, "forall x L(x, b)", "assume", []),
            (1, "L(a, b)", "allE", [2]),
            (1, "exists y L(a, y)", "exI", [3]),
            (1, "forall x exists y L(x, y)", "allI", [4]),
            (0, "forall x exists y L(x, y)", "exE", [1, (2, 5)])]
    assert check_fitch(good, goal="forall x exists y L(x, y)") == (True, "valid")
    # the converse: the generalization at line 4 is illegal (a is in the open assumption)
    bad = [(0, "forall x exists y L(x, y)", "premise", []),
           (0, "exists y L(a, y)", "allE", [1]),
           (1, "L(a, b)", "assume", []),
           (1, "forall x L(x, b)", "allI", [3])]
    ok, msg = check_fitch(bad)
    assert not ok and "line 4" in msg and "not arbitrary" in msg
    # existential elimination with a constant that escapes is rejected
    esc = [(0, "exists x P(x)", "premise", []),
           (1, "P(a)", "assume", []),
           (0, "P(a)", "exE", [1, (2, 2)])]
    assert not check_fitch(esc)[0]
    # Socrates
    soc = [(0, "forall x (H(x) -> M(x))", "premise", []), (0, "H(s)", "premise", []),
           (0, "H(s) -> M(s)", "allE", [1]), (0, "M(s)", "impE", [3, 2])]
    assert check_fitch(soc, goal="M(s)")[0]
    # from P(a) alone, 'everything is P' does not follow
    hasty = [(0, "P(a)", "premise", []), (0, "forall x P(x)", "allI", [1])]
    assert not check_fitch(hasty)[0]


def test_unify_and_resolution():
    from explainer.philosophy.reasoner.fol import parse_clause, resolution, resolution_proof, resolve_term, unify
    s = unify(parse("Knows(john, x)"), parse("Knows(y, mother(y))"))
    assert resolve_term("x", s) == ("f", "mother", ("john",)) and resolve_term("y", s) == "john"
    assert unify(parse("Knows(x, x)"), parse("Knows(y, mother(y))")) is None       # occurs check
    assert unify(parse("P(a)"), parse("P(b)")) is None
    cl = [parse_clause("~L(x, y) | L(z, x)"), parse_clause("L(romeo, juliet)"), parse_clause("~L(me, you)")]
    ok, der = resolution(cl)
    assert ok
    proof = resolution_proof(cl, der)
    assert proof[-1][1] == "□" and len(proof) == 6
    # a satisfiable set is not refuted
    ok, _ = resolution([parse_clause("P(x) | Q(x)"), parse_clause("~P(a)")], max_steps=200)
    assert not ok
    # the drinker, clausified: ~(D(x) -> D(f(x))) for all x, i.e. D(x) and ~D(f(x))
    ok, _ = resolution([parse_clause("D(x)"), parse_clause("~D(f(x))")])
    assert ok


def test_part3_problem_answers():
    cm = countermodel([parse("forall x (P(x) | Q(x))")], parse("forall x P(x) | forall x Q(x)"))
    assert cm is not None and len(cm.domain) == 2
    pf = [(0, "forall x (P(x) -> Q(x))", "premise", []), (0, "exists x P(x)", "premise", []),
          (1, "P(a)", "assume", []), (1, "P(a) -> Q(a)", "allE", [1]), (1, "Q(a)", "impE", [4, 3]),
          (1, "exists x Q(x)", "exI", [5]), (0, "exists x Q(x)", "exE", [2, (3, 6)])]
    assert check_fitch(pf, goal="exists x Q(x)") == (True, "valid")
