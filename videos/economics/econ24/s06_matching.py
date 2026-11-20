from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

URN_SEED = 2   # 8 of 12 openings filled: close to the expected 7.8


class Matching(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The matching function", r"How many hires do a million searchers and a million openings "
             r"make?", "Chapter five. The matching function.",
             lit={1977: r"Butters", 1979: r"Hall", 2001: r"Petrongolo and Pissarides"}, scale=("market",),
             horizon=("a month",))
        self.urns()
        self.function()
        self.estimate()

    def urns(self):
        rng = np.random.default_rng(URN_SEED)
        n = 12
        boxes = VGroup(*[Square(0.72, color=JOB, stroke_width=3) for _ in range(n)]).arrange(RIGHT, buff=0.28)
        boxes.move_to(UP * 0.1)
        blabel = label(r"12 job openings", font_size=22, color=JOB).next_to(boxes, UP, buff=0.3)
        seekers = VGroup(*[Dot(radius=0.13, color=WORKER) for _ in range(n)]).arrange(RIGHT, buff=0.6)
        seekers.move_to(DOWN * 2.2)
        slabel = label(r"12 job seekers, \ each applying to one opening at random", font_size=22,
                       color=WORKER).next_to(seekers, DOWN, buff=0.3)
        picks = rng.integers(0, n, size=n)
        count = np.zeros(n, int)
        moves = []
        for k, j in enumerate(picks):
            target = boxes[j].get_center() + UP * (0.18 - 0.22 * count[j]) + RIGHT * (0.18 * (count[j] % 2) - 0.09)
            count[j] += 1
            moves.append(seekers[k].animate.move_to(target))
        filled = int((count > 0).sum())
        empty = VGroup(*[boxes[j] for j in range(n) if count[j] == 0])
        crowded = VGroup(*[boxes[j] for j in range(n) if count[j] > 1])
        expect = n * (1 - (1 - 1 / n) ** n)
        res = VGroup(
            label(rf"hires: \ {filled}, \ not 12", font_size=28, color=MATCH),
            label(rf"{len(empty)} openings got nobody; \ {len(crowded)} got more than one", font_size=22, color=SEP),
            MathTex(r"\text{expected hires} \;=\; V\big(1 - (1 - \tfrac1V)^U\big) \;\approx\; V\,(1 - e^{-U/V})"
                    rf"\;\approx\; {expect:.1f}", font_size=34, color=WHITE),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why don't searchers and openings simply pair off? Here is the simplest answer, from Gerard Butters and "
            "Robert Hall in the 1970s. <bookmark mark='a'/> Twelve openings, and twelve people looking for work. "
            "Each applies to one opening, chosen at random, because nobody knows where the others are applying. "
            f"<bookmark mark='b'/> Watch. <bookmark mark='c'/> Only {filled} openings are filled. "
            f"<bookmark mark='d'/> {len(empty)} received no applicant at all, while {len(crowded)} received more "
            "than one and could hire only one. Nobody was lazy or choosy; they just failed to coordinate. "
            "<bookmark mark='e'/> On average, with U searchers and V openings, the number of hires is V times one "
            f"minus e to the minus U over V: here about {expect:.1f} out of twelve. A missing price is not the "
            "problem. Missing information is."
        ) as vo:
            self.play(FadeIn(boxes), FadeIn(blabel), FadeIn(seekers), FadeIn(slabel))
            vo.wait_until("b")
            self.play(LaggedStart(*moves, lag_ratio=0.25), run_time=5)
            vo.wait_until("c")
            self.play(FadeOut(blabel), FadeOut(slabel), FadeIn(res[0]))
            vo.wait_until("d")
            self.play(FadeIn(res[1]), *[b.animate.set_stroke(SEP, 5) for b in empty],
                      *[b.animate.set_fill(JOB, 0.25) for b in crowded])
            vo.wait_until("e")
            self.play(Write(res[2]))
        self.clear_scene()

    def function(self):
        rows = VGroup(
            MathTex(r"M \;=\; A\, U^{\eta}\, V^{1-\eta}", font_size=52, color=MATCH),
            label(r"hires each month, \ from searchers $U$ and openings $V$: \ constant returns", font_size=22,
                  color=GREY_A),
            MathTex(r"\theta \;=\; \frac{V}{U} \quad \text{(tightness)}", font_size=40, color=TIGHT),
            MathTex(r"f(\theta) = \frac{M}{U} = A\,\theta^{1-\eta} \qquad q(\theta) = \frac{M}{V} = A\,\theta^{-\eta}",
                    font_size=40, color=WHITE),
            label(r"a tighter market: \ easier for workers to find jobs, \ harder for firms to fill them", font_size=23,
                  color=E.ACCENT),
            label(r"a congestion externality, \ in both directions: \ each searcher makes the others' search harder",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        with self.voiceover(
            "Economists summarize all this with a matching function. <bookmark mark='a'/> The number of hires each "
            "month depends on the number of searchers and the number of openings. Usually it is written as a "
            "Cobb-Douglas with constant returns: double both, and hires double. <bookmark mark='b'/> Then everything "
            "depends on one ratio, openings per searcher, called the market's tightness, theta. "
            "<bookmark mark='c'/> A searcher finds a job at rate f, which rises with tightness; a vacancy is filled "
            "at rate q, which falls with it. <bookmark mark='d'/> In a tight market, workers find jobs easily and "
            "firms struggle to fill them; in a slack market, the reverse. <bookmark mark='e'/> And every new "
            "searcher makes it slightly harder for the others, every new vacancy slightly harder for other firms: "
            "an externality that chapter eight returns to."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def estimate(self):
        m = load("matching")
        ax = plane([-2.0, 0.4], [-1.6, -0.3], center=LEFT * 2.3 + DOWN * 0.3, x_length=7.0, y_length=5.0,
                   xticks=[-2.0, -1.5, -1.0, -0.5, 0.0], yticks=[-1.5, -1.0, -0.5],
                   xlabel=r"$\ln(V/U)$: \ openings per unemployed worker", ylabel=r"$\ln f$: \ the unemployed's "
                   r"job-finding rate", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)
        pts = VGroup(*[dot(ax, x, y, color=WORKER, r=0.045) for x, y in zip(m["f_x"], m["f_y"])])
        xs = np.linspace(-1.95, 0.3, 20)
        fit = path(ax, xs, m["f_intercept"] + m["f_slope"] * xs, color=MATCH, width=4)
        side = VGroup(
            label(rf"{m['f_n']} quarters, \ 2001--2019", font_size=20, color=WORKER),
            label(rf"slope $1 - \eta = {m['f_slope']:.2f}$, \\ so $\eta \approx {m['f_eta']:.2f}$", font_size=23,
                  color=MATCH),
            label(rf"JOLTS hires against openings \\ give a slope of {m['slope']:.2f}, \ but those \\ hires include "
                  r"people \\ who already had jobs", font_size=19, color=GREY_A),
            label(r"Petrongolo and Pissarides's \\ survey: \ constant returns, \\ $\eta$ between 0.5 and 0.7",
                  font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"job finding from the CPS by duration \ (chapter 10); \ JOLTS openings; \ via FRED",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Can the matching function be seen in data? Take logs: the log of the job-finding rate is a constant "
            "plus one minus eta times the log of tightness. <bookmark mark='a'/> Here are the American quarters "
            "from 2001 to 2019: the share of the unemployed who found work, which chapter ten measures, against "
            "openings per unemployed worker. <bookmark mark='b'/> The slope is "
            f"{m['f_slope']:.2f}, so the elasticity of hires with respect to unemployment, eta, is about "
            f"{m['f_eta']:.2f}. <bookmark mark='c'/> Using JOLTS's count of all hires instead gives a slope of "
            f"{m['slope']:.2f}, but those hires include people moving from one job to another, who are not in the "
            "unemployment pool. Which measure of searchers to use is a large part of this literature. "
            "<bookmark mark='d'/> Barbara Petrongolo and Christopher Pissarides surveyed dozens of estimates in "
            "2001: constant returns hold up well, and the elasticity on unemployment is usually between a half "
            "and seven-tenths. That number is a dial in chapter thirteen."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.02), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
