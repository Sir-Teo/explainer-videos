"""Precompute everything in Part 22 of *Philosophy, Built* ("Possible Worlds").

    python -m videos.philosophy.philosophy22.compute            # everything missing (seconds)

Items:
    census      which modal principles fail in counterpart theory and in Kripke's semantics, over every small model
    humphrey    Lewis's islands: Humphrey, Nixon and their counterparts; five sentences, translated and evaluated
    cyclist     Quine's mathematical cyclist: de dicto true, de re false
    rigid       a name and a description across four worlds
    twod        the two-dimensional matrices of six sentences, and their classes
    aliens      ersatz descriptions undercount worlds with alien properties
    barcan      Wittgenstein's possible child, for the contingentist and the necessitist
    essence     the modal account of essence against Fine's examples
    cposs       counterpossibles with and without impossible worlds
    disp        finks, masks and the conditional analyses of fragility
    cfx         a counterfactual explanation of a credit decision: the closest worlds that flip it
    problog     the distribution semantics: probabilities over eight possible worlds
    pierre      the Price List for Kripke's puzzle about belief
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import worlds as Wd

CACHE = Cache("philosophy22")
load = CACHE.load

PIERRE = [
    ("D", r"disquotation: \ a sincere, \ reflective speaker who assents to `$p$' believes that $p$",
     prop.Var("D")),
    ("T", r"translation: \ a truth in French stays true translated into English", prop.Var("T")),
    ("R", r"Pierre is rational: \ he holds no contradictory beliefs he could detect by reflection", prop.Var("R")),
    ("M", r"`Londres' and `London' say the same: \ a name contributes only its bearer", prop.Var("M")),
]


def compute_pierre() -> dict:
    claims = {k: f for k, _, f in PIERRE}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _, _ in PIERRE]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in PIERRE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"census": Wd.census, "humphrey": Wd.humphrey, "cyclist": Wd.cyclist, "rigid": Wd.rigid, "twod": Wd.twod,
         "aliens": Wd.alien_properties, "barcan": Wd.barcan, "essence": Wd.essence, "cposs": Wd.counterpossibles,
         "disp": Wd.dispositions, "cfx": Wd.counterfactual_explanation, "problog": Wd.distribution_semantics,
         "pierre": compute_pierre}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
