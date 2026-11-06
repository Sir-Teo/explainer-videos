"""Part 12's Reasoner: epistemic models, announcements, common knowledge, agreement, and networks of inquiry."""

from fractions import Fraction

from explainer.philosophy.reasoner import epistemic as Ep


def test_muddy_children():
    r = Ep.muddy_rounds(3, (1, 1, 0))
    assert r["knows_at"][:2] == [2, 2] and r["sizes"][:2] == [8, 7]
    r8 = Ep.muddy_rounds(8, (1, 1, 1, 0, 0, 1, 0, 1))
    assert all(r8["knows_at"][i] == 5 for i in (0, 1, 2, 5, 7))
    assert Ep.without_father(3)
    e = Ep.everyone_knew_already(3, (1, 1, 0))
    assert e["everyone_knows"] and not e["common"] and e["after"]


def test_coordinated_attack_and_email_game():
    rows = Ep.attack_depth(6)
    assert [r["depth"] for r in rows[1:]] == list(range(6)) and not any(r["common"] for r in rows)
    assert Ep.email_game()["final"] == ([], [])


def test_agreement_fitch_moore_private():
    g = Ep.GP_EXAMPLE
    d = Ep.agreement_dialogue(g["states"], g["prior"], g["A"], g["B"], g["event"], g["actual"])
    assert d[0]["A"] != d[0]["B"] and d[-1]["A"] == d[-1]["B"] == Fraction(1, 3)
    f = Ep.fitch_check()
    assert f["valid_in_T"] and not f["valid_in_K"]
    m = Ep.moore_update()
    assert m["before"] and not m["after"] and m["b_knows_after"]
    p = Ep.private_update()
    assert p["a_knows_p"] and not p["b_knows_p"] and p["b_thinks_a_ignorant"] and not p["common_p"]


def test_crowds_and_networks():
    d = Ep.diversity(Ep.ox_guesses(), 1198)
    assert d["identity"] and d["crowd_error"] < d["average_error"]
    z = Ep.zollman(runs=60, seed=1)
    assert z["cycle"]["right"] > z["complete"]["right"]
    assert z["cycle"]["mean_rounds"] > z["complete"]["mean_rounds"]
