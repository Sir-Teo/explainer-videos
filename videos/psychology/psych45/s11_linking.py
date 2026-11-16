from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Linking(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.anchors()
        self.equate()

    def card(self):
        card = chapter_card(10, r"Linking and equating", r"Is this year's test as hard as last year's?",
                            lit={2014: r"Kolen \& Brennan"}, part=PART, scale=("person", "society"), marr=("how",))
        with self.voiceover("Chapter ten. Linking and equating."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        head = heading(r"Two years, \ two forms")
        rows = rows_of([
            (r"a test is given every year; \ its items must change, \ or they leak", WHITE),
            (r"each year's calibration puts that year's people at mean 0 and SD 1: \ the scale's zero moves with the "
             r"cohort", AUTH),
            (r"if this year's students are abler, \ a separate calibration hides it, \ and makes this year's items "
             r"look harder than they are", PERSON),
            (r"the fix: \ common items, \ anchors, \ given in both years, \ whose difficulties tie the two scales "
             r"together", GOOD),
        ], 12.4, 23, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "A test given every year faces a problem. <bookmark mark='a'/> Its items must change, or they leak. "
            "<bookmark mark='b'/> But each year's calibration puts that year's people at a mean of zero and a "
            "standard deviation of one. The zero of the scale moves with the cohort. <bookmark mark='c'/> If this "
            "year's students are abler, a separate calibration hides it, and makes this year's items look harder than "
            "they are. <bookmark mark='d'/> The fix is common items, called anchors, given in both years, whose "
            "difficulties tie the two scales together."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def anchors(self):
        d = load("linking")
        head = heading(r"Mean and sigma")
        A = axes([-3.5, 3.5], [-3.5, 3.5], x_length=3.6, y_length=3.6, xticks=[-3, 0, 3], yticks=[-3, 0, 3],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"anchor, \ this year's scale",
                 ylabel=r"anchor, \ last year's", center=[-4.0, 0.2, 0], font_size=13)
        pts = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.07, color=PERSON) for x, y in zip(d["anchor_y"], d["anchor_x"])])
        xx = np.linspace(-3.5, 3.5, 50)
        fit = curve(A.ax, xx, d["A"] * xx + d["B"], GOOD, stroke_width=3)
        ident = DashedLine(A.ax.c2p(-3.5, -3.5), A.ax.c2p(3.5, 3.5), color=GREY_B, stroke_width=1.5)
        eq = MathTex(r"A = \frac{\mathrm{SD}(b^{\text{old}})}{\mathrm{SD}(b^{\text{new}})}, \quad B = \bar b^{\text{old}}"
                     r" - A\,\bar b^{\text{new}}", font_size=30, color=MODEL).move_to([-3.6, -2.7, 0])
        rows = rows_of([
            (r"Psyche: \ two 30-item forms sharing 10 anchors; \ this year's 2{,}000 students are abler (mean 0.5) and "
             r"more varied (SD 1.2)", WHITE),
            (r"each form calibrated alone; \ the anchors' two sets of difficulties fall on a line, \ not the diagonal",
             PERSON),
            (rf"mean-sigma linking: \ $A = {d['A']:.2f}$, \ $B = {d['B']:.2f}$; \ the truth was 1.2 and 0.5", MODEL),
            (rf"the new items' difficulties, \ off by {d['err_before']:.2f} on average before linking, \ are off by "
             rf"{d['err_after']:.2f} after", GOOD),
        ], 6.2, 19, 0.38).move_to([3.2, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.mean\_sigma}; \ two simulated forms")
        with self.voiceover(
            "Here's linking at work. <bookmark mark='a'/> Psyche makes two thirty-item forms that share ten anchors. "
            "This year's students are abler and more varied. <bookmark mark='b'/> Calibrate each form alone, and the "
            "anchors' two sets of difficulties fall on a line, but not on the diagonal. <bookmark mark='c'/> The "
            "slope and intercept of that line come from the anchors' means and standard deviations. Here, one point "
            "two one and zero point four three, against a truth of one point two and zero point five. "
            "<bookmark mark='d'/> Before linking, the new items' difficulties were off by about zero point four. "
            "After, by less than zero point one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(ident))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(pts))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(fit), FadeIn(eq))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def equate(self):
        d = load("linking")
        head = heading(r"From score to score")
        A = axes([-4, 4], [0, 30], x_length=5.6, y_length=3.4, xticks=[-4, -2, 0, 2, 4], yticks=[0, 10, 20, 30],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", xlabel=r"ability (last year's scale)",
                 ylabel=r"expected score (of 30)", center=[-3.3, 0.3, 0], font_size=13)
        cx = curve(A.ax, d["th"], d["tcc_x"], GOOD, stroke_width=4)
        cy = curve(A.ax, d["th"], d["tcc_y"], PERSON, stroke_width=4)
        k = 2
        th15 = float(np.interp(d["scores"][k], d["tcc_y"], d["th"]))
        path = VGroup(DashedLine(A.ax.c2p(-4, d["scores"][k]), A.ax.c2p(th15, d["scores"][k]), color=PERSON,
                                 stroke_width=2),
                      DashedLine(A.ax.c2p(th15, d["scores"][k]), A.ax.c2p(th15, d["equated"][k]), color=GREY_B,
                                 stroke_width=2),
                      DashedLine(A.ax.c2p(th15, d["equated"][k]), A.ax.c2p(-4, d["equated"][k]), color=GOOD,
                                 stroke_width=2))
        key = VGroup(label(r"last year's form", font_size=13, color=GOOD), label(r"this year's form", font_size=13,
                                                                                 color=PERSON)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"each form's test characteristic curve: \ the expected score at each ability, \ now on one scale", WHITE),
            (rf"this year's form is a little harder: \ a score of {d['scores'][k]} on it means the ability that "
             rf"scores {d['equated'][k]:.1f} on last year's", PERSON),
            (r"true-score equating reads across the two curves: \ score, \ to ability, \ to the other form's score",
             MODEL),
            (r"so a pass mark can mean the same thing every year, \ though no two years share a test", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.prob}; \ the linked forms")
        with self.voiceover(
            "Linking puts the items on one scale. Equating puts the scores there too. <bookmark mark='a'/> Each "
            "form has a test characteristic curve: the expected score at each ability, now on last year's scale. "
            "<bookmark mark='b'/> This year's form is a little harder. A score of fifteen on it means the ability "
            "that scores about sixteen on last year's. <bookmark mark='c'/> True-score equating reads across the two "
            "curves: from a score, to an ability, to the other form's score. <bookmark mark='d'/> So a pass mark can "
            "mean the same thing every year, though no two years share a test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cx), Create(cy))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(path), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
