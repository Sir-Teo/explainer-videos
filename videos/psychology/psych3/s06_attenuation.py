from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403

RAW, FIXED = OBS, P.ACCENT


class Attenuation(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.lengths()
        self.caution()

    def card(self):
        card = chapter_card(5, r"Spearman's correction", r"What does error do to a correlation?",
                            lit={1904: r"Spearman's correction for attenuation"},
                            part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter five. Spearman's correction."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def formula(self):
        d = load("attenuation")
        hc = history_card(1904, r"Charles Spearman", r"``The proof and measurement of association between two "
                          r"things''", color=P.ARCHIVE, width=7.0, font_size=26).to_edge(UP, buff=0.35)

        def node(text, color, pos, dashed=False):
            c = Circle(radius=0.5, color=color, stroke_width=3)
            if dashed:
                c = DashedVMobject(c, num_dashes=22)
            return VGroup(c, label(text, font_size=34, color=color)).move_to(pos)

        tx, ty = node(r"$T_x$", TRUE, [-5.2, 0.9, 0], True), node(r"$T_y$", TRUE, [-1.6, 0.9, 0], True)
        x, y = node(r"$X$", OBS, [-5.2, -1.5, 0]), node(r"$Y$", OBS, [-1.6, -1.5, 0])
        top = Line(tx.get_right(), ty.get_left(), color=TRUE, stroke_width=6)
        top_l = label(rf"$\rho = {r2(d['true_r'])}$", font_size=30, color=TRUE).next_to(top, UP, buff=0.1)
        ax_, ay_ = (Arrow(tx.get_bottom(), x.get_top(), buff=0.05, color=GREY_B, stroke_width=4),
                    Arrow(ty.get_bottom(), y.get_top(), buff=0.05, color=GREY_B, stroke_width=4))
        lx = label(r"$\sqrt{r_{xx}}$", font_size=28, color=GREY_A).next_to(ax_, LEFT, buff=0.1)
        ly = label(r"$\sqrt{r_{yy}}$", font_size=28, color=GREY_A).next_to(ay_, RIGHT, buff=0.1)
        bottom = DashedLine(x.get_right(), y.get_left(), color=OBS, stroke_width=4)
        bot_l = label(r"$r_{xy}$: \ what you observe", font_size=28, color=OBS).next_to(VGroup(x, y), DOWN, buff=0.2)
        steps = VGroup(
            wrapped_label(r"Errors are unrelated to everything, so the scores covary only through the true scores.",
                          5.8, 26, GREY_A),
            label(r"$r_{xy} \;=\; \rho \,\sqrt{r_{xx}\, r_{yy}}$", font_size=44, color=WHITE),
            label(r"error makes correlations look smaller than they are", font_size=26, color=ERRC),
            label(r"$\rho \;=\; \dfrac{r_{xy}}{\sqrt{r_{xx}\, r_{yy}}}$", font_size=44, color=P.ACCENT),
            label(r"the correction for attenuation", font_size=26, color=P.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to([3.6, -0.9, 0])
        with self.voiceover(
            "The first person to see what error does to psychology's results was Charles Spearman, in 1904, and "
            "the paper is still worth reading. His question: you correlate two measurements, and both are noisy. "
            "What have you learned about the things you were trying to measure? <bookmark mark='a'/> Draw it. Two "
            f"true scores, here related by {d['true_r']:.2f}. That's the fact about people you want. "
            "<bookmark mark='b'/> You never see them. You see two observed scores, each a degraded copy of its "
            "true score. How good a copy is exactly what reliability says. <bookmark mark='c'/> Because errors "
            "are unrelated to everything, the observed scores can only covary through the true scores. Work it "
            "through, <bookmark mark='d'/> and the observed correlation is the true one, multiplied by the square "
            "root of the two reliabilities. That factor is never more than one. So unreliable measures make every "
            "relationship look weaker than it is. A real effect measured badly looks like a small effect. "
            "<bookmark mark='e'/> And the formula can be turned round. Divide what you observed by that factor, "
            "and you have an estimate of the relation between the true scores. Spearman called it the "
            "correction for attenuation."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(tx), FadeIn(ty), Create(top), FadeIn(top_l))
            vo.wait_until("b")
            self.play(FadeIn(x), FadeIn(y), GrowArrow(ax_), GrowArrow(ay_), FadeIn(lx), FadeIn(ly))
            self.play(Create(bottom), FadeIn(bot_l))
            vo.wait_until("c")
            self.play(FadeIn(steps[0]))
            vo.wait_until("d")
            self.play(FadeIn(steps[1], shift=UP * 0.1), FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3], shift=UP * 0.1), FadeIn(steps[4]))
        self.clear_scene()

    def lengths(self):
        d = load("attenuation")
        head = heading(r"The same two traits, through shorter and longer questionnaires")
        A = axes([0, 42], [0, 1.0], x_length=8.2, y_length=4.0, xticks=[2, 6, 10, 20, 30, 40],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xlabel=r"questions in each scale", ylabel=r"correlation",
                 center=[-2.3, -0.45, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(0, d["true_r"]), ax.c2p(42, d["true_r"]), color=TRUE, stroke_width=3)
        tlab = label(rf"the true correlation: \ {r2(d['true_r'])}", font_size=24, color=TRUE)
        tlab.next_to(ax.c2p(21, d["true_r"]), UP, buff=0.22)
        raw = VGroup(*[Dot(ax.c2p(k, r), radius=0.08, color=RAW) for k, r in zip(d["lengths"], d["observed"])])
        raw_line = curve(ax, d["lengths"], d["observed"], RAW, stroke_width=3)
        fix = VGroup(*[Dot(ax.c2p(k, r), radius=0.08, color=FIXED) for k, r in zip(d["lengths"], d["corrected"])])
        i6 = d["lengths"].index(6)
        leg = legend([(RAW, r"what a study observes"), (FIXED, r"after Spearman's correction")], font_size=24)
        leg.move_to([4.6, 1.6, 0])
        six = VGroup(
            label(r"six questions each:", font_size=26, color=GREY_A),
            label(rf"reliability {r2(d['reliabilities'][i6])}", font_size=28, color=WHITE),
            label(rf"observed {r2(d['observed'][i6])}", font_size=28, color=RAW),
            label(rf"corrected {r2(d['corrected'][i6])}", font_size=28, color=FIXED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        tag = simulated_tag(rf"simulated: the Pool, {fmt_int(d['n'])} people")
        with self.voiceover(
            "Here it is on the Pool. Two traits whose true scores correlate "
            f"{d['true_r']:.2f}, each measured by a questionnaire. <bookmark mark='a'/> With two questions "
            f"apiece, a study sees a correlation of {d['observed'][0]:.2f}: half the truth. As the scales get "
            "longer, and so more reliable, the observed correlation climbs toward the real one, and never quite "
            f"arrives. <bookmark mark='b'/> With six questions each, a common length, the reliability is "
            f"{d['reliabilities'][i6]:.2f} and the study reports {d['observed'][i6]:.2f}. "
            "<bookmark mark='c'/> Now apply the correction at every length. The corrected values sit on the "
            "truth, whatever the length of the test. This is why a correlation should never be read without the "
            "reliabilities of the two measures beside it. Two studies can disagree about how strongly two things "
            "are related and both be right, because they used tests of different quality."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(raw_line), LaggedStart(*[FadeIn(p_) for p_ in raw], lag_ratio=0.3), FadeIn(leg[0]),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(Flash(raw[i6], color=WHITE), FadeIn(six[0]), FadeIn(six[1]), FadeIn(six[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in fix], lag_ratio=0.25), FadeIn(leg[1]), FadeIn(six[3]),
                      run_time=3.0)
        self.clear_scene()

    def caution(self):
        d = load("attenuation")
        head = heading(rf"The same correction in studies of {d['study_n']} people")
        lo, hi, bins = 0.2, 1.3, 44
        e1, h1 = density(d["raw"], lo, hi, bins)
        e2, h2 = density(d["fixed"], lo, hi, bins)
        top = float(max(h1.max(), h2.max())) * 1.15
        A = axes([lo, hi], [0, top], x_length=8.4, y_length=3.6, xticks=[0.2, 0.4, 0.6, 0.8, 1.0, 1.2],
                 xlabel=r"correlation reported by one study", center=[-2.2, -0.35, 0])
        ax = A.ax
        hb = hist(ax, e1, h1, RAW, 0.6)
        hf = hist(ax, e2, h2, FIXED, 0.65)
        truth = DashedLine(ax.c2p(d["true_r"], 0), ax.c2p(d["true_r"], top), color=TRUE, stroke_width=3)
        one = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, top), color=ERRC, stroke_width=2)
        tlab = label(rf"truth: \ {r2(d['true_r'])}", font_size=22, color=TRUE).next_to(truth, UP, buff=0.05)
        olab = label(r"1: \ the limit", font_size=22, color=ERRC).next_to(one, UP, buff=0.05).shift(RIGHT * 0.45)
        notes = VGroup(
            label(rf"observed: \ centred on {r2(d['raw_median'])}", font_size=26, color=RAW),
            label(rf"corrected: \ centred on {r2(d['fixed_median'])}", font_size=26, color=FIXED),
            wrapped_label(rf"19 studies in 20 fall between {r2(d['fixed_lo'])} and {d['fixed_hi']:.2f}", 4.2, 24, GREY_A),
            wrapped_label(rf"{100 * d['above_one']:.0f} in 100 report a correlation above 1", 4.2, 24, ERRC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.75, 0.6, 0])
        end = label(r"The correction removes a bias and adds noise. \ It describes the true scores, not the test "
                    r"you have.", font_size=27, color=WHITE).to_edge(DOWN, buff=0.75)
        tag = simulated_tag(rf"simulated: the Pool, {fmt_int(d['studies'])} studies")
        with self.voiceover(
            "Before you correct everything in sight, look at what the correction costs. That last picture used "
            f"twenty thousand people. Here are four thousand studies of {d['study_n']} people each, with six-item "
            f"scales. <bookmark mark='a'/> The observed correlations centre on {d['raw_median']:.2f}, well below "
            f"the truth. <bookmark mark='b'/> The corrected ones centre close to it. But look how wide they've "
            "become. Dividing by an estimated reliability multiplies the noise as well as the signal. "
            f"<bookmark mark='c'/> Nineteen studies in twenty fall somewhere between {d['fixed_lo']:.2f} and "
            f"{d['fixed_hi']:.2f}, and about {100 * d['above_one']:.0f} in a hundred report a correlation greater "
            "than one, which is impossible. <bookmark mark='d'/> So two cautions. The correction trades bias for "
            "variance, and it needs a big sample to be worth it. And it answers a particular question: how "
            "strongly are the two attributes related? If your question is how well this test predicts that "
            "outcome, the uncorrected number is the honest one, because the test you'll be using is the one with "
            "the error in it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hb, lag_ratio=0.03), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hf, lag_ratio=0.03), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(one), FadeIn(olab), FadeIn(notes[2]), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()
