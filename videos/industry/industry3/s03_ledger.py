from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403

LEFT_ACCTS = ["Cash", "Oven", "Flour", "Owed by the cafe"]
RIGHT_ACCTS = ["Bank loan", "Owed to the miller", "Owner's money", "Profit so far"]


class Ledger(VoiceoverScene):
    def construct(self):
        card(self, 2, "A bakery's books", "What does writing everything down twice actually do?",
             "Chapter two. A bakery's books.", lit=("dollar",))
        self.books()

    def books(self):
        B = R["bakery"]
        E = B["entries"]
        panels = VGroup(
            RoundedRectangle(corner_radius=0.12, width=5.9, height=3.9, fill_color=I.PANEL, fill_opacity=1,
                             stroke_color=OWN, stroke_width=1.5).move_to(np.array([-3.25, -0.35, 0])),
            RoundedRectangle(corner_radius=0.12, width=5.9, height=3.9, fill_color=I.PANEL, fill_opacity=1,
                             stroke_color=OWE, stroke_width=1.5).move_to(np.array([3.25, -0.35, 0])))
        heads = VGroup(TB("What the bakery has", 24, OWN).next_to(panels[0], UP, buff=0.12),
                       TB("Where the money came from", 24, OWE).next_to(panels[1], UP, buff=0.12))
        rows, vals = {}, {}
        glyph = {"Cash": draw.coin(0.16), "Oven": _oven(), "Flour": _sack(), "Owed by the cafe": _cup(),
                 "Bank loan": _bank(), "Owed to the miller": draw.factory(0.5, color="#C9A26B"),
                 "Owner's money": draw.person(0.4), "Profit so far": draw.coin_stack(4, 0.13)}
        for side, accts in ((0, LEFT_ACCTS), (1, RIGHT_ACCTS)):
            for k, a in enumerate(accts):
                y = 1.05 - k * 0.62
                x = -3.25 if side == 0 else 3.25
                g_ = glyph[a]
                g_.scale_to_fit_height(min(g_.height, 0.36)).move_to(np.array([x - 2.45, y, 0]))
                rows[a] = VGroup(g_, T(a, 22, I.TEXT).move_to(np.array([x - 2.1, y, 0]), aligned_edge=LEFT))
                vals[a] = TB("0", 22, I.TEXT).move_to(np.array([x + 2.6, y, 0]), aligned_edge=RIGHT)
        tl = VGroup(T("Total", 22, I.DIM).move_to(np.array([-5.85, -1.85, 0]), aligned_edge=LEFT),
                    T("Total", 22, I.DIM).move_to(np.array([0.65, -1.85, 0]), aligned_edge=LEFT))
        tv = [TB("$0", 26, I.ACCENT).move_to(np.array([-0.65, -1.85, 0]), aligned_edge=RIGHT),
              TB("$0", 26, I.ACCENT).move_to(np.array([5.85, -1.85, 0]), aligned_edge=RIGHT)]
        rule = VGroup(Line(np.array([-5.9, -1.5, 0]), np.array([-0.6, -1.5, 0]), color=I.EDGE),
                      Line(np.array([0.6, -1.5, 0]), np.array([5.9, -1.5, 0]), color=I.EDGE))
        memo = T("", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = estimate_tag("illustrative: a model bakery, explainer/industry/works/firm.py", corner=DR)

        def value(entry, acct):
            bal = entry["balances"]
            if acct == "Profit so far":
                return bal.get("Sales", 0) - bal.get("Flour used", 0) - bal.get("Wages", 0)
            return bal.get(acct, 0)

        say = [
            "The owner puts in her savings, forty thousand dollars. The bakery now has forty thousand of cash, "
            "and that cash came from her.",
            "The bank lends twenty thousand. More cash, and a debt to the bank on the other side.",
            "She buys an oven for forty-five thousand. Cash goes down, an oven goes up. Nothing new came in from "
            "anyone, so the right-hand side does not move.",
            "The miller delivers three thousand dollars of flour, to be paid in thirty days. Flour on one side, a "
            "debt to the miller on the other.",
            "She bakes, and sells six thousand dollars of bread for cash...",
            "...and three thousand to a cafe that will pay next month. Where did that nine thousand come from? From "
            "her customers, and it belongs to her: profit, on the owner's side.",
            "But the bread used the flour, three thousand dollars of it. The flour is gone, and the profit is three "
            "thousand smaller.",
            "And she pays her baker four thousand in wages. Cash down, profit down.",
        ]
        with self.voiceover(
            "Let's keep the books of a small business ourselves. A woman opens a bakery. <bookmark mark='a'/> On the "
            "left, everything the bakery has. On the right, where the money for it came from: borrowed, owed, or put "
            "in by the owner. Pacioli's rule is that every entry changes the two sides by the same amount, or moves "
            "money within one side, so the totals always match."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(panels), FadeIn(heads), FadeIn(VGroup(*rows.values())), FadeIn(VGroup(*vals.values())),
                      FadeIn(tl), FadeIn(rule), FadeIn(VGroup(*tv)))
        for e, line in zip(E, say):
            touched = {e["debit"], e["credit"]}
            if touched & {"Sales", "Flour used", "Wages"}:
                touched = (touched - {"Sales", "Flour used", "Wages"}) | {"Profit so far"}
            with self.voiceover(line):
                new_memo = T(e["memo"] + f":  ${e['amount']:,.0f}", 24, I.TEXT).to_edge(UP, buff=0.35)
                anims = [Transform(memo, new_memo)]
                for a in touched:
                    v = value(e, a)
                    anims.append(Transform(vals[a], TB(f"{v:,.0f}", 22, I.ACCENT).move_to(vals[a], aligned_edge=RIGHT)))
                anims += [Transform(tv[0], TB(f"${e['assets']:,.0f}", 26, I.ACCENT).move_to(tv[0], aligned_edge=RIGHT)),
                          Transform(tv[1], TB(f"${e['liabilities'] + e['equity']:,.0f}", 26, I.ACCENT).move_to(
                              tv[1], aligned_edge=RIGHT))]
                self.play(*anims, *[Indicate(rows[a], color=I.ACCENT, scale_factor=1.05) for a in touched])
                for a in touched:
                    vals[a].set_color(I.TEXT)
            assert abs(e["assets"] - e["liabilities"] - e["equity"]) < 1e-6
        last = E[-1]
        with self.voiceover(
            f"Eight entries, and the two sides still agree: {say_usd(last['assets'])} of things on the left, and "
            f"{say_usd(last['assets'])} of claims on them on the right. The left side is the bakery's assets. The "
            "right side is its liabilities, what it owes, and its equity, what belongs to the owner, including the "
            f"{say_usd(B['profit'])} of profit so far. That balance is not luck. It is how the system is built, and "
            "it is why a company's balance sheet always balances."
        ):
            self.play(Indicate(VGroup(tv[0], tv[1]), color=I.ACCENT, scale_factor=1.15))
            self.play(Transform(heads[0], TB("Assets", 26, OWN).move_to(heads[0])),
                      Transform(heads[1], TB("Liabilities and equity", 26, OWE).move_to(heads[1])))
        self.clear_scene()


def _oven() -> VGroup:
    body = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.4, stroke_width=0, fill_color="#8C929B",
                            fill_opacity=1)
    door = RoundedRectangle(corner_radius=0.03, width=0.34, height=0.18, stroke_width=0, fill_color="#F2A65A",
                            fill_opacity=0.9).move_to(body).shift(DOWN * 0.04)
    pipe = Rectangle(width=0.08, height=0.14, stroke_width=0, fill_color="#8C929B", fill_opacity=1).next_to(
        body, UP, buff=0).shift(RIGHT * 0.15)
    return VGroup(body, door, pipe)


