from __future__ import annotations

from explainer.industry.works import mill
from videos.industry.industry11.common import *  # noqa: F403


class MustRun(VoiceoverScene):
    def construct(self):
        card(self, 4, "A plant that must run", "Why does a half-empty mill lose money so fast?",
             "Chapter four. A plant that must run.", lit=("make", "change"))
        self.curves()
        self.utilization()
        self.profits()

    def curves(self):
        M = R["mustrun"]
        rates, ci, cm = M["rates"], M["curves"]["integrated"], M["curves"]["minimill"]
        pa = viz.plot_axes([0.38, 1.02], [400, 1400], x_length=7.6, y_length=4.6, xticks=[0.4, 0.6, 0.8, 1.0],
                           yticks=[500, 800, 1100, 1400], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="cost of a tonne", size=13).move_to([-2.0, -0.2, 0])
        xl = tx("share of capacity in use", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        li = VMobject(stroke_color=ORE, stroke_width=3.5).set_points_smoothly([pa.ax.c2p(r_, c) for r_, c in zip(rates, ci)])
        lm = VMobject(stroke_color=SCRAP, stroke_width=3.5).set_points_smoothly([pa.ax.c2p(r_, c) for r_, c in zip(rates, cm)])
        ti = tx("integrated mill", 16, ORE, bold=True).next_to(pa.ax.c2p(0.45, ci[5]), RIGHT, buff=0.15)
        tm = tx("minimill", 16, SCRAP, bold=True).next_to(pa.ax.c2p(0.45, cm[5]), DOWN, buff=0.2)
        t = ValueTracker(1.0)
        im, mm_ = mill.INTEGRATED, mill.MINIMILL
        di = always_redraw(lambda: Dot(pa.ax.c2p(t.get_value(), im.unit_cost(t.get_value())), radius=0.08, color=ORE))
        dm = always_redraw(lambda: Dot(pa.ax.c2p(t.get_value(), mm_.unit_cost(t.get_value())), radius=0.08, color=SCRAP))
        vline = always_redraw(lambda: DashedLine(pa.ax.c2p(t.get_value(), 400), pa.ax.c2p(t.get_value(), 1400),
                                                 stroke_color=GREY_B, stroke_width=1.2, dash_length=0.06))
        read = always_redraw(lambda: VGroup(
            tx(f"running at {100 * t.get_value():.0f}%", 20, WHITE, bold=True),
            tx(f"integrated: ${im.unit_cost(t.get_value()):,.0f} a tonne", 18, ORE),
            tx(f"minimill: ${mm_.unit_cost(t.get_value()):,.0f} a tonne", 18, SCRAP)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.08).move_to([4.6, 1.2, 0]))
        share = VGroup(tx("Costs that do not move with output,", 16, WHITE), tx("at full output:", 16, WHITE),
                       tx(f"integrated {100 * M['int_fixed_share']:.0f}%", 18, ORE, bold=True),
                       tx(f"minimill {100 * M['mini_fixed_share']:.0f}%", 18, SCRAP, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.6, -1.6, 0])
        tag = estimate_tag("the Works (mill.py): the two model mills of chapter one", corner=DR, size=13)
        with self.voiceover(
            "Here is the problem in one picture. On the left, how much of the mill is being used; up the side, what a "
            "tonne costs to make. <bookmark mark='a'/> For the integrated mill of chapter one, nearly a third of the "
            "cost of a tonne, at full output, is fixed: it is there whether the furnace runs or not. "
            "<bookmark mark='b'/> For a minimill, about a sixth. <bookmark mark='c'/> Now let orders fall. At eighty "
            "per cent, the integrated mill's tonne costs noticeably more. At sixty per cent, the fixed costs are spread "
            "over so few tonnes that each one costs hundreds of dollars more than at full output. The minimill's costs "
            "rise too, but far more gently. <bookmark mark='d'/> That is why a heavy plant wants to run full at almost "
            "any price, and why an industry full of them keeps producing into a glut."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(li), FadeIn(ti), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(tm), run_time=1.6)
            self.add(vline, di, dm, read)
            vo.wait_until("c")
            self.play(t.animate.set_value(0.8), run_time=2.0)
            self.play(t.animate.set_value(0.6), run_time=2.0)
            self.play(t.animate.set_value(0.45), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(share), t.animate.set_value(0.95), run_time=1.5)
        for m_ in (vline, di, dm, read):
            m_.clear_updaters()
        self.clear_scene()

    def utilization(self):
        M = R["mustrun"]
        cu, nu = M["cap_util"], M["nucor_util"]
        ys = sorted(cu)
        pa = viz.plot_axes([1971, 2026.5], [40, 105], x_length=10.6, y_length=4.4, xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                           yticks=[50, 70, 90], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                           ylabel="share of capacity in use", size=13).move_to([0, -0.4, 0])
        ln = VMobject(stroke_color=STEELC, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, cu[y]) for y in ys])
        ny = sorted(nu)
        ln2 = VMobject(stroke_color=SCRAP, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, nu[y]) for y in ny])
        l1 = tx("US iron and steel mills (Federal Reserve)", 15, STEELC, bold=True).move_to(pa.ax.c2p(1984, 99))
        l2 = tx("Nucor's steel mills", 15, SCRAP, bold=True).next_to(pa.ax.c2p(2004, nu[2004]), UP, buff=0.1)
        lows = [(1982, "1982"), (2009, "2009")]
        marks = VGroup(*[VGroup(Dot(pa.ax.c2p(y, cu[y]), radius=0.05, color=BAD),
                                tx(f"{lab}: {cu[y]:.0f}%", 13, BAD).next_to(pa.ax.c2p(y, cu[y]), DOWN, buff=0.08)) for y, lab in lows
                         if y in cu])
        n09 = VGroup(Dot(pa.ax.c2p(2009, nu[2009]), radius=0.05, color=SCRAP),
                     tx(f"Nucor 2009: {nu[2009]:.0f}%", 13, SCRAP).next_to(pa.ax.c2p(2009, nu[2009]), RIGHT, buff=0.1))
        src = source("Federal Reserve G.17, capacity utilization: iron and steel products (CAPUTLG3311A2S), annual averages, "
                     "via FRED; Nucor, Forms 10-K 2003-2025", size=13)
        with self.voiceover(
            "How full are American mills, in practice? <bookmark mark='a'/> Here is the Federal Reserve's measure for "
            "the whole industry since 1972. <bookmark mark='b'/> In good years, eighty or ninety per cent. In the slump "
            f"of 1982, {cu[1982]:.0f} per cent; in 2009, after the financial crisis, {cu[2009]:.0f}. "
            "<bookmark mark='c'/> Nucor's mills follow the same tide: ninety-seven per cent in 2004, "
            f"{nu[2009]:.0f} per cent in 2009, {nu[2025]:.0f} per cent in 2025. The tide is the economy: steel goes into "
            "buildings, cars and machines, which are exactly what people stop buying in a recession."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(l1), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(Create(ln2), FadeIn(l2), run_time=2.0)
            self.play(FadeIn(n09))
        self.clear_scene()

    def profits(self):
        nets = R["mustrun"]["nets"]
        show = [("NUE", "Nucor", SCRAP), ("STLD", "Steel Dynamics", "#5DA9E9"), ("X", "US Steel", ORE),
                ("CLF", "Cleveland-Cliffs", "#E8A07A")]
        ys = list(range(2016, 2026))
        pa = viz.plot_axes([2015.4, 2025.6], [-2.5, 8.5], x_length=10.0, y_length=4.4, xticks=[2016, 2018, 2020, 2022, 2024],
                           yticks=[-2, 0, 2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="net income", size=13).move_to([-0.6, -0.4, 0])
        zero = Line(pa.ax.c2p(2015.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.2)
        lines, labs = VGroup(), VGroup()
        for t, n, c in show:
            pts = [pa.ax.c2p(y, nets[t][y]) for y in ys if y in nets[t]]
            lines.add(VMobject(stroke_color=c, stroke_width=3).set_points_as_corners(pts))
            last = max(y for y in ys if y in nets[t])
            labs.add(tx(n, 14, c, bold=True).next_to(pa.ax.c2p(last, nets[t][last]), RIGHT, buff=0.1))
        src = source("SEC company facts, Forms 10-K (net income attributable to the company); US Steel's last 10-K is for "
                     "2024", size=13)
        with self.voiceover(
            "And so the profits of steelmakers swing like few others. <bookmark mark='a'/> Here are four American "
            "steelmakers over ten years. A few hundred million dollars a year in the quiet years. <bookmark mark='b'/> "
            f"Then 2021 and 2022: Nucor earns {nets['NUE'][2022]:.1f} billion dollars in a single year, US Steel "
            f"{nets['X'][2021]:.1f} billion. <bookmark mark='c'/> And then back down, and for the blast-furnace "
            f"companies, below zero: Cleveland-Cliffs lost money in 2024 and again in 2025. A business with big fixed "
            "costs magnifies every swing in price: a little more price falls straight to profit, and a little less "
            "comes straight out of it."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), Create(zero))
            vo.wait_until("a")
            self.play(*[Create(l_) for l_ in lines], run_time=3.5, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.2))
            vo.wait_until("b")
            k = ys.index(2022)
            self.play(Flash(pa.ax.c2p(2022, nets["NUE"][2022]), color=GOOD, flash_radius=0.4), run_time=0.8)
            vo.wait_until("c")
            self.play(Flash(pa.ax.c2p(2025, nets["CLF"][2025]), color=BAD, flash_radius=0.4), run_time=0.8)
            del k
        self.clear_scene()
