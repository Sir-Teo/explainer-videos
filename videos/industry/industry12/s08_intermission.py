from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


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
        self.america()
        self.story()

    def film(self):
        W = {y: v / 1e6 for y, v in R["hook"]["world_n"].items()}
        US = {y: v / 1e6 for y, v in R["fertilizer"]["us_n"].items()}
        US[2025] = get("usgs.n.us.2025") / 1000
        ys = sorted(W)
        pa = viz.plot_axes([1945, 2027], [0, 175], x_length=11.4, y_length=4.8, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[40, 80, 120, 160], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f} Mt",
                           ylabel="million tonnes of nitrogen, as ammonia", size=14).move_to([0, -0.5, 0])
        t = ValueTracker(ys[0])
        gap0 = max(y for y in W if y < 2025)

        def line():
            xs = [y for y in ys if y <= min(t.get_value(), gap0)] + [min(t.get_value(), gap0)]
            q = [pa.ax.c2p(x, interp(W, x)) for x in xs]
            return VMobject(stroke_color=NITRO, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()

        def bridge():
            if t.get_value() <= gap0:
                return VMobject()
            return DashedLine(pa.ax.c2p(gap0, W[gap0]), pa.ax.c2p(t.get_value(), interp(W, t.get_value())), stroke_color=NITRO,
                              stroke_width=3, dash_length=0.08)

        def us():
            uy = sorted(y for y in US if y <= 2022)
            xs = [y for y in uy if y <= t.get_value()]
            if len(xs) < 2:
                return VMobject()
            pts = [pa.ax.c2p(x, US[x]) for x in xs]
            return Polygon(*pts, pa.ax.c2p(xs[-1], 0), pa.ax.c2p(xs[0], 0), stroke_width=0, fill_color=TEXAS, fill_opacity=0.6)
        ln, br, ua = always_redraw(line), always_redraw(bridge), always_redraw(us)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        eps = [(1970, f"1970: {W[1970]:.0f} Mt"), (1989, f"1989: {W[1989]:.0f} Mt"), (1993, "a dip, as the Soviet Union broke up"),
               (2025, f"2025: {W[2025]:.0f} Mt")]
        marks = VGroup()
        for x, name in eps:
            p = pa.ax.c2p(x, W[x])
            lab = tx(name, 15, WHITE, bold=True)
            if x == 1993:
                lab.next_to(p, DOWN + RIGHT, buff=0.12)
            elif x == 2025:
                lab.next_to(p, LEFT, buff=0.15)
            else:
                lab.next_to(p, UP + LEFT, buff=0.1)
            marks.add(VGroup(Dot(p, radius=0.06, color=WHITE), lab))
        lu = tx("America", 15, TEXAS, bold=True).move_to(pa.ax.c2p(1985, 6))
        head = tx(f"The world's ammonia, {ys[0]}-2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        note = tx("dashed: 2023-24 not in the series", 12, GREY_B).next_to(pa, DOWN, buff=0.05).align_to(pa, RIGHT)
        src = source("USGS, Data Series 140 (nitrogen) and Mineral Commodity Summaries 2026", size=13)
        with self.voiceover(
            "An intermission: eighty years of the world's ammonia, in the Geological Survey's records. "
            f"<bookmark mark='a'/> After the Second World War, about {W[ys[0]]:.0f} million tonnes of nitrogen a year. By "
            f"1970, {W[1970]:.0f} million: the fertilizer that came with new seeds and new farming around the world. "
            f"<bookmark mark='b'/> It doubled again by the end of the 1980s. <bookmark mark='c'/> A dip in the early "
            "1990s, as the Soviet Union broke up. <bookmark mark='d'/> And then a steady climb, to about "
            f"{W[2025]:.0f} million tonnes in 2025. <bookmark mark='e'/> The gold underneath is America: about "
            f"{100 * US[1950] / W[1950]:.0f} per cent of the world's ammonia in 1950, about "
            f"{100 * US[2025] / W[2025]:.0f} per cent now, though its story has a twist."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), FadeIn(note))
            self.add(ln, br, ua, yr)
            for m, x1, show in zip("abcd", (1970, 1989, 1993, 2025), (0, 1, 2, 3)):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.0, rate_func=linear)
                self.play(FadeIn(marks[show], shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(lu), Indicate(lu, color=TEXAS))
        for m in (ln, br, ua, yr):
            m.clear_updaters()
        self.clear_scene()

    def america(self):
        US = {y: v / 1e6 for y, v in R["fertilizer"]["us_n"].items()}
        US25 = get("usgs.n.us.2025") / 1000
        gc = R["fertilizer"]["cost"]["US"]
        uy = sorted(US)
        top = viz.plot_axes([1942, 2027], [0, 16], x_length=10.6, y_length=3.0, xticks=[], yticks=[5, 10, 15],
                            yfmt=lambda v: f"{v:.0f} Mt", ylabel="America's ammonia, million tonnes of nitrogen", size=13).move_to(
            [0, 1.3, 0])
        bot = viz.plot_axes([1942, 2027], [0, 350], x_length=10.6, y_length=1.6, xticks=[1950, 1970, 1990, 2010, 2025],
                            yticks=[150, 300], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}",
                            ylabel="the gas in a ton of ammonia, at American prices", size=13).move_to([0, -2.2, 0])
        lb = DashedLine(top.ax.c2p(uy[-1], US[uy[-1]]), top.ax.c2p(2025, US25), stroke_color=TEXAS, stroke_width=3, dash_length=0.08)
        gy = sorted(gc)
        pk = max((y for y in uy if y < 1990), key=lambda y: US[y])
        lo = min((y for y in uy if y > 1995), key=lambda y: US[y])
        g_pk = max((y for y in gy if y <= 2010), key=lambda y: gc[y])
        m1 = VGroup(Dot(top.ax.c2p(pk, US[pk]), radius=0.06, color=WHITE),
                    tx(f"{pk}: {US[pk]:.1f} Mt", 14, WHITE, bold=True).next_to(top.ax.c2p(pk, US[pk]), UP, buff=0.1))
        m2 = VGroup(Dot(top.ax.c2p(lo, US[lo]), radius=0.06, color=BAD),
                    tx(f"{lo}: {US[lo]:.1f} Mt", 14, BAD, bold=True).next_to(top.ax.c2p(lo, US[lo]), DOWN, buff=0.1))
        m3 = VGroup(Dot(top.ax.c2p(2025, US25), radius=0.06, color=GOOD),
                    tx(f"2025: {US25:.0f} Mt", 14, GOOD, bold=True).next_to(top.ax.c2p(2025, US25), UP + LEFT, buff=0.08))
        mg = tx(f"{g_pk}: ${gc[g_pk]:.0f}", 13, GAS).next_to(bot.ax.c2p(g_pk, gc[g_pk]), UP, buff=0.06)
        shade = Rectangle(width=top.ax.c2p(2009, 0)[0] - top.ax.c2p(1999, 0)[0], height=6.0, stroke_width=0, fill_color=BAD,
                          fill_opacity=0.08).move_to([(top.ax.c2p(2009, 0)[0] + top.ax.c2p(1999, 0)[0]) / 2, -0.2, 0])
        src = source("USGS, Data Series 140 and MCS 2026 (nitrogen); gas: IMF via FRED x CF's 34.6 MMBtu a ton", size=13)
        with self.voiceover(
            "Here is the twist. <bookmark mark='a'/> American ammonia grew for forty years, to about "
            f"{US[pk]:.0f} million tonnes of nitrogen in {pk}. <bookmark mark='b'/> Then, in the 2000s, American gas got "
            f"dear. <bookmark mark='c'/> The gas in a ton of ammonia rose to about {gc[g_pk]:.0f} dollars by {g_pk}, and "
            f"America's output fell by almost half, to {US[lo]:.1f} million tonnes in {lo}, as plants shut or sat "
            "idle. <bookmark mark='d'/> Then shale gas made America one of the cheapest places on "
            f"earth to make ammonia, and the plants came back: about {US25:.0f} million tonnes in 2025. The industry "
            "follows its molecule."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(src))
            vo.wait_until("a")
            cut = [y for y in uy if y <= 1999]
            l1 = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([top.ax.c2p(y, US[y]) for y in cut])
            self.play(Create(l1), run_time=3.0, rate_func=linear)
            self.play(FadeIn(m1))
            vo.wait_until("b")
            g1 = VMobject(stroke_color=GAS, stroke_width=3).set_points_as_corners([bot.ax.c2p(y, gc[y]) for y in gy if y <= 2009])
            self.play(FadeIn(shade), Create(g1), run_time=2.0)
            vo.wait_until("c")
            l2 = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([top.ax.c2p(y, US[y]) for y in uy if 1999 <= y <= 2009])
            self.play(Create(l2), FadeIn(mg), run_time=2.0)
            self.play(FadeIn(m2))
            vo.wait_until("d")
            l3 = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([top.ax.c2p(y, US[y]) for y in uy if y >= 2009])
            g2 = VMobject(stroke_color=GAS, stroke_width=3).set_points_as_corners([bot.ax.c2p(y, gc[y]) for y in gy if y >= 2009])
            self.play(Create(l3), Create(g2), run_time=2.5)
            self.play(Create(lb), FadeIn(m3))
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["Chemistry starts from gas, oil and salt, and a handful of building blocks.",
                 "A cracker is a furnace that turns ethane or naphtha into ethylene.",
                 "The feedstock is most of the cost, and the cheapest molecules win.",
                 "Shale made American ethane and gas the cheapest in the rich world.",
                 "Everyone builds in the good years, so the bad years follow.",
                 "Ammonia is natural gas in another form; fertilizer follows the gas."]
        pics = [draw.molecule("CH4", bond=0.3), draw.cracker_unit(1.2), draw.molecule("C2H4", bond=0.3),
                draw.derrick(0.8), draw.crane(0.6), draw.sack(0.5, NITRO, label_="N")]
        rows = VGroup()
        for pic, l_ in zip(pics, lines):
            pic.scale_to_fit_height(min(pic.height, 0.45))
            if pic.width > 0.8:
                pic.scale_to_fit_width(0.8)
            rows.add(VGroup(pic, tx(l_, 23, WHITE)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.6)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        nxt = tx("Next: the gas companies, paint, Europe's shock, plastics, harm, and the landscape.", 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> The chemical industry turns gas, oil and salt into a handful of "
            "building blocks, and those into almost everything. <bookmark mark='b'/> At its root is the cracker, a "
            "furnace that turns ethane or naphtha into ethylene. <bookmark mark='c'/> The feedstock is most of the cost, "
            "and the cheapest molecules win. <bookmark mark='d'/> Shale made America's ethane and gas the cheapest in "
            "the rich world. <bookmark mark='e'/> Everyone builds in the good years, so the bad years follow. "
            "<bookmark mark='f'/> And ammonia is natural gas in another form. Next: the businesses that do not "
            "cycle, Europe's shock, plastics, the harm, and the landscape."
        ) as vo:
            self.play(FadeIn(head))
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(nxt))
        self.clear_scene()
