from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

COLS = {"TXN": "#7EC8F5", "ADI": "#7BD88F", "NXPI": "#B58CFF", "MCHP": "#F6C453", "ON": "#F2A65A", "STM": "#E8554E"}


class Trailing(VoiceoverScene):
    def construct(self):
        card(self, 9, "Analog, power and the trailing edge", "What about the chips that are not at the frontier?",
             "Chapter nine. Analog, power and the trailing edge.", lit=("make", "change"))
        self.shortage()
        self.margins()

    def shortage(self):
        T = R["trailing"]
        car = draw.car(4.6, "#9AA3B2").move_to([-3.3, 0.9, 0])
        # where the chips go: engine, lights, dashboard, seats, brakes, battery, mirrors, windows
        spots = [(0.38, 0.16, "engine"), (0.47, 0.13, "lights"), (0.1, 0.27, "dashboard"), (-0.18, 0.2, "seats"),
                 (0.3, 0.06, "brakes"), (-0.38, 0.14, "battery"), (0.16, 0.26, "mirrors"), (-0.3, 0.06, "brakes")]
        x0, y0 = car.get_left()[0], car.get_bottom()[1]
        chips = VGroup(*[draw.chip(0.26) for _ in spots]).arrange_in_grid(rows=1, buff=0.18).move_to([-3.3, -1.6, 0])
        targets = [np.array([x0 + (fx + 0.5) * 4.6, y0 + fy * 4.6, 0]) for fx, fy, _ in spots]
        jobs = VGroup(*[tx(j, 12, GREY_B) for j in ("power", "sensing", "display", "motors", "braking", "charging")]).arrange(
            RIGHT, buff=0.22).move_to([-3.3, -2.25, 0])
        chips.set_z_index(3)
        holes = VGroup(*[DashedVMobject(Square(0.24, stroke_color=BAD, stroke_width=2.5), num_dashes=8).move_to(t) for t in targets]).set_z_index(4)
        quote = VGroup(tx("'The impact on production in 2021 due to the", 16, WHITE), tx("ongoing semiconductor supply shortage exceeded", 16, WHITE),
                       tx("the impact of production suspensions in 2020", 16, WHITE), tx("due to the COVID-19 pandemic.'", 16, WHITE),
                       tx("General Motors, annual report for 2021", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([2.6, 1.2, 0])
        mature = VGroup(tx(f"TSMC, 2025: {T['mature']:.0f}% of wafer revenue still from", 16, GREY_A),
                        tx("processes of 28 nanometres and older", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([2.6, -1.4, 0])
        src = source("General Motors, Form 10-K 2021; TSMC, Form 20-F 2025 (wafer revenue by technology)", size=13)
        with self.voiceover(
            "Most chips are not at the frontier at all. The chips that manage power, read sensors and convert signals "
            "are made on older, cheaper processes, and sold for years. <bookmark mark='a'/> A car is full of them. "
            "<bookmark mark='b'/> In 2021, when they ran short, General Motors told its shareholders that the chip "
            "shortage cost it more production than the pandemic shutdowns of 2020 had. <bookmark mark='c'/> Even at TSMC, "
            f"about {T['mature']:.0f} per cent of wafer revenue in 2025 still came from processes of 28 nanometres and older: "
            "fabs whose machines were written off long ago, making chips that do not need to be the smallest."
        ) as vo:
            self.play(FadeIn(src), FadeIn(ghost(car, quote)), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.08))
            self.play(FadeIn(jobs))
            vo.wait_until("a")
            self.play(FadeIn(car))
            self.play(LaggedStart(*[c.animate.scale(0.6).move_to(t) for c, t in zip(chips, targets)], lag_ratio=0.12), run_time=2.2)
            vo.wait_until("b")
            self.play(FadeIn(quote, shift=LEFT * 0.1), *[c.animate.set_opacity(0.15) for c in chips], FadeIn(holes), jobs.animate.set_opacity(0.3))
            vo.wait_until("c")
            self.play(FadeIn(mature, shift=UP * 0.1))
        self.clear_scene()

    def margins(self):
        T = R["trailing"]["margins"]
        pa = viz.plot_axes([2015, 2025], [-0.05, 0.45], x_length=8.4, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[0, 0.1, 0.2, 0.3, 0.4], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="net income per dollar of revenue", size=13).move_to([-1.4, -0.4, 0])
        lines, labs = VGroup(), VGroup()
        for tk, col in COLS.items():
            pts = sorted((y, v) for y, v in T[tk].items() if 2015 <= y <= 2025)
            lines.add(poly(pa, pts, col, 3.5))
            labs.add(tx(NAMES[tk], 14, col, bold=True).next_to(pa.ax.c2p(*pts[-1]), RIGHT, buff=0.1))
        # spread the end labels
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.0, 0])
        zero = DashedLine(pa.ax.c2p(2015, 0), pa.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.2, dash_length=0.08)
        band = Rectangle(width=pa.ax.c2p(2022.5, 0)[0] - pa.ax.c2p(2020.5, 0)[0], height=4.4, stroke_width=0, fill_color=PRICE, fill_opacity=0.08).move_to(
            [(pa.ax.c2p(2020.5, 0)[0] + pa.ax.c2p(2022.5, 0)[0]) / 2, pa.get_center()[1], 0])
        bl = tx("the shortage", 13, PRICE).next_to(band, UP, buff=0.05)
        txn = T["TXN"]
        py = max((y for y in txn if 2015 <= y <= 2025), key=lambda y: txn[y])
        peak = Dot(pa.ax.c2p(py, txn[py]), radius=0.08, color=COLS["TXN"])
        pl = tx(f"Texas Instruments, {py}: {100 * txn[py]:.0f}%", 14, COLS["TXN"], bold=True).next_to(peak, RIGHT, buff=0.15).shift(UP * 0.12)
        lows = [tk for tk in COLS if T[tk].get(2025, 1) < 0.03]
        lw = VGroup(*[Dot(pa.ax.c2p(2025, T[tk][2025]), radius=0.07, color=COLS[tk]) for tk in lows])
        ll = tx(f"2025: {len(lows)} of 6 kept under 3%", 14, WHITE, bold=True).next_to(pa.ax.c2p(2025, 0.01), RIGHT, buff=0.3)
        src = source("SEC EDGAR: Forms 10-K of Texas Instruments, Analog Devices, NXP, Microchip and onsemi; STMicroelectronics, "
                     "Forms 20-F (fiscal years)", size=13)
        with self.voiceover(
            "These are the companies that make them. <bookmark mark='a'/> Texas Instruments, Analog Devices, NXP, "
            "Microchip, onsemi and STMicroelectronics. Through the shortage years their margins swelled; Texas Instruments "
            f"kept {100 * txn[py]:.0f} cents in the dollar at the peak. <bookmark mark='b'/> Then demand from "
            "the carmakers and factories that buy their chips weakened, and by 2025 "
            f"{['none', 'one', 'two', 'three', 'four', 'five', 'six'][len(lows)]} of the six were keeping almost nothing. These are steady businesses compared with memory, but they have a cycle of their own, "
            "and it follows cars and factories, not AI."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(src), FadeIn(band), FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.15), FadeIn(labs), run_time=3.0)
            self.play(FadeIn(peak, scale=0.5), FadeIn(pl))
            vo.wait_until("b")
            self.play(Indicate(band, color=PRICE, scale_factor=1.0))
            self.play(FadeIn(lw, scale=0.5), FadeIn(ll))
        self.clear_scene()
