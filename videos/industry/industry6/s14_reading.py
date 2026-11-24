from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Reading(VoiceoverScene):
    def construct(self):
        card(self, 13, "Reading where you are", "How can you tell where an industry is in its cycle?",
             "Chapter thirteen. Reading where you are.", lit=("change",))
        rd, S = R["reading"], R["ships"]
        inv = dict(rd["inventory"])
        mur = dict(rd["micron"])

        def instrument(title, glyph, lo_lab, lo_v, hi_lab, hi_v, now_lab, now_v, fmt, vmax, col):
            t = ValueTracker(0.0)
            dial = draw.gauge(t, 0, vmax, r=0.85, bands=((BOOM, 0.4), (ORDER, 0.7), (BUST, 1.0)))
            head = tx(title, 19, WHITE, bold=True)
            glyph.scale_to_fit_height(0.55)
            top = VGroup(glyph, head).arrange(RIGHT, buff=0.2)
            num = draw.number(lambda: t.get_value(), 1, suffix=fmt, size=26, color=col)
            notes = VGroup(tx(f"{lo_lab}: {lo_v:.1f}{fmt}", 15, GREY_B), tx(f"{hi_lab}: {hi_v:.1f}{fmt}", 15, BUST)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            body = VGroup(dial, VGroup(num, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(RIGHT, buff=0.4)
            g = VGroup(top, body).arrange(DOWN, buff=0.2)
            num.add_updater(lambda m: m.next_to(notes, UP, buff=0.12).align_to(notes, LEFT))
            g.tracker, g.target, g.num, g.now = t, now_v, num, now_lab
            return g
        a = instrument("Ships on order", draw.ship(0.9), "2014", 100 * get_book(2014), "2009", 100 * get_book(2009),
                       "early 2025", 100 * get_book(2025), "% of fleet", 60, ORDER)
        b = instrument("Spending against wear", draw.factory(0.8, color="#8C929B"), "Micron 2023", mur[2023],
                       "Micron 2026", mur[2026], "fiscal 2026", mur[2026], "×", 4, ORDER)
        c = instrument("Unsold stock", draw.chip(0.5), "Micron 2026", inv[2026], "Micron 2023", inv[2023],
                       "fiscal 2023", inv[2023], " months", 8, ORDER)
        d = instrument("Houses for sale", draw.house(0.6, color=STONE), "September 2026", rd["houses"]["latest"][1],
                       "January 2009", rd["houses"]["worst"][1], "September 2026", rd["houses"]["latest"][1],
                       " months", 14, ORDER)
        grid = VGroup(a, b, c, d).arrange_in_grid(rows=2, cols=2, buff=(1.3, 0.7)).move_to([0, -0.25, 0])
        src = source("UNCTAD; Micron Forms 10-K; Census via FRED", size=13)
        with self.voiceover(
            "If you cannot stop the cycle, you can at least try to read it. A handful of gauges help. "
            "<bookmark mark='a'/> First, the order book: how much new capacity is already on its way, compared with "
            f"what exists. In shipping it read {100 * get_book(2009):.0f} percent in 2009, with the boom's orders still "
            f"arriving, and "
            f"{100 * get_book(2014):.0f} percent in 2014. In early 2025 it read {100 * get_book(2025):.0f}, and rising. "
            "<bookmark mark='b'/> Second, spending against wear: what a company spends on new plant, against its "
            "depreciation. Near one, it is just replacing what wears out. Micron's reading in fiscal 2026 was "
            f"{mur[2026]:.1f}, its highest since at least 2010. <bookmark mark='c'/> Third, unsold stock. At the end "
            f"of fiscal 2023, Micron held chips worth {inv[2023]:.1f} months of its sales; at the end of fiscal 2026, "
            f"under one month: {inv[2026]:.1f}. Shelves that empty are what a peak looks like. "
            "<bookmark mark='d'/> Fourth, for houses, the months it would take to sell every new home for sale: "
            f"{rd['houses']['worst'][1]:.1f} at the worst, in January 2009; {rd['houses']['latest'][1]:.1f} in "
            "September 2026. <bookmark mark='e'/> None of these says when a cycle will turn. Together, they say "
            "how much is coming, and how little room there is if demand stops growing. For memory chips, the one to "
            "watch is the third: when Micron's stock of unsold chips climbs back from under one month of sales "
            "toward the two or three months it held in calmer years, buyers will have stopped scrambling, and prices will "
            "follow."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(g[0].copy().set_opacity(0.25)) for g in grid], lag_ratio=0.2),
                      run_time=1.4)
            for g, m in zip(grid, "abcd"):
                vo.wait_until(m)
                self.play(FadeIn(g), run_time=0.8)
                self.play(g.tracker.animate.set_value(g.target), run_time=1.6)
            vo.wait_until("e")
            self.play(*[Indicate(g[0], color=GOLD) for g in grid])
        for g in grid:
            g.num.clear_updaters()
        self.clear_scene()


def get_book(y):
    return R["ships"]["book"][y]
