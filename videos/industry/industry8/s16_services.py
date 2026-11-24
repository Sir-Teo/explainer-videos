from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Services(VoiceoverScene):
    def construct(self):
        card(self, 14, "The drillers' drillers", "Who gets hit hardest when oil companies stop spending?",
             "Chapter fourteen. The drillers' drillers.", lit=("make", "change"))
        self.who()
        self.cycle()

    def who(self):
        crew = VGroup(draw.derrick(1.6, color=STONE), draw.truck(1.4, color="#E8554E"), draw.truck(1.4, color="#7EC8F5"),
                      draw.platform(1.8)).arrange(RIGHT, buff=1.2).move_to([0, 0.9, 0])
        labs = VGroup(tx("rigs and crews", 17, GREY_A), tx("fracking fleets", 17, GREY_A),
                      tx("logging, cementing", 17, GREY_A), tx("offshore equipment", 17, GREY_A))
        for l_, c_ in zip(labs, crew):
            l_.next_to(c_, DOWN, buff=0.2)
        names = VGroup(*[pill(n, color=WHITE, size=20) for n in ("SLB (formerly Schlumberger)", "Halliburton", "Baker Hughes")]
                       ).arrange(RIGHT, buff=0.4).move_to([0, -1.9, 0])
        src = source("company descriptions from their Forms 10-K", size=13)
        with self.voiceover(
            "Oil companies decide where to drill. Mostly, other companies do the drilling. "
            "<bookmark mark='a'/> They rent out rigs and crews, pump the water and sand that crack the shale, measure "
            "the rock as the bit goes down, cement the wells, and build the equipment for the sea floor. "
            "<bookmark mark='b'/> The biggest are SLB, which used to be called Schlumberger, Halliburton, and Baker "
            "Hughes. Their customers' spending is their revenue, and their customers' spending is the first thing to "
            "be cut when the price falls."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c_, shift=UP * 0.2), FadeIn(l_)) for c_, l_ in zip(crew, labs)],
                                  lag_ratio=0.3), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_, scale=0.9) for n_ in names], lag_ratio=0.2))
        self.clear_scene()

    def cycle(self):
        C = R["companies"]
        U = R["us"]
        ms = U["months"]
        ys = list(range(2012, 2026))

        def avg_rigs(y):
            v = [U["rigs"][k] for k, m in enumerate(ms) if m.startswith(str(y)) and U["rigs"][k] is not None]
            return sum(v) / len(v)
        idx = {"rigs": [100 * avg_rigs(y) / avg_rigs(2014) for y in ys],
               "HAL": [100 * C["HAL"]["revenue"][y] / C["HAL"]["revenue"][2014] for y in ys],
               "SLB": [100 * C["SLB"]["revenue"][y] / C["SLB"]["revenue"][2014] for y in ys],
               "XOM": [100 * C["XOM"]["capex"][y] / C["XOM"]["capex"][2014] for y in ys]}
        pa = viz.plot_axes([2011.6, 2025.6], [0, 120], x_length=8.4, y_length=4.2, xticks=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}", size=14)
        pa.move_to([-0.8, -0.5, 0])
        cols = {"rigs": STATE, "HAL": PRICE, "SLB": BRENT, "XOM": GREY_B}
        names = {"rigs": "US oil rigs", "HAL": "Halliburton revenue", "SLB": "SLB revenue", "XOM": "ExxonMobil capital spending"}
        lines = {k: VMobject(stroke_color=cols[k], stroke_width=4 if k != "XOM" else 2.5).set_points_as_corners(
            [pa.ax.c2p(y, v) for y, v in zip(ys, idx[k])]) for k in idx}
        key_ = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.3, stroke_color=cols[k], stroke_width=4), tx(names[k], 14, cols[k])).arrange(
            RIGHT, buff=0.1) for k in ("rigs", "HAL", "SLB", "XOM")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.5)
        head = tx("Each as a share of its 2014 level", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        hal = tx(f"Halliburton: {100 * C['hal_fall']:.0f}% in two years, a ${-C['HAL']['net'][2016]:.1f}bn loss in 2016", 17,
                 PRICE, bold=True).move_to([0.6, -2.95, 0])
        src = source("EIA, crude oil rigs (Baker Hughes); Halliburton, SLB and ExxonMobil, Forms 10-K (SEC company facts)",
                     size=13)
        with self.voiceover(
            "Here is the 2014 bust from their side. <bookmark mark='a'/> The number of oil rigs working in America fell "
            "by almost three-quarters in two years. <bookmark mark='b'/> Halliburton's revenue fell by "
            f"{abs(100 * C['hal_fall']):.0f} percent, and SLB's by {abs(100 * C['slb_fall']):.0f}. In 2016 Halliburton "
            f"lost {-C['HAL']['net'][2016]:.1f} billion dollars. <bookmark mark='c'/> And in 2020 it happened again. "
            "<bookmark mark='d'/> Compare ExxonMobil's own capital spending, in grey: it fell too, but its business "
            "kept producing and selling oil from the wells it already had. A service company's business is the new "
            "wells. Part 6's accelerator works here as it does for the makers of machines: a fall in spending on new "
            "capacity hits hardest the companies that sell it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), FadeIn(key_))
            vo.wait_until("a")
            self.play(Create(lines["rigs"]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines["HAL"]), Create(lines["SLB"]), run_time=2.0)
            self.play(FadeIn(hal))
            vo.wait_until("c")
            self.play(Indicate(lines["rigs"], color=WHITE))
            vo.wait_until("d")
            self.play(Create(lines["XOM"]), run_time=1.6)
        self.clear_scene()
