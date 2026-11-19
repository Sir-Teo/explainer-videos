from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

DESIGN_SHORT = {"IV": "IV", "survey": "survey", "meta-analysis": "meta", "calibration": "calib.", "structural": "str.",
                "lab": "lab"}


class EIS(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Time meets risk", r"Is disliking risk the same thing as disliking ups and downs over time?",
             "Chapter ten. Time meets risk: substitution against aversion.", lit={1989: r"Epstein and Zin"},
             horizon=("a year", "a decade"))
        self.one_number()
        self.plane_of_estimates()
        self.epstein_zin()
        self.puzzles()

    def one_number(self):
        rows = VGroup(
            MathTex(r"u(c) = \frac{c^{1-\gamma}}{1-\gamma}", font_size=44, color=UTIL),
            label(r"across \emph{states}: \ relative risk aversion \ $=\gamma$", font_size=29, color=RISKY),
            label(r"across \emph{time}: \ the elasticity of intertemporal substitution \ $= 1/\gamma$", font_size=29,
                  color=LATER),
            label(r"one number for two different attitudes: \\ to gambles, \ and to a bumpy path of consumption",
                  font_size=27, color=E.ACCENT),
            label(r"a person who hates risk must hate saving for growth, \ and the reverse", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "The power function has been doing two jobs at once. <bookmark mark='a'/> Across states of the world, the "
            "outcomes of a gamble, its gamma is relative risk aversion. <bookmark mark='b'/> Across time, in Fisher's "
            "diagram, one over gamma is the elasticity of intertemporal substitution. <bookmark mark='c'/> So a single "
            "number sets two different attitudes: how much you dislike gambles, and how much you dislike a bumpy path "
            "of consumption from year to year. <bookmark mark='d'/> Someone who hates risk must be unwilling to "
            "postpone consumption for a higher return, and someone happy to postpone must enjoy risk. There's no "
            "reason people should be built that way."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def plane_of_estimates(self):
        e = load("eis")
        ax = plane([-1.4, 0.6], [-0.6, 1.4], center=LEFT * 2.6 + DOWN * 0.2, x_length=6.4, y_length=6.0,
                   xticks=[-1, float(np.log10(0.3)), 0, float(np.log10(3))], yticks=[0, float(np.log10(3)), 1.0],
                   xlabel=r"elasticity of intertemporal substitution \ (log scale)",
                   ylabel=r"relative risk aversion \ (log scale)", font_size=16, xfmt=lambda v: f"{10 ** v:.1g}",
                   yfmt=lambda v: f"{10 ** v:.1g}")
        a = ax.ax
        diag = Line(a.c2p(-1.4, 1.4), a.c2p(0.6, -0.6), color=UTIL, stroke_width=3)
        dl = label(r"expected utility: \\ aversion $= 1/$EIS", font_size=19, color=UTIL).next_to(a.c2p(-0.1, 0.1), UR,
                                                                                               buff=0.1)
        ex = VGroup()
        for who, yr, design, val in e["eis_rows"]:
            x = np.log10(val) if val > 0.05 else -1.32          # zero has no place on a log scale: pinned left
            ex.add(Line(a.c2p(x, -0.6), a.c2p(x, -0.48), color=LATER, stroke_width=4))
        ex.add(label(r"$\approx 0$", font_size=17, color=LATER).next_to(a.c2p(-1.32, -0.48), UP, buff=0.06))
        ry = VGroup()
        for who, yr, design, val in e["rra_rows"]:
            y = np.log10(val)
            ry.add(Line(a.c2p(-1.4, y), a.c2p(-1.28, y), color=RISKY, stroke_width=4))
        by = Dot(a.c2p(np.log10(1.5), 1.0), radius=0.1, color=E.ACCENT)
        byl = label(r"Bansal and Yaron (2004): \\ $\gamma = 10$, \ EIS 1.5", font_size=18, color=E.ACCENT).next_to(
            by, LEFT, buff=0.12)
        side = VGroup(
            label(r"the estimates, each on its own axis:", font_size=24),
            label(r"the EIS: \ about 0 in aggregate data, \\ 0.3--0.4 for stockholders, \ 0.8--1 for \\ bondholders, "
                  r"\ about 2 from tax changes", font_size=21, color=LATER),
            label(r"risk aversion: \ about 1 from consumption \\ and labour supply, \ 4 from survey gambles, \\ 2--7 "
                  r"in finance, \ 10 in calibrations", font_size=21, color=RISKY),
            label(r"Barsky et al.\ (1997): \ across people, \\ risk tolerance and the EIS \\ are unrelated",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"the dials' rows (chapter 13)", corner=DR, font_size=14)
        with self.voiceover(
            "Here's the plane of both attitudes, on log scales. <bookmark mark='a'/> Expected utility with the power "
            "function forces everyone onto this line, where risk aversion is one over the elasticity. "
            "<bookmark mark='b'/> Now the estimates, which chapter thirteen collects. Along the bottom, estimates of "
            "the elasticity: from near zero in aggregate data, through a third for stockholders and nearly one for "
            "bondholders, to about two from tax changes. <bookmark mark='c'/> Up the side, estimates of risk "
            "aversion: about one, four, five, ten. <bookmark mark='d'/> If people lived on the line, an elasticity "
            "of a third would mean risk aversion of three, and an elasticity of two would mean a half. And when "
            "Robert Barsky and his colleagues measured both attitudes in the same people, in 1997, they found them "
            "essentially unrelated. <bookmark mark='e'/> The models that price assets need a point far off the line: "
            "Ravi Bansal and Amir Yaron's, in 2004, has risk aversion ten and an elasticity of one and a half."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(dl))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in ex], lag_ratio=0.2), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t) for t in ry], lag_ratio=0.2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(by, scale=0.5), FadeIn(byl))
        self.clear_scene()

    def epstein_zin(self):
        e = load("eis")
        eq = MathTex(r"V_t \;=\; \Bigl[(1-\beta)\,c_t^{\,1-1/\psi} \;+\; \beta\,\bigl(\mathrm{CE}_\gamma"
                     r"[V_{t+1}]\bigr)^{1-1/\psi}\Bigr]^{\frac{1}{1-1/\psi}}", font_size=40).to_edge(UP, buff=0.6)
        names = VGroup(label(r"$\psi$: \ the EIS, \ for time", font_size=26, color=LATER),
                       label(r"$\gamma$: \ risk aversion, \ inside the certainty equivalent", font_size=26,
                             color=RISKY)).arrange(RIGHT, buff=1.0).next_to(eq, DOWN, buff=0.35)
        head = label(r"Kreps and Porteus (1978); \ Epstein and Zin (1989)", font_size=23, color=GREY_B).next_to(
            names, DOWN, buff=0.3)
        lot = label(r"consumption 1 now, 1 next season, then 0.8 or 1.2 (50--50): \ learn which next season, or only "
                    r"when it comes?", font_size=23).next_to(head, DOWN, buff=0.45)
        rows = VGroup()
        for c in e["calibrations"]:
            col = E.ACCENT if c["prefers_early"] else (GREY_A if abs(c["gamma"] * c["psi"] - 1) < 1e-9 else LATER)
            verdict = (rf"pays {100 * c['premium']:.1f}\% of today's consumption to learn early" if c["prefers_early"]
                       else (r"indifferent: \ expected utility" if abs(c["gamma"] * c["psi"] - 1) < 1e-9 else
                             r"prefers to learn late"))
            rows.add(VGroup(label(rf"$\gamma = {c['gamma']:g}$, \ $\psi = {c['psi']:g}$", font_size=25),
                            label(verdict, font_size=25, color=col)).arrange(RIGHT, buff=0.6))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(lot, DOWN, buff=0.35)
        rule = label(r"early resolution is preferred exactly when $\gamma > 1/\psi$", font_size=26,
                     color=E.ACCENT).to_edge(DOWN, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The way out was found in 1978 by David Kreps and Evan Porteus, and turned into a workhorse by Larry "
            "Epstein and Stanley Zin in 1989. <bookmark mark='a'/> Value today is a blend of consumption today and the "
            "certainty equivalent of value tomorrow. The blend across time uses one parameter, psi, the elasticity of "
            "substitution. The certainty equivalent across states uses another, gamma, risk aversion. Two attitudes, "
            "two numbers. <bookmark mark='b'/> The separation has a strange consequence: people can care when risk is "
            "resolved. Take a sure season now and next, and then consumption of nought point eight or one point two. "
            "Would you rather learn which next season, or only when it arrives? Nothing you can do depends on it. "
            "<bookmark mark='c'/> Expected utility doesn't care. Bansal and Yaron's chooser would give up six "
            "percent of today's consumption to know early. A chooser with little risk aversion, gamma a half, "
            "against an elasticity of a half, would rather not know. <bookmark mark='d'/> The rule: early resolution is preferred exactly when "
            "gamma is larger than one over psi."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head), Write(eq), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(lot))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.5), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.clear_scene()

    def puzzles(self):
        mp = tables.MEHRA_PRESCOTT_1985.data
        c1 = history_card(1985, r"Mehra and Prescott: \ the equity premium", rf"American stocks beat short-term "
                          rf"bills by about {100 * mp['premium']:.0f} points a year, {mp['period'][0]}--"
                          rf"{mp['period'][1]}; \ with consumption as smooth as it is, risk aversion of 10 or less "
                          r"cannot produce it", color=RISKY, width=11.6, font_size=23)
        c2 = history_card(1989, r"Weil: \ the risk-free rate puzzle", r"raise $\gamma$ to fit the premium, and with "
                          r"expected utility the EIS falls to $1/\gamma$: \ people would then want to borrow against "
                          r"their growing incomes, \ and interest rates would be far higher than they are",
                          color=LATER, width=11.6, font_size=23)
        c3 = history_card(r"since", r"Epstein--Zin preferences in asset pricing", r"high risk aversion for the "
                          r"premium, \ a high EIS for the low safe rate: \ long-run risks (Bansal and Yaron), \ "
                          r"habits, \ disasters; \ Part 23", color=E.ACCENT, width=11.6, font_size=23)
        g = VGroup(c1, c2, c3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        tag = published_tag(r"Mehra and Prescott, JME (1985); Weil, JME (1989)", corner=DR, font_size=14)
        with self.voiceover(
            "Why does finance care so much? <bookmark mark='a'/> In 1985 Rajnish Mehra and Edward Prescott pointed "
            "out that American stocks had beaten short-term bills by about six percentage points a year from 1889 to "
            "1978. Consumption is so smooth from year to year that, with any risk aversion they thought plausible, "
            "ten or less, the standard model couldn't come close. <bookmark mark='b'/> Raise gamma high enough to fit "
            "the premium, and Philippe Weil showed in 1989 that a second puzzle appears. With expected utility, a "
            "high gamma means a tiny elasticity of substitution: people would badly want to borrow against their "
            "growing future incomes, and safe interest rates would have to be far higher than they've been. "
            "<bookmark mark='c'/> Separating the two attitudes lets a model have high risk aversion for the premium "
            "and a high elasticity for the low safe rate. That's why Epstein and Zin's preferences are everywhere in "
            "asset pricing, and Part twenty-three picks the story up."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.clear_scene()
