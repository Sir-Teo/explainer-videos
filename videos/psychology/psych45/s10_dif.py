from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Dif(VoiceoverScene):
    def construct(self):
        self.card()
        self.impact()
        self.mh()

    def card(self):
        card = chapter_card(9, r"Fairness as a statistic", r"When is an item unfair?",
                            lit={1988: r"Holland \& Thayer"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter nine. Fairness as a statistic."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def impact(self):
        d = load("dif")
        head = heading(r"A gap is not a bias")
        A = axes([0, 15], [0, 1], x_length=5.6, y_length=3.2, xticks=[0, 5, 10, 15], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"total score (of 15)",
                 ylabel=r"P(item 8 right)", center=[-3.3, 0.3, 0], font_size=13)
        s = np.arange(16)
        g0 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.06, color=SYMP) for x, y in zip(s, d["by_score_none"][0])
                      if np.isfinite(y)])
        g1 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.06, color=PERSON) for x, y in zip(s, d["by_score_none"][1])
                      if np.isfinite(y)])
        key = VGroup(label(r"reference group", font_size=14, color=SYMP), label(r"focal group", font_size=14,
                                                                                color=PERSON)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ two groups of 3{,}000 whose mean abilities differ by 0.8 SD; \ 15 items, \ all perfectly fair", WHITE),
            (rf"on item 8 the groups' proportions correct differ by {d['gap_none']:.2f}: \ that is impact, \ a "
             rf"difference between the groups, \ not in the item", PERSON),
            (r"compare people of equal ability instead, \ matched on their total score: \ the two groups' curves lie "
             r"on top of each other", GOOD),
            (r"differential item functioning: \ people of equal ability, \ unequal chances", MODEL),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.mantel\_haenszel}, \ 6{,}000 simulated people")
        with self.voiceover(
            "When is an item unfair? <bookmark mark='a'/> Psyche makes two groups of three thousand whose mean "
            "abilities differ by zero point eight standard deviations, and fifteen items that are all perfectly fair. "
            "<bookmark mark='b'/> On item eight the groups' proportions correct differ by about fifteen points. That "
            "is impact: a difference between the groups, not in the item. <bookmark mark='c'/> So compare people of "
            "equal ability instead, matched on their total score. The two groups' curves lie on top of each other. "
            "<bookmark mark='d'/> An item is unfair, in the statistical sense, when people of equal ability have "
            "unequal chances. It's called differential item functioning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(g0), FadeIn(g1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mh(self):
        d = load("dif")
        head = heading(r"Mantel and Haenszel, \ score by score")
        eq = MathTex(r"\hat\alpha_{\mathrm{MH}} = \frac{\sum_s A_s D_s / N_s}{\sum_s B_s C_s / N_s}, \qquad "
                     r"\Delta = -2.35 \ln \hat\alpha_{\mathrm{MH}}", font_size=34, color=MODEL).move_to([0, 2.2, 0])
        A = axes([0, 15], [0, 1], x_length=5.6, y_length=3.0, xticks=[0, 5, 10, 15], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"total score (of 15)",
                 ylabel=r"P(item 8 right)", center=[-3.3, -0.6, 0], font_size=13)
        s = np.arange(16)
        g0 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.06, color=SYMP) for x, y in zip(s, d["by_score_dif"][0])
                      if np.isfinite(y)])
        g1 = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.06, color=PERSON) for x, y in zip(s, d["by_score_dif"][1])
                      if np.isfinite(y)])
        n, f = d["none"], d["dif"]
        rows = rows_of([
            (r"at each score, \ a two-by-two table: \ group by right or wrong; \ pool the odds ratios (Holland and "
             r"Thayer, \ 1988)", WHITE),
            (rf"the fair item: \ $\Delta = {n['delta']:.2f}$, \ $p = {n['p']:.2f}$: \ category {n['category']}, \ "
             rf"negligible", GOOD),
            (rf"now make item 8 harder by 0.8 for the focal group only: \ $\Delta = {f['delta']:.2f}$, \ category "
             rf"{f['category']}, \ flagged for review", AUTH),
            (r"a flag is a question for content experts, \ not a verdict: \ what in the item favours one group?", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.6, 0])
        tag = published_tag(r"Holland \& Thayer (1988)")
        with self.voiceover(
            "Testing companies screen every item this way. <bookmark mark='a'/> At each total score, make a two by "
            "two table, group by right or wrong, and pool the odds ratios across scores. Paul Holland and Dorothy "
            "Thayer brought Mantel and Haenszel's method to testing in 1988. <bookmark mark='b'/> On the fair item, "
            "the index is near zero: negligible. <bookmark mark='c'/> Now make item eight harder by zero point eight "
            "for the focal group only. The curves separate, and the index flags it in the most serious category. "
            "<bookmark mark='d'/> A flag is a question for content experts, not a verdict: what in this item favours "
            "one group?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(g0), FadeIn(g1))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
