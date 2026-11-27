from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Tonne(VoiceoverScene):
    def construct(self):
        card(self, 3, "A ton of steel and its dollar", "What does a ton of steel sell for, and where does the money go?",
             "Chapter three. A ton of steel and its dollar.", lit=("unit", "dollar"))
        self.ton()
        self.spread()
        self.integrated()
        self.century()

    def ton(self):
        T_ = R["tonne"]
        p, m = T_["p25"], T_["m25"]
        H = 5.0
        base = -2.6
        bar_m = Rectangle(width=1.6, height=H * m / p, stroke_width=0, fill_color=SCRAP, fill_opacity=0.9).move_to(
            [-1.5, base, 0], aligned_edge=DOWN)
        bar_r = Rectangle(width=1.6, height=H * (p - m) / p, stroke_width=0, fill_color=PRICE, fill_opacity=0.85).next_to(
            bar_m, UP, buff=0)
        outline = Rectangle(width=1.6, height=H, stroke_color=WHITE, stroke_width=2).move_to([-1.5, base, 0], aligned_edge=DOWN)
        top = tx(f"${p:,.0f}", 30, WHITE, bold=True).next_to(outline, UP, buff=0.1)
        lm = VGroup(tx(f"${m:,.0f}", 24, SCRAP, bold=True), tx(f"the scrap: {get('nucor.scrap.per_ton'):.1f} gross tons", 15, GREY_A),
                    tx(f"at ${T_['s25']:.0f} a gross ton", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(
            bar_m, RIGHT, buff=0.3)
        lr = VGroup(tx(f"${p - m:,.0f}", 24, PRICE, bold=True), tx("the 'metal spread': it pays for power, electrodes,", 15, GREY_A),
                    tx("alloys, wages, upkeep, depreciation and profit", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.04).next_to(bar_r, RIGHT,
                                                                                                               buff=0.3)
        coil = draw.coil(0.9).move_to([-5.0, 0.0, 0])
        cl = VGroup(tx("A ton of steel", 22, WHITE, bold=True), tx("from Nucor's mills, 2025", 16, GREY_A)).arrange(
            DOWN, buff=0.05).next_to(coil, DOWN, buff=0.2)
        note = tx("a ton here is a US short ton, 2,000 lb (907 kg); a gross ton of scrap is 2,240 lb", 13, GREY_B).to_edge(
            DOWN, buff=0.75)
        src = source("Nucor Corporation, Form 10-K 2025: average sales price per ton, steel mills segment; average cost "
                     "of scrap and scrap substitutes", size=13)
        with self.voiceover(
            "Take a ton of steel from Nucor, America's largest steelmaker, which makes all of it in electric furnaces. "
            f"<bookmark mark='a'/> In 2025, its mills sold steel for {p:,.0f} dollars a ton on average. "
            f"<bookmark mark='b'/> Each ton took about {get('nucor.scrap.per_ton'):.1f} tons of scrap, which cost "
            f"{T_['s25']:.0f} dollars a ton: about {m:.0f} dollars of metal in every ton sold. "
            f"<bookmark mark='c'/> The rest, about {p - m:.0f} dollars, is what the industry calls the metal spread. It "
            "has to pay for the electricity, the electrodes and alloys, the wages, the upkeep, the wear on the plant, "
            "and then, if anything is left, the profit. A steelmaker is a business that buys metal, adds heat and "
            "know-how, and lives on the spread."
        ) as vo:
            self.play(FadeIn(coil), FadeIn(cl), FadeIn(src), FadeIn(note))
            vo.wait_until("a")
            self.play(Create(outline), FadeIn(top))
            vo.wait_until("b")
            self.play(GrowFromEdge(bar_m, DOWN), FadeIn(lm), run_time=1.2)
            vo.wait_until("c")
            self.play(GrowFromEdge(bar_r, DOWN), FadeIn(lr), run_time=1.2)
        self.clear_scene()

    def spread(self):
        T_ = R["tonne"]
        ys = sorted(T_["price"])
        pa = viz.plot_axes([2017.6, 2025.4], [0, 1450], x_length=8.0, y_length=4.4, xticks=ys, yticks=[0, 500, 1000],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}", size=13).move_to([-1.6, -0.3, 0])
        pl = VMobject(stroke_color=PRICE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, T_["price"][y]) for y in ys])
        ml = VMobject(stroke_color=SCRAP, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, T_["metal"][y]) for y in ys])
        area = Polygon(*[pa.ax.c2p(y, T_["price"][y]) for y in ys], *[pa.ax.c2p(y, T_["metal"][y]) for y in reversed(ys)],
                       stroke_width=0, fill_color=PRICE, fill_opacity=0.18)
        lp = tx("steel price a ton", 15, PRICE, bold=True).next_to(pa.ax.c2p(2022, T_["price"][2022]), UP, buff=0.1)
        lm = tx("scrap in a ton", 15, SCRAP, bold=True).next_to(pa.ax.c2p(2019, T_["metal"][2019]), DOWN, buff=0.15)
        sp = {y: T_["spread"][y] for y in ys}
        nets = R["mustrun"]["nets"]["NUE"]
        side = VGroup(tx("the spread, $ a ton", 16, WHITE, bold=True),
                      *[tx(f"{y}: ${sp[y]:,.0f}", 15, PRICE if y in (2021, 2022) else GREY_A) for y in ys]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.4, 0.6, 0])
        prof = VGroup(tx("Nucor's profit", 16, WHITE, bold=True),
                      tx(f"2020: ${nets[2020]:.1f}bn", 15, GREY_A), tx(f"2022: ${nets[2022]:.1f}bn", 15, GOOD, bold=True),
                      tx(f"2025: ${nets[2025]:.1f}bn", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).next_to(
            side, DOWN, buff=0.35).align_to(side, LEFT)
        src = source("Nucor Corporation, Forms 10-K 2019-2025 (steel mills segment price; scrap cost x 1.1, gross to short "
                     "tons); SEC company facts", size=13)
        with self.voiceover(
            "The spread moves a great deal. <bookmark mark='a'/> Here is Nucor's steel price, year by year since 2018, "
            "<bookmark mark='b'/> and the scrap in each ton. <bookmark mark='c'/> In 2020, with the pandemic, the "
            f"spread was about {sp[2020]:.0f} dollars. In 2021 and 2022, as the economy reopened and steel ran short, "
            f"prices rose far faster than scrap, and the spread more than doubled, to over {sp[2022]:.0f} dollars. "
            f"<bookmark mark='d'/> Nucor's profit went from {nets[2020]:.1f} billion dollars in 2020 to "
            f"{nets[2022]:.1f} billion in 2022, ten times as much, and back down to {nets[2025]:.1f} billion in 2025. A "
            "few hundred dollars of spread, on twenty-odd million tons, decides everything."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(pl), FadeIn(lp), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(ml), FadeIn(lm), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(area), FadeIn(side[0]), LaggedStart(*[FadeIn(t_) for t_ in side[1:]], lag_ratio=0.15), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(prof, shift=UP * 0.1))
        self.clear_scene()

    def integrated(self):
        T_ = R["tonne"]
        left = VGroup(draw.coil(0.6), tx("Nucor (electric furnaces)", 18, SCRAP, bold=True),
                      tx(f"${T_['p25']:,.0f} a ton", 28, WHITE, bold=True), tx("steel mills segment, 2025", 14, GREY_A),
                      tx(f"profit ${T_['nue_net']:.1f} billion", 20, GOOD, bold=True)).arrange(DOWN, buff=0.12).move_to(
            [-3.4, 0.4, 0])
        right = VGroup(draw.blast_furnace(1.4), tx("Cleveland-Cliffs (blast furnaces)", 18, ORE, bold=True),
                       tx(f"${T_['clf_asp']:,.0f} a ton", 28, WHITE, bold=True), tx("average steel product price, 2025", 14,
                                                                                     GREY_A),
                       tx(f"gross margin {T_['clf_margin']:.0f}%; loss ${abs(T_['clf_net']):.1f} billion", 20, BAD, bold=True)
                       ).arrange(DOWN, buff=0.12).move_to([3.4, 0.4, 0])
        vs = tx("vs", 30, GREY_B).move_to([0, 0.4, 0])
        hrc = VGroup(tx(f"The benchmark, hot-rolled coil: ${T_['hrc']:.0f} a ton in 2025, up from ${T_['hrc24']:.0f},", 17, PRICE),
                     tx("lifted by tariffs on imported steel, says Cliffs", 15, GREY_A)).arrange(DOWN, buff=0.05).to_edge(
            DOWN, buff=0.7)
        src = source("Nucor and Cleveland-Cliffs, Forms 10-K 2025; SEC company facts", size=13)
        with self.voiceover(
            "Now the same year for an integrated mill. <bookmark mark='a'/> Nucor sold its mills' steel at about "
            f"{T_['p25']:,.0f} dollars a ton and earned {T_['nue_net']:.1f} billion dollars. <bookmark mark='b'/> "
            f"Cleveland-Cliffs, with its blast furnaces, sold its steel for {T_['clf_asp']:,.0f} dollars a ton on "
            f"average, almost exactly the same price, and lost money on it before it paid a cent of interest: its "
            f"gross margin was minus {abs(T_['clf_margin']):.0f} per cent. <bookmark mark='c'/> And 2025 was not a bad "
            f"year for prices: the benchmark, hot-rolled coil, averaged {T_['hrc']:.0f} dollars, up from "
            f"{T_['hrc24']:.0f}, lifted, Cliffs says, by tariffs on imports. Same product, same price, opposite results. "
            "The difference is in the costs, and above all in the costs that do not go away."
        ) as vo:
            self.play(FadeIn(src), FadeIn(vs), FadeIn(left[:2]), FadeIn(right[:2]))
            vo.wait_until("a")
            self.play(FadeIn(left[2:], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(right[2:], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(hrc, shift=UP * 0.1))
        self.clear_scene()

    def century(self):
        T_ = R["tonne"]
        r = T_["real_ppi"]
        ys = sorted(r)
        pa = viz.plot_axes([1938, 2027], [0, 1.6], x_length=11.0, y_length=4.4, xticks=[1940, 1960, 1980, 2000, 2025],
                           yticks=[0.5, 1.0, 1.5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.1f}x",
                           ylabel="price of steel mill products after inflation (2025 = 1)", size=13).move_to([0, -0.4, 0])
        ln = VMobject(stroke_color=STEELC, stroke_width=3.2).set_points_as_corners([pa.ax.c2p(y, r[y]) for y in ys])
        one = DashedLine(pa.ax.c2p(1938, 1.0), pa.ax.c2p(2027, 1.0), stroke_color=PRICE, stroke_width=1.5, dash_length=0.08)
        pk = [y for y in (1974, 2008, 2021) if y in r]
        marks = VGroup(*[VGroup(Dot(pa.ax.c2p(y, r[y]), radius=0.05, color=WHITE),
                                tx(str(y), 13, WHITE).next_to(pa.ax.c2p(y, r[y]), UP, buff=0.08)) for y in pk])
        head = tx(f"The real price of steel since {ys[0]}", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("BLS producer price index for steel mill products (WPU1017) over the consumer price index (CPIAUCSL), "
                     "annual averages, via FRED", size=13)
        with self.voiceover(
            f"Step back and look at the price of steel since {ys[0]}, after taking out inflation. "
            "<bookmark mark='a'/> It spikes in booms: 1974, 2008, 2021. <bookmark mark='b'/> But over the long run it "
            f"goes nowhere: in 2025 a ton cost, in real terms, about what it did in 1960, when the index stood at "
            f"{r[1960]:.1f} times today's. Steelmakers have become far more productive, and almost none of it has "
            "turned into a higher price. Competition has handed it to the people who buy steel."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), Create(one))
            self.play(Create(ln), run_time=3.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m_, shift=DOWN * 0.1) for m_ in marks], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Indicate(one, color=PRICE), run_time=1.2)
        self.clear_scene()
