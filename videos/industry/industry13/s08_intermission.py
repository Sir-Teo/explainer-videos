from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


def interp(d, x):
    k = sorted(d)
    if x <= k[0]:
        return d[k[0]]
    for a, b in zip(k, k[1:]):
        if a <= x <= b:
            return d[a] + (d[b] - d[a]) * (x - a) / (b - a)
    return d[k[-1]]


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.price()
        self.story()

    def film(self):
        H = R["history"]
        S = {y: v for y, v in H["sales"].items() if y >= 1950}
        ys = sorted(S)
        pa = viz.plot_axes([1949, 2027], [0, 4400], x_length=11.0, y_length=4.6, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[1000, 2000, 3000, 4000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="US electricity sales, billion kWh a year", size=14).move_to([0, -0.5, 0])
        t = ValueTracker(ys[0])

        def line():
            xs = [y for y in ys if y <= t.get_value()] + [t.get_value()]
            q = [pa.ax.c2p(x, interp(S, x)) for x in xs]
            return VMobject(stroke_color=PRICE, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        dec = H["decades"]
        marks = VGroup()
        for y0, g in dec.items():
            x = y0 + 5
            p = pa.ax.c2p(x, interp(S, x))
            marks.add(tx(f"{y0}s: {g:+.1f}% a year", 14, WHITE, bold=True).next_to(p, UP + LEFT if y0 < 1990 else UP, buff=0.12))
        head = tx("Seventy-five years of American electricity", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("EIA, Monthly Energy Review, Table 7.6 (retail sales of electricity)", size=13)
        with self.voiceover(
            "An intermission: seventy-five years of American electricity. <bookmark mark='a'/> In the 1950s, sales grew "
            f"about {dec[1950]:.0f} per cent a year, doubling every eight years. <bookmark mark='b'/> In the 1960s, still "
            "about seven: at that rate, a utility needs twice as many plants every ten years. <bookmark mark='c'/> Then, "
            "in the decade of the oil shocks, growth slowed: four per cent, then two. <bookmark mark='d'/> In the 2000s, "
            "under one; and in the 2010s, sales were flat for a whole decade. <bookmark mark='e'/> And now the line has "
            f"turned up again, to about {S[ys[-1]]:,.0f} billion kilowatt-hours in {ys[-1]}. More about why in chapter "
            "eleven."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.add(ln, yr)
            for m, x1, idx in zip("abcde", (1960, 1970, 2000, 2020, ys[-1]), ((0,), (1,), (2, 3, 4), (5, 6), ())):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.0, rate_func=linear)
                if idx:
                    self.play(*[FadeIn(marks[i], shift=DOWN * 0.1) for i in idx if i < len(marks)], run_time=0.6)
        for m in (ln, yr):
            m.clear_updaters()
        self.clear_scene()

    def price(self):
        H = R["history"]
        rl = H["real"]
        ys = sorted(rl)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 0.26], x_length=9.0, y_length=4.2, xticks=[1980, 1990, 2000, 2010, 2020],
                           yticks=[0.05, 0.10, 0.15, 0.20, 0.25], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}¢",
                           ylabel=f"a kWh for a household, in {max(ys)}'s dollars", size=14).move_to([-1.4, -0.4, 0])
        ln = poly(pa, [(y, rl[y]) for y in ys], PRICE, 3.5)
        lo = min(ys, key=lambda y: rl[y])
        notes = VGroup(tx(f"{ys[0]}: {100 * rl[ys[0]]:.1f}¢", 17, WHITE, bold=True), tx(f"{lo}: {100 * rl[lo]:.1f}¢, the lowest", 17, GOOD, bold=True),
                       tx(f"{ys[-1]}: {100 * rl[ys[-1]]:.1f}¢", 17, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.8, 0.6, 0])
        head = tx("What a household paid for a kWh, after inflation", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("BLS, average price of electricity per kWh, US city average, and the CPI, via FRED", size=13)
        with self.voiceover(
            "And the price. <bookmark mark='a'/> In today's money, an American household paid about "
            f"{100 * rl[ys[0]]:.0f} cents a kilowatt-hour in {ys[0]}. <bookmark mark='b'/> By {lo} it had fallen to about "
            f"{100 * rl[lo]:.0f} cents: power got cheaper for a quarter of a century. <bookmark mark='c'/> Since then it has crept back "
            f"up, to about {100 * rl[ys[-1]]:.0f} cents in {ys[-1]}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Flash(pa.ax.c2p(lo, rl[lo]), color=GOOD))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["Electricity must be made the instant it is used, so the grid is built for the peak.",
                 "Load factor, average over peak, decides what every kilowatt-hour costs.",
                 "Some plants cost a lot to build and little to run; some the reverse.",
                 "The cheapest plants run first; the last one needed sets the price.",
                 "The wires are a monopoly; a state commission sets what they earn.",
                 "When a market runs short, the price hits the cap and the lights can go out."]
        pics = [draw.house(0.5), draw.skyline(1.2), draw.cooling_tower(0.6),
                draw.gas_plant(0.6), draw.pylon(0.6), draw.cylinder(0.5, WIND)]
        rows = VGroup()
        for pic, l_ in zip(pics, lines):
            pic.scale_to_fit_height(min(pic.height, 0.45))
            if pic.width > 0.8:
                pic.scale_to_fit_width(0.8)
            rows.add(VGroup(pic, tx(l_, 22, WHITE)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        nxt = tx("Next: wind and sun, storage, retailers, the world, the new load, and the landscape.", 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> Electricity has to be made the instant it is used, so the whole system "
            "is built for its busiest hour. <bookmark mark='b'/> Insull's load factor, average use over peak, decides "
            "what every kilowatt-hour costs. <bookmark mark='c'/> Plants trade fixed cost against running cost. "
            "<bookmark mark='d'/> The cheapest run first, and the last one needed sets the price. <bookmark mark='e'/> "
            "The wires are a monopoly, and a state commission sets what they earn. <bookmark mark='f'/> And when a market "
            "runs short, the price goes to the cap, and the lights can go out. Next: what wind, sun and batteries do to "
            "all of this."
        ) as vo:
            self.play(FadeIn(head))
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(nxt))
        self.clear_scene()
