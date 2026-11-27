from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.output()
        self.transistors()

    def output(self):
        H = R["history"]
        ip = H["ip"]
        rp = H["real_ppi"]
        ys = [y for y in sorted(ip) if y <= 2025]
        pa = viz.plot_axes([1967, 2026], [-2, 4], x_length=10.4, y_length=4.6, xticks=[1970, 1980, 1990, 2000, 2010, 2020, 2025],
                           yticks=[-2, -1, 0, 1, 2, 3, 4], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{10 ** v:,g}",
                           ylabel="index, first year = 1 (log scale)", size=13).move_to([-0.6, -0.6, 0])
        one = DashedLine(pa.ax.c2p(1967, 0), pa.ax.c2p(2026, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        lo = poly(pa, [(y, np.log10(ip[y] / ip[ys[0]])) for y in ys], GOOD, 4)
        ry = [y for y in sorted(rp) if y <= 2025]
        lp = poly(pa, [(y, np.log10(rp[y])) for y in ry], BAD, 4)
        lab_o = tx(f"US output of semiconductors: x{H['ip_x']:,.0f} since 1972", 16, GOOD, bold=True).next_to(pa.ax.c2p(2025, np.log10(ip[2025] / ip[ys[0]])), LEFT, buff=0.3).shift(DOWN * 0.7)
        lab_p = tx(f"their producer price, after inflation: down {100 * H['real_fall']:.0f}% since 1967", 16, BAD, bold=True).next_to(pa.ax.c2p(2025, np.log10(rp[2025])), LEFT, buff=0.2).shift(DOWN * 0.3)
        head = tx("Intermission: fifty years of cheaper chips", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Federal Reserve, industrial production of semiconductors and other electronic components (IPG3344S); BLS, PPI for "
                     "semiconductor and related devices (PCU334413334413), divided by the CPI", size=13)
        with self.voiceover(
            "An intermission, and two lines from America's official statistics. <bookmark mark='a'/> The Federal "
            "Reserve's index of American output of semiconductors and other electronic components: about "
            f"{H['ip_x']:,.0f} times as much in 2025 as in 1972. "
            "<bookmark mark='b'/> And the government's producer price index for semiconductors, after allowing for "
            f"inflation: down about {100 * H['real_fall']:.0f} per cent since 1967. In money that is not adjusted for "
            f"inflation it fell by {100 * H['ppi_fall']:.0f} per cent, while prices in general rose about "
            f"{H['cpi_x']:.0f} times."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(one), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lo), run_time=3.5)
            self.play(FadeIn(lab_o))
            vo.wait_until("b")
            self.play(Create(lp), run_time=3.5)
            self.play(FadeIn(lab_p))
        self.clear_scene()

    def transistors(self):
        H = R["history"]
        tr = H["transistors"]
        ys = sorted(tr)
        pa = viz.plot_axes([1970, 2022], [3, 11], x_length=10.0, y_length=4.8, xticks=[1971, 1980, 1990, 2000, 2010, 2021],
                           yticks=[3, 5, 7, 9, 11], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{10 ** v:,.0f}",
                           ylabel="transistors on a microprocessor (log scale)", size=13).move_to([-0.6, -0.4, 0])
        dots = VGroup(*[Dot(pa.ax.c2p(y, np.log10(tr[y])), radius=0.06, color=LIGHT) for y in ys])
        y0 = ys[0]
        moore = DashedLine(pa.ax.c2p(y0, np.log10(tr[y0])), pa.ax.c2p(2021, np.log10(tr[y0]) + (2021 - y0) / 2 * np.log10(2)),
                           stroke_color=PRICE, stroke_width=3, dash_length=0.1)
        ml = tx("doubling every two years (Moore, 1975)", 15, PRICE, bold=True).next_to(moore.get_end(), LEFT, buff=0.2).shift(UP * 0.35)
        a = tx(f"{y0}: {tr[y0]:,.0f}", 15, WHITE, bold=True).next_to(dots[0], UP, buff=0.12)
        b = tx(f"{ys[-1]}: {tr[ys[-1]] / 1e9:.1f} billion", 15, WHITE, bold=True).next_to(dots[-1], DOWN, buff=0.15).shift(LEFT * 0.6)
        src = source("Karl Rupp, Microprocessor Trend Data (2022), via Our World in Data; G. E. Moore, IEDM 1975", size=13)
        with self.voiceover(
            "And here is Moore's law itself. <bookmark mark='a'/> The number of transistors on a microprocessor, from "
            f"about {tr[y0]:,.0f} in {y0} to about {tr[ys[-1]] / 1e9:.0f} billion in {ys[-1]}. <bookmark mark='b'/> In "
            "1975 Moore had revised his forecast to a doubling every two years. Over the next half-century the counts "
            f"doubled about every {H['doubling']:.1f} years. The forecast held for half a century, because an industry "
            "spent ever more money to keep it true."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03), run_time=3.0)
            self.play(FadeIn(a), FadeIn(b))
            vo.wait_until("b")
            self.play(Create(moore), FadeIn(ml), run_time=2.0)
        self.clear_scene()
