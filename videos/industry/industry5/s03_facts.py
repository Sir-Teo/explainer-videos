from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403

SHOW = {"Tobacco", "Retail (Building Supply)", "Beverage (Soft)", "Software (System & Application)",
        "Air Transport", "Auto & Truck", "Coal & Related Energy", "Electronics (Consumer & Office)"}


class Facts(VoiceoverScene):
    def construct(self):
        card(self, 2, "The facts first", "Do some industries really earn more, year after year?",
             "Chapter two. The facts first.", lit=("moat",))
        self.skyline()
        self.persist()

    def skyline(self):
        D = R["roc"]
        inds = D["industries"]
        n = len(inds)
        x0, w = -6.4, 12.6 / n
        base = -1.6
        u = 6.0  # inches per unit of return (100%)

        def y(v):
            return base + u * max(min(v, 0.66), -0.12)
        bars, dots = VGroup(), VGroup()
        for i, d in enumerate(inds):
            above = d["roc"] > d["wacc"]
            h = y(d["roc"]) - base
            b = Rectangle(width=w * 0.8, height=max(abs(h), 0.01), stroke_width=0,
                          fill_color=RET if above else COST_, fill_opacity=0.85)
            b.move_to([x0 + w * (i + 0.5), base, 0], aligned_edge=DOWN if h >= 0 else UP)
            bars.add(b)
            dots.add(Dot([x0 + w * (i + 0.5), y(d["wacc"]), 0], radius=0.035, color=WHITE))
        zero = Line([x0, base, 0], [x0 + 12.6, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        ticks = VGroup(*[VGroup(DashedLine([x0, y(v), 0], [x0 + 12.6, y(v), 0], stroke_color="#2A3140", stroke_width=1),
                                tx(f"{int(100 * v)}%", 15, GREY_B).next_to([x0, y(v), 0], LEFT, buff=0.08))
                         for v in (0.2, 0.4, 0.6)])
        labs = VGroup()
        for i, d in enumerate(inds):
            if d["name"] in SHOW:
                t_ = tx(d["name"].replace(" (System & Application)", "").replace(" (Consumer & Office)", ""), 14,
                        RET if d["roc"] > d["wacc"] else COST_)
                t_.rotate(PI / 2).next_to(bars[i], UP if d["roc"] > 0 else DOWN, buff=0.08)
                labs.add(t_)
        head = tx("Return on capital, 90 US industries, January 2026", 26, bold=True).to_edge(UP, buff=0.3)
        key = VGroup(VGroup(Dot(radius=0.06, color=WHITE), tx("each industry's cost of capital", 16, GREY_B)).arrange(
            RIGHT, buff=0.1)).to_corner(UR, buff=0.45).shift(DOWN * 0.45)
        above = tx(f"{100 * D['above']:.0f}% earn more than their cost of capital; the median earns "
                   f"{100 * D['median']:.0f}% against a cost of {100 * D['wacc_median']:.0f}%", 19, GREY_A).to_edge(
            DOWN, buff=0.55)
        src = source("Aswath Damodaran, NYU Stern: Excess Returns (EVA) by industry, US companies, January 2026")
        top, bot = inds[0], inds[-1]
        with self.voiceover(
            "Before any theory, the facts. Each January the finance professor Aswath Damodaran publishes, for every "
            "American industry, the return its companies earn on the capital invested in them, and what that "
            f"capital costs. <bookmark mark='a'/> Here are {n} industries from his January 2026 file, highest on the "
            "left. <bookmark mark='b'/> The white dots are each industry's cost of capital: what investors could "
            f"expect elsewhere at the same risk, around {100 * D['wacc_median']:.0f} percent. "
            f"<bookmark mark='c'/> Tobacco earns {100 * top['roc']:.0f} percent on its capital. Home-improvement "
            "chains, soft drinks and software earn around thirty. <bookmark mark='d'/> At the other end, "
            "carmakers earn two percent, coal and consumer electronics lose money. <bookmark mark='e'/> In a "
            "good year most industries beat their cost of capital. The spread between them is the puzzle: in a "
            "market where anyone can build a factory, why doesn't money flood into tobacco until it earns seven "
            "percent like everything else?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(zero), FadeIn(ticks))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.01), FadeIn(key), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs[:4]], lag_ratio=0.2))
            self.play(Indicate(bars[0], color=GOLD, scale_factor=1.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs[4:]], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(above, shift=UP * 0.1))
        del bot
        self.clear_scene()

    def persist(self):
        P = R["persist"]
        ax = CornerAxes(x_range=[0, 0.7, 0.1], y_range=[0, 0.7, 0.1], x_length=5.4, y_length=5.4,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-2.4, -0.3, 0])
        xt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0.2, 0.4, 0.6)])
        yt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08) for v in (0.2, 0.4, 0.6)])
        xl = tx("return on capital, 2015-2019 average", 17, GREY_B).next_to(ax, DOWN, buff=0.4)
        yl = tx("2022-2026 average", 17, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.7, 0.7), stroke_color=GREY_C, stroke_width=1.5)
        diag_t = tx("no change", 15, GREY_C).rotate(PI / 4).move_to(ax.c2p(0.6, 0.63))

        def clip(v):
            return max(min(v, 0.69), 0.0)
        pts = VGroup(*[Dot(ax.c2p(clip(a), clip(b)), radius=0.055, color=GOLD, fill_opacity=0.85) for _, a, b in P["pairs"]])
        q = R["persist"]
        stats = VGroup(tx(f"{q['n']} industries in both periods", 18, GREY_B),
                       tx(f"rank correlation: {q['rho']:.2f}", 26, GOLD, bold=True),
                       tx(f"top quarter: {100 * q['top_early']:.0f}% then {100 * q['top_late']:.0f}%", 20, RET),
                       tx(f"bottom quarter: {100 * q['bottom_early']:.0f}% then {100 * q['bottom_late']:.0f}%", 20, COST_),
                       tx(f"{q['still_top']} of the top {q['quartile']} are still in the top quarter", 18, WHITE)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.9, 0.2, 0])
        src = source("Damodaran, Excess Returns by industry, January files 2015-2024 and 2026; this film's averages")
        with self.voiceover(
            "Does it last? Damodaran has published the same table every January for years. "
            "<bookmark mark='a'/> Put each industry's average return from 2015 to 2019 along the bottom, and its "
            "average from 2022 to 2026 up the side. If returns were pure luck, the cloud would be round. If they "
            "never changed, every point would sit on the dashed line. <bookmark mark='b'/> It is neither. The rank "
            f"correlation is {q['rho']:.2f}: industries that earned a lot then mostly earn a lot now. "
            "<bookmark mark='c'/> The top quarter averaged thirty percent and still averages twenty-seven. "
            f"<bookmark mark='d'/> The bottom quarter has crept up, from five to ten. And {q['still_top']} of the "
            f"{q['quartile']} industries that were in the top quarter are still there. High returns fade, slowly, "
            "and some barely fade at all. Something is stopping the money from flooding in."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(diag_t))
            self.play(LaggedStart(*[FadeIn(p_, scale=1.8) for p_ in pts], lag_ratio=0.02), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(stats[2]))
            vo.wait_until("d")
            self.play(FadeIn(stats[3]), FadeIn(stats[4]))
        self.clear_scene()
