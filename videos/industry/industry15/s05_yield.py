from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Yield(VoiceoverScene):
    def construct(self):
        card(self, 4, "Yield", "Why does a bigger chip cost far more than its size?",
             "Chapter four. Yield.", lit=("make", "dollar"))
        self.defects()
        self.curve()
        self.learn()

    def _wafer(self, die, center, rng, n_def):
        r = 1.9
        disc = Circle(radius=r, stroke_color="#C9D3E0", stroke_width=2, fill_color="#2A2F3A", fill_opacity=1).move_to(center)
        dies = VGroup()
        n = int(r / die) + 1
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                x, y = (i + 0.5) * die, (j + 0.5) * die
                if np.hypot(abs(x) + die / 2, abs(y) + die / 2) < r * 0.97:
                    dies.add(Square(die * 0.9, stroke_width=0, fill_color=DIE, fill_opacity=0.85).move_to(center + np.array([x, y, 0])))
        pts = []
        while len(pts) < n_def:
            p = rng.uniform(-r, r, 2)
            if np.hypot(*p) < r * 0.95:
                pts.append(p)
        defects = VGroup(*[Dot(center + np.array([p[0], p[1], 0]), radius=0.04, color=DEFECT) for p in pts])
        hit = [d for d in dies if any(abs(d.get_center()[0] - q.get_center()[0]) < die / 2 and abs(d.get_center()[1] - q.get_center()[1]) < die / 2 for q in defects)]
        return disc, dies, defects, hit

    def defects(self):
        Y = R["yield"]
        rng = np.random.default_rng(8)
        a = self._wafer(0.22, np.array([-3.4, -0.4, 0]), rng, 14)
        rng = np.random.default_rng(8)
        b = self._wafer(0.62, np.array([3.4, -0.4, 0]), rng, 14)
        la = VGroup(tx("small dies: 100 mm2", 18, WHITE, bold=True), tx(f"about {Y['small']['dpw']:.0f} per wafer", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(a[0], UP, buff=0.15)
        lb = VGroup(tx("big dies: 800 mm2", 18, WHITE, bold=True), tx(f"about {Y['big']['dpw']:.0f} per wafer", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(b[0], UP, buff=0.15)
        ra = VGroup(tx(f"{100 * Y['small']['y']:.0f}% good: about {Y['small']['good']:.0f} chips", 17, GOOD, bold=True)).next_to(a[0], DOWN, buff=0.15)
        rb = VGroup(tx(f"{100 * Y['big']['y']:.0f}% good: about {Y['big']['good']:.0f} chips", 17, BAD, bold=True)).next_to(b[0], DOWN, buff=0.15)
        tag = estimate_tag("illustration: random defects at 0.1 per cm2 (the Works)", corner=DR, size=12)
        with self.voiceover(
            "Every wafer comes out of the fab with a few specks of dust or flaws scattered across it, and a die with a "
            "flaw in the wrong place is scrap. <bookmark mark='a'/> Take two wafers with the same scattering of defects. "
            "One is cut into small dies, a hundred square millimetres each; the other into big ones, eight hundred. "
            "<bookmark mark='b'/> Here are the defects. <bookmark mark='c'/> On the small dies, a defect ruins one small "
            f"die: about {100 * Y['small']['y']:.0f} per cent come out good. <bookmark mark='d'/> On the big dies, the "
            f"same defects ruin far more silicon: only about {100 * Y['big']['y']:.0f} per cent are good. A big die costs "
            "more than its area, because each flaw throws away more."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(a[0]), FadeIn(b[0]))
            vo.wait_until("a")
            self.play(FadeIn(a[1]), FadeIn(b[1]), FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=3) for d in a[2]], lag_ratio=0.05), LaggedStart(*[FadeIn(d, scale=3) for d in b[2]], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(*[d.animate.set_fill(DEFECT, opacity=0.8) for d in a[3]], FadeIn(ra))
            vo.wait_until("d")
            self.play(*[d.animate.set_fill(DEFECT, opacity=0.8) for d in b[3]], FadeIn(rb))
        self.clear_scene()

    def curve(self):
        Y = R["yield"]
        sizes = Y["sizes"]
        pa = viz.plot_axes([0, 850], [0, 1.0], x_length=8.2, y_length=4.4, xticks=[100, 200, 400, 600, 800], yticks=[0.25, 0.5, 0.75, 1.0],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%", ylabel="share of dies that work", size=13).move_to([-1.4, -0.4, 0])
        xl = tx("die size, mm2", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        cols = {0.1: GOOD, 0.3: PRICE, 0.5: BAD}
        lines = VGroup(*[poly(pa, list(zip(sizes, Y["y"][d])), cols[d], 4) for d in (0.1, 0.3, 0.5)])
        labs = VGroup(*[tx(f"{d} defects per cm2", 15, cols[d], bold=True).next_to(pa.ax.c2p(850, Y["y"][d][-1]), RIGHT, buff=0.1) for d in (0.1, 0.3, 0.5)])
        eq = VGroup(tx("yield = e^(-area x defect density)", 18, WHITE, bold=True), tx("if defects fall at random", 14, GREY_A)).arrange(DOWN, buff=0.05).move_to([3.8, 2.4, 0])
        tag = estimate_tag("the Works: a standard Poisson yield model", corner=DR, size=12)
        with self.voiceover(
            "If defects fall at random, the share of good dies falls exponentially with the die's area times the defect "
            "density. <bookmark mark='a'/> On a mature process, with one defect in ten square centimetres, small chips "
            "nearly all work and big ones mostly do. <bookmark mark='b'/> On a new process, with three or five defects "
            "per ten square centimetres, small chips still come out well, but big ones are mostly scrap. So on a new "
            "process the small chips pay first, and the biggest chips are worth making only once the process has "
            "matured."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(eq), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(labs[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(labs[1]), FadeIn(labs[2]), run_time=2.5)
        self.clear_scene()

    def learn(self):
        F = R["fab"]
        from explainer.industry.works import fab as W
        ws = np.linspace(0, 600_000, 61)
        d = [W.learning(0.5, 0.1, w, 150_000) for w in ws]
        pa = viz.plot_axes([0, 600_000], [0, 0.55], x_length=6.2, y_length=4.0, xticks=[0, 200_000, 400_000, 600_000], yticks=[0.1, 0.3, 0.5],
                           xfmt=lambda v: f"{v / 1000:.0f}k", yfmt=lambda v: f"{v:.1f}", ylabel="defects per cm2", size=13).move_to([-3.0, -0.4, 0])
        xl = tx("wafers made on the process so far", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        ln = poly(pa, list(zip(ws, d)), DEFECT, 4)
        gm = F["gm"]
        bars = VGroup()
        for i, (k, v) in enumerate(gm.items()):
            b = Rectangle(width=0.7, height=v / 100 * 4.0, stroke_width=0, fill_color=GOOD, fill_opacity=0.5 + 0.12 * i).move_to([2.2 + 1.0 * i, -2.4, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{v:.1f}%", 15, WHITE, bold=True).next_to(b, UP, buff=0.06), tx(str(k), 13, GREY_A).next_to(b, DOWN, buff=0.08)))
        bh = tx("TSMC's gross margin", 16, GREY_A).move_to([3.7, 2.3, 0])
        tag = estimate_tag("left: the Works' learning curve, an illustration", corner=DR, size=12)
        src = source("TSMC, Form 20-F 2025 (gross margin 2023-2025); Form 6-K of 15 October 2026 (third quarter 2026)", size=13)
        with self.voiceover(
            "Defect density is not fixed. <bookmark mark='a'/> Every wafer a fab makes on a process teaches its engineers "
            "something, and the defects fall: fast at first, then slowly. <bookmark mark='b'/> So the first company to "
            "reach a new node gets down the curve first, and can sell its customers good chips while rivals are still "
            "scrapping theirs. TSMC's gross margin went from "
            f"{gm[2023]:.1f} per cent in 2023 to {gm[2025]:.1f} in 2025, which it put down to fuller fabs and lower "
            f"costs, and to {gm['3Q26']:.1f} in the third quarter of 2026."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag), FadeIn(src), FadeIn(bh))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars], lag_ratio=0.25), run_time=2.5)
        self.clear_scene()
