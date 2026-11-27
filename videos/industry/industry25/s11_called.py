from __future__ import annotations

from videos.industry.industry25.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 9, "Called it?", "How well do the builders and the lenders forecast?",
             "Chapter nine. Called it? America's largest builder forecasts its year every October; Fannie Mae forecasts the "
             "mortgage market every February.", lit=("change",))
        self.horton()
        self.fannie()
        self.ours()

    def horton(self):
        C = R["called"]
        pa = viz.plot_axes([76000, 90000], [0, 2], x_length=10.0, y_length=2.8, xticks=[76000, 79000, 82000, 85000, 88000],
                           xfmt=lambda v: f"{v / 1e3:.0f}k", grid=False, size=13).move_to([0.4, 0.4, 0])
        ax = pa.ax
        b26 = Line(ax.c2p(C["g26_homes"][0], 1.5), ax.c2p(C["g26_homes"][1], 1.5), stroke_color=PRICE, stroke_width=14)
        l26 = tx(f"October 2025: {C['g26_homes'][0]:,.0f}-{C['g26_homes'][1]:,.0f} homes in fiscal 2026", 15, PRICE).next_to(b26, UP, buff=0.15)
        a26 = marker(ax, C["a26"][1], 1.5, f"actual: {C['a26'][1]:,.0f}", BAD, side=DOWN)
        b27 = Line(ax.c2p(C["g27_homes"][0], 0.5), ax.c2p(C["g27_homes"][1], 0.5), stroke_color=PRICE, stroke_width=14)
        l27 = tx(f"October 2026: {C['g27_homes'][0]:,.0f}-{C['g27_homes'][1]:,.0f} homes in fiscal 2027", 15, PRICE).next_to(b27, DOWN, buff=0.15)
        src = source("D.R. Horton, Inc., Forms 8-K of 28 October 2025 and 29 October 2026", size=12)
        beat(self,
             f"D.R. Horton first. <bookmark mark='a'/> In October 2025 it expected to close {C['g26_homes'][0]:,.0f} to "
             f"{C['g26_homes'][1]:,.0f} homes in fiscal 2026, and revenue of {C['g26_rev'][0]} to {C['g26_rev'][1]} billion "
             f"dollars. <bookmark mark='b'/> It closed {C['a26'][1]:,.0f}, below the range, for {C['a26'][0]} billion, also "
             f"below. <bookmark mark='c'/> For fiscal 2027 it expects {C['g27_homes'][0]:,.0f} to {C['g27_homes'][1]:,.0f} "
             f"homes and {C['g27_rev'][0]:.0f} to {C['g27_rev'][1]:.0f} billion dollars: a lower range, set with mortgage "
             "rates rising.",
             base=[pa, src], steps=[[b26, l26], a26, [b27, l27]])

    def fannie(self):
        C = R["called"]
        M = R["mortgage"]["rate_2026"]
        pts = {int(m[:4]) + (int(m[5:7]) - 0.5) / 12: v for m, v in M.items()}
        ch = line_chart({"30-year rate": (pts, LOAN)}, x=(2025, 2027), y=(5.5, 7.5), xticks=[2025, 2026, 2027], yticks=[5.5, 6.0, 6.5, 7.0, 7.5],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.1f}%", ylabel="30-year mortgage rate, monthly average",
                        width=7.0, height=3.4, center=(-2.0, -0.6), label_end=False)
        line = ch.lines["30-year rate"]
        a, b = C["fnm"]
        c = VGroup(tx("Fannie Mae, February 2026:", 16, GREY_A), tx(f"originations ${a:.2f}tn in 2025", 18, WHITE, bold=True),
                   tx(f"to ${b:.2f}tn in 2026 (+24%)", 18, PRICE, bold=True), tx("on lower rates", 16, GREY_A)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.4, 0])
        src = source("Fannie Mae, Form 10-K for 2025; Freddie Mac rates via FRED", size=12)
        beat(self,
             "Then Fannie Mae. <bookmark mark='a'/> In February 2026 it forecast that Americans would take out "
             f"{b:.2f} trillion dollars of new home loans in 2026, a quarter more than in 2025, mostly because more "
             "owners would refinance at lower rates. <bookmark mark='b'/> Mortgage rates did fall a little in early 2026, "
             "then rose through the summer and passed seven per cent in October. Fannie Mae's own count for 2026 will "
             "come with its next annual report.",
             base=[ch.frame, src], steps=[c, line])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx(f"D.R. Horton will close fewer than {C['call']:,.0f} homes in fiscal 2027,", 22, WHITE, bold=True),
                       tx("the middle of its own range.", 22, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0, 1.7, 0])
        why = bullets([f"for: it missed the bottom of last year's range; fourth-quarter orders fell 7%, to {C['orders_q4']:,.0f}",
                       "for: mortgage rates above 7% in October and November 2026",
                       f"against: a range already cut, and {C['a26'][1]:,.0f} closings in a year it called challenging"], size=18).move_to([0, -0.5, 0])
        rule = tx("scored on D.R. Horton's fiscal 2027 results, due October 2027", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             f"Now ours. <bookmark mark='a'/> We say D.R. Horton will close fewer than {C['call']:,.0f} homes in fiscal "
             f"2027, the middle of its own range, and give it {100 * C['prob']:.0f} per cent. <bookmark mark='b'/> For: it "
             f"fell short of last year's range, its orders in the last quarter fell seven per cent, and mortgage rates "
             "have risen above seven. Against: it has already cut its range, and it closed "
             f"{C['a26'][1]:,.0f} homes in a year it called challenging. <bookmark mark='c'/> Its results next October will "
             "settle it, and the call stays in the log either way.",
             base=[tag], steps=[claim, why, rule])
