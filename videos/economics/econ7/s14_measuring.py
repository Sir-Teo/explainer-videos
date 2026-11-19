from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Measuring(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Measuring it", r"How do economists measure risk preferences, and how far can the "
             r"measurements be trusted?", "Chapter twelve. Measuring it.", lit={2002: r"Holt and Laury's menu"},
             scale=("person",), horizon=("a day",))
        self.menu()
        self.stakes()
        self.island()
        self.surveys()
        self.called()

    def menu(self):
        m = load("measuring")
        head = VGroup(label(r"", font_size=20), label(r"option A", font_size=23, color=SAFE),
                      label(r"option B", font_size=23, color=RISKY), label(r"A $-$ B, on average", font_size=21,
                                                                           color=GREY_B))
        xs = [-5.6, -2.9, 0.6, 3.8]
        rows = VGroup()
        for r in m["menu"]:
            k, p = r["k"], r["p"]
            pa = rf"{k}/10"
            rr = VGroup(label(rf"{k}", font_size=22, color=GREY_B),
                        label(rf"{pa} of \$2.00, \ else \$1.60", font_size=21, color=SAFE),
                        label(rf"{pa} of \$3.85, \ else \$0.10", font_size=21, color=RISKY),
                        label(rf"{r['ev_a'] - r['ev_b']:+.2f}".replace("-", "{-}"), font_size=22,
                              color=SAFE if r["ev_a"] > r["ev_b"] else RISKY))
            rows.add(rr)
        for j, c in enumerate(head):
            c.move_to([xs[j], 3.3, 0])
        for i, rr in enumerate(rows):
            for j, c in enumerate(rr):
                c.move_to([xs[j], 2.75 - 0.43 * i, 0])
        neutral = SurroundingRectangle(VGroup(rows[3], rows[4]), color=GREY_B, buff=0.05, stroke_width=1.5)
        nl = label(r"a risk-neutral chooser \\ switches here", font_size=19, color=GREY_B).next_to(neutral, RIGHT,
                                                                                                 buff=0.25)
        iv = m["intervals"]
        bottom = VGroup(
            label(r"the number of safe choices brackets $\gamma$ (CRRA over the prizes):", font_size=24),
            label(rf"4: \ {iv['4'][0]:.2f} to {iv['4'][1]:.2f} \qquad 5: \ {iv['5'][0]:.2f} to {iv['5'][1]:.2f} "
                  rf"\qquad 6: \ {iv['6'][0]:.2f} to {iv['6'][1]:.2f} \qquad 7: \ {iv['7'][0]:.2f} to "
                  rf"{iv['7'][1]:.2f}", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Holt and Laury, AER (2002)", corner=DR, font_size=14)
        with self.voiceover(
            "How do you measure someone's risk aversion? The most used tool is a menu designed by Charles Holt and "
            "Susan Laury in 2002. <bookmark mark='a'/> Ten rows, each a choice between a safe option A, which pays two "
            "dollars or one sixty, and a risky option B, which pays three eighty-five or ten cents. Row by row, the "
            "chance of the high prize rises from a tenth to certainty. One row is chosen at random and paid for real. "
            "<bookmark mark='b'/> At the top, A is better on average; from row five down, B is. A risk-neutral "
            "chooser makes four safe choices and switches. <bookmark mark='c'/> The more safe choices before the "
            "switch, the more risk averse the chooser, and the row of the switch brackets gamma: four safe choices "
            "means roughly risk neutral, five means a gamma between about nought point one five and nought point "
            "four one, six between nought point four one and nought point six eight."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:3])) for r_ in rows], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[3]) for r_ in rows], lag_ratio=0.1), Create(neutral), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(bottom))
        self.clear_scene()

    def stakes(self):
        t = load("measuring")["table"]
        ax = plane([0, 4], [3, 8], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.8, y_length=4.8, xticks=[],
                   yticks=[4, 5, 6, 7, 8], xlabel=r"", ylabel=r"average safe choices, \ of 10", font_size=17)
        a = ax.ax
        scales = [1, 20, 50, 90]
        real, hyp, scale_l = VGroup(), VGroup(), VGroup()
        for i, s in enumerate(scales):
            for key, col, dx, grp in (("real_2002", SAFE, -0.17, real), ("hypothetical_2002", GREY_B, 0.17, hyp)):
                v = t[key].get(str(s), t[key].get(s))
                if v is None:
                    continue
                h = a.c2p(0, v)[1] - a.c2p(0, 3)[1]
                b = Rectangle(width=0.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                    a.c2p(i + 0.5, 3) + RIGHT * dx, aligned_edge=DOWN)
                grp.add(VGroup(b, label(f"{v:.1f}", font_size=17, color=col).next_to(b, UP, buff=0.05)))
            scale_l.add(label(rf"stakes $\times${s}", font_size=19, color=GREY_A).next_to(a.c2p(i + 0.5, 3), DOWN,
                                                                                       buff=0.15))
        neutral = DashedLine(a.c2p(0, 4), a.c2p(4, 4), color=GREY_C, stroke_width=1.5)
        nl = label(r"risk neutral", font_size=17, color=GREY_C).next_to(a.c2p(0, 4), UP, buff=0.05).shift(RIGHT * 0.55)
        leg = VGroup(label(r"real money", font_size=20, color=SAFE), label(r"hypothetical", font_size=20,
                                                                           color=GREY_B)).arrange(RIGHT, buff=0.4).next_to(
            ax, UP, buff=0.1)
        side = VGroup(
            label(r"most people are risk averse \\ even for a few dollars", font_size=24),
            label(r"real risk aversion rises with the stakes: \\ at 90 times, \ prizes up to \$346.50", font_size=24,
                  color=SAFE),
            label(r"hypothetical answers barely move: \\ asking is not the same as paying", font_size=24,
                  color=GREY_A),
            label(r"constant relative aversion predicts \\ the same choices at every scale; \\ the data reject it",
                  font_size=23, color=E.ACCENT),
            label(rf"a 2004 rerun without order effects: \\ {t['real_unordered_2004']['1']}  $\to$ "
                  rf"{t['real_unordered_2004']['20']} at 20 times", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Holt and Laury, AER (2005), table 1", corner=DR, font_size=14)
        with self.voiceover(
            "What did they find? <bookmark mark='a'/> With real money and stakes of a few dollars, the average "
            "subject made five point two safe choices: most people are risk averse even over pocket change. "
            "<bookmark mark='b'/> Then they scaled the prizes up, twenty, fifty and ninety times, with the top prize "
            "reaching three hundred and forty-six dollars fifty. Safe choices rose to six, six point eight, and seven "
            "point two. <bookmark mark='c'/> When the larger stakes were only hypothetical, choices hardly moved. "
            "Asking people what they would do is not the same as making them pay for it. <bookmark mark='d'/> "
            "Constant relative risk aversion over the prizes would give the same choices at every scale. The data "
            "say aversion rises with the stakes. <bookmark mark='e'/> A rerun in 2004, without the order effects "
            "critics worried about, found the same pattern."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(neutral), FadeIn(nl), FadeIn(leg), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(real[0]), FadeIn(scale_l[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in real[1:]], lag_ratio=0.4), FadeIn(scale_l[1:]),
                      FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in hyp], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def island(self):
        m = load("measuring")
        h, he = np.array(m["hist"]), np.array(m["hist_exact"])
        ax = plane([-0.5, 10.5], [0, 110], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=4.8,
                   xticks=list(range(0, 11)), yticks=[0, 25, 50, 75, 100], xlabel=r"safe choices",
                   ylabel=r"islanders", font_size=17)
        a = ax.ax

        def barset(v, col, dx):
            g = VGroup()
            for k, n in enumerate(v):
                hh = a.c2p(0, n)[1] - a.c2p(0, 0)[1]
                if n > 0:
                    g.add(Rectangle(width=0.34, height=hh, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                        a.c2p(k, 0) + RIGHT * dx, aligned_edge=DOWN))
            return g

        b1, b2 = barset(he, LATER, -0.18), barset(h, RISKY, 0.18)
        leg = VGroup(label(r"if they chose without error", font_size=19, color=LATER),
                     label(r"what they chose", font_size=19, color=RISKY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.08).next_to(
            a.c2p(10.4, 108), DL, buff=0.05)
        side = VGroup(
            label(rf"{m['people']} islanders take the menu", font_size=25),
            label(r"planted: \ $\gamma$ normal, \ mean 0.35, \ s.d.\ 0.35; \\ each choice noisy (a logit, \ "
                  r"\$0.20 scale)", font_size=21, color=GREY_A),
            label(rf"{100 * m['switch_back']:.0f}\% switch back to A after B: \\ no single $\gamma$ fits them",
                  font_size=23, color=RISKY),
            label(rf"scoring the rest by their brackets: \\ mean $\gamma$ {m['mean_scored']:.2f} \ (planted "
                  rf"{m['mean_true']:.2f})", font_size=23, color=E.ACCENT),
            label(rf"correlation with the truth: \ {m['corr']:.2f}", font_size=23),
            label(r"good on average; \ noisy for any one person", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "How well does the menu measure? On the Island we can check, because we planted the truth. "
            "<bookmark mark='a'/> Four hundred islanders take the menu. Their gammas are drawn around nought point "
            "three five, and each of their choices has a little noise in it, as real choices do. "
            "<bookmark mark='b'/> In blue, the choices they would make without error; in red, what they choose. "
            "<bookmark mark='c'/> Sixteen percent switch back from B to A somewhere down the menu, which no single "
            "gamma can explain. Real subjects do this too. <bookmark mark='d'/> Score the rest by the middle of their "
            "bracket, and the average comes out at nought point three six, against a planted nought point three five. "
            "<bookmark mark='e'/> For individuals the measure is rougher: the correlation between score and truth is "
            "nought point eight five. Good for averages, noisy for any one person."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(b1), FadeIn(leg[0]))
            self.play(FadeIn(b2), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()

    def surveys(self):
        m = load("measuring")
        b = m["barsky"]
        hrs = m["hrs"]
        q = VGroup(label(r"the Health and Retirement Study (Barsky, Juster, Kimball and Shapiro, 1997):",
                         font_size=24, color=GREY_B),
                   wrapped_label(tex_safe(b["question"]), 12.2, 27, WHITE)).arrange(DOWN, buff=0.2).to_edge(UP,
                                                                                                buff=0.5)
        cuts = VGroup()
        for c, txt in ((0.5, r"a half"), (1 / 3, r"a third"), (0.2, r"a fifth")):
            g_ = hrs[f"{c:.4f}"]
            cuts.add(VGroup(label(rf"double, \ or cut by {txt}", font_size=27),
                            label(rf"indifferent at $\gamma$ = {g_:.2f}", font_size=27, color=RISKY)).arrange(
                RIGHT, buff=0.7))
        cuts.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(q, DOWN, buff=0.5)
        res = VGroup(
            label(rf"answers sort people into four groups by $\gamma$; \ the mean risk tolerance was "
                  rf"{b['mean_risk_tolerance']:.2f}, \ a $\gamma$ near 4", font_size=24),
            label(r"risk tolerance predicted behaviour: \ smoking, \ drinking, \ going uninsured, \ holding stocks",
                  font_size=24, color=GREY_A),
            label(r"Deal or No Deal (Post, van den Assem, Baltussen and Thaler, 2008): \ contestants took bigger "
                  r"risks \\ after bad luck and after good: \ the path mattered, \ as reference points predict",
                  font_size=22, color=FAN),
        ).arrange(DOWN, buff=0.25).next_to(cuts, DOWN, buff=0.45)
        tag = published_tag(r"Barsky et al., QJE (1997); Post et al., AER (2008)", corner=DR, font_size=14)
        with self.voiceover(
            "Laboratory stakes are small. To ask about the stakes of a whole life, Robert Barsky, Thomas Juster, Miles "
            "Kimball and Matthew Shapiro put questions to thousands of older Americans in the Health and Retirement "
            "Study. <bookmark mark='a'/> Would you take a job with your current income for life, or one with a fifty-"
            "fifty chance of doubling it or cutting it by a third? Then by a half, or by a fifth. "
            "<bookmark mark='b'/> Each question has a threshold. Someone with the power function is indifferent to "
            "doubling or halving at a gamma of exactly one; to doubling or losing a third at two; to doubling or "
            "losing a fifth at three point seven six. <bookmark mark='c'/> Most respondents refused even the "
            "smallest cut; the mean risk tolerance was a quarter, a gamma near four. And the answers predicted "
            "behaviour: smoking, drinking, going without insurance, holding stocks. <bookmark mark='d'/> Television "
            "has run experiments too. In the game show Deal or No Deal, with prizes up to millions, Thierry Post and "
            "his colleagues found that contestants took bigger risks after bad luck, and after good luck, than at the "
            "start: their choices depended on the path that led there, as reference points predict."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(q[1], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cuts], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("d")
            self.play(FadeIn(res[2]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["bernoulli_1738"]
        s = load("stpete")
        hp = tables.HAYDEN_PLATT_2009.data
        n = s["named"]
        cc = call_card(r"Daniel Bernoulli", c.when,
                       rf"the game is worth a small, finite sum that rises with wealth: \ on his logarithm, \ "
                       rf"\${n['100']['log']:.2f} with \$100, \ \${n['1000']['log']:.2f} with \$1{{,}}000, \ "
                       rf"\${n['1e+06']['log']:.2f} with \$1 million",
                       rf"2009: \ {hp['real']['n']} students bidding real money paid a median \$"
                       rf"{hp['real']['median_bid']:.2f}; \ {hp['hypothetical']['n']} asked hypothetically, \$"
                       rf"{hp['hypothetical']['median_bid']:.2f}; \ cut the game to 3 tosses or to 15, \ and bids "
                       r"stayed at \$1.50 to \$2", c.verdict, width=12.4, font_size=23).move_to(UP * 1.0)
        tr = VGroup(label(r"Bernoulli's price at \$1{,}000, \ game cut off after", font_size=21, color=GREY_B))
        for k, v in zip(s["trunc_tosses"], s["trunc_log"]):
            tr.add(label(rf"{k} tosses: \ \${v:.2f}", font_size=21, color=COINC))
        tr.arrange(RIGHT, buff=0.35).next_to(cc, DOWN, buff=0.35)
        if tr.width > 13.2:
            tr.width = 13.2
        foot = label(r"the price is finite and small, \ as he said; \ but people pay less still, \ and ignore the "
                     r"stakes his theory says matter: \\ the median prize, \ \$1 or \$2, \ predicts the bids "
                     r"(Hayden and Platt's ``median heuristic'')", font_size=22, color=E.ACCENT).to_edge(DOWN,
                                                                                                    buff=0.6)
        tag = published_tag(r"Bernoulli (1738); Hayden and Platt, JDM (2009)", corner=DR, font_size=13)
        with self.voiceover(
            "And so to the price you named at the start. Called it? <bookmark mark='a'/> In 1738 Bernoulli said "
            "the game is worth a small sum that grows with your wealth: on his logarithm, four dollars thirty-six "
            "to someone with a hundred dollars, five ninety-seven with a thousand, ten ninety-four with a million. "
            "<bookmark mark='b'/> In 2009 Benjamin Hayden and Michael Platt asked. Twenty students bidding with real "
            "money paid a median of a dollar seventy-five. Two hundred and twenty people asked hypothetically said "
            "a dollar fifty. <bookmark mark='c'/> And when the game was cut off after three tosses, or after fifteen, "
            "bids stayed at a dollar fifty to two dollars, though on Bernoulli's own logarithm the price should "
            "more than double over that range. <bookmark mark='d'/> Partly right. The price is finite and small, "
            "as he said. But people pay less still, and their bids ignore the stakes his theory says should matter. "
            "What predicts them best is the median prize, a dollar or two. How did your own price compare?"
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(tr))
            vo.wait_until("d")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(foot))
        self.clear_scene()
