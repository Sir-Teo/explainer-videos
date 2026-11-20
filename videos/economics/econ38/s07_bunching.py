from __future__ import annotations

from scipy.stats import lognorm

from videos.economics.econ38.common import *  # noqa: F403


class Bunching(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Missing jobs, \ excess jobs", r"How can we count the jobs a minimum wage destroys?",
             "Chapter six. Missing jobs, excess jobs.",
             lit={2019: r"Cengiz, \ Dube, \ Lindner and Zipperer", 2022: r"Jardim et al."}, scale=("market", "nation"),
             horizon=("a year", "a decade"))
        self.bunching()
        self.results()

    def bunching(self):
        edges = np.arange(7.0, 20.01, 0.5)
        mids = (edges[:-1] + edges[1:]) / 2
        dist = lognorm(s=0.35, scale=12.0)
        base = 1000 * (dist.cdf(edges[1:]) - dist.cdf(edges[:-1]))
        m = 10.0
        missing = np.where(edges[1:] <= m, base, 0.0)
        excess = np.zeros_like(base)
        spread = (mids >= m) & (mids < m + 2.0)
        excess[spread] = missing.sum() * 0.97 * np.array([0.5, 0.25, 0.15, 0.10])[: spread.sum()]
        ax = plane([7, 20], [0, 160], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                   xticks=[8, 10, 12, 14, 16, 18, 20], yticks=[0, 40, 80, 120, 160], xlabel=r"hourly wage, \ \$",
                   ylabel=r"jobs", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)

        def bars(vals, col, op):
            g = VGroup()
            for x0, x1, v in zip(edges[:-1], edges[1:], vals):
                p0, p1 = ax.ax.c2p(x0 + 0.03, 0), ax.ax.c2p(x1 - 0.03, max(v, 0.0))
                g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0, fill_color=col,
                                fill_opacity=op if v > 0.01 else 0.0).move_to((p0 + p1) / 2))
            return g
        b0 = bars(base, GREY_B, 0.6)
        miss = bars(missing, LOSS, 0.85)
        exc = VGroup()
        for x0, x1, b, e in zip(edges[:-1], edges[1:], base, excess):
            if e > 0:
                p0, p1 = ax.ax.c2p(x0 + 0.03, b), ax.ax.c2p(x1 - 0.03, b + e)
                exc.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=WAGE,
                                  fill_opacity=0.9).move_to((p0 + p1) / 2))
        line = vline(ax, m, 0, 160, NJ)
        side = VGroup(
            label(r"red: \ jobs that vanish \\ below the new minimum", font_size=18, color=LOSS),
            label(r"green: \ jobs that appear \\ at and just above it", font_size=18, color=WAGE),
            label(r"the employment effect \\ = green $-$ red", font_size=20, color=E.ACCENT),
            label(r"jobs far above \\ are the control", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = label(r"an illustration", font_size=14, color=GREY_B).to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 2019 Doruk Cengiz, Arindrajit Dube, Attila Lindner and Ben Zipperer counted jobs differently. Here is "
            "an illustrative distribution of jobs by their hourly wage. <bookmark mark='a'/> Raise the minimum to ten "
            "dollars. Jobs that paid less must either disappear or be paid more. <bookmark mark='b'/> So count the "
            "jobs that vanish below the new minimum, <bookmark mark='c'/> and the jobs that appear at and just above "
            "it. <bookmark mark='d'/> The employment effect is the difference. Jobs that paid well above the minimum "
            "should not move, so they check the comparison."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(b0, lag_ratio=0.02), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(line))
            vo.wait_until("b")
            self.play(FadeIn(miss), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(exc), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def results(self):
        D = tables.CDLZ_2019.data
        J = tables.JARDIM_2022.data
        cards = point_cards([
            (rf"{D['events']} state increases", rf"{D['first']}--{D['last']}: \\ low-wage jobs \\ essentially "
                                                 r"unchanged \\ over five years", WAGE),
            (r"the elasticity", rf"of employment to \\ low-wage pay: \\ {D['owe']:.2f} \ (s.e.\ {D['owe_se']:.2f})",
             E.ACCENT),
            (r"Seattle, \ 2015--16", rf"to \${J['m2015']}, \ then \${J['m2016']}: \\ hours at low wages \\ fell, "
                                     r"\ most for \\ the inexperienced", LOSS),
            (r"Seattle's elasticities", rf"{J['lo']:.1f} to {J['hi']:.1f}, \\ mostly in hours, \\ not jobs", LOSS),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what the counts found", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"moderate minimums: \ little job loss; \ high ones relative to local pay: \ hours can fall",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.CDLZ_2019.tag + r"; \ " + tables.JARDIM_2022.tag, corner=DR, font_size=11)
        with self.voiceover(
            f"Across {D['events']} state increases from {D['first']} to {D['last']}, <bookmark mark='a'/> the jobs "
            "missing below each new minimum were matched by jobs appearing just above it: the number of low-wage "
            "jobs was essentially unchanged five years later. <bookmark mark='b'/> Their elasticity of employment "
            f"with respect to low-wage pay is {D['owe']:.2f}, with a standard error of {D['owe_se']:.2f}: zero cannot "
            "be ruled out, but large losses can. <bookmark mark='c'/> Seattle is the warning. When it raised its "
            f"minimum to {J['m2015']} dollars and then {J['m2016']}, high relative to local pay, a team at the "
            "University of Washington found hours at low wages falling, mostly for the least experienced, "
            f"<bookmark mark='d'/> with elasticities between {J['lo']:.1f} and {J['hi']:.1f}, mostly in hours rather "
            "than jobs. <bookmark mark='e'/> The evidence fits a pattern: moderate minimums cost few jobs; high ones, "
            "relative to local wages, can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
