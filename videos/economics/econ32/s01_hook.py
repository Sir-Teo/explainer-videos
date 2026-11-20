from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403

COUNTRIES = ("Australia", "Austria", "Belgium", "Canada", "Denmark", "Finland", "France", "Germany", "Greece",
             "Ireland", "Italy", "Japan", "Netherlands", "New Zealand", "Norway", "Portugal", "Spain", "Sweden", "UK",
             "US")
LEFT_OUT = ("Australia", "Austria", "Belgium", "Canada", "Denmark")


class Hook(VoiceoverScene):
    def construct(self):
        self.claim()
        self.sheet()
        self.question()
        self.title()
        self.objectives()

    def claim(self):
        H = load("hap")
        pub = H["steps"][0]["means"]
        ax = plane([0, 4.6], [-1, 5], center=LEFT * 1.8 + DOWN * 0.5, x_length=7.6, y_length=4.2, xticks=[],
                   yticks=[0, 2, 4], ylabel=r"average real GDP growth, \ \% a year", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        zero = seg(ax, 0, 0, 4.6, 0, GREY_C, 1.5)
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (b, m) in enumerate(zip(H["bins"], pub)):
            p0, p1 = ax.ax.c2p(0.35 + k * 1.1, 0), ax.ax.c2p(1.15 + k * 1.1, m)
            col = INFL if k == 3 else DEBT
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]) + 1e-3, fill_color=col, fill_opacity=0.85,
                          stroke_width=0).move_to((p0 + p1) / 2)
            bars.add(r)
            names.add(label(rf"debt {b.replace('%', r'\%')}", font_size=16, color=GREY_A).next_to(
                ax.ax.c2p(0.75 + k * 1.1, -1), DOWN, buff=0.1))
            vals.add(label(rf"{m:+.1f}\%", font_size=18, color=col).next_to(r, UP if m >= 0 else DOWN, buff=0.08))
        head = VGroup(label(r"2010: \ ``Growth in a Time of Debt''", font_size=28, color=E.ACCENT),
                      label(r"Carmen Reinhart and Kenneth Rogoff: \ 20 advanced economies, \ 1946--2009", font_size=21,
                            color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        foot = label(r"above 90\% of GDP, \ growth seemed to stop", font_size=24, color=INFL).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Reinhart and Rogoff, \ \emph{AER: P\&P} 100(2) (2010); \ the data as replicated by "
                            r"Herndon, \ Ash and Pollin", corner=DR, font_size=12)
        with self.voiceover(
            "In 2010 two of the most respected economists in the world, Carmen Reinhart and Kenneth Rogoff, "
            "published a short paper called Growth in a Time of Debt. <bookmark mark='a'/> They sorted twenty "
            "advanced economies' years since 1946 by the size of the government's debt. <bookmark mark='b'/> Below "
            f"thirty percent of GDP, growth averaged {pub[0]:.1f} percent a year; between thirty and ninety, about "
            "three. <bookmark mark='c'/> Above ninety percent, the average they reported was "
            f"{say_num(pub[3], 1)} percent. <bookmark mark='d'/> Growth seemed simply to stop once debt passed ninety "
            "percent of GDP, and the threshold was quoted in debates over austerity on both sides of the Atlantic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ax), FadeIn(zero), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(names))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:3]], lag_ratio=0.3), FadeIn(vals[:3]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3], UP), FadeIn(vals[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def sheet(self):
        H = load("hap")
        pub, cor = H["steps"][0]["means"][3], H["steps"][-1]["means"][3]
        rows = VGroup()
        for c in COUNTRIES:
            t = label(c, font_size=17, color=GREY_A)
            rows.add(t)
        grid = VGroup(*rows).arrange_in_grid(rows=10, cols=2, buff=(1.2, 0.14), col_alignments="ll")
        grid.move_to(LEFT * 3.6 + DOWN * 0.3)
        box = SurroundingRectangle(grid, color=GREY_D, buff=0.25, corner_radius=0.08)
        cap = label(r"the spreadsheet's countries", font_size=19, color=GREY_B).next_to(box, UP, buff=0.12)
        strikes = VGroup(*[Line(r.get_left() + LEFT * 0.05, r.get_right() + RIGHT * 0.05, color=INFL, stroke_width=3)
                           for r, c in zip(rows, COUNTRIES) if c in LEFT_OUT])
        side = VGroup(
            label(r"2013: \ Thomas Herndon, \ a graduate student \\ at the University of Massachusetts Amherst, \\ "
                  r"is asked to replicate it for a class", font_size=19, color=E.ACCENT),
            label(r"the formula: \ \texttt{=AVERAGE(L30:L44)} \\ it should have been \texttt{L30:L49}", font_size=19,
                  color=INFL),
            label(r"five countries left out", font_size=19, color=INFL),
            label(r"with Michael Ash and Robert Pollin: \\ two other choices mattered more", font_size=19,
                  color=GREY_A),
            label(rf"corrected: \ {say_num(pub, 1)}\% \ becomes \ {cor:+.1f}\%", font_size=24, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Herndon, \ Ash and Pollin, \ \emph{Cambridge Journal of Economics} 38(2) (2014)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Three years later a graduate student at the University of Massachusetts Amherst, Thomas Herndon, was "
            "asked to replicate a well-known result for a class, and chose this one. He "
            "could not. <bookmark mark='a'/> Reinhart and Rogoff kindly sent him their spreadsheet. "
            "<bookmark mark='b'/> The formula that averaged the countries ran over rows thirty to forty-four, not "
            "thirty to forty-nine. <bookmark mark='c'/> Five countries had been left out: Australia, Austria, "
            "Belgium, Canada and Denmark. <bookmark mark='d'/> With his professors Michael Ash and Robert Pollin he "
            "found two further choices that mattered even more: some years of high debt and decent growth were "
            "left out, and each country's average counted the same, whether it spent one year above ninety percent "
            f"or nineteen. <bookmark mark='e'/> Corrected, growth above ninety percent averaged {cor:.1f} percent, "
            "lower than below it, but nothing like a cliff. This part takes the government's budget seriously, "
            "and the evidence about it more seriously still."
        ) as vo:
            self.play(FadeIn(grid), Create(box), FadeIn(cap), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(box, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s_) for s_ in strikes], lag_ratio=0.2),
                      *[r.animate.set_color(GREY_D) for r, c in zip(rows, COUNTRIES) if c in LEFT_OUT],
                      FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4], scale=1.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"when does debt grow, \ and what does it take to hold it steady?", font_size=26, color=DEBT),
            label(r"how much output does a dollar of spending or taxes move, \ and how do we know?", font_size=26,
                  color=SPEND),
            label(r"when do debts become dangerous, \ and why do countries repay at all?", font_size=26, color=INFL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: what can a government's budget do for the economy, and how much debt is too "
            "much? <bookmark mark='a'/> When does debt grow, and what does it take to hold it steady? "
            "<bookmark mark='b'/> How much does a dollar of government spending or taxes move output, and how can "
            "anyone tell? <bookmark mark='c'/> And when do debts become dangerous, and why do countries repay them "
            "at all?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1889, 2027], [0, 120], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["debt"], DEBT, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 32 \ $\cdot$ \ The Treasury", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-two: the treasury."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the budget constraint and debt dynamics; \ r minus g; \ the minister's budget",
            r"the multiplier in theory, \ and in four kinds of evidence; \ tax changes",
            r"automatic stabilizers; \ austerity; \ the 90\% threshold recomputed",
            r"is debt a burden? \ tax smoothing; \ the fiscal theory of the price level",
            r"sovereign default solved; \ modern monetary theory; \ two dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> The government's budget constraint and how debt evolves, which "
            "turns on the gap between the interest rate and growth; then you balance a budget. "
            "<bookmark mark='b'/> The multiplier in theory, and in four kinds of evidence, and what tax changes "
            "do. <bookmark mark='c'/> Automatic stabilizers, the fight over austerity, and the ninety percent "
            "threshold recomputed from the original data. <bookmark mark='d'/> Whether debt is a burden at all, "
            "why debt should absorb wars, and a theory in which the budget sets the price level. "
            "<bookmark mark='e'/> Sovereign default as a model solved on screen, modern monetary theory, and two "
            "dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
