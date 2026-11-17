from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Utility(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"From a correlation to money", r"What is a validity of 0.3 worth?", marr=("how",))
        self.tr()
        self.bcg()

    def tr(self):
        d = load("tr")
        head = heading(r"Taylor and Russell, \ 1939")
        A = axes([0, 1.0], [0.45, 0.92], x_length=5.6, y_length=3.0, xticks=[0.1, 0.3, 0.5, 0.7, 0.9],
                 yticks=[0.5, 0.7, 0.9], xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"share of applicants hired", ylabel=r"hires who succeed", center=[-3.3, 0.3, 0], font_size=12)
        cols = [GREY_B, SYMP, MODEL, PERSON, GOOD]
        cs = VGroup(*[curve(A.ax, d["ratios"], d["success"][i], cols[i], stroke_width=3) for i in range(5)])
        key = VGroup(*[label(rf"$r$ = {v:.1f}", font_size=12, color=c) for v, c in zip(d["validity"], cols)])
        key.arrange(RIGHT, buff=0.3).next_to(A, UP, buff=0.2)
        k = int(np.where(np.isclose(d["ratios"], 0.2))[0][0])
        rows = rows_of([
            (r"half of all applicants would succeed (the base rate); \ hire some share of them by a test of validity "
             r"$r$", WHITE),
            (rf"with $r$ = 0.3 and the top 20\% hired, \ {100 * d['success'][2][k]:.0f}\% of hires succeed, \ against "
             rf"50\% by chance", MODEL),
            (r"the same test is worth more when you can be choosy: \ at 90\% hired almost nothing changes", PERSON),
            (r"a modest correlation is a real gain when the selection ratio is small: \ the tables made this visible "
             r"in 1939", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.taylor\_russell}, \ base rate 50\%")
        with self.voiceover(
            "What is a validity of zero point three worth? <bookmark mark='a'/> In 1939 H. C. Taylor and J. T. Russell "
            "answered with tables. Suppose half of all applicants would succeed, and you hire some share of them by a "
            "test with validity r. <bookmark mark='b'/> With a validity of zero point three and the top fifth hired, "
            "sixty-seven percent of hires succeed, against fifty by chance. <bookmark mark='c'/> The same test is "
            "worth more when you can be choosy. If you hire nine applicants in ten, almost nothing changes. "
            "<bookmark mark='d'/> A modest correlation is a real gain when the selection ratio is small. The tables "
            "made that visible in 1939."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.2))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bcg(self):
        d = load("utility")
        head = heading(r"The Brogden-Cronbach-Gleser formula")
        eq = MathTex(r"\Delta U = N_s\,T\,r\,SD_y\,\bar z_x - C", font_size=40).move_to([0, 2.0, 0])
        A = axes([0.3, 4.7], [0, 8], x_length=5.0, y_length=2.6, xticks=None, yticks=[0, 4, 8],
                 yfmt=lambda v: f"{v:.0f}M", ylabel=r"net gain over 5 years", center=[-3.5, -0.6, 0], font_size=12)
        keys = ["unstructured_2022", "ability_2022", "structured_2022", "ability_1998"]
        cols = [AUTH, MODEL, GOOD, GREY_B]
        vals = [d[k] / 1e6 for k in keys]
        b = bars(A.ax, [1, 2, 3, 4], vals, cols, width=0.6)
        names = VGroup(*[label(s, font_size=12, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, s in enumerate([r"unstructured", r"ability (2022)", r"structured", r"ability (1998)"])])
        rows = rows_of([
            (r"the gain from hiring $N_s$ people for $T$ years: \ validity, \ times the money value of one SD of "
             r"performance, \ times how far above average the hires score, \ minus the cost of testing", WHITE),
            (r"100 hires, \ 5 years, \ $SD_y$ = 20,000 a year, \ the top 20\% of applicants, \ 100 a test", MODEL),
            (rf"structured interview (0.42): \ about {d['structured_2022'] / 1e6:.1f} million; \ ability test at the "
             rf"2022 estimate (0.31): \ {d['ability_2022'] / 1e6:.1f} million; \ at the 1998 estimate: \ "
             rf"{d['ability_1998'] / 1e6:.1f} million", PERSON),
            (r"$SD_y$ is the shakiest number: \ estimates of what a better worker is worth vary widely, \ so treat "
             r"the money as a scale, \ not a promise", YOU),
        ], 6.4, 18, 0.32).move_to([3.3, -0.6, 0])
        tag = psyche_tag(r"\texttt{work.bcg\_utility}, \ illustrative costs")
        with self.voiceover(
            "Hubert Brogden, Lee Cronbach and Goldine Gleser turned validity into money. <bookmark mark='a'/> The gain "
            "from hiring N people for T years is the validity, times the money value of one standard deviation of "
            "performance, times how far above average the hires score on the predictor, minus the cost of testing. "
            "<bookmark mark='b'/> Take a hundred hires for five years, a standard deviation worth twenty thousand a "
            "year, the top fifth of applicants, and a hundred per test. <bookmark mark='c'/> A structured interview "
            "is worth almost six million. An ability test at the 2022 estimate, about four. At the 1998 estimate it "
            "would have been seven. <bookmark mark='d'/> The standard deviation in money is the shakiest number. "
            "Estimates of what a better worker is worth vary widely, so treat the money as a scale, not a promise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in b], lag_ratio=0.25))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
