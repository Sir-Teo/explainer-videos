from __future__ import annotations

from explainer.industry.data.fetch import read
from explainer.industry.register import get
from videos.industry.industry5.common import *  # noqa: F403


class Tobacco(VoiceoverScene):
    def construct(self):
        card(self, 9, "A moat that held", "How can an industry losing its customers keep the highest returns?",
             "Chapter nine. A moat that held.", lit=("moat",))
        s65, s22 = get("smoke.1965"), get("smoke.2022")
        people = VGroup(*[draw.person(0.36) for _ in range(100)]).arrange_in_grid(rows=5, cols=20, buff=(0.1, 0.12))
        people.move_to([0, 1.55, 0])
        share = ValueTracker(s65)

        def paint(m):
            k = int(round(100 * share.get_value()))
            for i, p in enumerate(m):
                p.set_fill(ENTRANT if i < k else "#3A4250", opacity=1)
        people.add_updater(paint)
        num = draw.number(lambda: 100 * share.get_value(), 0, suffix=" in 100 adults smoke", size=30, color=ENTRANT)
        num.add_updater(lambda m: m.next_to(people, UP, buff=0.2), call_updater=True)
        year = ValueTracker(1965)
        yr = draw.number(lambda: year.get_value(), 0, size=30, color=GREY_A, commas=False)
        yr.add_updater(lambda m: m.next_to(people, LEFT, buff=0.3), call_updater=True)

        rows = [r for r in read("damodaran_roc") if r["name"] == "Tobacco" and isinstance(r["roc"], float)]
        rows.sort(key=lambda r: r["year"])
        ax = CornerAxes(x_range=[2014.5, 2025.5, 1], y_range=[0, 1.0, 0.2], x_length=8.0, y_length=2.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-0.6, -2.15, 0])
        bars = VGroup()
        for r in rows:
            y, v = int(r["year"]), r["roc"]
            bars.add(Rectangle(width=0.5, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=RET,
                               fill_opacity=0.85).move_to(ax.c2p(y, 0), aligned_edge=DOWN))
        xt = VGroup(*[tx(f"{y}", 14, GREY_B).next_to(ax.c2p(y, 0), DOWN, buff=0.06) for y in (2015, 2020, 2025)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 14, GREY_B).next_to(ax.c2p(2014.5, v), LEFT, buff=0.06) for v in (0.4, 0.8)])
        yl = tx("tobacco's return on capital", 16, RET).next_to(ax, RIGHT, buff=0.2).align_to(ax, UP)
        lo, hi = min(r["roc"] for r in rows), max(r["roc"] for r in rows)
        why = VGroup(tx("a few firms that rarely fight on price", 17, WHITE),
                     tx("brands smokers stay loyal to", 17, WHITE),
                     tx("advertising limits that freeze the leaders in place", 17, WHITE),
                     tx("and a product that is itself a habit", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.08).move_to([4.6, -2.0, 0])
        src = source("CDC (1965, 2022); Damodaran, Excess Returns by industry (Tobacco), 2015-2025", corner=UL, size=13)
        with self.voiceover(
            "Habit can hold a moat in place even while the market shrinks under it. <bookmark mark='a'/> In 1965, "
            f"about {100 * s65:.0f} of every hundred American adults smoked cigarettes. <bookmark mark='b'/> By "
            f"2022, by the government's count, it was under {100 * s22 + 0.5:.0f}. Few industries have lost "
            "customers so steadily for so long. <bookmark mark='c'/> And yet tobacco has earned the highest "
            f"return on capital in Damodaran's table in seven of the last eleven years, and the second highest in the "
            f"other four: between {100 * lo:.0f} and {100 * hi:.0f} percent "
            "since 2015. <bookmark mark='d'/> Every force is on its side. A few firms that rarely fight on price. "
            "Brands that smokers stay loyal to. Limits on advertising that keep newcomers from building a brand of "
            "their own. And a product that is, quite literally, a habit. With fewer customers every year, the castle "
            "has stayed full."
        ) as vo:
            self.add(people)
            self.play(FadeIn(src), FadeIn(num), FadeIn(yr))
            vo.wait_until("a")
            self.play(Indicate(num, color=ENTRANT))
            vo.wait_until("b")
            self.play(share.animate.set_value(s22), year.animate.set_value(2022), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=2.4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(w_, shift=LEFT * 0.15) for w_ in why], lag_ratio=0.5), run_time=3.0)
        for m in (people, num, yr):
            m.clear_updaters()
        self.clear_scene()
