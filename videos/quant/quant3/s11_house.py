from __future__ import annotations

from datetime import date

from explainer.quant import *  # noqa: F403
from explainer.quant.house.fundamentals import Store
from videos.quant.quant3.common import PART

EVENTS = [(20191231, r"year ends", GREY_B), (20200220, r"10-K filed: 200", QC.IDEA),
          (20210315, r"restated: 150", QC.LOSS)]


def _d(n: int) -> float:
    d = date(n // 10000, n // 100 % 100, n % 100)
    return float(d.toordinal())


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.store()
        self.desk()

    def card(self):
        c = chapter_card(10, r"The fundamentals store", r"When could the market have known?", part=PART)
        with self.voiceover("Chapter ten. The fundamentals store."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def store(self):
        s = Store()
        s.add("ACME", "NetIncomeLoss", 20191231, 20200220, 200.0, "10-K")
        s.add("ACME", "NetIncomeLoss", 20191231, 20210315, 150.0, "10-K/A")
        lo, hi = _d(20191201), _d(20210630)
        line = NumberLine(x_range=[lo, hi, 30], length=11.5, include_ticks=False, color=GREY_C).shift(UP * 0.6)
        marks = VGroup()
        for n, txt, col in EVENTS:
            p = line.n2p(_d(n))
            tick = Line(p + DOWN * 0.15, p + UP * 0.15, color=col, stroke_width=4)
            lab = label(txt, font_size=22, color=col).next_to(tick, UP, buff=0.15)
            if n == 20191231:
                lab.next_to(tick, UP, buff=0.15).align_to(tick, RIGHT).shift(LEFT * 0.1)
            elif n == 20200220:
                lab.next_to(tick, UP, buff=0.15).align_to(tick, LEFT).shift(RIGHT * 0.1)
            day = label(f"{n // 10000}-{n // 100 % 100:02d}-{n % 100:02d}", font_size=18, color=GREY_B)
            day.next_to(tick, DOWN, buff=0.15)
            if n == 20191231:
                day.align_to(tick, RIGHT).shift(LEFT * 0.05)
            elif n == 20200220:
                day.align_to(tick, LEFT).shift(RIGHT * 0.05)
            marks.add(VGroup(tick, lab, day))
        q = ValueTracker(_d(20200105))

        def query():
            dd = date.fromordinal(int(q.get_value()))
            n = dd.year * 10000 + dd.month * 100 + dd.day
            v = s.asof("ACME", "NetIncomeLoss", n)
            col = GREY_B if v is None else (QC.IDEA if v == 200 else QC.LOSS)
            txt = r"nothing filed yet" if v is None else rf"{v:.0f}"
            p = line.n2p(q.get_value())
            arrow = Arrow(p + DOWN * 1.35, p + DOWN * 0.45, buff=0, color=QC.HOUSE, stroke_width=4,
                          max_tip_length_to_length_ratio=0.3)
            read = MathTex(rf"\texttt{{asof}}(\text{{{dd.isoformat()}}})", r"=", rf"\text{{{txt}}}", font_size=30)
            read[0].set_color(QC.HOUSE)
            read[2].set_color(col)
            read.next_to(arrow, DOWN, buff=0.12)
            if read.get_left()[0] < -6.8:
                read.shift(RIGHT * (-6.8 - read.get_left()[0]))
            if read.get_right()[0] > 6.8:
                read.shift(LEFT * (read.get_right()[0] - 6.8))
            return VGroup(arrow, read)

        probe = always_redraw(query)
        head = label(r"one fact, FY2019 net income, as the House stores it", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.5)
        code = VGroup(
            MathTex(r"\texttt{Fact(period\_end, filed, value, form, accession)}", font_size=26),
            label(r"append-only: a restatement is a new fact, never an edit", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the House's rule for company numbers, on one fact: a firm's net income for 2019. The year ended "
            "on the thirty-first of December. <bookmark mark='a'/> The annual report reached the SEC on the twentieth "
            "of February, saying two hundred. <bookmark mark='b'/> A year later the firm restated it to a hundred "
            "and fifty. <bookmark mark='c'/> The store keeps both, each with its filing date, and a query names the "
            "day it is asked as of. Ask in January 2020 and nothing has been filed: the year is over but nobody "
            "knows the number. <bookmark mark='d'/> Ask in the summer of 2020 and the answer is two hundred, the "
            "number the market actually traded on. <bookmark mark='e'/> Only after March 2021 does the store answer "
            "a hundred and fifty. A database that simply overwrites the old value would hand a backtest the "
            "corrected number in 2020, a number nobody had yet."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            self.play(FadeIn(marks[0]))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]))
            vo.wait_until("b")
            self.play(FadeIn(marks[2]))
            vo.wait_until("c")
            self.play(FadeIn(probe), FadeIn(code))
            vo.wait_until("d")
            self.play(q.animate.set_value(_d(20200801)), run_time=3)
            vo.wait_until("e")
            self.play(q.animate.set_value(_d(20210501)), run_time=3)
        self.wait(0.4)
        self.remove(probe)
        self.clear_scene()

    def desk(self):
        chart = house_chart(PART, lit=("data",)).scale(0.72).to_edge(UP, buff=0.25)
        items = VGroup(
            label(r"\texttt{valuation}: NPV, IRR, annuities, Gordon, DCF, WACC, Modigliani--Miller, Merton's equity",
                  font_size=22),
            label(r"\texttt{fundamentals}: the bitemporal store, loading the SEC's XBRL company facts", font_size=22),
            label(r"the envelope: Shiller's and French's hold-outs from 2021 sealed; the CAPE forecast registered",
                  font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(chart, DOWN, buff=0.4)
        if items.width > 13.0:
            items.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 4: a reported number exists from the day it was filed, as first reported; a "
                             r"restatement is a new fact, never an edit of the past.", 12.0, 24,
                             QC.HOUSE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The data desk grows. It now has a valuation library, tested, with every formula in this part, and the "
            "fundamentals store, which reads the SEC's machine-readable company facts directly. <bookmark mark='a'/> "
            "The hold-out years of every dataset this part used are sealed, and the CAPE forecast is registered. "
            "<bookmark mark='b'/> And the House adds its fourth rule: a reported number exists from the day it was "
            "filed, as it was first reported, and a restatement is a new fact, never an edit of the past."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05), FadeIn(items[:2]))
            vo.wait_until("a")
            self.play(FadeIn(items[2]))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
