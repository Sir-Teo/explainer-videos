from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class IslandBorder(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The same design on the Island", r"Can the design tell competition from monopsony?",
             "Chapter eight. The same design on the Island.", lit={1994: r"Card and Krueger"},
             scale=("firm", "market"), horizon=("a year",))
        self.runs()

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
            self.play(FadeIn(head, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(hc, lag_ratio=0.03), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(hm, lag_ratio=0.03), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ck), FadeIn(ckl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
