from explainer.philosophy.reasoner import dl as D


def test_family_subsumptions():
    q = D.family_demo()["queries"]
    assert q["Mother is a Parent"]["subsumed"] and q["Grandmother is a Parent"]["subsumed"]
    assert not q["Parent is a Mother"]["subsumed"] and q["Parent is a Mother"]["model"] is not None
    assert not q["Father is a Woman"]["subsumed"]


def test_basic_tableau():
    assert not D.satisfiable(D.And("A", D.Not("A")))["satisfiable"]
    assert not D.satisfiable(D.And(D.Some("r", "A"), D.All("r", D.Not("A"))))["satisfiable"]
    assert D.satisfiable(D.Or(D.And("A", D.Not("A")), "B"))["satisfiable"]
    assert D.nnf(D.Not(D.Some("r", D.And("A", "B")))) == ("all", "r", ("or", ("not", "A"), ("not", "B")))


def test_ontoclean_flags():
    o = D.ontoclean()
    bad = {(r["sub"], r["sup"]) for r in o["report"] if not r["ok"]}
    assert bad == {("Person", "Legal agent"), ("Apple", "Food"), ("Physical object", "Amount of matter")}


def test_transe_answers_everything():
    t = D.transe(epochs=1500)
    assert t["tokyo_in"][0][0] == "Asia"
    assert t["possible_triples"] == 512 and len(t["europe_capital_of"]) == 3


def test_abox_open_world():
    ans = {(a["ind"], a["concept"]): a["answer"] for a in D.abox_demo()["answers"]}
    assert ans[("Mary", "Grandmother")] == "yes" and ans[("Tom", "Parent")] == "yes"
    assert ans[("Tom", "Father")] == "unknown" and ans[("Ann", "Man")] == "no"
