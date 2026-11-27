from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

H1C, Q3C = "#7EC8F5", "#B58CFF"


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "Who saw the boom coming?", "Chapter thirteen. Called it?", lit=("change",))
        self.moore()
        self.market()

    def moore(self):
        C = R["called"]
        pa = viz.plot_axes([1964, 1976], [1.4, 5.1], x_length=7.4, y_length=4.4, xticks=[1965, 1967, 1969, 1971, 1973, 1975],
                           yticks=[2, 3, 4, 5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{10 ** v:,.0f}",
                           ylabel="components on a chip (log scale)", size=13).move_to([-2.6, -0.5, 0])
        line = poly(pa, [(1965, np.log10(C["start65"])), (1975, np.log10(C["target"]))], PRICE, 4)
        steps = VGroup(*[Dot(pa.ax.c2p(y, np.log10(C["start65"] * 2 ** (y - 1965))), radius=0.05, color=PRICE) for y in range(1965, 1976)])
        quote = VGroup(tx("'by 1975, the number of components per", 16, WHITE), tx("integrated circuit for minimum cost", 16, WHITE),
                       tx("will be 65,000'", 16, WHITE), tx("Gordon Moore, Electronics, 19 April 1965", 13, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.7, 1.7, 0])
        hit = Dot(pa.ax.c2p(1975, np.log10(C["target"])), radius=0.11, color=GOOD).set_z_index(3)
        hl = VGroup(tx(f"1975: a {C['chip75']:,.0f}-bit memory chip,", 15, GOOD, bold=True), tx("at the predicted complexity", 15, GOOD, bold=True),
                    tx("(Moore, IEDM 1975)", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.7, -0.4, 0])
        verdict = tx("Called it? Yes, for ten years. Then he changed the slope, and the new one held for fifty.", 18, PRICE, bold=True).to_edge(DOWN, buff=0.75)
        src = source("G. E. Moore, 'Cramming more components onto integrated circuits', Electronics, 1965; 'Progress in Digital "
                     "Integrated Electronics', IEDM 1975", size=13)
        with self.voiceover(
            "Two forecasts about chips, one old and one new. <bookmark mark='a'/> In April 1965 Gordon Moore, then at "
            "Fairchild, wrote that the number of components on the cheapest chip to make had been doubling every year, "
            f"and that by 1975 it would be {C['target']:,.0f}: ten more doublings. <bookmark mark='b'/> In 1975 he "
            f"checked. A {C['chip75']:,.0f}-bit memory chip of that year sat where the line said it would. "
            "<bookmark mark='c'/> Then he slowed the forecast to a doubling every two years, the version that, as the "
            "intermission showed, held for the next half-century."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, quote)))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=LEFT * 0.1))
            self.play(Create(line), LaggedStart(*[GrowFromCenter(d) for d in steps], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromCenter(hit), FadeIn(hl, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def market(self):
        C = R["called"]
        x0, sc, yb = -5.6, 11.2 / 2000, -1.2

        def X(v):
            return x0 + v * sc
        axis = Line([X(0), yb - 0.55, 0], [X(2000), yb - 0.55, 0], stroke_color=GREY_B, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), yb - 0.62, 0], [X(v), yb - 0.48, 0], stroke_color=GREY_B, stroke_width=2),
                                tx(f"${v / 1000:g}tn" if v else "$0", 13, GREY_B).move_to([X(v), yb - 0.85, 0])) for v in (0, 500, 1000, 1500, 2000)])
        h1 = Rectangle(width=C["h1"] * sc, height=0.8, stroke_width=0, fill_color=H1C, fill_opacity=0.9).move_to([X(0), yb, 0], aligned_edge=LEFT)
        q3 = Rectangle(width=C["q3"] * sc, height=0.8, stroke_width=0, fill_color=Q3C, fill_opacity=0.9).next_to(h1, RIGHT, buff=0)
        h1l = tx(f"first half: ${C['h1']:.0f}bn", 15, "#0E1117", bold=True).move_to(h1)
        q3l = tx(f"third quarter: ${C['q3']:.0f}bn", 14, "#0E1117", bold=True).move_to(q3)
        total = tx(f"to September: ${C['to_sep'] / 1000:.2f}tn", 17, WHITE, bold=True).next_to(VGroup(h1, q3), UP, buff=0.12).align_to(q3, RIGHT)
        bar_lab = tx("World chip sales in 2026, so far", 15, GREY_A).next_to(h1, DOWN, buff=0.06).align_to(h1, LEFT).shift(DOWN * 0.55)
        y25 = VGroup(DashedLine([X(795.64), yb - 0.4, 0], [X(795.64), yb + 0.7, 0], stroke_color=GREY_A, stroke_width=2, dash_length=0.06),
                     tx("all of 2025: $796bn", 13, GREY_A)).set_z_index(2)
        y25[1].next_to(y25[0].get_end(), LEFT, buff=0.08)
        fc = []
        for v, when, lvl, col in ((C["aut"], "WSTS, December 2025", 2.8, BAD), (C["spring"], "WSTS, May 2026", 1.9, PRICE),
                                  (C["q2calc"], "WSTS, August 2026", 1.1, PRICE)):
            ln = DashedLine([X(v), yb + 0.45, 0], [X(v), lvl, 0], stroke_color=col, stroke_width=2.5, dash_length=0.08)
            lab = VGroup(tx(when, 13, GREY_A), tx(f"forecast for 2026: ${v / 1000:.2f}tn" if v >= 1000 else f"forecast for 2026: ${v:.0f}bn", 16, col, bold=True)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.03).next_to([X(v), lvl, 0], RIGHT, buff=0.1).shift(DOWN * 0.15)
            fc.append(VGroup(ln, lab))
        head = tx("How big would 2026 be?", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        mem = tx(f"memory, forecast for 2026: ${C['aut_mem']:.0f}bn (December 2025), ${get('wsts.mem.2026f'):.0f}bn (May 2026)", 15, GREY_A).move_to([0.6, 3.1, 0])
        verdict = tx("Called it? No. Even the industry's own statisticians missed the size of the boom.", 18, PRICE, bold=True).to_edge(DOWN, buff=0.55)
        src = source("WSTS: Autumn 2025 and Spring 2026 forecasts, Q2 2026 release; Semiconductor Industry Association, 3 November 2026", size=13)
        with self.voiceover(
            "The new forecast is the industry's own. <bookmark mark='a'/> In December 2025, WSTS, the statistics body the "
            "chipmakers run together, forecast that 2026 would approach a trillion dollars: "
            f"${C['aut']:.0f} billion, up about a quarter on 2025. <bookmark mark='b'/> By June the first half alone had "
            f"brought in ${C['h1']:.0f} billion. <bookmark mark='c'/> Add the third quarter, about ${C['q3']:.0f} billion, "
            f"and by September the year had passed ${C['to_sep'] / 1000:.1f} trillion, with a quarter still to go. "
            f"<bookmark mark='d'/> WSTS raised its forecast to ${C['spring'] / 1000:.2f} trillion in May, and to "
            f"${C['q2calc'] / 1000:.2f} trillion in August. <bookmark mark='e'/> The miss was memory: forecast in December "
            f"at ${C['aut_mem']:.0f} billion for 2026, and in May at ${get('wsts.mem.2026f'):.0f} billion. Called it? No. "
            "Even the industry's own statisticians did not see the size of this boom coming."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis), FadeIn(ticks), FadeIn(bar_lab), FadeIn(y25))
            vo.wait_until("a")
            self.play(Create(fc[0][0]), FadeIn(fc[0][1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(GrowFromEdge(h1, LEFT), FadeIn(h1l), run_time=1.5)
            vo.wait_until("c")
            self.play(GrowFromEdge(q3, LEFT), FadeIn(q3l), run_time=1.5)
            self.play(FadeIn(total, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Create(fc[1][0]), FadeIn(fc[1][1], shift=RIGHT * 0.1))
            self.play(Create(fc[2][0]), FadeIn(fc[2][1], shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(mem), FadeIn(verdict, shift=UP * 0.1))

        # our call: the fourth quarter it takes to pass the threshold
        q4 = DashedVMobject(Rectangle(width=C["q4_needed"] * sc, height=0.8, stroke_color=PRICE, stroke_width=3), num_dashes=40).next_to(q3, RIGHT, buff=0)
        q4f = Rectangle(width=C["q4_needed"] * sc, height=0.8, stroke_width=0, fill_color=PRICE, fill_opacity=0.18).move_to(q4)
        q4l = VGroup(tx("fourth quarter needed:", 12, PRICE), tx(f"${C['q4_needed']:.0f}bn", 15, PRICE, bold=True)).arrange(DOWN, buff=0.02).move_to(q4)
        thr = DashedLine([X(C["threshold"]), yb - 0.5, 0], [X(C["threshold"]), yb + 0.75, 0], stroke_color=WHITE, stroke_width=2.5, dash_length=0.07)
        thl = tx(f"${C['threshold'] / 1000:.1f}tn", 16, WHITE, bold=True).next_to(thr, UP, buff=0.06)
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("World semiconductor sales in 2026, as WSTS first reports them,", 16, WHITE),
                       tx(f"will be more than ${C['threshold'] / 1000:.1f} trillion.", 18, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked against WSTS's full-year figure in early 2027", 14, GREY_A)).arrange(DOWN, buff=0.1).move_to([0, 2.2, 0])
        why = VGroup(tx(f"For: sales grew more than a fifth a quarter for three quarters running; a fourth quarter {100 * C['q4_growth']:.0f}% above the third is enough", 14, GOOD),
                     tx("Against: memory booms end abruptly (chapter eight); buyers who stocked up early stop ordering", 14, BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([0, 0.55, 0])
        src2 = source("WSTS Q2 2026 release; SIA, 3 November 2026 (third quarter, 'more than 20% quarter-to-quarter for the third "
                      "consecutive quarter')", size=13)
        with self.voiceover(
            "Now our own call, written down so you can check it. <bookmark mark='a'/> To pass "
            f"${C['threshold'] / 1000:.1f} trillion for the year, the fourth quarter has to bring in about "
            f"${C['q4_needed']:.0f} billion: {100 * C['q4_growth']:.0f} per cent more than the third. <bookmark mark='b'/> "
            "Sales have grown by more than a fifth a quarter for three quarters running, so we think it will. Against us: "
            "memory booms end abruptly, as chapter eight showed, and buyers who stocked up early can stop ordering all at "
            f"once. <bookmark mark='c'/> We give it {100 * C['prob']:.0f} per cent, and we will check it against WSTS's "
            "first full-year figure, due early in 2027, right or wrong."
        ) as vo:
            self.play(FadeOut(VGroup(*fc), mem, verdict, head, src, total), FadeIn(src2))
            vo.wait_until("a")
            self.play(Create(thr), FadeIn(thl))
            self.play(FadeIn(q4f), Create(q4), FadeIn(q4l), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(card_[:3]), FadeIn(why))
            vo.wait_until("c")
            self.play(FadeIn(card_[3:], scale=1.1))
        self.clear_scene()
