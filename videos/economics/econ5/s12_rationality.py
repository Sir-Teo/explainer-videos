from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Rationality(VoiceoverScene):
    def construct(self):
        card(self, 10, r"What rationality does not assume", r"Selfish, calculating, human: which does it need?",
             "Chapter ten. What rationality does not assume.")
        self.notes()
        self.becker()

    def notes(self):
        st = load("studies")
        am = st["andreoni_miller"]
        h = st["harbaugh"]
        cards = point_cards([
            (r"not selfishness", rf"Andreoni and Miller (2002): \ {am['subjects']} people \\ sharing money at "
                                 rf"different prices of giving: \\ over {100 * am['consistent']:.0f}\% consistent; \ "
                                 rf"only a quarter selfish", PASS),
            (r"not calculation", r"children of seven \\ (Harbaugh et al., 2001); \ capuchin monkeys \\ trading tokens "
                                 r"for food \ (Chen et al., 2006)", IC),
            (r"not even a human", rf"rats and pigeons working levers: \ {100 * h['animals']['rats']:.0f}\% and "
                                  rf"{100 * h['animals']['pigeons']:.0f}\% \\ cut back when a price rose \\ with "
                                  r"income compensated \ (Kagel et al.)", E.ACCENT),
            (r"not fixed tastes for life", r"only that the choices compared \\ were made by the same tastes",
             GREY_B),
        ], width=12.6, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"Rational, \ in the economist's sense, \ means consistent", font_size=32).to_edge(UP,
                                                                                                    buff=0.45)
        tag = published_tag(r"Andreoni and Miller, Econometrica 70(2) (2002); Chen, Lakshminarayanan and Santos, JPE "
                            r"114(3) (2006); Kagel, Battalio and Green (1995)", corner=DR, font_size=12)
        with self.voiceover(
            "This changes what the word rational means. In economics it means consistent, and nothing more. So it "
            "doesn't assume several things it's often accused of. <bookmark mark='a'/> It doesn't assume "
            "selfishness. In 2002 James Andreoni and John Miller let a hundred and seventy-six people divide money "
            "between themselves and a stranger, with the price of giving varied from budget to budget. Over "
            "ninety-eight percent chose consistently, and only a quarter were purely selfish. Generosity can be "
            "perfectly rational. <bookmark mark='b'/> It doesn't assume calculation. Seven-year-olds are mostly "
            "consistent, and so are capuchin monkeys trading tokens for food, as Keith Chen, Venkat "
            "Lakshminarayanan and Laurie Santos found in 2006. <bookmark mark='c'/> It doesn't even assume a human. "
            "In experiments summarized by John Kagel, Raymond Battalio and Leonard Green, most rats and pigeons, "
            "pressing levers or pecking keys for food and drink, bought less of something when its price rose, even "
            "when they were given enough extra income to afford the old amount. <bookmark mark='d'/> And it "
            "doesn't assume tastes never change: only that the choices being compared were made by the same "
            "tastes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.1))
        self.clear_scene()

    def becker(self):
        be = load("becker")
        from explainer.ai.viz import axes

        ax = axes([0, 10], [0.5, 6.5], x_length=5.6, y_length=4.4, xticks=[0, 2, 4, 6, 8, 10],
                  yticks=[1, 2, 3, 4, 5, 6], xlabel=r"fish bought", ylabel=r"price of fish, \$", font_size=18,
                  center=LEFT * 3.0 + DOWN * 0.3)
        a = ax.ax
        prices = np.array(be["prices"])
        few = np.array(be["few"])
        cols = (GREY_B, "#9AA5B8", "#C9A0FF")
        people = VGroup()
        for k, q in enumerate(few):
            people.add(VGroup(*[Dot(a.c2p(min(x, 10), p), radius=0.06, color=cols[k]) for x, p in zip(q, prices)]),
                       VMobject(stroke_color=cols[k], stroke_width=1.5, stroke_opacity=0.6).set_points_as_corners(
                           [a.c2p(min(x, 10), p) for x, p in zip(q, prices)]))
        mean = VGroup(*[Dot(a.c2p(x, p), radius=0.1, color=E.ACCENT) for x, p in zip(be["mean"], prices)])
        ps = np.linspace(0.62, 6.5, 120)
        theory = VMobject(stroke_color=E.ACCENT, stroke_width=3).set_points_smoothly(
            [a.c2p(0.5 * be["income"] / p, p) for p in ps if 0.5 * be["income"] / p <= 10])
        rows = VGroup(
            label(r"Becker (1962): \ ``impulsive'' households", font_size=24, color=E.ACCENT),
            label(rf"each of {be['people']:,} islanders spends a share \\ of \${be['income']:.0f} on fish drawn at "
                  r"random, \\ whatever the price".replace(",", "{,}"), font_size=22),
            label(r"one islander's ``demand'': \ a zigzag", font_size=22, color=GREY_B),
            label(r"the average: \ half of \$12 on fish, \ $q = 6/p$: \\ a demand curve that slopes down",
                  font_size=22, color=E.ACCENT),
            label(r"a falling demand curve is no evidence \\ of rationality: \ budgets alone produce it; \\ "
                  r"consistency is what has to be tested", font_size=22, color=PASS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: Becker's random choosers on the Island", corner=DR, font_size=13)
        with self.voiceover(
            "If rationality is so little, does it explain anything? Gary Becker asked the question from the other "
            "side in 1962. <bookmark mark='a'/> Imagine households that don't maximize anything. "
            "<bookmark mark='b'/> On the Island, two thousand of them each spend a random share of twelve dollars on "
            "fish, whatever fish costs. <bookmark mark='c'/> Follow one of them as the price changes, and their "
            "demand jumps about with no pattern at all. <bookmark mark='d'/> But average them, and demand slopes "
            "neatly down: on average half the money goes on fish, so when fish costs more, fewer fish are bought. "
            "The budget does the work. <bookmark mark='e'/> So a falling demand curve tells you almost nothing about "
            "whether people are rational. Becker's point was that much of economics follows from budgets alone. "
            "What rationality adds is consistency, and that is the thing to test."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=E.ACCENT, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in people], lag_ratio=0.3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(m_, scale=1.4) for m_ in mean], lag_ratio=0.15), Create(theory),
                      FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
