from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

SOFT = "#7EC8F5"


def doc(h: float = 0.5, color: str = SOFT) -> VGroup:
    """A document with a folded corner: one copy of a piece of software."""
    w = 0.78 * h
    body = Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - 0.22 * h, 0], [w / 2 - 0.22 * h, h / 2, 0],
                   [-w / 2, h / 2, 0], stroke_width=0, fill_color=color, fill_opacity=0.95)
    fold = Polygon([w / 2 - 0.22 * h, h / 2, 0], [w / 2 - 0.22 * h, h / 2 - 0.22 * h, 0], [w / 2, h / 2 - 0.22 * h, 0],
                   stroke_width=0, fill_color="#0E1117", fill_opacity=0.35)
    lines = VGroup(*[Line([-w / 2 + 0.1 * h, y, 0], [w / 2 - 0.12 * h, y, 0], stroke_color="#0E1117", stroke_width=1.5,
                          stroke_opacity=0.6) for y in np.linspace(0.12 * h, -0.32 * h, 4)])
    return VGroup(body, fold, lines)


class Zero(VoiceoverScene):
    def construct(self):
        card(self, 11, "Zero marginal cost", "What happens when one more costs nothing at all?",
             "Chapter eleven. Zero marginal cost.", lit=("dollar", "who"))
        self.copies()
        self.microsoft()

    def copies(self):
        n = ValueTracker(1)
        grid_pos = [np.array([-6.3 + 0.36 * (i % 16), 2.6 - 0.44 * (i // 16), 0]) for i in range(256)]
        master = doc(0.42).move_to(grid_pos[0])
        made = [master]
        first = VGroup(tx("the first copy", 20, GREY_B), tx("years of engineers' work", 22, SOFT, bold=True)).arrange(
            DOWN, buff=0.06).move_to([-3.6, -3.0, 0])
        ax = CornerAxes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=4.8, y_length=3.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([3.9, 0.7, 0])
        soft = ax.plot(lambda q: min(9.8, 4.0 / q), x_range=[0.41, 10, 0.02], color=SOFT, stroke_width=4)
        hard = ax.plot(lambda q: min(9.8, 2.0 / q + 3.0), x_range=[0.29, 10, 0.02], color=VAR, stroke_width=3)
        soft_t = tx("software: falls towards zero", 17, SOFT).next_to(ax.c2p(10, 0.4), UP, buff=0.08).align_to(
            ax.c2p(10, 0), RIGHT)
        hard_t = tx("a factory: flattens at the cost of one more", 17, VAR).next_to(ax.c2p(10, 3.2), UP, buff=0.08).align_to(
            ax.c2p(10, 0), RIGHT)
        xl = tx("copies sold", 17, GREY_B).next_to(ax, DOWN, buff=0.12)
        yl = tx("average cost per copy", 17, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cnt = draw.number(lambda: n.get_value(), 0, size=40, color=SOFT)
        cnt.add_updater(lambda m: m.move_to([3.9, -2.55, 0]), call_updater=True)
        cnt_t = tx("copies", 18, GREY_B).move_to([3.9, -3.1, 0])
        tag = estimate_tag("illustrative", corner=DR)
        with self.voiceover(
            "Now push the cost curve to its limit. <bookmark mark='a'/> The first copy of a piece of software costs "
            "years of engineers' work. <bookmark mark='b'/> The second copy costs nothing: copy the file. So does the "
            "thousandth, and the millionth. <bookmark mark='c'/> A factory's average cost falls as it fills, then "
            "flattens at the cost of one more unit. Software's never flattens. It just keeps falling, towards zero, "
            "the more copies are sold."
        ) as vo:
            self.play(FadeIn(master, scale=1.5), FadeIn(first), FadeIn(tag), FadeIn(cnt), FadeIn(cnt_t))
            vo.wait_until("a")
            vo.wait_until("b")
            for k in range(8):
                have = len(made)
                new = [made[i].copy() for i in range(have)]
                targets = grid_pos[have:2 * have]
                self.play(*[m.animate.move_to(p) for m, p in zip(new, targets)], n.animate.set_value(2 * have),
                          run_time=0.6 if k < 5 else 0.4)
                made += new
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(hard), FadeIn(hard_t), run_time=1.2)
            self.play(Create(soft), FadeIn(soft_t), run_time=1.2)
        cnt.clear_updaters()
        self.clear_scene()

    def microsoft(self):
        rev, oi = R["software"]["rev"], R["software"]["margin"] * R["software"]["rev"]
        from explainer.industry.register import get
        ic_rev, ic_oi, growth = get("msft.ic_rev"), get("msft.ic_oi"), get("msft.ic_cogs_growth")
        head = tx("Microsoft, fiscal 2026: two businesses", 28, bold=True).to_edge(UP, buff=0.3)
        base = -2.5
        u = 0.026

        def pair(x, r_, o_, col, name, sub):
            b1 = Rectangle(width=1.3, height=r_ * u, stroke_width=0, fill_color=col, fill_opacity=0.4).move_to(
                [x - 0.7, base, 0], aligned_edge=DOWN)
            b2 = Rectangle(width=1.3, height=o_ * u, stroke_width=0, fill_color=col, fill_opacity=0.95).move_to(
                [x + 0.7, base, 0], aligned_edge=DOWN)
            l1 = tx(f"${r_:.0f}bn", 20, GREY_A).next_to(b1, UP, buff=0.08)
            l2 = tx(f"${o_:.0f}bn", 20, WHITE, bold=True).next_to(b2, UP, buff=0.08)
            n1 = tx("sales", 16, GREY_B).next_to(b1, DOWN, buff=0.1)
            n2 = tx("operating profit", 16, GREY_B).next_to(b2, DOWN, buff=0.1)
            ttl = VGroup(tx(name, 24, col, bold=True), tx(sub, 16, GREY_B)).arrange(DOWN, buff=0.06).move_to([x, 2.8, 0])
            m = tx(f"{100 * o_ / r_:.0f}% margin", 28, col, bold=True).move_to([x, 1.95, 0])
            return VGroup(b1, b2, l1, l2, n1, n2, ttl, m)
        office = pair(-3.3, rev, oi, SOFT, "Productivity and Business Processes", "Microsoft 365, LinkedIn, Dynamics")
        cloud = pair(3.3, ic_rev, ic_oi, PRICE, "Intelligent Cloud", "Azure and server software")
        src = source("Microsoft Form 10-K, fiscal year to 30 June 2026: segment results")
        with self.voiceover(
            "Microsoft shows what that does to a business. <bookmark mark='a'/> Its office software, Microsoft 365, "
            "with LinkedIn and its business applications, sold about a hundred and forty billion dollars in fiscal "
            "2026 and kept about eighty-four billion as operating profit: sixty cents of every dollar. Selling one "
            "more subscription costs Microsoft almost nothing. <bookmark mark='b'/> But look at its cloud. Renting "
            "out computing power, and above all running artificial intelligence, needs a data centre, electricity "
            "and chips for every answer. The cost of one more is no longer zero. The cloud's margin is forty-one "
            f"percent, and its cost of revenue grew {100 * growth:.0f} percent in a year, driven, Microsoft says, by "
            "its investment in AI infrastructure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(office[6]), GrowFromEdge(office[0], DOWN), FadeIn(office[2]), FadeIn(office[4]))
            self.play(GrowFromEdge(office[1], DOWN), FadeIn(office[3]), FadeIn(office[5]), FadeIn(office[7]))
            vo.wait_until("b")
            self.play(FadeIn(cloud[6]), GrowFromEdge(cloud[0], DOWN), FadeIn(cloud[2]), FadeIn(cloud[4]))
            self.play(GrowFromEdge(cloud[1], DOWN), FadeIn(cloud[3]), FadeIn(cloud[5]), FadeIn(cloud[7]))
        lesson = VGroup(tx("When one more costs nothing, price is set by what buyers will pay, not by cost,", 22, WHITE),
                        tx("and the firm with the most users spreads its fixed cost thinnest.", 22, WHITE)).arrange(
            DOWN, buff=0.1).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Zero marginal cost changes the rules. <bookmark mark='a'/> A price can no longer be cost plus a markup, "
            "because there is no cost to add to: it is set by what buyers will pay. And the company with the most "
            "users spreads its fixed cost thinnest, can spend the most on the next version, and pulls further ahead. "
            "That is why software markets so often end with one winner, a story this series takes up again when it "
            "reaches the platforms."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(src), FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
