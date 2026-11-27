from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

SEG = [("parts cost", "parts: their makers' costs", PARTS, 0.45), ("parts profit", "parts: their makers' profit", PARTS, 1.0),
       ("assembler", "assembly and test", ASSEMBLER, 1.0), ("brand costs", "the brand's design, software, marketing", BRAND, 0.45),
       ("brand profit", "the brand's profit", BRAND, 1.0)]


class Dollar(VoiceoverScene):
    def construct(self):
        card(self, 3, "Where the device's dollar goes", "Of the price of a device, who keeps what?",
             "Chapter three. Where the device's dollar goes.", lit=("dollar",))
        self.split()
        self.cheap()
        self.real()

    def split(self):
        D, G = R["dollar"], R["run"]
        sp = D["split"]
        W = 11.6
        x = -W / 2
        segs, labs = VGroup(), VGroup()
        for i, (k, name, col, op) in enumerate(SEG):
            w = W * sp[k] / D["price"]
            r_ = Rectangle(width=w, height=0.9, stroke_color=BG if "BG" in globals() else "#0E1117", stroke_width=2, fill_color=col, fill_opacity=op).move_to(
                [x + w / 2, 1.6, 0])
            segs.add(r_)
            lab = VGroup(tx(f"${sp[k]:.0f}", 18 if w > 1 else 14, WHITE, bold=True), tx(name, 12, GREY_A)).arrange(DOWN, buff=0.04)
            lab.next_to(r_, DOWN if i % 2 == 0 else UP, buff=0.12)
            if lab.width > 2.4:
                lab.scale_to_fit_width(2.4)
            labs.add(lab)
            x += w
        head = tx(f"A ${D['price']:.0f} device, as the Works build it", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        # profit kept by each link, as a share of the price: the smile, from the numbers
        per_unit_fixed = G["fixed"] * 1e6 / G["units"]
        asm_profit = D["fee"] - G["labour"] - G["other"] - per_unit_fixed
        kept = [("parts makers", sp["parts profit"], PARTS), ("assembler", asm_profit, ASSEMBLER), ("brand", sp["brand profit"], BRAND)]
        base_y, sc = -2.6, 0.006
        pts = []
        dots, dl = VGroup(), VGroup()
        for i, (name, v, col) in enumerate(kept):
            px = -4.0 + 4.0 * i
            py = base_y + v * sc
            pts.append([px, py, 0])
            dots.add(Dot([px, py, 0], radius=0.12, color=col))
            dl.add(VGroup(tx(name, 15, col, bold=True), tx(f"keeps ${v:.0f} ({100 * v / D['price']:.1f}%)", 14, WHITE)).arrange(DOWN, buff=0.03).next_to(
                dots[-1], DOWN if i == 1 else (LEFT if i == 0 else RIGHT), buff=0.15))
        curve = VMobject(stroke_color=PRICE, stroke_width=4, fill_opacity=0).set_points_smoothly(pts)
        floor = Line([-5.5, base_y, 0], [5.5, base_y, 0], stroke_color=GREY_B, stroke_width=1.5)
        tag = estimate_tag("the Works' device: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            f"Follow the money from a ${D['price']:.0f} device, built by the Works in round numbers. <bookmark mark='a'/> "
            f"About ${D['bom']:.0f} buys the parts: the chips, the screen, the battery, the cameras, the case. Their makers "
            f"keep perhaps a quarter of that, ${sp['parts profit']:.0f}. <bookmark mark='b'/> The assembler is paid "
            f"${D['fee']:.0f} for putting it together and testing it. <bookmark mark='c'/> The brand spends about "
            f"${sp['brand costs']:.0f} a device on design, software, marketing and selling, and keeps the rest, "
            f"${sp['brand profit']:.0f}. <bookmark mark='d'/> Now plot what each link keeps. The parts makers, about "
            f"${sp['parts profit']:.0f}; the assembler, after paying for its people and its plant, about ${asm_profit:.0f}; "
            f"the brand, ${sp['brand profit']:.0f}. Shih's smile, from the arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ghost(segs, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(segs[0], LEFT), GrowFromEdge(segs[1], LEFT), FadeIn(labs[0]), FadeIn(labs[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(segs[2], LEFT), FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(segs[3], LEFT), GrowFromEdge(segs[4], LEFT), FadeIn(labs[3]), FadeIn(labs[4]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(floor), LaggedStart(*[AnimationGroup(GrowFromCenter(d_), FadeIn(l_)) for d_, l_ in zip(dots, dl)], lag_ratio=0.4), run_time=2.0)
            self.play(Create(curve), run_time=1.5)
        self.clear_scene()

    def real(self):
        B, C = R["brand"], R["contract"]
        L = {c["ticker"]: c for c in R["landscape"]["companies"]}
        comp = R["components"]["margins"]
        groups = [("components", [("APH", comp["APH"][2025]), ("TEL", comp["TEL"][2025]), ("GLW", comp["GLW"][2025])], PARTS),
                  ("assemblers", [("HONHAI", C["margins"]["HONHAI"][2025]), ("JBL", C["margins"]["JBL"][2025]),
                                  ("FLEX", C["margins"]["FLEX"][2025])], ASSEMBLER),
                  ("brands", [("AAPL", B["ni"] / B["rev"]), ("LOGI", B["margins"]["LOGI"][max(B["margins"]["LOGI"])]),
                              ("HPQ", B["margins"]["HPQ"][2025]), ("DELL", B["margins"]["DELL"][max(B["margins"]["DELL"])])], BRAND)]
        pa = viz.plot_axes([0, 3], [0, 0.3], x_length=9.0, y_length=4.6, xticks=[], yticks=[0, 0.1, 0.2, 0.3],
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="net income per dollar of revenue, latest year", size=13).move_to([-0.8, -0.4, 0])
        cols_g = VGroup()
        for gi, (gname, items, col) in enumerate(groups):
            g = VGroup()
            for j, (tk, m) in enumerate(items):
                x = gi + 0.5 + (j - (len(items) - 1) / 2) * 0.22
                d_ = Dot(pa.ax.c2p(x, max(m, 0)), radius=0.1, color=col)
                lab = tx(NAMES[tk].replace(" (Foxconn)", ""), 12, col, bold=True).next_to(d_, RIGHT, buff=0.06)
                g.add(VGroup(d_, lab))
            gl = tx(gname, 16, col, bold=True).move_to([pa.ax.c2p(gi + 0.5, 0)[0], pa.ax.c2p(0, 0)[1] - 0.35, 0])
            cols_g.add(VGroup(gl, g))
        # spread labels within each group vertically if crowded
        for grp in cols_g:
            labs_ = [it[1] for it in grp[1]]
            labs_.sort(key=lambda m: m.get_center()[1])
            for a_, b_ in zip(labs_, labs_[1:]):
                if b_.get_bottom()[1] < a_.get_top()[1] + 0.04:
                    b_.shift(UP * (a_.get_top()[1] + 0.04 - b_.get_bottom()[1]))
        smile_pts = [pa.ax.c2p(0.5, comp["APH"][2025]), pa.ax.c2p(1.5, C["margins"]["HONHAI"][2025]), pa.ax.c2p(2.5, B["ni"] / B["rev"])]
        curve = VMobject(stroke_color=PRICE, stroke_width=3, fill_opacity=0).set_points_smoothly(smile_pts)
        curve.set_stroke(opacity=0.6)
        src = source("SEC EDGAR: Forms 10-K of Amphenol, TE Connectivity, Corning, Jabil, Flex, Apple, Logitech, HP and Dell; Hon Hai, "
                     "audited statements 2025", size=12)
        with self.voiceover(
            "And in real accounts? <bookmark mark='a'/> Three makers of components: Amphenol, which makes connectors, kept "
            f"about {100 * comp['APH'][2025]:.0f} cents of every dollar in 2025; TE Connectivity about "
            f"{100 * comp['TEL'][2025]:.0f}; Corning, the glass maker, about {100 * comp['GLW'][2025]:.0f}. "
            "<bookmark mark='b'/> Three assemblers: Hon Hai, Jabil and Flex, two to three cents each. "
            f"<bookmark mark='c'/> And the brands: Apple, {100 * B['ni'] / B['rev']:.0f} cents. <bookmark mark='d'/> But "
            "not every brand sits on the high end. HP and Dell, whose personal computers are built from the same standard "
            "parts as everyone else's, keep only a few cents. The right end of the smile is for brands that own something "
            "others cannot copy."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), *[FadeIn(cg[0]) for cg in cols_g])
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(it) for it in cols_g[0][1]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(it) for it in cols_g[1][1]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromCenter(cols_g[2][1][0]), Create(curve), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(it) for it in cols_g[2][1][1:]], lag_ratio=0.3), run_time=1.5)
        self.clear_scene()

    def cheap(self):
        D = R["dollar"]
        rows = [(D["price"], D["split"], "the Works' $900 device"), (D["cheap"]["price"], D["cheap"]["split"], "the Works' $300 device")]
        W = 11.0
        bars = VGroup()
        for i, (price, sp, name) in enumerate(rows):
            y = 1.4 - 2.6 * i
            x = -W / 2
            g = VGroup()
            for k, label, col, op in SEG:
                w = W * sp[k] / price
                r_ = Rectangle(width=w, height=0.8, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=op).move_to([x + w / 2, y, 0])
                g.add(r_)
                x += w
            head = tx(name, 17, WHITE, bold=True).next_to(g, UP, buff=0.1).align_to(g, LEFT)
            kept = tx(f"the brand keeps ${sp['brand profit']:.0f}: {100 * sp['brand profit'] / price:.0f}% of the price", 16, BRAND, bold=True).next_to(
                g, DOWN, buff=0.12).align_to(g, LEFT)
            bars.add(VGroup(g, head, kept))
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=col, fill_opacity=op), tx(lab_, 12, GREY_A)).arrange(RIGHT, buff=0.06)
                       for k, lab_, col, op in SEG]).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.75)
        tag = estimate_tag("the Works' devices: illustrations in round numbers", corner=DR, size=12)
        c = D["cheap"]
        with self.voiceover(
            "Not every brand sits on that right end. <bookmark mark='a'/> Take a cheaper phone from the Works: "
            f"${c['price']:.0f}, with ${c['bom']:.0f} of parts, a ${c['fee']:.0f} assembly fee and ${c['brand_costs']:.0f} of "
            "the brand's own costs. <bookmark mark='b'/> The parts are most of the price, and the brand keeps "
            f"${c['split']['brand profit']:.0f}, {100 * c['split']['brand profit'] / c['price']:.0f} per cent, against "
            f"{100 * D['split']['brand profit'] / D['price']:.0f} per cent on the dearer device. A brand that cannot charge "
            "much more than its parts cost sits nearly as low as its assembler."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(key), FadeIn(bars[0]), FadeIn(bars[1][1]), FadeIn(ghost(bars[1][0], opacity=0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_, LEFT) for r_ in bars[1][0]], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bars[1][2], shift=UP * 0.1), Indicate(bars[1][0][4], color=BRAND, scale_factor=1.1))
        self.clear_scene()
