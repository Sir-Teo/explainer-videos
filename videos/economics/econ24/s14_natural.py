from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Natural(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The natural rate, \ duration and scarring", r"How low can unemployment go, \ and what does "
             r"a long spell do to a person?", "Chapter twelve. The natural rate, duration and scarring.",
             lit={1968: r"Friedman", 2011: r"Davis and von Wachter", 2013: r"Kroft, Lange, Notowidigdo"},
             scale=("person", "nation"), horizon=("years", "decades"))
        self.natural()
        self.duration()
        self.callbacks()
        self.scars()

    def natural(self):
        n = load("natural")
        ax = plane([1949, 2027], [0, 15], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 3, 6, 9, 12, 15], ylabel=r"\% of the labour force",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        u = path(ax, n["t"], n["u"], color=WORKER, width=2, smooth=False)
        nr = path(ax, n["t"], n["nrou"], color=E.ACCENT, width=4, smooth=False)
        side = VGroup(
            label(r"unemployment rate", font_size=20, color=WORKER),
            label(r"CBO's estimate of the \\ natural rate", font_size=20, color=E.ACCENT),
            label(rf"1979: \ {n['nrou_1979']:.1f}\%; \ 2025: \ {n['nrou_2025']:.1f}\%", font_size=21,
                  color=E.ACCENT),
            label(r"an older, \ more educated workforce; \\ temporary-help agencies; \\ online search \ (Part 28 "
                  r"returns)", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"BLS unemployment rate; \ CBO noncyclical rate of unemployment; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Every model in this part has a steady state: a rate of unemployment that the flows return to when the "
            "shocks die away. Milton Friedman called it the natural rate in 1968. Nothing about it is natural in "
            "the sense of good or fixed: it depends on how fast people separate and find jobs. "
            "<bookmark mark='a'/> Here is American unemployment since 1949. <bookmark mark='b'/> And the "
            "Congressional Budget Office's estimate of the natural rate, which it uses to judge how far the "
            "economy is from capacity. <bookmark mark='c'/> It peaked at about "
            f"{n['nrou_1979']:.1f} percent in the late 1970s and has drifted down to about {n['nrou_2025']:.1f}. "
            "<bookmark mark='d'/> Among the explanations: an older and more educated workforce, which separates "
            "less; temporary-help agencies and better matching; and perhaps online search. Part twenty-eight "
            "returns to the natural rate as a guide for central banks, where estimating it in real time turns out "
            "to be hard."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(u), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(nr), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def duration(self):
        n = load("natural")
        ax = plane([1948, 2027], [0, 50], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 10, 20, 30, 40, 50],
                   ylabel=r"\% of the unemployed looking for 27 weeks or more", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        line_ = path(ax, n["lt_t"], n["lt_share"], color=SEP, width=3, smooth=False)
        k = int(np.argmax(n["lt_share"]))
        peak = dot(ax, n["lt_t"][k], n["lt_share"][k], color=E.ACCENT, r=0.09)
        side = VGroup(
            label(rf"peak: \ {n['lt_peak']:.0f}\% \\ in {int(n['lt_peak_when'])}", font_size=23, color=E.ACCENT),
            label(r"the slow recovery: \\ job finding stayed low \\ for years", font_size=20, color=GREY_A),
            label(r"do long spells cause \\ longer spells?", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"BLS, \ CPS: \ unemployed 27 weeks and over, \ all unemployed; \ via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Averages hide who is unemployed for how long. <bookmark mark='a'/> This is the share of the unemployed "
            "who have been looking for more than six months. Before 2008 it never "
            "passed about a quarter, reached in the slump of the early 1980s. <bookmark mark='b'/> After the 2008 crisis it reached about "
            f"{n['lt_peak']:.0f} percent in {int(n['lt_peak_when'])}: almost half of all unemployed Americans had "
            "been looking for more than half a year, because job finding stayed low for years. "
            "<bookmark mark='c'/> That raises a hard question. Do people who have been unemployed longer find jobs "
            "more slowly because of the spell itself, or because the people who are hardest to employ are the ones "
            "left in the pool?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(line_), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromCenter(peak), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def callbacks(self):
        rows = VGroup(
            label(r"Kroft, \ Lange and Notowidigdo, \ 2013: \ fictitious r\'esum\'es sent to real job postings in "
                  r"100 cities", font_size=22, color=GREY_A),
            label(r"the only difference: \ how long the applicant had been unemployed, \ assigned at random",
                  font_size=23, color=WORKER),
            label(r"callbacks fell from about 7\% \ to about 4\% \ as the spell lengthened, \ mostly within eight "
                  r"months", font_size=24, color=SEP),
            label(r"and fell faster where the labour market was tight: \ there, \ a long spell says more",
                  font_size=22, color=TIGHT),
            label(r"the spell itself is held against people: \ duration dependence is partly real", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Kroft, Lange and Notowidigdo, QJE 128(3) (2013): \ 1123--1167", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Kory Kroft, Fabian Lange and Matthew Notowidigdo answered with an experiment. "
            "<bookmark mark='a'/> They sent fictitious résumés to real job postings in a hundred American cities. "
            "<bookmark mark='b'/> The résumés were alike except for one thing, assigned at random: how long the "
            "applicant had been out of work. <bookmark mark='c'/> The chance of being called back for an interview "
            "fell from about seven percent to about four as the spell lengthened, with most of the fall within the "
            "first eight months. <bookmark mark='d'/> And it fell faster where the labour market was tight, where a "
            "long spell is more of a warning sign, since jobs are easy to find. "
            "<bookmark mark='e'/> So employers do hold the spell itself against people. The pool is not just sorted; "
            "it is shaped by how long people have been in it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def scars(self):
        ax = plane([-0.6, 1.6], [0, 3.2], center=LEFT * 2.2 + DOWN * 0.3, x_length=6.2, y_length=4.8, xticks=[],
                   yticks=[0, 1, 2, 3], ylabel=r"years of earlier earnings lost \ (over 20 years, \ discounted)",
                   yfmt=lambda v: f"{v:.0f}", font_size=16)
        vals = ((1.4, r"displaced when \\ unemployment $< 6\%$", JOB), (2.8, r"displaced when \\ unemployment "
                                                                         r"$> 8\%$", SEP))
        bars, tops, names = VGroup(), VGroup(), VGroup()
        for k, (val, name, c) in enumerate(vals):
            lo, hi = ax.ax.c2p(k, 0), ax.ax.c2p(k, val)
            bars.add(Rectangle(width=0.9, height=hi[1] - lo[1], fill_color=c, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
            tops.add(label(f"{val:.1f}", font_size=24, color=c).next_to(bars[-1], UP, buff=0.08))
            names.add(label(name, font_size=17, color=c).next_to(lo, DOWN, buff=0.15))
        side = VGroup(
            label(r"Davis and von Wachter, \ 2011: \\ men with three or more years \\ in their job, \ in mass "
                  r"layoffs, \\ Social Security records \\ from 1974", font_size=19, color=GREY_A),
            label(r"the loss doubles \\ in a recession", font_size=23, color=SEP),
            label(r"the DMP model with search \\ on the job: \ about a quarter \\ of the loss", font_size=19,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Davis and von Wachter, BPEA (Fall 2011)", corner=DR, font_size=12)
        with self.voiceover(
            "Losing a job leaves a scar. <bookmark mark='a'/> Steven Davis and Till von Wachter used Social "
            "Security earnings records from 1974 on, for men who had held their jobs for at least three years and "
            "lost them in mass layoffs, which are less likely to reflect the worker's own performance. "
            "<bookmark mark='b'/> Displaced when unemployment was below six percent, a man lost, over the next "
            "twenty years and discounted, about 1.4 years of his earlier earnings. <bookmark mark='c'/> Displaced "
            "when unemployment was above eight percent, about 2.8 years: twice as much. Recessions do not just "
            "delay careers; they knock people down the ladder. <bookmark mark='d'/> And when Davis and von "
            "Wachter put the same question to the Mortensen-Pissarides model, extended to allow search on the job, "
            "it produced losses only about a quarter as large. Another gap between the model and the data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=0.8)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(tops[0]), FadeIn(names[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(tops[1]), FadeIn(names[1]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()
