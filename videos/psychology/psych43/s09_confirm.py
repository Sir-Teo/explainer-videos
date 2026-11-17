from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403
from videos.psychology.psych43.s08_data import lab_forest


def sig_words(p: float, alpha: float = 0.05) -> str:
    return "significant in the predicted direction" if p < alpha else "not significant"


def verbal_tex(words: str) -> str:
    return words


class Confirm(VoiceoverScene):
    def construct(self):
        self.card()
        self.overshadowing()
        self.depletion()
        self.spread()

    def card(self):
        card = chapter_card(8, r"The confirmatory analysis", r"Exactly as registered", lit=(), part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter eight. The confirmatory analysis."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def panel(self, key, color, x_range, xlabel, scale, orig, orig_lo, orig_hi):
        c = load("confirm")
        A, g, z = lab_forest(c[f"{key}_y"], c[f"{key}_v"], [-3.3, 0.2, 0], color, x_range, xlabel, height=4.2,
                             scale=scale)
        k = len(c[f"{key}_y"])
        est, lo, hi = c[f"{key}_est"] * scale, c[f"{key}_lo"] * scale, c[f"{key}_hi"] * scale
        dia = Polygon(A.ax.c2p(lo, -0.2), A.ax.c2p(est, 0.25), A.ax.c2p(hi, -0.2), A.ax.c2p(est, -0.65),
                      stroke_width=0, fill_color=color, fill_opacity=1)
        o = VGroup(Line(A.ax.c2p(max(x_range[0], orig_lo), k + 0.6), A.ax.c2p(min(x_range[1], orig_hi), k + 0.6),
                        color=GREY_A, stroke_width=2),
                   Square(0.14, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(A.ax.c2p(orig, k + 0.6)))
        o_l = label(r"original", font_size=12, color=GREY_A).next_to(o, UP, buff=0.05)
        return A, g, z, dia, VGroup(o, o_l)

    def overshadowing(self):
        c, p = load("confirm"), load("plans")
        fewer, lo, hi = -100 * c["vo_est"], -100 * c["vo_hi"], -100 * c["vo_lo"]
        o = p["vo_orig"]
        A, g, z, dia, orig = self.panel("vo", GOOD, (-60, 30), r"difference in correct picks per 100", 100.0,
                                        100 * o, 100 * (o - 1.96 * p["vo_se"]), 100 * (o + 1.96 * p["vo_se"]))
        head = heading(r"Verbal overshadowing")
        verdict = sig_words(c["vo_p_one"])
        fewer_s, lo_s, hi_s = f"{fewer:.0f}", f"{lo:.0f}", f"{hi:.0f}"
        rows = rows_of([
            (r"registered: \ random-effects pooling of each lab's difference in correct picks, \ one-sided test, \ "
             r"every lab that ran the protocol", WHITE),
            (rf"result: \ {fewer_s} fewer correct picks per 100 among those who described the face, \ 95\% interval "
             rf"{lo_s} to {hi_s}", GOOD),
            (rf"{verbal_tex(verdict)}; \ between-lab spread $\hat\tau^2 = {c['vo_tau2']:.3f}$", MODEL),
            (rf"the original found {-100 * o:.0f} fewer per 100, \ with 44 people per group", GREY_A),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        with self.voiceover(
            f"Verbal overshadowing first. <bookmark mark='a'/> As registered: random-effects pooling of each lab's "
            f"difference in correct picks, a one-sided test, and every lab that ran the protocol. "
            f"<bookmark mark='b'/> The result: people who described the face made {fewer_s} fewer correct picks per "
            f"hundred, with an interval from {lo_s} to {hi_s}. <bookmark mark='c'/> That's {verdict}. "
            f"<bookmark mark='d'/> The original study found {-100 * o:.0f} fewer per hundred, with forty-four people in "
            f"each group."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(z), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dia))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(orig))
        self.clear_scene()

    def depletion(self):
        c, p = load("confirm"), load("plans")
        o = p["ed_orig"]
        A, g, z, dia, orig = self.panel("ed", AUTH, (-1.0, 1.4), r"Hedges's $g$", 1.0, o, o - 1.96 * p["ed_se"],
                                        o + 1.96 * p["ed_se"])
        head = heading(r"Ego depletion")
        verdict = sig_words(c["ed_p_one"])
        g_s, lo_s, hi_s = f"{c['ed_est']:.2f}", f"{c['ed_lo']:.2f}", f"{c['ed_hi']:.2f}"
        rows = rows_of([
            (r"registered: \ random-effects pooling of each lab's Hedges's $g$, \ one-sided test, \ every lab that ran "
             r"the protocol", WHITE),
            (rf"result: \ $g = {g_s}$, \ 95\% interval {lo_s} to {hi_s}", AUTH),
            (rf"{verbal_tex(verdict)}; \ between-lab spread $\hat\tau^2 = {c['ed_tau2']:.3f}$", MODEL),
            (rf"the study the protocol followed found $g = {o:.2f}$, \ with 23 and 24 people", GREY_A),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        with self.voiceover(
            f"Now ego depletion. <bookmark mark='a'/> As registered: random-effects pooling of each lab's standardized "
            f"difference, a one-sided test, and every lab that ran the protocol. <bookmark mark='b'/> The result: an "
            f"effect of {g_s}, with an interval from {lo_s} to {hi_s}. <bookmark mark='c'/> That's {verdict}. "
            f"<bookmark mark='d'/> The study the protocol followed found {o:.2f}, with twenty-three and twenty-four "
            f"people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(z), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dia))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(orig))
        self.clear_scene()


    def spread(self):
        c = load("confirm")
        head = heading(r"How much do the labs differ?")
        tv, te = np.sqrt(c["vo_tau2"]), np.sqrt(c["ed_tau2"])
        pi_lo = c["ed_est"] - 1.96 * np.sqrt(c["ed_tau2"] + c["ed_se"] ** 2)
        pi_hi = c["ed_est"] + 1.96 * np.sqrt(c["ed_tau2"] + c["ed_se"] ** 2)
        eq = MathTex(r"\hat\mu \pm 1.96\sqrt{\hat\tau^2 + \mathrm{SE}^2}", font_size=36, color=MODEL).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"random effects let each lab have its own true effect, \ spread with SD $\tau$ around the mean", WHITE),
            (rf"verbal overshadowing: \ $\hat\tau = {tv:.2f}$, \ $I^2 = {100 * c['vo_I2']:.0f}\%$: \ the labs differ "
             rf"no more than chance would make them", GOOD),
            (rf"ego depletion: \ $\hat\tau = {te:.2f}$, \ $I^2 = {100 * c['ed_I2']:.0f}\%$: \ some spread around an "
             rf"average near zero", AUTH),
            (rf"a 95\% prediction interval for a new lab's ego-depletion effect runs from {pi_lo:.2f} to {pi_hi:.2f}: "
             rf"\ a single lab could find either sign", PERSON),
            (r"the hidden-moderator objection (chapter 15) needs exactly this number to be large", YOU),
        ], 12.4, 21, 0.38).move_to([0, -0.8, 0])
        tag = psyche_tag(r"\texttt{capstone.pool}, \ DerSimonian-Laird")
        with self.voiceover(
            "One more question for the confirmatory analysis: how much do the labs differ? <bookmark mark='a'/> The "
            "random-effects model lets each lab have its own true effect, spread with a standard deviation tau. "
            "<bookmark mark='b'/> For verbal overshadowing, tau is estimated at zero. The labs differ no more than "
            "chance would make them. <bookmark mark='c'/> For ego depletion, there's some spread, around an average "
            "near zero. <bookmark mark='d'/> So a prediction interval for one new lab's result runs from about minus "
            "zero point three to plus zero point three five. A single lab could find either sign. <bookmark mark='e'/> The "
            "hidden-moderator objection, in chapter fifteen, needs exactly this number to be large."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
