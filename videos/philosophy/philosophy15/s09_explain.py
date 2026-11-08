from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

IBE_C = "#F2A65A"
BAY_C = "#6FB7FF"


class Explain(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The best explanation", r"Is explaining a reason to believe?", lit=(1903,),
                            part=PART)
        with self.voiceover("Chapter eight. The best explanation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.abduction()
        self.objections()
        self.race()
        self.verdict()

    def abduction(self):
        hc = history_card(1903, r"Charles S.\ Peirce", r"Harvard lectures on pragmatism", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        schema = VGroup(label(r"the surprising fact $C$ is observed;", font_size=24, color=PAST),
                        label(r"but if $A$ were true, \ $C$ would be a matter of course;", font_size=24, color=WHITE),
                        label(r"hence there is reason to suspect that $A$ is true.", font_size=24, color=FUT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).next_to(hc, DOWN, buff=0.4).set_x(0)
        ex = stack([(r"Semmelweis, \ 1847: \ doctors from the dissecting room deliver babies; \ midwives don't", GREY_A),
                    (r"`cadaverous matter' explains the difference; \ chlorine hand-washing \ $\Rightarrow$ \ deaths "
                     r"fall from over 10\% to about 2\%", OK)], font_size=21).next_to(schema, DOWN, buff=0.45)
        virt = label(r"Harman \ (1965): \ inference to the best explanation; \ Lipton \ (2004): \ prefer the "
                     r"\textit{loveliest}: \ scope, \ mechanism, \ unification", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Scientists rarely reason by enumerating instances. They infer the hypothesis that would best explain "
            "what they see. <bookmark mark='a'/>Charles Sanders Peirce called it abduction. The surprising fact C is "
            "observed. But if A were true, C would be a matter of course. Hence there is reason to suspect that A "
            "is true. <bookmark mark='b'/>Ignaz Semmelweis, in Vienna in 1847, saw that mothers delivered by doctors "
            "who came from the dissecting room died of childbed fever far more often than those delivered by "
            "midwives. <bookmark mark='c'/>Particles from the corpses would explain it. He made the doctors wash in "
            "chlorinated lime, and the death rate fell from over ten percent to about two. "
            "<bookmark mark='d'/>Gilbert Harman named the pattern inference to the best explanation, and Peter "
            "Lipton refined it: prefer the loveliest explanation, the one with the widest scope, a mechanism, and "
            "the most unification, and expect it to be the likeliest."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in schema], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            vo.wait_until("c")
            self.play(FadeIn(ex[1]))
            vo.wait_until("d")
            self.play(FadeIn(virt))
        self.clear_scene()

    def objections(self):
        hc = history_card(1989, r"Bas van Fraassen", r"\textit{Laws and Symmetry}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        # the bad lot: the hypotheses we thought of, inside the space of all hypotheses
        space = RoundedRectangle(width=5.4, height=3.4, corner_radius=0.2, stroke_color=GREY_C, stroke_width=2,
                                 fill_color=GREY_E, fill_opacity=0.3).move_to([-3.3, -1.1, 0])
        sl = label(r"every possible hypothesis", font_size=18, color=GREY_B).next_to(space, UP, buff=0.1)
        lot = VGroup(*[Dot(radius=0.12, color=c).move_to(space.get_center() + np.array(v)) for c, v in
                       ((IBE_C, [-1.4, 0.5, 0]), (GREY_B, [-0.9, -0.6, 0]), (GREY_B, [-1.9, -0.3, 0]))])
        lot_l = label(r"the ones we thought of", font_size=17, color=IBE_C).next_to(lot, DOWN, buff=0.15)
        truth = Star(n=5, outer_radius=0.16, color=OK, fill_opacity=1).move_to(space.get_center() + RIGHT * 1.7 +
                                                                                 UP * 0.6)
        tl = label(r"the truth", font_size=17, color=OK).next_to(truth, DOWN, buff=0.1)
        bad = label(r"1. \ the bad lot: \ the best of what we thought of \ may be false", font_size=21,
                    color=BAD).move_to([3.4, 0.5, 0])
        db = VGroup(label(r"2. \ an explanation \textit{bonus} on top of Bayes:", font_size=21, color=BAD),
                    MathTex(r"P_{\text{new}}(H) \neq P(H \mid E)", font_size=30, color=BAD),
                    label(r"so a bookie can make a dynamic Dutch book \ (Part 13)", font_size=20,
                          color=GREY_A)).arrange(DOWN, buff=0.15).move_to([3.4, -1.4, 0])
        comp = label(r"compatibilists \ (Lipton, \ Okasha): \ explanation is how we \textit{set} priors and "
                     r"likelihoods, \ not a bonus", font_size=20, color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Bas van Fraassen pressed two objections. <bookmark mark='a'/>The first is the bad lot. We can only "
            "compare the hypotheses someone has thought of. <bookmark mark='b'/>The truth may not be among them, and "
            "then the best of a bad lot is still false. <bookmark mark='c'/>The second is sharper. If you give the "
            "best explanation a bonus, over and above what conditionalization gives it, your new credence is no "
            "longer your old credence conditional on the evidence, and Part 13 showed that a bookie can then "
            "arrange a dynamic Dutch book against you. <bookmark mark='d'/>Compatibilists like Lipton and Samir "
            "Okasha reply that explanatory considerations are how we set the priors and likelihoods in the first "
            "place, not a bonus added afterwards. But some philosophers have defended the bonus itself."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(space), FadeIn(sl), FadeIn(lot), FadeIn(lot_l))
            vo.wait_until("b")
            self.play(FadeIn(truth, scale=1.5), FadeIn(tl), FadeIn(bad))
            vo.wait_until("c")
            self.play(FadeIn(db))
            vo.wait_until("d")
            self.play(FadeIn(comp))
        self.clear_scene()

    def race(self):
        d = load("explain")
        head = label(r"Douven's race: \ a Bayesian against an explanationist", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        setup = stack([(r"eleven hypotheses: \ the coin's bias is $0, 0.1, \dots, 1$; \ the truth is " +
                        f"{d['truth']}", WHITE),
                       (r"the explanationist conditionalizes, \ then adds " + f"{d['bonus']}" + r" to the bias nearest "
                        r"the observed frequency", IBE_C)], font_size=21).next_to(head, DOWN, buff=0.25)
        n = d["n"]
        xs = list(range(0, n, 3))
        ax = Axes(x_range=[0, n, 50], y_range=[0, 1, 0.25], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.6, -1.4, 0])
        xl = label(r"tosses", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.28)
        yl = label(r"average P(the truth)", font_size=18, color=GREY_B).next_to(ax.y_axis, UP, buff=0.08).align_to(
            ax.y_axis, LEFT)
        cb = series_plot(ax, d["bayes"]["curve"], BAY_C, xs=xs, width=4)
        ci = series_plot(ax, d["ibe"]["curve"], IBE_C, xs=xs, width=4)
        hd = [r"", r"\text{Bayes}", r"\text{IBE}"]
        rows = [[label(r"first over 0.9", font_size=19), MathTex(f"{d['bayes']['t90']:.0f}", font_size=24,
                                                                  color=BAY_C),
                 MathTex(f"{d['ibe']['t90']:.0f}", font_size=24, color=OK)],
                [label(r"ever over 0.9 \ on a falsehood", font_size=19),
                 MathTex(f"{100 * d['bayes']['false90']:.0f}" + r"\%", font_size=24, color=OK),
                 MathTex(f"{100 * d['ibe']['false90']:.0f}" + r"\%", font_size=24, color=BAD)],
                [label(r"average Brier inaccuracy", font_size=19), MathTex(f"{d['bayes']['brier']:.2f}", font_size=24,
                                                                           color=OK),
                 MathTex(f"{d['ibe']['brier']:.2f}", font_size=24, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 1.1, 1.1], cell_h=0.62, font_size=22).move_to([3.9, -1.1, 0])
        note = label(str(d["runs"]) + r" runs of " + str(n) + r" tosses", font_size=17, color=GREY_B).next_to(
            grid, DOWN, buff=0.15)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=BAY_C, stroke_width=4),
                            label(r"Bayes", font_size=18, color=BAY_C)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=IBE_C, stroke_width=4),
                            label(r"explanationist", font_size=18, color=IBE_C)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.4).next_to(ax, UP, buff=0.05).shift(RIGHT * 1.2)
        with self.voiceover(
            "Igor Douven did, in 2013, by racing the two rules. The Reasoner reruns his race. "
            "<bookmark mark='a'/>A coin's bias is one of eleven values, zero, a tenth, up to one; the truth is "
            "point seven. Both agents start uniform. The Bayesian conditionalizes. The explanationist "
            "conditionalizes and then adds a bonus of a tenth to the bias that best explains the data so far, the "
            "one nearest the observed frequency. <bookmark mark='b'/>Averaged over a thousand runs, the "
            "explanationist's confidence in the truth rises faster. <bookmark mark='c'/>It first passes ninety "
            "percent after about eighty tosses, against the Bayesian's hundred and seventy. "
            "<bookmark mark='d'/>But it pays for its speed. In fifty-nine percent of runs it is, at some point, "
            "more than ninety percent sure of a false hypothesis; the Bayesian, in twelve percent. "
            "<bookmark mark='e'/>And its average inaccuracy, by the Brier score, is worse."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(leg))
            self.play(Create(cb), Create(ci), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]], FadeIn(note))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("e")
            self.play(*[FadeIn(c) for c in grid.cell[2]])
        self.clear_scene()

    def verdict(self):
        head = label(r"Speed or reliability?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"conditionalization minimizes \textit{expected} inaccuracy \ (Greaves and Wallace, \ 2006)", BAY_C),
            (r"a bold rule can reach the truth sooner, \ and act on it sooner \ (Douven)", IBE_C),
            (r"and jumps to falsehoods more often: \ the same trade-off as Kelly's bold learner \ (Ch.\ 11)", BAD),
            (r"in machine learning: \ keeping the full posterior vs committing to the single best fit", GREY_A),
            (r"which rule is right depends on what errors cost: \ a decision, \ not a theorem", GOAL),
        ], font_size=23, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "So which rule is right? <bookmark mark='a'/>Hilary Greaves and David Wallace proved that "
            "conditionalization minimizes expected inaccuracy, by your own lights. <bookmark mark='b'/>Douven "
            "replies that we also care about getting to the truth quickly, and acting on it. "
            "<bookmark mark='c'/>The price of speed is jumping to falsehoods, the same trade-off we will meet with "
            "Kelly's bold learner in chapter eleven. <bookmark mark='d'/>Machine learning faces it too: keep the "
            "whole posterior, or commit to the single best fit. <bookmark mark='e'/>Which rule is right depends on "
            "what each kind of error costs. That is a decision, not a theorem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
