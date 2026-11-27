from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.tv()
        self.others()
        self.output()

    def tv(self):
        H = R["history"]
        tv, al = H["tv"], H["all"]
        ys = sorted(y for y in tv if y in al and y <= 2025)
        y0 = ys[0]
        pa = viz.plot_axes([1950, 2026], [-3, 1.5], x_length=10.2, y_length=4.6, xticks=[1951, 1970, 1990, 2010, 2025],
                           yticks=[-3, -2, -1, 0, 1], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{10 ** v:g}",
                           ylabel=f"price index, {y0} = 1 (log scale)", size=13).move_to([-0.6, -0.6, 0])
        one = DashedLine(pa.ax.c2p(1950, 0), pa.ax.c2p(2026, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        la = poly(pa, [(y, np.log10(al[y] / al[y0])) for y in ys], GREY_A, 4)
        lt = poly(pa, [(y, np.log10(tv[y] / tv[y0])) for y in ys], PARTS, 4)
        lab_a = tx(f"all consumer prices: x{H['cpi_x']:.1f}", 16, GREY_A, bold=True).next_to(pa.ax.c2p(2025, np.log10(al[2025] / al[y0])), LEFT, buff=0.2).shift(UP * 0.35)
        lab_t = tx(f"televisions: down {100 * H['tv_fall']:.1f}%", 16, PARTS, bold=True).next_to(pa.ax.c2p(2025, np.log10(tv[2025] / tv[y0])), LEFT, buff=0.3).shift(DOWN * 0.45 + LEFT * 0.2)
        tvs = VGroup(*[RoundedRectangle(corner_radius=0.03, width=w, height=w * 0.62, stroke_color=PARTS, stroke_width=2, fill_color="#1B2230", fill_opacity=1)
                       for w in (0.5, 0.9, 1.4)]).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([3.8, 2.4, 0])
        head = tx("Intermission: seventy-five years of cheaper televisions", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, CPI-U televisions (SERA01) and all items, US city average, annual averages; the index adjusts for quality", size=13)
        with self.voiceover(
            "An intermission, and one line from America's consumer price index. <bookmark mark='a'/> Prices in general "
            f"have risen about {H['cpi_x']:.0f} times since {y0}. <bookmark mark='b'/> The government's price index for "
            f"televisions, which allows for the better sets each year buys, has fallen {100 * H['tv_fall']:.1f} per cent. "
            f"After inflation, {100 * H['real_tv_fall']:.2f} per cent. <bookmark mark='c'/> The television went from a "
            "luxury to something almost every household could afford. A set built from standard parts, which many "
            "factories can make, gets cheaper year after year."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(one), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(la), run_time=2.5)
            self.play(FadeIn(lab_a))
            vo.wait_until("b")
            self.play(Create(lt), run_time=3.5)
            self.play(FadeIn(lab_t))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.1) for t_ in tvs], lag_ratio=0.3))
        self.clear_scene()

    def others(self):
        H = R["history"]
        cp, ph = H["computers"], H["phones"]
        rows = [(draw.server_rack(0.8, 0.5), "Computers and peripherals", f"down {100 * H['comp_fall']:.0f}% since 1998", PARTS),
                (draw.phone(0.8), "Smartphones", f"down {100 * H['phone_fall']:.0f}% since {H['phone_first']}", BRAND)]
        g = VGroup()
        for i, (ic, name, what, col) in enumerate(rows):
            y = 1.2 - 2.2 * i
            ic.scale_to_fit_height(1.0).move_to([-4.6, y, 0])
            t = VGroup(tx(name, 22, WHITE, bold=True), tx(what, 26, col, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.6, y, 0], aligned_edge=LEFT)
            g.add(VGroup(ic, t))
        note = VGroup(tx("Quality-adjusted price indexes:", 15, GREY_A), tx("a faster computer at the same price", 15, GREY_A),
                      tx("counts as a lower price.", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.0, 0, 0])
        src = source("BLS, CPI-U computers, peripherals and smart home assistants (SEEE01) and smartphones (SSEE041), annual averages", size=13)
        with self.voiceover(
            "The same index tells the story of the other boxes. <bookmark mark='a'/> Computers: down "
            f"{100 * H['comp_fall']:.0f} per cent since 1998. <bookmark mark='b'/> Smartphones, which the index has tracked "
            f"on their own only since {H['phone_first']}: down {100 * H['phone_fall']:.0f} per cent already. "
            "<bookmark mark='c'/> These are quality-adjusted: a faster computer at the same price counts as a cheaper one. "
            "Year after year, better factories and better parts have reached the buyer as lower prices."
        ) as vo:
            self.play(FadeIn(src), *[FadeIn(r_[0]) for r_ in g], FadeIn(ghost(*[r_[1] for r_ in g], opacity=0.25)))
            vo.wait_until("a")
            self.play(FadeIn(g[0][1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[1][1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(note, shift=LEFT * 0.1))
        self.clear_scene()

    def output(self):
        H = R["history"]
        ip = H["ip_comp"]
        J = R["cluster"]["jobs"]
        ys = sorted(y for y in ip if 1972 <= y <= 2025)
        pa = viz.plot_axes([1971, 2026], [-2, 3], x_length=9.0, y_length=4.4, xticks=[1972, 1980, 1990, 2000, 2010, 2025],
                           yticks=[-2, -1, 0, 1, 2, 3], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{10 ** v:g}",
                           ylabel="US output of computers and peripherals, 2017 = 100 (log scale)", size=12).move_to([-1.0, -0.4, 0])
        line = poly(pa, [(y, np.log10(ip[y])) for y in ys], PARTS, 4)
        x_ = ip[2025] / ip[1972]
        lab = tx(f"x{x_:,.0f} since 1972", 18, PARTS, bold=True).next_to(pa.ax.c2p(2025, np.log10(ip[2025])), LEFT, buff=0.2).shift(UP * 0.3)
        jobs = VGroup(tx("while jobs making computers", 14, GREY_A), tx("and electronics fell from", 14, GREY_A),
                      tx(f"{J[1990] / 1000:.1f}m (1990) to {J[2025] / 1000:.1f}m (2025)", 16, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.6, -1.8, 0])
        src = source("Federal Reserve, industrial production: computers and peripheral equipment (IPG3341S), annual averages; BLS via FRED", size=12)
        with self.voiceover(
            "One more line: what America's own computer factories produce, measured, like the prices, with allowance for "
            f"quality. <bookmark mark='a'/> The Federal Reserve's index is about {x_:,.0f} times its 1972 level. "
            f"<bookmark mark='b'/> In the same years the jobs making computers and electronics roughly halved. Better "
            "machines and better chips multiply what each factory turns out, with fewer people."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, opacity=0.25)))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            self.play(FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(jobs, shift=LEFT * 0.1))
        self.clear_scene()
