from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

NODE_COL = {"2nm": "#F6C453", "3nm": "#B58CFF", "5nm": "#7EC8F5", "7nm": "#7BD88F", "16nm": "#5DA9E9", "28nm": "#9AA3B2",
            "40-65nm": "#6B7280", "90nm and older": "#3A4152", "older": "#3A4152"}


class Node(VoiceoverScene):
    def construct(self):
        card(self, 3, "The node", "What does '3 nanometres' mean, and why does every chip company chase the next one?",
             "Chapter three. The node.", lit=("make", "change"))
        self.names()
        self.mix()

    def names(self):
        M = R["making"]
        rows = [("1961", f"lines about {M['line61']:.0f} micrometres wide", "a measurement"),
                ("1975", f"about {M['line75']:.0f} micrometres", "a measurement"),
                ("2025", "Intel's '18A', 'A' for angstrom", "the name of a generation"),
                ("2026", "TSMC's '3-nanometer', '2-nanometer'", "the names of generations")]
        tbl = VGroup()
        for i, (y, a, b) in enumerate(rows):
            tbl.add(VGroup(tx(y, 22, PRICE, bold=True).move_to([-5.0, 1.5 - 0.9 * i, 0]),
                           tx(a, 18, WHITE).move_to([-4.2, 1.5 - 0.9 * i, 0], aligned_edge=LEFT),
                           tx(b, 16, GREY_A).move_to([2.6, 1.5 - 0.9 * i, 0], aligned_edge=LEFT)))
        intel = VGroup(tx("Intel 18A, first products in 2025:", 16, WHITE, bold=True),
                       tx("gate-all-around transistors and power delivered from the back of the wafer", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).to_edge(DOWN, buff=0.85)
        src = source("G. E. Moore, IEDM 1975; TSMC, Form 20-F 2025 and Form 6-K of 15 October 2026; Intel, Form 10-K 2025", size=13)
        with self.voiceover(
            "Every few years the industry moves to a new 'node', a new generation of process. <bookmark mark='a'/> When "
            f"Moore wrote, the number was a real measurement: lines {M['line61']:.0f} micrometres wide in 1961, "
            f"{M['line75']:.0f} by 1975. <bookmark mark='b'/> Today's numbers, TSMC's three and two nanometres, are the "
            "names each company gives its generations. <bookmark mark='c'/> Intel calls its newest one 18A, A for "
            "angstrom, a tenth of a nanometre. What each new generation actually delivers is more transistors in the same "
            "space, using less power, and the new transistor shapes that make that possible: Intel's 18A brought "
            "transistors wrapped in their gate on every side, and power wired in from the back of the wafer."
        ) as vo:
            head = tx("What the number on a process means", 22, WHITE, bold=True).to_edge(UP, buff=0.4)
            self.play(FadeIn(src), FadeIn(head), *[FadeIn(r_[0]) for r_ in tbl], FadeIn(ghost(*[r_[1:] for r_ in tbl], opacity=0.2)))
            vo.wait_until("a")
            self.play(FadeIn(tbl[0][1:]), FadeIn(tbl[1][1:]))
            vo.wait_until("b")
            self.play(FadeIn(tbl[3][1:]))
            vo.wait_until("c")
            self.play(FadeIn(tbl[2][1:]), FadeIn(intel, shift=UP * 0.1))
        self.clear_scene()

    def mix(self):
        N = R["node"]
        share = N["share"]
        order = ["90nm and older", "40-65nm", "28nm", "16nm", "7nm", "5nm", "3nm"]
        cols = VGroup()
        h = 4.6
        for j, (lab, year_i) in enumerate((("2023", 0), ("2024", 1), ("2025", 2))):
            x = -4.6 + 2.0 * j
            y = -2.4
            col = VGroup()
            for k in order:
                v = share[k][year_i]
                b = Rectangle(width=1.2, height=h * v / 100, stroke_color="#0E1117", stroke_width=1.5, fill_color=NODE_COL[k], fill_opacity=0.95).move_to(
                    [x, y, 0], aligned_edge=DOWN)
                y += h * v / 100
                col.add(b)
            cols.add(VGroup(col, tx(lab, 16, GREY_A).move_to([x, -2.7, 0])))
        q3 = N["q3"]
        y = -2.4
        qcol = VGroup()
        for k in ("older", "7nm", "5nm", "3nm", "2nm"):
            v = q3[k]
            b = Rectangle(width=1.2, height=h * v / 100, stroke_color="#0E1117", stroke_width=1.5, fill_color=NODE_COL[k], fill_opacity=0.95).move_to(
                [1.8, y, 0], aligned_edge=DOWN)
            y += h * v / 100
            qcol.add(b)
        qlab = tx("3Q 2026", 16, PRICE, bold=True).move_to([1.8, -2.7, 0])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=NODE_COL[k], fill_opacity=0.95), tx(k, 14, GREY_A)).arrange(RIGHT, buff=0.08)
                       for k in ("2nm", "3nm", "5nm", "7nm", "16nm", "28nm", "40-65nm", "90nm and older")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.6, 0.0, 0])
        head = tx("TSMC's wafer revenue by node", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        three = tx(f"3nm: {share['3nm'][0]}% → {share['3nm'][1]}% → {share['3nm'][2]}% → {q3['3nm']:.0f}%", 17, NODE_COL["3nm"], bold=True).move_to([-2.0, 2.65, 0])
        src = source("TSMC, Form 20-F 2025 (wafer revenue by technology, grouped); Form 6-K of 15 October 2026", size=13)
        with self.voiceover(
            "Why chase the next node? Because that is where the money goes. <bookmark mark='a'/> Here is TSMC's wafer "
            f"revenue by node. In 2023, its three-nanometre process brought in {share['3nm'][0]} per cent. "
            f"<bookmark mark='b'/> In 2024, {share['3nm'][1]}. In 2025, {share['3nm'][2]}. <bookmark mark='c'/> And in the "
            f"third quarter of 2026, {q3['3nm']:.0f} per cent, with the two-nanometre process already at {q3['2nm']:.0f}. "
            "Each new node takes over the top of the market within a few years, at the highest prices, because the "
            "customers who need the fastest chips will pay for them. The older nodes do not disappear; they become the "
            "factories for everything else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), *[FadeIn(c[1]) for c in cols], FadeIn(qlab))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cols[0][0]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cols[1][0]], lag_ratio=0.08), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cols[2][0]], lag_ratio=0.08), run_time=1.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in qcol], lag_ratio=0.1), FadeIn(three), run_time=1.5)
        self.clear_scene()
