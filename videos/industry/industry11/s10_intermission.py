from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.film()
        self.story()

    def film(self):
        G = R["glut"]
        W, CH = G["world"], G["china"]
        ys = sorted(W)
        pa = viz.plot_axes([1948, 2027], [0, 2100], x_length=11.4, y_length=4.8, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[500, 1000, 1500, 2000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f} Mt",
                           size=14).move_to([0, -0.4, 0])
        t = ValueTracker(ys[0])

        def interp(d, x):
            k = sorted(d)
            if x <= k[0]:
                return d[k[0]]
            for a, b in zip(k, k[1:]):
                if a <= x <= b:
                    return d[a] + (d[b] - d[a]) * (x - a) / (b - a)
            return d[k[-1]]

        def line():
            xs = [y for y in ys if y <= t.get_value()] + [t.get_value()]
            q = [pa.ax.c2p(x, interp(W, x)) for x in xs]
            return VMobject(stroke_color=STEELC, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()

        def china():
            cy = sorted(CH)
            xs = [y for y in cy if y <= t.get_value()]
            if len(xs) < 2:
                return VMobject()
            pts = [pa.ax.c2p(x, CH[x]) for x in xs]
            return Polygon(*pts, pa.ax.c2p(xs[-1], 0), pa.ax.c2p(xs[0], 0), stroke_width=0, fill_color=CHINA, fill_opacity=0.5)
        ln = always_redraw(line)
        ca = always_redraw(china)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=36, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        eps = [(1955, "the post-war boom"), (1975, "oil shocks, then a long plateau"), (1992, "the Soviet Union's mills collapse"),
               (2008, "China builds"), (2021, f"the peak: {W[2021]:,.0f} Mt")]
        marks = VGroup()
        for x, name in eps:
            p = pa.ax.c2p(x, interp(W, x))
            marks.add(VGroup(Dot(p, radius=0.06, color=WHITE),
                             tx(name, 15, WHITE, bold=True).next_to(p, UP if x != 1992 else DOWN, buff=0.15)))
        lc = tx("China", 15, CHINA, bold=True).move_to(pa.ax.c2p(2016, 300))
        head = tx("World crude steel production, 1950-2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("World Steel Association, World Steel in Figures 2026; China: Steel Statistical Yearbooks and World "
                     "Steel in Figures", size=13)
        with self.voiceover(
            "An intermission: seventy-five years of the world's steel. <bookmark mark='a'/> The post-war boom, when "
            "Europe and Japan rebuilt and America made cars by the million. <bookmark mark='b'/> The oil shocks of the "
            "1970s, and then twenty years in which the world made about the same amount of steel every year, and the "
            "old steel towns of America and Europe shut their furnaces one after another. <bookmark mark='c'/> The "
            "collapse of the Soviet Union, and of the mills that had served it. <bookmark mark='d'/> Then China, whose "
            f"output went from about {CH[2000]:.0f} million tonnes in 2000 to more than a billion in 2020. "
            "<bookmark mark='e'/> And the peak, so far, in 2021. Look at the shape: long flat stretches, and one great "
            "climb that was almost entirely one country."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.add(ln, ca, yr)
            for m, x1 in zip("abcde", (1965, 1990, 1998, 2015, 2025)):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.0, rate_func=linear)
                new = [marks[i] for i, (x, _) in enumerate(eps) if x <= x1 and marks[i] not in self.mobjects]
                if new:
                    self.play(*[FadeIn(g, shift=DOWN * 0.1) for g in new], run_time=0.6)
                if m == "d":
                    self.play(FadeIn(lc))
        for m in (ln, ca, yr):
            m.clear_updaters()
        self.clear_scene()

    def story(self):
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["A kilo of steel sheet costs less than a kilo of bananas; stone costs almost nothing.",
                 "Steel is made from ore and coal, or from scrap and electricity.",
                 "A steelmaker lives on the spread between its price and its metal.",
                 "Heavy fixed costs: a mill must run, so gluts last and profits swing.",
                 "Minimills climbed from rebar to sheet and took most of American steel.",
                 "China makes half the world's steel, and exports what it cannot use.",
                 "Cement travels badly: each plant has its circle, and a temptation to keep it."]
        pics = [draw.banana(0.4), draw.blast_furnace(0.6), draw.coil(0.22), draw.ladle(0.4), draw.eaf(0.6), draw.ship(0.8),
                draw.rotary_kiln(0.8)]
        rows = VGroup()
        for pic, l_ in zip(pics, lines):
            pic.scale_to_fit_height(min(pic.height, 0.42))
            if pic.width > 0.8:
                pic.scale_to_fit_width(0.8)
            rows.add(VGroup(pic, tx(l_, 21, WHITE)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(head, DOWN, buff=0.45)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        nxt = tx("Next: aluminium, packaging, the quarry, carbon, and the landscape.", 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> The materials the world is built from are among the cheapest things it "
            "buys by weight. <bookmark mark='b'/> Steel is made two ways, from ore and coal, or from scrap and "
            "electricity. <bookmark mark='c'/> A steelmaker lives on the spread between its price and its metal. "
            "<bookmark mark='d'/> Its fixed costs make it run in good times and bad, so gluts last and profits swing. "
            "<bookmark mark='e'/> The minimills climbed from the bottom of the market to the top. <bookmark mark='f'/> "
            "China makes half the world's steel. <bookmark mark='g'/> And cement, which travels badly, gives every plant "
            "its own small territory. Next: the metal that is really electricity, the box, the quarry, and the carbon."
        ) as vo:
            self.play(FadeIn(head))
            for m, r_ in zip("abcdefg", rows):
                vo.wait_until(m)
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(nxt))
        self.clear_scene()
