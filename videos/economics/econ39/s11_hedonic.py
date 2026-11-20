from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Hedonic(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Compensating differentials", r"What is the price of a job's risks, \ or its hours?",
             "Chapter nine. Compensating differentials.",
             lit={1776: r"Smith", 1974: r"Rosen", 2017: r"Mas and Pallais"}, scale=("person", "firm"),
             horizon=("a year",))
        self.smith()
        self.locus()
        self.flexibility()

    def smith(self):
        qc = quote_card(r"The wages of labour vary with the ease or hardship, \ the cleanliness or dirtiness, \ the "
                        r"honourableness or dishonourableness of the employment.",
                        r"Adam Smith, \ \emph{The Wealth of Nations}, \ Book I, \ chapter 10 (1776)", width=11.0)
        qc.move_to(UP * 0.8)
        pts = VGroup(
            label(r"a dangerous or unpleasant job must pay more \ to attract the same worker", font_size=22,
                  color=WHITE),
            label(r"so some pay gaps are not unfair: \ they are the price of a job's drawbacks", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(qc, DOWN, buff=0.6)
        with self.voiceover(
            "Not every pay gap is a puzzle. Adam Smith noticed in 1776 that wages vary with the ease or hardship, "
            "the cleanliness or dirtiness, the honour or dishonour of the work. <bookmark mark='a'/> If a job is "
            "dangerous or unpleasant, an employer must pay more to fill it with the same kind of worker. "
            "<bookmark mark='b'/> Such a gap is not unfair; it is a price, the compensating differential for the "
            "job's drawbacks."
        ) as vo:
            self.play(FadeIn(qc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
        self.clear_scene()

    def locus(self):
        H = load("hedonic")
        r, w, d = np.array(H["r"]), np.array(H["w"]), np.array(H["d"])
        ax = plane([0, 1.0], [0, 1.0], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"the job's risk", ylabel=r"wage, \ above the safest job", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        jobs = VGroup(*[dot(ax, x, y, FIRM, 0.05) for x, y in zip(r, w) if y <= 1.0])
        loc = path(ax, r, w, FIRM, 3.4, yr=(0, 1.0))
        tang = VGroup()
        for k in (6, len(r) // 2, len(r) - 8):
            x0, y0, s = r[k], w[k], d[k]
            xs = np.array([max(x0 - 0.22, 0), min(x0 + 0.22, 1)])
            tang.add(path(ax, xs, y0 + s * (xs - x0) + 0.0, WORKER, 3.4, smooth=False))
            tang.add(dot(ax, x0, y0, WORKER, 0.08))
        side = VGroup(
            label(r"gold: \ the jobs; \\ each pairs a worker \\ with a firm", font_size=17, color=FIRM),
            label(r"blue: \ a worker's \\ indifference line: \\ its slope is how much \\ that worker minds risk",
                  font_size=17, color=WORKER),
            label(rf"slope of the wage \\ on risk: \ {H['slope_ols']:.2f}; \\ average distaste: \ {H['mean_d']:.2f}",
                  font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1974 Sherwin Rosen showed what such a price means in a market. On the Island, workers differ in how "
            "much they mind risk, and firms differ in how costly it is to make their work safe. "
            "<bookmark mark='a'/> Workers who mind risk least end up in the firms where safety is dearest, and take "
            "the riskiest jobs, at higher pay. <bookmark mark='b'/> The jobs trace out a wage locus. "
            "<bookmark mark='c'/> At each job, the locus is tangent to the indifference line of the worker who holds "
            "it: its slope is exactly what that worker needs to accept a little more risk. <bookmark mark='d'/> So "
            "a regression of wages on risk measures a price, about "
            f"{H['slope_ols']:.2f} here, close to the islanders' average distaste of {H['mean_d']:.2f}. The same "
            "logic, applied to the risk of death at work, gives the value of a statistical life that governments "
            "use to weigh safety rules. But it reads the preferences of those who sorted into risky jobs, who mind "
            "risk least."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(jobs, lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(jobs[-12:], color=WHITE))
            vo.wait_until("b")
            self.play(Create(loc), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(t_) for t_ in tang], lag_ratio=0.4), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def flexibility(self):
        M = load("hedonic")["mp"]
        rows = [(r"to avoid a schedule set by the employer \\ at short notice", M["avoid_short_notice"], LOSS),
                (r"for the option \\ to work from home", M["wfh"], GAIN)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 0.8 - 1.5 * k
            r = Rectangle(width=v * 0.2, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([0.0 + v * 0.1, y, 0]))
            bars.add(VGroup(label(nm, font_size=20, color=WHITE).next_to(np.array([-0.1, y, 0]), LEFT, buff=0.15),
                            r, label(f"{v}\\% of wages", font_size=20, color=col).next_to(r, RIGHT, buff=0.15)))
        head = label(r"what the average job-seeker would give up", font_size=26, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        design = label(r"applicants to a national call centre, \ offered schedules at different wages, \ chose "
                       r"between them", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.3)
        foot = label(r"most would pay nothing for flexibility; \ a minority would pay a lot", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.MAS_PALLAIS_2017.tag, corner=DR, font_size=12)
        with self.voiceover(
            "Hours are a job characteristic too. In 2017 Alexandre Mas and Amanda Pallais ran an experiment inside a "
            "real hiring process: applicants to a national call centre were offered jobs with different schedules "
            "at different wages. <bookmark mark='a'/> The average applicant would give up "
            f"{M['avoid_short_notice']} percent of wages to avoid a schedule an employer sets at short notice, "
            f"<bookmark mark='b'/> and {M['wfh']} percent for the option of working from home. "
            "<bookmark mark='c'/> Most would pay nothing for flexibility; a minority, with high valuations, would pay "
            "a great deal. Chapter twelve returns to hours, which turn out to be at the heart of the gender gap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(design))
            for mk, b_ in zip("ab", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
