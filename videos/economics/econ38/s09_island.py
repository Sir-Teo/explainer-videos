from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class IslandBorder(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The same design on the Island", r"Can the design tell competition from monopsony?",
             "Chapter eight. The same design on the Island.", lit={1994: r"Card and Krueger"},
             scale=("firm", "market"), horizon=("a year",))
        self.runs()
        self.power()

    def runs(self):
        B = load("border")
        edges = np.arange(-0.25, 0.46, 0.025)
        ax = plane([-0.25, 0.45], [0, 60], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.6,
                   xticks=[-0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 20, 40, 60],
                   xlabel=r"estimated effect on employment \ (log points, \ treated minus control)",
                   ylabel=r"runs of the experiment", xfmt=lambda v: f"{v:+.1f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)

        def hist(vals, col):
            h, _ = np.histogram(vals, bins=edges)
            g = VGroup()
            for x0, x1, v in zip(edges[:-1], edges[1:], h):
                p0, p1 = ax.ax.c2p(x0 + 0.002, 0), ax.ax.c2p(x1 - 0.002, v)
                g.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0,
                                fill_color=col, fill_opacity=0.75 if v else 0).move_to((p0 + p1) / 2))
            return g
        hc = hist(B["competitive"]["did"], DEMAND)
        hm = hist(B["monopsony"]["did"], SUPPLY)
        zero = vline(ax, 0, 0, 60, GREY_B)
        ck = vline(ax, B["ck_emp"], 0, 60, NJ)
        ckl = label(r"New Jersey, \ 1992", font_size=16, color=NJ).next_to(ax.ax.c2p(B["ck_emp"], 60), UP, buff=0.05)
        side = VGroup(
            label(rf"competitive stores: \\ average {B['competitive']['mean_did']:+.3f}; \\ "
                  rf"{100 * B['competitive']['share_negative']:.0f}\% of runs negative", font_size=17, color=DEMAND),
            label(rf"stores that set wages: \\ average {B['monopsony']['mean_did']:+.3f}; \\ "
                  rf"{100 * B['monopsony']['share_negative']:.0f}\% negative", font_size=17, color=SUPPLY),
            label(rf"Card and Krueger: \ {B['ck_emp']:+.3f}", font_size=17, color=NJ),
            label(r"one run's standard error \\ is about 0.045: \\ a single study \\ can mislead", font_size=16,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        head = label(rf"{B['n_treat']} and {B['n_ctrl']} restaurants, \ the same rise, \ 200 runs in each world",
                     font_size=22, color=E.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Which world was New Jersey in? On the Island the truth is known, so run the same design there, "
            f"with {B['n_treat']} and {B['n_ctrl']} restaurants and the same rise, two hundred times in each "
            "world. <bookmark mark='a'/> When restaurants hire on competitive demand curves, the design finds job "
            f"losses: {B['competitive']['mean_did']:+.3f} on average, negative in "
            f"{100 * B['competitive']['share_negative']:.0f} percent of runs. <bookmark mark='b'/> When restaurants "
            "set "
            f"their own wages, the same design finds gains, {B['monopsony']['mean_did']:+.3f} on average, and never a "
            "loss. The method can tell the worlds apart. <bookmark mark='c'/> New Jersey's "
            f"{B['ck_emp']:+.3f} sits with the monopsony runs. <bookmark mark='d'/> But one run's standard error is "
            "about four and a half points, so a single study can land in the wrong place: the reason one border "
            "study, however careful, did not settle the question, and why the evidence had to accumulate."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(hc, lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(hc, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(hm, lag_ratio=0.03), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ck), FadeIn(ckl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def power(self):
        P = load("power")
        rows = P["rows"]
        ax = plane([np.log10(150), np.log10(9000)], [0, 0.07], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2,
                   y_length=4.6, xticks=[np.log10(v) for v in (200, 500, 1000, 2000, 5000)],
                   yticks=[0, 0.02, 0.04, 0.06], xlabel=r"restaurants in the study \ (log scale)",
                   ylabel=r"standard error of the estimate", xfmt=lambda v: f"{10 ** v:,.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        pts = VGroup(*[dot(ax, np.log10(r["n"]), r["sd"], NJ, 0.08) for r in rows])
        xs = np.linspace(np.log10(150), np.log10(9000), 60)
        sd1 = rows[1]["sd"]
        th = path(ax, xs, sd1 * np.sqrt(P["n"] / 10 ** xs), GREY_B, 2.4)
        mde = abs(P["effect"]) / 2.8
        need = seg(ax, np.log10(150), mde, np.log10(9000), mde, LOSS, 2.0, dashed=True)
        here = dot(ax, np.log10(P["n"]), sd1, WHITE, 0.1)
        even = dot(ax, np.log10(P["n"]), P["even_sd"], GAIN, 0.1)
        side = VGroup(
            label(rf"{P['n']} stores: \ {sd1:.3f}", font_size=18, color=WHITE),
            label(rf"the competitive effect: \ {P['effect']:+.3f}; \\ to find it 4 times in 5 \\ needs a "
                  rf"standard error \\ of {mde:.3f} (red)", font_size=17, color=LOSS),
            label(rf"about {round(P['need'], -2):,.0f} stores", font_size=19, color=LOSS),
            label(rf"the same {P['n']}, \ split evenly: \\ {P['even_sd']:.3f}", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How large would a border study need to be? Rerun the competitive world with more and fewer "
            "restaurants. <bookmark mark='a'/> With Card and Krueger's "
            f"{P['n']}, the estimate's standard error is about {sd1:.3f}. <bookmark mark='b'/> It shrinks with the "
            "square root of the number of stores: four times the stores, half the error. <bookmark mark='c'/> The "
            f"competitive prediction here is a fall of about {abs(100 * P['effect']):.1f} percent. To detect it four "
            f"times in five, the standard error must be below {mde:.3f}, <bookmark mark='d'/> which takes about "
            f"{round(P['need'], -2):,.0f} restaurants, seven times as many. <bookmark mark='e'/> And the design can be "
            f"cheaper: with {P['n_treat']} stores in one state and only {P['n_ctrl']} in the other, the small group "
            "limits precision; the same number split evenly gives a standard error of "
            f"{P['even_sd']:.3f}. Planning the size of a study before running it, its power, is part of the design."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts[1]), FadeIn(here), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.3) for p_ in pts], lag_ratio=0.2), Create(th), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(need), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(even, scale=1.5), FadeIn(side[3]))
        self.clear_scene()
