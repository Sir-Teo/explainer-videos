from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        head = tx("The cycle", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        wave = FunctionGraph(lambda x: 0.55 * np.sin(1.1 * x), x_range=[-6.8, -1.0], color=ORDER, stroke_width=4).shift(
            DOWN * 0.2)
        boat = draw.ship(0.8)
        t = ValueTracker(-6.6)
        boat.add_updater(lambda b: b.move_to([t.get_value(), 0.55 * np.sin(1.1 * t.get_value()) - 0.2 + 0.18, 0]))
        lines = VGroup(
            tx("Capacity that takes years to build, ordered by today's price,", 23),
            tx("arrives together, and prices swing.", 23, GREY_A),
            tx("The longer the wait, the bigger the swing:", 23),
            tx("hogs, ships, chips, houses and oil all show it.", 23, GREY_A),
            tx("Fixed costs and debt turn a fall in sales", 23),
            tx("into a collapse in profit.", 23, GREY_A),
            tx("Read the order book, spending against wear, and the stock;", 23),
            tx("the low-cost producer with little debt survives.", 23, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.0, -0.3, 0])
        pairs = [VGroup(lines[2 * k], lines[2 * k + 1]) for k in range(4)]
        with self.voiceover(
            "The cycle. <bookmark mark='a'/> When capacity takes years to build and is ordered by looking at "
            "today's price, it arrives together, and prices swing. <bookmark mark='b'/> The longer the wait, the "
            "bigger the swing, even when demand grows smoothly: hog farmers in the 1880s and memory makers in the "
            "2020s draw the same shape. <bookmark mark='c'/> Fixed costs and debt turn a modest fall in sales into "
            "a collapse in profit. <bookmark mark='d'/> No one can say when the turn will come. But you can read "
            "how much is on its way, how fast it is being built, and how empty the shelves are; and the plant "
            "with the lowest cost and the least debt is the one still standing at the bottom."
        ) as vo:
            self.add(boat)
            self.play(FadeIn(head), Create(wave), t.animate.set_value(-5.0), run_time=1.6)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(pairs[k]), t.animate.set_value(-5.0 + 1.0 * (k + 1)), run_time=1.2)
        boat.clear_updaters()
        self.clear_scene()
        nxt = VGroup(tx("Next: Part 7", 26, GREY_B), tx("Sizing a Market", 64, WHITE, bold=True),
                     tx("How big is a market, and how would anyone know?", 26, GREY_A, italic=True)).arrange(
            DOWN, buff=0.3).move_to(UP * 0.8)
        crowd = VGroup(*[draw.person(0.4, color=STONE) for _ in range(24)]).arrange_in_grid(rows=2, cols=12,
                                                                                         buff=(0.12, 0.1))
        crowd.next_to(nxt, DOWN, buff=0.7)
        with self.voiceover(
            "Every part so far has used numbers about how big a market is. The next part asks where those numbers "
            "come from, and why three honest ways of counting the same market give three different answers. Part "
            "seven: sizing a market."
        ):
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.5)
            self.play(FadeIn(nxt[2], shift=UP * 0.1), LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in crowd],
                                                                  lag_ratio=0.04), run_time=2.0)
        self.wait(1.0)
        self.clear_scene()
