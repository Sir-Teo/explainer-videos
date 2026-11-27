from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

COLS = {"APH": "#7EC8F5", "TEL": "#7BD88F", "GLW": "#F6C453", "ASX": "#B58CFF", "LPL": "#E8554E"}
WHAT = {"APH": "connectors, sensors", "TEL": "connectors, sensors", "GLW": "glass: phone covers, fibre", "ASX": "chip packaging and test",
        "LPL": "display panels"}


class Components(VoiceoverScene):
    def construct(self):
        card(self, 7, "Components with moats", "Which parts of a device make money for their makers?",
             "Chapter seven. Components with moats.", lit=("moat", "change"))
        self.margins()
        self.sole()
        self.squeeze()

    def margins(self):
        M = R["components"]["margins"]
        pa = viz.plot_axes([2012, 2025], [-0.16, 0.22], x_length=8.4, y_length=4.6, xticks=[2013, 2016, 2019, 2022, 2025],
                           yticks=[-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue", size=13).move_to([-1.4, -0.4, 0])
        zero = DashedLine(pa.ax.c2p(2012, 0), pa.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.2, dash_length=0.08)
        lines, labs = {}, VGroup()
        for tk, col in COLS.items():
            pts = sorted((y, max(min(v, 0.22), -0.16)) for y, v in M[tk].items())
            lines[tk] = poly(pa, pts, col, 3.5)
            labs.add(VGroup(tx(NAMES[tk], 14, col, bold=True), tx(WHAT[tk], 11, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.02))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.8, 0.2, 0])
        steady = [lines[k] for k in ("APH", "TEL", "GLW", "ASX")]
        lpl = M["LPL"]
        bad = [y for y, v in sorted(lpl.items()) if v < 0]
        streak = max(lpl)
        while streak - 1 in lpl and lpl[streak - 1] < 0:
            streak -= 1
        src = source("SEC EDGAR: Forms 10-K of Amphenol, TE Connectivity and Corning; Forms 20-F of ASE (NT$) and LG Display (won)", size=13)
        with self.voiceover(
            "The left end of the smile is crowded too, and not every part pays. <bookmark mark='a'/> Amphenol and TE "
            "Connectivity make connectors and sensors: thousands of small, specified parts that a design engineer picks once "
            "and rarely changes. In most years they have kept ten to twenty cents in the dollar. Corning, the glass "
            "maker, and ASE, which packages and tests chips, a little less. <bookmark mark='b'/> Then displays. LG Display "
            f"makes panels for televisions, laptops and phones, in factories that cost billions. It lost money in "
            f"{len(bad)} of the {len(lpl)} years shown, and in every year from {streak} to {max(lpl)}. A screen is a commodity "
            "bought by the square metre, made "
            "in plants that keep running when prices fall: the memory cycle, again."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(src), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in steady], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(lines["LPL"]), run_time=2.0)
            self.play(Indicate(labs[4], color=BAD, scale_factor=1.05))
        self.clear_scene()

    def sole(self):
        phone = draw.phone(3.0, screen="#1B2230").move_to([-3.6, -0.3, 0])
        parts = [("processor", "#B58CFF"), ("memory", "#F2A65A"), ("display", "#7EC8F5"), ("camera", "#9AA3B2"),
                 ("battery", "#7BD88F"), ("modem", "#E8554E"), ("glass", "#C9D3E0"), ("connectors", "#F6C453")]
        chips = VGroup()
        for i, (name, col) in enumerate(parts):
            r_, c_ = divmod(i, 2)
            box = RoundedRectangle(corner_radius=0.05, width=1.7, height=0.5, stroke_color=col, stroke_width=2, fill_color="#151A23", fill_opacity=1)
            chips.add(VGroup(box, tx(name, 14, col, bold=True).move_to(box)).move_to([-0.4 + c_ * 1.95, 1.8 - r_ * 0.72, 0]))
        quote = VGroup(tx("'Although most components essential to the Company's", 14, WHITE),
                       tx("business are generally available from multiple sources,", 14, WHITE),
                       tx("certain components are currently obtained from single", 14, WHITE),
                       tx("or limited sources.'", 14, WHITE),
                       tx("'...supply constraints and rising costs ... for key components,", 14, PRICE),
                       tx("including advanced semiconductors, memory and storage.'", 14, PRICE),
                       tx("Apple, Form 10-K, fiscal 2026", 12, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([1.6, -1.9, 0])
        src = source("Apple, Form 10-K FY2026 (Item 1A, risk factors)", size=13)
        with self.voiceover(
            "What makes a part pay is whether it can be replaced. <bookmark mark='a'/> A phone holds a processor, memory, a "
            "screen, cameras, a battery, a modem, glass and connectors. <bookmark mark='b'/> Apple's annual report says most "
            "of its components are available from more than one source, but that certain ones come from a single source "
            "or a few. <bookmark mark='c'/> And in 2026 it reported supply constraints and rising costs for advanced chips, "
            "memory and storage: the part makers' turn to set the price. The left end of the smile belongs to whoever "
            "makes a part nobody else can."
        ) as vo:
            self.play(FadeIn(src), FadeIn(phone), FadeIn(ghost(chips, quote, opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in chips], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(quote[:4], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(quote[4:], shift=UP * 0.1), Indicate(chips[0], color="#B58CFF"), Indicate(chips[1], color="#F2A65A"))
        self.clear_scene()

    def squeeze(self):
        C = R["components"]
        a, b = C["memory_share"]
        def pie(share, center, year):
            rest = Sector(radius=1.4, angle=TAU * (1 - share), start_angle=PI / 2 + TAU * share, fill_color=GREY_D, fill_opacity=0.8, stroke_width=0)
            mem = Sector(radius=1.4, angle=TAU * share, start_angle=PI / 2, fill_color="#F2A65A", fill_opacity=0.95, stroke_width=0)
            g = VGroup(rest, mem).move_to(center)
            lab = VGroup(tx(year, 18, WHITE, bold=True), tx(f"memory: {100 * share:.0f}% of the parts' cost", 15, "#F2A65A", bold=True)).arrange(
                DOWN, buff=0.05).next_to(g, DOWN, buff=0.25)
            return VGroup(g, lab)
        p25 = pie(a, [-3.0, 0.4, 0], "iPhone 17 Pro, 2025")
        p26 = pie(b, [3.0, 0.4, 0], "iPhone 18 Pro, 2026")
        rise = tx(f"parts cost of the newer phone: about +{100 * C['bom_rise']:.0f}%", 17, WHITE, bold=True).to_edge(DOWN, buff=0.75)
        tag = estimate_tag("TrendForce's estimates, as reported by MacRumors (August 2026)", corner=DR, size=12)
        src = source("TrendForce smartphone analysis, via MacRumors, 10 August 2026 (256GB iPhone Pro); Apple, Form 10-K FY2026", size=12)
        with self.voiceover(
            "In 2026 the part that set the price was memory, the boom of the semiconductors film. <bookmark mark='a'/> "
            "TrendForce, a market tracker, estimated that memory was about a tenth of the parts' cost of a top iPhone in "
            f"2025. <bookmark mark='b'/> For the 2026 model it put the share at about a third, {100 * b:.0f} per cent, and "
            f"the parts' cost about {100 * C['bom_rise']:.0f} per cent higher. These are a tracker's estimates, not Apple's "
            "figures; Apple's own report says only that memory costs rose. When a component is scarce, its maker can raise "
            "its price, even to the most powerful buyer."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tag), FadeIn(p25[0][0]), FadeIn(p26[0][0]), FadeIn(p25[1][0]), FadeIn(p26[1][0]))
            vo.wait_until("a")
            self.play(Create(p25[0][1]), FadeIn(p25[1][1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(p26[0][1]), FadeIn(p26[1][1]), run_time=1.5)
            self.play(FadeIn(rise, shift=UP * 0.1))
        self.clear_scene()