def _sack() -> VGroup:
    bag = Polygon([-0.2, -0.22, 0], [0.2, -0.22, 0], [0.24, 0.1, 0], [0.12, 0.2, 0], [-0.12, 0.2, 0], [-0.24, 0.1, 0],
                  stroke_width=0, fill_color="#E8DCC2", fill_opacity=1)
    tie = Line([-0.1, 0.18, 0], [0.1, 0.18, 0], stroke_color="#A0855B", stroke_width=3)
    return VGroup(bag, tie)


def _cup() -> VGroup:
    cup = Polygon([-0.16, 0.16, 0], [0.16, 0.16, 0], [0.12, -0.18, 0], [-0.12, -0.18, 0], stroke_width=0,
                  fill_color="#C9D3E0", fill_opacity=1)
    handle = Arc(radius=0.08, start_angle=-PI / 2, angle=PI, stroke_color="#C9D3E0", stroke_width=3).move_to(
        [0.19, 0.0, 0])
    steam = VGroup(*[Line([x, 0.2, 0], [x + 0.03, 0.32, 0], stroke_color="#8C929B", stroke_width=2) for x in (-0.06, 0.05)])
    return VGroup(cup, handle, steam)


def _bank() -> VGroup:
    roof = Polygon([-0.28, 0.12, 0], [0.28, 0.12, 0], [0, 0.28, 0], stroke_width=0, fill_color="#C9D3E0", fill_opacity=1)
    cols = VGroup(*[Rectangle(width=0.06, height=0.24, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to(
        [x, -0.02, 0]) for x in (-0.18, -0.06, 0.06, 0.18)])
    base = Rectangle(width=0.56, height=0.06, stroke_width=0, fill_color="#C9D3E0", fill_opacity=1).move_to([0, -0.17, 0])
    return VGroup(roof, cols, base)
