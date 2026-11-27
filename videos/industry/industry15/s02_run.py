from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

OWN, BOOK = "#F2A65A", "#7EC8F5"
VOLS = (5_000, 20_000, 50_000)


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: build a fab or book a foundry", "You have designed a chip. Where should it be made?",
             "Chapter one. Run it: build a fab or book a foundry.", lit=("make", "dollar"))
        self.setup_()
        self.three()
        self.curve()

    def setup_(self):
        G = R["run"]
        F, ch = G["fab"], G["chip"]
        chip = draw.chip(1.1).move_to([0, 1.6, 0])
        chip_l = VGroup(tx("your chip", 20, WHITE, bold=True), tx(f"{ch['die']:.0f} mm2 of silicon; sells for ${ch['price']:.0f}", 15, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(chip, DOWN, buff=0.15)
        own = VGroup(draw.factory(1.8),
                     tx("1. Build your own fab", 20, OWN, bold=True),
                     tx(f"${F['capex']:.0f}bn to build; tools last {F['life']:.0f} years", 15, GREY_A),
                     tx(f"{F['capacity']:,.0f} wafers a month at most", 15, GREY_A),
                     tx(f"${F['fixed']:.0f}bn a year to run, ${F['variable']:,.0f} a wafer", 15, GREY_A),
                     tx(f"a new process: {G['d_new']} defects a cm2 at first", 15, BAD)).arrange(DOWN, buff=0.08).move_to([-4.0, -1.2, 0])
        book = VGroup(draw.factory(1.8, "#5D6B82"),
                      tx("2. Book a foundry", 20, BOOK, bold=True),
                      tx(f"${G['foundry_price']:,.0f} a wafer, as many as you need", 15, GREY_A),
                      tx("no fab to build, nothing idle", 15, GREY_A),
                      tx(f"a mature process: {G['d_mature']} defects a cm2", 15, GOOD),
                      tx(" ", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([4.0, -1.2, 0])
        tag = estimate_tag("the Works' fab: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "You run a chip-design company, and your new chip is ready. <bookmark mark='a'/> It is a square of silicon "
            f"about {ch['die']:.0f} square millimetres, and each good one sells for ${ch['price']:.0f}. "
            "<bookmark mark='b'/> You can build your own factory, a fab: about "
            f"${F['capex']:.0f} billion, with tools that are obsolete in about {F['life']:.0f} years, able to start "
            f"{F['capacity']:,.0f} wafers a month. And because the process is new to you, your first wafers will be full "
            "of defects. <bookmark mark='c'/> Or you can book a foundry, which already runs the process, at "
            f"${G['foundry_price']:,.0f} a wafer. Which is cheaper depends on one thing: how many wafers you need."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chip, scale=0.8), FadeIn(ghost(own, book, opacity=0.3)))
            vo.wait_until("a")
            self.play(FadeIn(chip_l), Indicate(chip, color=PRICE, scale_factor=1.1))
            vo.wait_until("b")
            self.play(FadeIn(own, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(book, shift=LEFT * 0.2))
        self.clear_scene()

    def three(self):
        G = R["run"]
        games = G["games"]
        sc = 0.22
        base_y = -0.6
        cols = VGroup()
        for i, v in enumerate(VOLS):
            x = -4.2 + 4.2 * i
            fb, ow = games[f"{v}|foundry"], games[f"{v}|own"]
            bars = VGroup()
            for j, (gm, col) in enumerate(((fb, BOOK), (ow, OWN))):
                p_ = gm["profit"]
                h = abs(p_) * sc
                b = Rectangle(width=0.8, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
                b.move_to([x - 0.5 + 1.0 * j, base_y, 0], aligned_edge=DOWN if p_ >= 0 else UP)
                lab = tx(f"{'+' if p_ >= 0 else '-'}${abs(p_):.1f}bn", 15, col, bold=True).next_to(b, UP if p_ >= 0 else DOWN, buff=0.06)
                bars.add(VGroup(b, lab))
            head = VGroup(tx(f"{v:,} wafers a month", 18, WHITE, bold=True),
                          tx(f"your fab {100 * ow['util']:.0f}% full; ${ow['cost_wafer']:,.0f} a wafer", 13, GREY_A)).arrange(DOWN, buff=0.04).move_to([x, 3.0, 0])
            cols.add(VGroup(head, bars))
        zero = Line([-6.4, base_y, 0], [6.4, base_y, 0], stroke_color=GREY_B, stroke_width=1.5)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=BOOK, fill_opacity=0.9), tx("book a foundry", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color=OWN, fill_opacity=0.9), tx("build your own", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.7)
        yl = tx("profit a year, $ billion", 13, GREY_B).move_to([-5.6, 2.3, 0])
        tag = estimate_tag("the Works' fab: an illustration in round numbers", corner=DR, size=12)
        s, m, l = (games[f"{v}|own"] for v in VOLS)
        fs, fm, fl = (games[f"{v}|foundry"] for v in VOLS)
        with self.voiceover(
            "Run it at three sizes. <bookmark mark='a'/> A small company needs five thousand wafers a month. Its own fab "
            f"would stand {100 * s['util']:.0f} per cent full, so each wafer would carry ten times its share of the fab: about "
            f"${s['cost_wafer']:,.0f}. It would lose about ${abs(s['profit']):.1f} billion a year; booking a foundry, it "
            f"makes about ${fs['profit']:.1f} billion. <bookmark mark='b'/> At twenty thousand wafers, the fab is "
            f"{100 * m['util']:.0f} per cent full and finally profitable, but still behind the foundry: "
            f"${m['profit']:.1f} billion against ${fm['profit']:.1f}. <bookmark mark='c'/> Only at fifty thousand, a full "
            f"fab, does owning win: ${l['profit']:.1f} billion against ${fl['profit']:.1f}, because now you keep the "
            "foundry's margin yourself."
        ) as vo:
            self.play(FadeIn(zero), FadeIn(key), FadeIn(yl), FadeIn(tag), *[FadeIn(c[0]) for c in cols])
            for m_, c in zip("abc", cols):
                vo.wait_until(m_)
                self.play(*[AnimationGroup(GrowFromEdge(b[0], DOWN if b[0].get_bottom()[1] >= base_y - 0.01 else UP), FadeIn(b[1])) for b in c[1]],
                          run_time=1.5)
        self.clear_scene()

    def curve(self):
        G = R["run"]
        cv = G["curve"]
        vs = sorted(cv)
        pa = viz.plot_axes([0, 50_000], [-5, 15], x_length=8.6, y_length=4.6, xticks=[0, 10_000, 20_000, 30_000, 40_000, 50_000],
                           yticks=[-5, 0, 5, 10, 15], xfmt=lambda v: f"{v / 1000:.0f}k", yfmt=lambda v: f"${v:.0f}bn",
                           ylabel="profit a year", size=13).move_to([-1.4, -0.4, 0])
        xl = tx("wafers you need a month", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        zero = DashedLine(pa.ax.c2p(0, 0), pa.ax.c2p(50_000, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        lb = poly(pa, [(v, cv[v][0]) for v in vs], BOOK, 4)
        lo = poly(pa, [(v, cv[v][1]) for v in vs], OWN, 4)
        e = G["even"]
        mark = DashedLine(pa.ax.c2p(e, -5), pa.ax.c2p(e, 15), stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        mark_l = tx(f"break-even: about {e:,} wafers a month", 16, PRICE, bold=True).next_to(pa.ax.c2p(e, 15), DOWN, buff=0.1).shift(LEFT * 1.6)
        labs = VGroup(tx("book a foundry", 15, BOOK, bold=True).next_to(pa.ax.c2p(50_000, cv[vs[-1]][0]), RIGHT, buff=0.1),
                      tx("build your own", 15, OWN, bold=True).next_to(pa.ax.c2p(50_000, cv[vs[-1]][1]), RIGHT, buff=0.1))
        side = VGroup(tx("TSMC shipped about", 15, GREY_A), tx(f"{get('tsm.ship.2025'):.0f} million wafers in 2025:", 15, GREY_A),
                      tx(f"about {get('tsm.ship.2025') / 12:.2f} million a month,", 15, WHITE, bold=True),
                      tx("for 534 customers", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([5.0, -1.6, 0])
        tag = estimate_tag("the Works' fab: an illustration in round numbers", corner=DR, size=12)
        with self.voiceover(
            "Draw it for every size. <bookmark mark='a'/> The foundry line rises steadily: you pay per wafer, so profit "
            "grows with volume. <bookmark mark='b'/> Your own fab starts deep in loss, because you pay for the whole fab "
            f"however little you use. <bookmark mark='c'/> They cross at about {e:,} wafers a month, every month, for five "
            "years. <bookmark mark='d'/> Very few chip companies need that much of one process. But a foundry adds up "
            f"everyone's demand: TSMC shipped about {get('tsm.ship.2025'):.0f} million wafers in 2025, more than a million "
            "a month, and keeps its fabs full with other people's chips. That arithmetic is why the industry split in two."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(labs[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lo), FadeIn(labs[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(mark), FadeIn(mark_l))
            vo.wait_until("d")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()
