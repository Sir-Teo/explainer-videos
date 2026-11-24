from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

WACC = 0.07   # illustrative: what the capital could earn elsewhere
START = 0.30  # an industry that starts out earning 30%


def ret(n: float, moat: float) -> float:
    """Return on capital after n entrants (illustrative): each newcomer takes a share of the excess, unless a moat
    keeps a fraction ``moat`` of it out of reach."""
    return WACC + (START - WACC) * (moat + (1 - moat) / (1 + 0.55 * n))


class Fade(VoiceoverScene):
    def construct(self):
        card(self, 3, "Why high returns fade", "What happens when money can flow in freely?",
             "Chapter three. Why high returns fade.", lit=("moat",))
        n = ValueTracker(0)
        ax = CornerAxes(x_range=[0, 12, 2], y_range=[0, 0.32, 0.05], x_length=6.4, y_length=4.2,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([2.6, -0.3, 0])
        xt = VGroup(*[tx(f"{v}", 15, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0, 4, 8, 12)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0.1, 0.2, 0.3)])
        xl = tx("newcomers who have come in", 17, GREY_B).next_to(ax, DOWN, buff=0.35)
        yl = tx("return on capital", 17, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cost = DashedLine(ax.c2p(0, WACC), ax.c2p(12, WACC), stroke_color=WHITE, stroke_width=2)
        cost_t = tx("what the capital could earn elsewhere", 15, WHITE).next_to(ax.c2p(12, WACC), DOWN, buff=0.08).align_to(
            ax.c2p(12, 0), RIGHT)
        open_ = ax.plot(lambda x: ret(x, 0.0), x_range=[0, 12, 0.05], color=COST_, stroke_width=4)
        moat_ = ax.plot(lambda x: ret(x, 0.6), x_range=[0, 12, 0.05], color=RET, stroke_width=4)
        open_t = tx("no moat", 17, COST_, bold=True).next_to(ax.c2p(12, ret(12, 0)), UP, buff=0.1).shift(LEFT * 0.4)
        moat_t = tx("a moat", 17, RET, bold=True).next_to(ax.c2p(12, ret(12, 0.6)), UP, buff=0.1).shift(LEFT * 0.3)
        dot = always_redraw(lambda: glow_dot(ax.c2p(n.get_value(), ret(n.get_value(), 0.0)), color=COST_, radius=0.09))
        keep = draw.castle(1.6).move_to([-4.4, 0.6, 0])
        camp = VGroup(*[draw.castle(0.55, color=ENTRANT) for _ in range(12)]).arrange_in_grid(rows=3, cols=4,
                                                                                         buff=(0.12, 0.12))
        camp.move_to([-4.4, -1.9, 0])

        def show(m):
            k = int(n.get_value())
            for i, c in enumerate(m):
                c.set_opacity(1 if i < k else 0.08)
        camp.add_updater(show)
        num = draw.number(lambda: 100 * ret(n.get_value(), 0.0), 0, suffix="%", size=40, color=COST_)
        num.add_updater(lambda m: m.next_to(keep, UP, buff=0.25), call_updater=True)
        tag = estimate_tag("illustrative: an industry that starts at 30%", corner=DR)
        with self.voiceover(
            "Why should high returns fade at all? <bookmark mark='a'/> Picture an industry earning thirty percent "
            "on its capital, when the same money could earn seven percent elsewhere. Every investor who notices "
            "wants in. <bookmark mark='b'/> The first newcomer builds a plant and takes some of the customers. "
            "The second does the same. Prices fall, and with them the return. <bookmark mark='c'/> If nothing stops "
            "them, newcomers keep arriving until the return is no better than the capital could earn anywhere "
            "else. That is what economists mean by competition, and it is why, in most industries, high returns "
            "do not last. <bookmark mark='d'/> A moat bends the curve. Newcomers can still come, but they cannot "
            "reach part of what the incumbents earn, and the return settles well above the cost of capital. "
            "The facts in the last chapter look like a world with some of each: most returns drift towards the "
            "middle, slowly, and a few hardly move."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(keep, shift=UP * 0.2), FadeIn(num))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(cost), FadeIn(cost_t))
            self.add(camp, dot)
            vo.wait_until("b")
            self.play(n.animate.set_value(2), run_time=2.0, rate_func=linear)
            vo.wait_until("c")
            self.play(n.animate.set_value(12), Create(open_), run_time=5.0, rate_func=linear)
            self.play(FadeIn(open_t))
            vo.wait_until("d")
            self.play(Create(moat_), FadeIn(moat_t), keep.animate.scale(1.0), run_time=2.0)
            self.play(Indicate(moat_t, color=RET))
        camp.clear_updaters()
        num.clear_updaters()
        self.clear_scene()
        self.measured()

    def measured(self):
        F = R["fade"]
        yrs = F["years"]
        pa = viz.plot_axes([2014.6, 2025.4], [0, 0.38], x_length=8.6, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[0.1, 0.2, 0.3], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%", size=15)
        pa.move_to([-0.6, -0.4, 0])
        cols = [RET, "#4FC3A1", GREY_B, "#F2A65A", COST_]
        names = ["top fifth in 2015", "second", "middle", "fourth", "bottom fifth in 2015"]
        lines = VGroup(*[VMobject(stroke_color=c, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(y, v) for y, v in zip(yrs, path)]) for c, path in zip(cols, F["paths"])])
        labs = VGroup(*[tx(f"{nm}: {100 * path[0]:.0f}% → {100 * path[-1]:.0f}%", 16, c).next_to(
            pa.ax.c2p(2025, path[-1]), RIGHT, buff=0.15) for nm, c, path in zip(names, cols, F["paths"])])
        # spread the labels so they do not overlap
        for k in range(1, 5):
            if labs[k].get_top()[1] > labs[k - 1].get_bottom()[1] - 0.05:
                labs[k].next_to(labs[k - 1], DOWN, buff=0.08).align_to(labs[k - 1], LEFT)
        head = tx(f"{F['n']} industries, sorted by their return in 2015 into fifths: each fifth's average since", 18,
                  GREY_A).next_to(pa, UP, buff=0.2)
        src = source("Damodaran, Excess Returns by industry, 2015-2025; this film's groups", size=13)
        top, bot = F["paths"][0], F["paths"][4]
        with self.voiceover(
            "Does it happen in real industries? <bookmark mark='a'/> Take the eighty-eight industries in "
            "Damodaran's tables every year from 2015 to 2025, sort them by their return in 2015 into five groups, "
            "and follow each group's average. <bookmark mark='b'/> The top fifth started at "
            f"{100 * top[0]:.0f} percent and ten years later earned {100 * top[-1]:.0f}. <bookmark mark='c'/> The "
            f"bottom fifth started at {100 * bot[0]:.0f} percent and climbed to {100 * bot[-1]:.0f}. "
            "<bookmark mark='d'/> The groups in between drifted toward the middle. That is the pull of competition, "
            "measured: money flows toward high returns and away from low ones. <bookmark mark='e'/> But look at the "
            "top line. After ten years the best industries of 2015 still earned nearly twice what the middle did. "
            "The pull is real, and it is slow. Something is holding it back."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(Dot(pa.ax.c2p(2015, path[0]), radius=0.07, color=c), scale=2)
                                    for c, path in zip(cols, F["paths"])], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(lines[0]), run_time=2.0)
            self.play(FadeIn(labs[0]))
            vo.wait_until("c")
            self.play(Create(lines[4]), run_time=2.0)
            self.play(FadeIn(labs[4]))
            vo.wait_until("d")
            self.play(*[Create(lines[k]) for k in (1, 2, 3)], run_time=2.0)
            self.play(*[FadeIn(labs[k]) for k in (1, 2, 3)])
            vo.wait_until("e")
            self.play(Indicate(lines[0], color=WHITE), Indicate(labs[0], color=WHITE))
        self.clear_scene()
