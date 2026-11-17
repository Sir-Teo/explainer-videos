from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Nps(VoiceoverScene):
    def construct(self):
        self.card()
        self.score()
        self.noise()

    def card(self):
        card = chapter_card(12, r"One number to rule them all?", r"Can one question predict a company's growth?",
                            lit={2003: r"Reichheld", 2007: r"Keiningham et al."}, part=PART, scale=("society",),
                            marr=("what",))
        with self.voiceover("Chapter twelve. One number to rule them all?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def score(self):
        d = load("nps")
        head = heading(r"The net promoter score")
        A = axes([-0.5, 10.5], [0, 0.2], x_length=5.6, y_length=2.8, xticks=list(range(11)), yticks=[0, 0.1, 0.2],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"how likely to recommend (0 to 10)",
                 ylabel=r"share", center=[-3.3, 0.5, 0], font_size=13)
        cols = [AUTH] * 7 + [GREY_B] * 2 + [GOOD] * 2
        b = bars(A.ax, np.arange(11), d["hist"], cols, width=0.7)
        eq = MathTex(r"\text{NPS} = \%\,\text{promoters (9--10)} - \%\,\text{detractors (0--6)}", font_size=30,
                     color=MODEL).move_to([-3.3, -1.9, 0])
        rows = rows_of([
            (r"Reichheld, \ 2003: \ ``the one number you need to grow'': \ how likely are you to recommend us?", WHITE),
            (rf"eleven answers become three groups: \ here {100 * d['share_promoters']:.0f}\% promoters, "
             rf"{100 * d['share_detractors']:.0f}\% detractors, \ NPS = {d['nps']:.0f}", MODEL),
            (r"the claim: \ it predicts growth better than other measures of satisfaction", PERSON),
            (r"Keiningham and colleagues, \ 2007: \ tested over time, \ it did no better than the alternatives; \ "
             r"the Ledger's verdict: \ failed", AUTH),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Reichheld (2003); \ Keiningham et al. (2007)")
        with self.voiceover(
            "In 2003 Fred Reichheld published the one number you need to grow. <bookmark mark='a'/> One question: "
            "how likely are you to recommend us, from nought to ten? <bookmark mark='b'/> The eleven answers become "
            "three groups. Subtract the percentage of detractors, nought to six, from the percentage of promoters, "
            "nine and ten. <bookmark mark='c'/> The claim was that this predicts a company's growth better than other "
            "measures of satisfaction. <bookmark mark='d'/> In 2007 Timothy Keiningham and colleagues tested it over "
            "time, and it did no better than the alternatives. The Ledger's verdict: failed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def noise(self):
        d = load("nps")
        head = heading(r"A noisy number")
        A = axes([0, 1050], [0, 13], x_length=5.6, y_length=3.0, xticks=[50, 200, 400, 1000], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"customers asked",
                 ylabel=r"standard error (points)", center=[-3.3, 0.3, 0], font_size=13)
        c = curve(A.ax, d["ns"], d["se_nps"], AUTH, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(n, s), radius=0.07, color=AUTH) for n, s in zip(d["ns"], d["se_nps"])])
        se200 = float(d["se_nps"][list(d["ns"]).index(200)])
        rows = rows_of([
            (rf"from 200 customers, \ the NPS has a standard error of about {se200:.1f} points: \ a margin of error "
             rf"of $\pm${1.96 * se200:.0f}", AUTH),
            (r"a month-to-month change of five points is usually noise", PERSON),
            (rf"collapsing eleven points to three groups loses some information: \ with 200 customers each, \ the "
             rf"NPS picks the better of two products {100 * d['right_nps']:.0f}\% of the time, \ the mean rating "
             rf"{100 * d['right_mean']:.0f}\%", MODEL),
            (r"a reasonable tracking number, \ if reported with its error; \ not a law of growth", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.nps\_se}, \ simulated customers")
        with self.voiceover(
            "It's also a noisy number. <bookmark mark='a'/> From two hundred customers, the score has a standard "
            "error of about five and a half points: a margin of error of about plus or minus eleven. "
            "<bookmark mark='b'/> So a month-to-month change of five points is usually noise. <bookmark mark='c'/> "
            "Collapsing eleven points into three groups loses a little information. With two hundred customers each, "
            "it picks the better of two products about ninety percent of the time, slightly less often than the "
            "plain mean. <bookmark mark='d'/> A reasonable number to track, if it's reported with its error. Not a "
            "law of growth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c), FadeIn(dots))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
