from __future__ import annotations

from explainer.industry.register import get, row
from videos.industry.industry7.common import *  # noqa: F403

NEW, REPL, OUT = GOLD, RETAIL, "#8C929B"


class Replace(VoiceoverScene):
    def construct(self):
        card(self, 12, "When everyone has one", "How big is a market once the S-curve is full?",
             "Chapter twelve. When everyone has one.", lit=("unit", "change"))
        self.tub()
        self.rule()

    def tub(self):
        M = R["replace"]
        yy, stock, first, repl = M["years"], M["stock"], M["first"], M["repl"]
        k0 = yy.index(1975)
        t = ValueTracker(1975)

        def at(series):
            x = t.get_value()
            k = min(max(int(np.floor(x)) - yy[0], 0), len(yy) - 2)
            f = x - yy[k]
            return series[k] * (1 - f) + series[k + 1] * f

        # the tub: microwaves in use; tap on top, drain below
        W, H = 2.6, 3.2
        c = np.array([-4.3, -0.6, 0])
        tub = VGroup(Line(c + [-W / 2, H / 2, 0], c + [-W / 2, -H / 2, 0]), Line(c + [-W / 2, -H / 2, 0],
                                                                                  c + [W / 2, -H / 2, 0]),
                     Line(c + [W / 2, -H / 2, 0], c + [W / 2, H / 2, 0])).set_stroke(STONE, 4)
        cap = 140.0  # millions, the tub's brim

        def level():
            h = max(H * at(stock) / cap, 0.001)
            return Rectangle(width=W - 0.08, height=h, stroke_width=0, fill_color=WATER, fill_opacity=0.75).move_to(
                c + [0, -H / 2 + h / 2 + 0.02, 0])
        lvl = always_redraw(level)

        def stream(series, x, top, col, scale=0.05):
            def make():
                w = max(at(series) * scale, 0.01)
                return Rectangle(width=w, height=1.1, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                    [x, top, 0])
            return always_redraw(make)
        s_new = stream(first, c[0] - 0.45, c[1] + H / 2 + 0.55, NEW)
        s_rep = stream(repl, c[0] + 0.45, c[1] + H / 2 + 0.55, REPL)
        s_out = stream(repl, c[0], c[1] - H / 2 - 0.55, OUT)
        tl = VGroup(tx("new homes buying", 15, NEW), tx("replacements", 15, REPL)).arrange(RIGHT, buff=0.35).next_to(
            tub, UP, buff=1.2)
        ol = tx("worn out, thrown away", 15, OUT).next_to(tub, DOWN, buff=1.2)
        inside = draw.number(lambda: at(stock), decimals=0, suffix="m in use", size=24, color=WHITE)
        inside.add_updater(lambda m: m.move_to(c + [0, -H / 2 + 0.35, 0]))
        yr = draw.number(lambda: t.get_value(), decimals=0, commas=False, size=34, color=GREY_A)
        yr.add_updater(lambda m: m.move_to(c + [0, H / 2 + 1.75, 0]).shift(RIGHT * 2.6))

        pa = viz.plot_axes([1974, 2026], [0, 16], x_length=6.0, y_length=3.6, xticks=[1980, 1990, 2000, 2010, 2020],
                           yticks=[4, 8, 12, 16], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m",
                           size=14, ylabel="sold a year")
        pa.move_to([2.9, -0.4, 0])

        def trace(series, col):
            def make():
                x = t.get_value()
                pts = [pa.ax.c2p(y, v) for y, v in zip(yy[k0:], series[k0:]) if y <= x]
                pts.append(pa.ax.c2p(x, at(series)))
                return VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(pts) if len(pts) > 1 else VMobject()
            return always_redraw(make)
        tr_new, tr_rep = trace(first, NEW), trace(repl, REPL)
        tag = estimate_tag(f"a model: the Bass fit of Chapter 10, US households, a {M['life']}-year life (assumed)",
                           corner=DR, size=14)
        src = source("Households: Census Bureau, Current Population Survey (via FRED, TTLHH); adoption: Our World in Data; "
                     "this film's model", size=13)
        with self.voiceover(
            "There is one more thing the S-curve hides, and it decides how big most markets are. "
            "<bookmark mark='a'/> Picture every microwave oven in American homes as water in a tub. Two taps fill "
            "it. Gold: homes buying their first one. Green: homes replacing one that wore out. And a drain at the "
            "bottom, the old ovens thrown away. <bookmark mark='b'/> Run the model from 1975, with the adoption curve "
            "of Chapter 10, the real count of American households, and an assumed life of ten years for each oven. "
            "<bookmark mark='c'/> In the early years nearly every sale is a first purchase. First purchases peak in "
            f"{M['peak_first']}, at about {M['peak_first_m']:.0f} million a year. <bookmark mark='d'/> Then they fade, "
            "because almost every home has one. But the tub is now full, and full tubs drain: the ovens bought in "
            "the boom start to wear out, and replacements take over. <bookmark mark='e'/> By the 2020s, in this "
            f"model, about {100 * M['repl_share']:.0f} percent of the ovens sold each year replace an old one, and "
            "the rest go to households that did not exist before. The S-curve flattened; the market did "
            "not."
        ) as vo:
            self.play(FadeIn(src), Create(tub), FadeIn(pa), FadeIn(tag))
            self.add(lvl, s_new, s_rep, s_out, tr_new, tr_rep)
            vo.wait_until("a")
            self.play(FadeIn(tl), FadeIn(ol), FadeIn(inside), FadeIn(yr))
            vo.wait_until("b")
            self.play(t.animate.set_value(1980), run_time=1.5, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(1987), run_time=3.5, rate_func=linear)
            vo.wait_until("d")
            self.play(t.animate.set_value(2005), run_time=5.0, rate_func=linear)
            vo.wait_until("e")
            self.play(t.animate.set_value(2025), run_time=4.0, rate_func=linear)
        for m in (lvl, s_new, s_rep, s_out, tr_new, tr_rep):
            m.clear_updaters()
        self.clear_scene()

    def rule(self):
        M = R["replace"]
        lo, hi = row("model.microwave.life").lo, row("model.microwave.life").hi
        inuse = M["stock"][-1]
        eq = MathTex(r"\text{sold a year} \approx \frac{\text{number in use}}{\text{years each one lasts}}",
                     font_size=44).move_to([0, 2.0, 0])
        cases = VGroup()
        for L, col in ((lo, GUESS), (get("model.microwave.life"), WHITE), (hi, UNITS)):
            n = inuse / L
            bar = Rectangle(width=n * 0.42, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85)
            lab = tx(f"lasts {L:g} years", 20, col, bold=True)
            val = tx(f"{n:.1f}m a year", 20, col)
            cases.add(VGroup(lab, bar, val))
        for k, g in enumerate(cases):
            g[0].move_to([-4.6, 0.4 - 0.9 * k, 0], aligned_edge=RIGHT)
            g[1].next_to(g[0], RIGHT, buff=0.4).align_to([-4.2, 0, 0], LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.25)
        inu = tx(f"{inuse:.0f} million ovens in use (the model, 2025)", 20, WATER).next_to(eq, DOWN, buff=0.35)
        note = VGroup(tx("For a product nearly everyone owns,", 21, GOLD, bold=True),
                      tx("how long people keep it matters as much as how many people there are", 21, GOLD, bold=True)
                      ).arrange(DOWN, buff=0.06).to_edge(DOWN, buff=0.55)
        tag = estimate_tag("the life is this film's assumption, and the point of the chart", corner=DR, size=14)
        with self.voiceover(
            "So a full market obeys a simple rule. <bookmark mark='a'/> Roughly, the number sold each year is the "
            "number in use, divided by how many years each one lasts, plus whatever the number of homes grows by. "
            f"<bookmark mark='b'/> With about {inuse:.0f} million ovens in use, a ten-year life means about "
            f"{inuse / 10:.0f} million sold a year. <bookmark mark='c'/> If ovens lasted {lo:g} years, "
            f"{inuse / lo:.0f} million. If they lasted {hi:g}, about {inuse / hi:.0f} million. Two years of life, "
            "either way, moves the whole market by a fifth or more, with not one extra household. "
            "<bookmark mark='d'/> That is why, for anything most people already own, a car, a phone, a fridge, "
            "how long people keep it matters as much as how many people there are. The life is our assumption here; "
            "a real sizing would have to measure it, and the measuring is hard."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.6)
            vo.wait_until("a")
            self.play(Indicate(eq, color=GOLD, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(inu))
            self.play(FadeIn(cases[1][0]), GrowFromEdge(cases[1][1], LEFT), FadeIn(cases[1][2]))
            vo.wait_until("c")
            for g in (cases[0], cases[2]):
                self.play(FadeIn(g[0]), GrowFromEdge(g[1], LEFT), FadeIn(g[2]), run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(note, shift=UP * 0.1))
        self.clear_scene()
