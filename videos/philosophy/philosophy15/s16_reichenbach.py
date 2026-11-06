from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

EXP_C = {"always 1": BLUEC, "always 0": GREY_B, "straight rule": PAST, "repeat last": A_C, "flip last": C_C}


class Reichenbach(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"A pragmatic vindication", r"If anything works, does induction?",
                            lit=(1938, 2008), part=PART)
        with self.voiceover("Chapter fifteen. A pragmatic vindication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.wager()
        self.straight()
        self.objections()
        self.meta()
        self.regret()

    def wager(self):
        hc = history_card(1938, r"Hans Reichenbach", r"\textit{Experience and Prediction}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        aim = label(r"not a proof that induction succeeds, \ but that it is the best bet", font_size=23,
                    color=GOAL).next_to(hc, DOWN, buff=0.35).set_x(0)
        hd = [r"", r"\text{the world has a limit}", r"\text{it has none}"]
        rows = [[MathTex(r"\text{use induction}", font_size=24, color=OK),
                 label(r"success \ (in the limit)", font_size=22, color=OK),
                 label(r"failure", font_size=22, color=BAD)],
                [MathTex(r"\text{use anything else}", font_size=24, color=BAD),
                 label(r"success or failure", font_size=22, color=GREY_A),
                 label(r"failure", font_size=22, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[3.6, 4.0, 2.6], cell_h=0.75, font_size=24).next_to(aim, DOWN, buff=0.45)
        foot = stack([(r"if any method finds the limiting frequency, \ the straight rule does", FUT),
                      (r"so you lose nothing by using it", GREY_A)], font_size=23).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Hans Reichenbach gave the most influential answer to Hume of the twentieth century. "
            "<bookmark mark='a'/>He did not claim to prove that induction succeeds. He claimed to prove that it is "
            "the best bet. <bookmark mark='b'/>Either the world has stable limiting frequencies, or it does not. "
            "<bookmark mark='c'/>If it does, induction finds them, in the limit. <bookmark mark='d'/>If it does not, "
            "induction fails, but so does every other method of prediction. <bookmark mark='e'/>Any other method "
            "might succeed or fail where there are limits, and fails where there are none. "
            "<bookmark mark='f'/>So if any method can find the limiting frequency, the straight rule can. Using it "
            "costs nothing."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(aim))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(grid.cell[0][0]), FadeIn(grid.cell[1][0]))
            vo.wait_until("c")
            self.play(FadeIn(grid.cell[0][1]))
            vo.wait_until("d")
            self.play(FadeIn(grid.cell[0][2]), FadeIn(grid.cell[1][2]))
            vo.wait_until("e")
            self.play(FadeIn(grid.cell[1][1]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def straight(self):
        d = load("straight")
        head = label(r"The straight rule: \ posit the observed frequency", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        eq = MathTex(r"\hat p_n = \frac{s_n}{n} \ \longrightarrow\ p \quad \text{if the limit } p \text{ exists}",
                     font_size=34, color=FUT).next_to(head, DOWN, buff=0.3)
        n = len(d["estimates"])
        ax = Axes(x_range=[0, n * 20, 500], y_range=[0, 0.6, 0.1], x_length=9.6, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([0, -0.95, 0])
        xl = label(r"trials", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        truth = DashedLine(ax.c2p(0, d["p"]), ax.c2p(n * 20, d["p"]), color=OK, stroke_width=2)
        tl = label(r"$p = 0.3$", font_size=19, color=OK).next_to(truth, RIGHT, buff=0.1)
        curve = series_plot(ax, d["estimates"], PAST, xs=[20 * i for i in range(n)])
        note = label(r"a \textit{posit}: \ treated as true for now, \ corrected as data come in", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Reichenbach's method is the straight rule. <bookmark mark='a'/>After n trials with s successes, posit "
            "that the limiting frequency is s over n. If a limit exists, the posits converge to it. "
            "<bookmark mark='b'/>Here is a coin with chance point three, two thousand tosses. "
            "<bookmark mark='c'/>The posits wander early and settle near point three. "
            "<bookmark mark='d'/>Reichenbach called each estimate a posit: a claim treated as true for now, in the "
            "knowledge that the method will correct it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), Create(truth), FadeIn(tl))
            vo.wait_until("c")
            self.play(Create(curve), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def objections(self):
        head = label(r"Three objections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"too many winners", r"$\dfrac{s_n}{n} + c_n$ \ converges too, \ for any $c_n \to 0$: \ Laplace, \ "
                                  r"Carnap's every $\lambda$", BAD),
            (r"", r"Salmon's `linguistic invariance' tried to single out the straight rule; \ few were convinced",
             GREY_A),
            (r"the long run", r"`In the long run we are all dead' \ (Keynes): \ no bound on when", BAD),
            (r"which limits?", r"frequencies of what? \ grue-frequencies converge too", BAD),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=23, color=c)
            y = label(b, font_size=21)
            if y.width > 9.0:
                y.width = 9.0
            x.move_to([-6.2 + x.width / 2, 1.5 - i * 0.95, 0])
            y.move_to([-3.4 + y.width / 2, 1.5 - i * 0.95, 0])
            g.add(VGroup(x, y))
        foot = label(r"vindication shows induction is \textit{a} good bet, \ not which one", font_size=23,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Three objections. <bookmark mark='a'/>First, there are too many winners. Add to the straight rule any "
            "correction that shrinks to zero, and the result converges just as well. Laplace's rule does, and so "
            "does every member of Carnap's continuum. <bookmark mark='b'/>Wesley Salmon tried to single out the "
            "straight rule by requiring that its answers not depend on how the outcomes are described; few were "
            "convinced. <bookmark mark='c'/>Second, the long run. As Keynes said, in the long run we are all dead, "
            "and the vindication gives no bound on when the posits become good. <bookmark mark='d'/>Third, which "
            "frequencies? The frequency of grue emeralds converges too. <bookmark mark='e'/>Reichenbach shows that "
            "induction is a good bet, not which bet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def meta(self):
        d = load("meta")
        hc = history_card(2008, r"Gerhard Schurz", r"`The Meta-inductivist's Winning Strategy'; \ "
                          r"\textit{Hume's Problem Solved} \ (2019)", width=7.6, color=HIST).to_corner(UL, buff=0.3)
        idea = label(r"don't justify one method: \ follow the methods in proportion to their track records",
                     font_size=21, color=GOAL).next_to(hc, DOWN, buff=0.25).set_x(0)
        ax = Axes(x_range=[0, d["T"], 50], y_range=[0, 180, 50], x_length=7.2, y_length=3.7, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.6, -1.4, 0])
        xl = label(r"round", font_size=17, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.28)
        yl = label(r"total loss", font_size=17, color=GREY_B).next_to(ax.y_axis, UP, buff=0.08)
        T = d["T"]
        regimes = VGroup(*[DashedLine(ax.c2p(t, 0), ax.c2p(t, 180), color=GREY_D, stroke_width=1.5)
                           for t in (T // 3, 2 * T // 3)])
        rl = VGroup(*[label(t, font_size=15, color=GREY_B).move_to(ax.c2p(x, 176)) for t, x in
                      ((r"mostly 1s", T // 6), (r"mostly 0s", T // 2), (r"alternating", 5 * T // 6))])
        curves = VGroup(*[series_plot(ax, d["cum"][n], EXP_C[n], xs=d["idx"], width=2.5) for n in d["names"]])
        fc = series_plot(ax, d["forecaster"], OK, xs=d["idx"], width=5)
        leg = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.35, color=EXP_C[n], stroke_width=4),
                              label(n + r": \ " + f"{d['final'][n]:.0f}", font_size=18, color=EXP_C[n])).arrange(
            RIGHT, buff=0.1) for n in d["names"]],
                     VGroup(Line(ORIGIN, RIGHT * 0.35, color=OK, stroke_width=6),
                            label(r"meta-inductor: \ " + f"{d['final_forecaster']:.0f}", font_size=19,
                                  color=OK)).arrange(RIGHT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        leg.move_to([4.5, -1.2, 0])
        with self.voiceover(
            "Gerhard Schurz found a sharper answer, using a tool from machine learning: prediction with expert "
            "advice. <bookmark mark='a'/>Don't try to justify one method. Follow all the methods you can see, each "
            "in proportion to its track record. <bookmark mark='b'/>Here is a world with three regimes: mostly "
            "ones, then mostly zeros, then strict alternation. <bookmark mark='c'/>Five object-level methods "
            "predict each bit: always one, always zero, the straight rule, repeat the last bit, and flip it. Each "
            "line is a method's running total of error. <bookmark mark='d'/>The meta-inductor weights each method by "
            "e to the minus its past loss, and predicts with the weighted average. It is never the best method, "
            "but it is never far behind whichever method has done best."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(idea))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(regimes), FadeIn(rl))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.15), FadeIn(VGroup(*leg[:-1])),
                      run_time=3)
            vo.wait_until("d")
            self.play(Create(fc), FadeIn(leg[-1]), run_time=2.5)
        self.clear_scene()

    def regret(self):
        d = load("meta")
        head = label(r"A guarantee for every possible world", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"L_{\text{meta}}(T) - \min_i L_i(T) \ \le\ \sqrt{\tfrac{T}{2}\ln N}", font_size=38,
                     color=FUT).next_to(head, DOWN, buff=0.35)
        eql = label(r"exponential weights, \ $\eta = \sqrt{8 \ln N / T}$ \ (Littlestone and Warmuth; \ "
                    r"Cesa-Bianchi and Lugosi)", font_size=20, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        ax = Axes(x_range=[0, d["T"], 50], y_range=[-5, 18, 5], x_length=7.6, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-1.9, -1.6, 0])
        bound = DashedLine(ax.c2p(0, d["bound"]), ax.c2p(d["T"], d["bound"]), color=BAD, stroke_width=2.5)
        bl = label(r"bound: \ " + f"{d['bound']:.1f}", font_size=18, color=BAD).next_to(bound, RIGHT, buff=0.1)
        rc = series_plot(ax, d["regret"], OK, xs=d["idx"], width=4)
        rl = label(r"regret: \ the meta-inductor's loss \ minus the best method's so far", font_size=18,
                   color=OK).next_to(ax, UP, buff=0.05).shift(RIGHT * 0.5)
        side = stack([(r"largest gap: \ " + f"{d['max_regret']:.1f}" + r" of " + f"{d['bound']:.1f}", OK),
                      (r"holds for \textit{every} sequence, \ even an adversary's", WHITE),
                      (r"per round, \ the gap $\to 0$", FUT),
                      (r"but only against the methods it can see", BAD)], font_size=20,
                     aligned_edge=LEFT).move_to([4.6, -1.5, 0])
        with self.voiceover(
            "And here is the theorem. <bookmark mark='a'/>For any sequence whatever, even one chosen by an "
            "adversary, the meta-inductor's total loss exceeds the best method's by at most the square root of T "
            "over two times log N. Nick Littlestone and Manfred Warmuth, and Nicolò Cesa-Bianchi and Gábor Lugosi, "
            "proved bounds of this kind. <bookmark mark='b'/>The Reasoner checks it on our world: the gap never "
            "comes near the bound. <bookmark mark='c'/>Unlike Reichenbach's argument, this is a guarantee about "
            "every world, and the average gap per round shrinks to zero. <bookmark mark='d'/>The price is that it "
            "holds only against the methods the meta-inductor can see. That is not a free lunch, and it is "
            "consistent with Wolpert: in a world where all those methods do badly, the meta-inductor does badly too. "
            "But it turns Hume's question into one we can answer: given the methods we have, follow the record."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(eql))
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(bound), FadeIn(bl), FadeIn(rl))
            self.play(Create(rc), run_time=2.5)
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
