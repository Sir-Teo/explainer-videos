from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.fair()
        self.ogive()
        self.crowd()
        self.objectives()

    def fair(self):
        tl = timeline(lit=(1907,)).to_edge(UP, buff=0.35)
        hc = history_card(1907, r"Francis Galton, \ ``Vox populi'', \ \emph{Nature} 75",
                          r"the West of England Fat Stock and Poultry Exhibition, Plymouth: \ 800 tickets at sixpence each, "
                          r"\ guess the weight of an ox once slaughtered and dressed; \ 787 legible", color=S.MUSEUM,
                          width=7.4, font_size=24).move_to([-2.4, 0.4, 0])
        ask = label(r"Galton's question: \ how trustworthy is a democratic judgment?", font_size=26, color=GREY_A)
        ask.next_to(hc, DOWN, buff=0.6).align_to(hc, LEFT)
        ox = VGroup(RoundedRectangle(width=2.6, height=1.5, corner_radius=0.3, stroke_color=S.MUSEUM, stroke_width=2.5),
                    MathTex(r"?\ \text{lb}", font_size=48, color=S.MUSEUM)).move_to([4.4, 0.4, 0])
        tickets = VGroup(*[Rectangle(width=0.32, height=0.2, stroke_color=GREY_B, stroke_width=1, fill_color="#1b2130",
                                     fill_opacity=1).move_to([3.2 + 0.36 * (k % 7), -1.4 - 0.26 * (k // 7), 0]).rotate(0.15 * ((k * 7) % 5 - 2))
                           for k in range(28)])
        with self.voiceover(
            "In 1906, at a livestock fair in Plymouth, a fat ox stood on display, and for sixpence "
            "you could guess its weight once it had been slaughtered and dressed. <bookmark mark='a'/> Eight hundred "
            "people bought tickets: butchers and farmers who knew cattle, and plenty of others who didn't. Francis "
            "Galton, now in his eighties, obtained the tickets afterwards; seven hundred and eighty-seven were "
            "legible. <bookmark mark='b'/> He wanted to know how trustworthy a popular judgment is, and he wasn't "
            "expecting much. <bookmark mark='c'/> He published what he found in Nature in March 1907, under the "
            "title Vox Populi: the voice of the people."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(ox), LaggedStart(*[FadeIn(t) for t in tickets], lag_ratio=0.05))
            vo.wait_until("b")
            self.play(FadeIn(ask))
            vo.wait_until("c")
            self.play(Indicate(hc, color=S.MUSEUM))
        self.clear_scene()

    def ogive(self):
        d = load("ox")
        deg, est = np.asarray(d["deg"]), np.asarray(d["est"])
        A = axes([0, 100], [1050, 1320], x_length=7.4, y_length=5.0, xlabel=r"position in Galton's array (percent of guesses)",
                 ylabel=r"estimate (lb)", xticks=[0, 25, 50, 75, 100], yticks=[1100, 1150, 1200, 1250, 1300],
                 center=[-2.4, -0.4, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=DATA) for a, b in zip(deg, est)])
        xs = np.linspace(2, 98, 120)
        from scipy import stats as st
        nrm = curve(ax, xs, d["median"] + d["sd"] * st.norm.ppf(xs / 100), EXACT, 2.5)
        truth = DashedLine(ax.c2p(0, d["truth"]), ax.c2p(100, d["truth"]), color=S.LIK, stroke_width=2.5)
        tl_ = label(r"dressed weight: \ 1{,}198 lb", font_size=22, color=S.LIK).next_to(ax.c2p(2, d["truth"]), UR, buff=0.08)
        med = Dot(ax.c2p(50, d["median"]), radius=0.1, color=S.EST)
        rows = VGroup(
            MathTex(r"\text{median: } 1{,}207\ \text{lb}", font_size=30, color=S.EST),
            MathTex(rf"\text{{error: }} +9\ \text{{lb}} = {d['err_pct']:.1f}\%", font_size=28, color=S.EST),
            MathTex(r"\text{quartiles: } 1{,}162 \text{ and } 1{,}236", font_size=26, color=GREY_A),
            MathTex(r"\text{mean (Galton's later letter): } 1{,}197", font_size=26, color=GREY_A),
            label(r"gold: \ a normal with Galton's probable error, \ 37 lb", font_size=22, color=EXACT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.3, 0.6, 0])
        for r in rows:
            if r.width > 5.2:
                r.width = 5.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.3, 0.6, 0])  # re-align after clamping
        tag = historical_tag(r"Galton (1907): \ the estimates at every 5th percentile", corner=DR)
        with self.voiceover(
            "Galton sorted the guesses from lowest to highest and printed every twentieth part of the line: the "
            "fifth percentile, the tenth, and so on. <bookmark mark='a'/> Here they are. Plotted against their "
            "position, they make an S-shaped curve, which Galton called an ogive. <bookmark mark='b'/> The middle "
            "guess, the median, was one thousand two hundred and seven pounds. <bookmark mark='c'/> The ox weighed "
            "one thousand one hundred and ninety-eight. The crowd was nine pounds high: less than one percent. "
            "<bookmark mark='d'/> The middle half of the guesses spanned seventy-four pounds; half of that, "
            "thirty-seven, is what Galton called the probable error. He drew the normal curve with that spread, in "
            "gold, and it fits the middle well, though the low guesses straggle further than the high ones. Three "
            "weeks later, in a letter, he gave the mean: eleven hundred and ninety-seven, one pound light."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(med), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(truth), FadeIn(tl_), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(nrm), FadeIn(rows[2:]))
        self.clear_scene()

    def crowd(self):
        d = load("ox")
        ns = np.asarray(d["crowd_ns"], float)
        A = axes([0, 3], [0, 2.1], x_length=6.6, y_length=4.4, xlabel=r"number of guessers averaged, $n$ (log scale)",
                 ylabel=r"typical error of the average (lb, log scale)", xticks=[0, 1, 2, 3], yticks=[0, 1, 2],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.6, -0.5, 0])
        ax = A.ax
        ind = curve(ax, np.log10(ns), np.log10(d["crowd_indep"]), SIM, 3.5)
        shr = curve(ax, np.log10(ns), np.log10(d["crowd_shared"]), BOUND, 3.5)
        floor = DashedLine(ax.c2p(0, np.log10(20)), ax.c2p(3, np.log10(20)), color=BOUND, stroke_width=1.5)
        leg = legend([(SIM, r"independent errors: \ $75/\sqrt n$"), (BOUND, r"plus a shared bias of 20 lb")], font_size=22)
        leg.move_to([3.8, 1.8, 0])
        qs = VGroup(label(r"why does averaging work?", font_size=28, color=S.ACCENT),
                    label(r"how fast?", font_size=28, color=S.ACCENT),
                    label(r"and when does it fail?", font_size=28, color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        qs.move_to([3.8, -0.6, 0])
        tag = note(r"simulated: guesses with error SD 75 lb, \ 2,000 crowds of each size").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Why should a crowd do so well? Here's a toy version. <bookmark mark='a'/> Suppose every guess is the "
            "truth plus an independent error of about seventy-five pounds. Average n guesses, and the typical error "
            "shrinks like seventy-five over root n: a straight line on these log scales, falling by a factor of ten "
            "for every hundredfold increase in the crowd. <bookmark mark='b'/> But suppose everyone shares a bias, "
            "say twenty pounds, because the ox looked heavier than it was. Then the error stops falling at twenty, "
            "Part 5's lesson about shared noise. <bookmark mark='c'/> This part asks three questions. Why does "
            "averaging work? How fast? And when does it fail?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ind), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(shr), Create(floor), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.2) for q in qs], lag_ratio=0.5))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 6", font_size=34, color=GREY_B), label(r"The Laws of Averages", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Markov's, Chebyshev's and Jensen's inequalities; \ the weak law of large numbers",
            r"convergence in probability and in distribution; \ the central limit theorem, seen and proved",
            r"the normal approximation; \ how fast it arrives, \ and how slowly for incomes",
            r"the delta method; \ Slutsky's theorem; \ when averages fail (Cauchy)",
            r"concentration (Hoeffding); \ the law of maxima; \ floods and return levels",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 2, 3 and 5").to_corner(DL, buff=0.3)
        built = label(r"Built in this part: \ a Galton board", font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> Part six: the laws of averages. <bookmark mark='b'/> We'll prove the inequalities "
            "that make averaging work, and the weak law of large numbers; meet the kinds of convergence; see the "
            "central limit theorem and prove it; measure how fast it arrives, which for the World's incomes is "
            "alarmingly slowly; learn the delta method and Slutsky's theorem, the tools that let every later part "
            "use the normal approximation; watch averages fail; bound them with Hoeffding's inequality; and turn "
            "from averages to maxima, and to the floods they predict. <bookmark mark='c'/> And we'll build a Galton "
            "board."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq))
            vo.wait_until("c")
            self.play(obj.animate.shift(UP * 0.4), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
