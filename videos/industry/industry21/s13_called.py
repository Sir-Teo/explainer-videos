from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 11, "Called it?", "How well does a device maker forecast its own operations?",
             "Chapter eleven. Called it? How well does a device maker forecast how many operations surgeons will do with "
             "its machines?", lit=("change",))
        self.intuitive()
        self.why()
        self.ours()

    def intuitive(self):
        C = R["called"]
        pa = viz.plot_axes([10, 20], [0, 2], x_length=10.0, y_length=2.6, xticks=[10, 12, 14, 16, 18, 20],
                           xfmt=lambda v: f"{int(v)}%", grid=False, size=13).move_to([0.4, 0.3, 0])
        ax = pa.ax
        y25, y26 = 1.5, 0.5
        r25 = Line(ax.c2p(C["g2025"][0], y25), ax.c2p(C["g2025"][1], y25), stroke_color=PRICE, stroke_width=12)
        l25 = tx(f"January 2025: {C['g2025'][0]}-{C['g2025'][1]}% growth in 2025", 14, PRICE).next_to(r25, UP, buff=0.12)
        a25 = marker(ax, C["a2025"], y25, f"actual: {C['a2025']}%", GOOD, side=RIGHT)
        r26 = Line(ax.c2p(C["g2026"][0], y26), ax.c2p(C["g2026"][1], y26), stroke_color=PRICE, stroke_width=12)
        l26 = tx(f"January 2026: {C['g2026'][0]}-{C['g2026'][1]}% in 2026", 14, PRICE).next_to(r26, DOWN, buff=0.12)
        r26b = Line(ax.c2p(C["g2026_oct"][0], y26 + 0.25), ax.c2p(C["g2026_oct"][1], y26 + 0.25), stroke_color=GOOD, stroke_width=12)
        l26b = tx(f"October 2026: {C['g2026_oct'][0]}-{C['g2026_oct'][1]}%, 'closer to the midpoint'", 14, GOOD, bold=True).next_to(r26b, UP, buff=0.12)
        nm = VGroup(tx("2025", 20, WHITE, bold=True).next_to(ax.c2p(10, y25), LEFT, buff=0.3),
                    tx("2026", 20, WHITE, bold=True).next_to(ax.c2p(10, y26), LEFT, buff=0.3))
        xl = tx("growth in da Vinci operations worldwide", 14, GREY_B).next_to(pa, DOWN, buff=0.3)
        src = source("Intuitive Surgical, Inc., Forms 8-K of 23 January 2025, 22 January 2026 and 20 October 2026; Form 10-K "
                     "2025", size=12)
        beat(self,
             "Intuitive publishes a forecast of how fast operations with its robots will grow. <bookmark mark='a'/> In "
             f"January 2025 it expected {C['g2025'][0]} to {C['g2025'][1]} per cent growth in 2025. <bookmark mark='b'/> "
             f"Operations grew {C['a2025']} per cent, above the top of its range. <bookmark mark='c'/> In January 2026 it "
             f"expected {C['g2026'][0]} to {C['g2026'][1]} per cent for 2026, <bookmark mark='d'/> and in October it "
             f"narrowed that to {C['g2026_oct'][0]} to {C['g2026_oct'][1]} per cent, closer to the middle. Its forecasts "
             "have leaned low, like Lilly's in Part 20.",
             base=[pa, nm, xl, src], steps=[[r25, l25], a25, [r26, l26], [r26b, l26b]])

    def why(self):
        C = R["called"]
        c = stat_cards([(f"+{C['a2025']}%", "da Vinci operations, 2025", DEVICE),
                        (f"+{C['ia_growth']}%", "instruments and accessories revenue, 2025", GOOD),
                        (f"+{C['q3_growth']}% / +{C['q3_ia_growth']}%", "operations / instruments revenue, third quarter 2026", PRICE)],
                       y=0.6, size=38, span=12)
        note = tx("The forecast of operations is a forecast of the instrument business.", 19, WHITE, bold=True).move_to([0, -1.6, 0])
        src = source("Intuitive Surgical, Inc., Form 10-K 2025 and Form 8-K of 20 October 2026", size=12)
        beat(self,
             "Why forecast operations rather than revenue? Because operations drive the instruments. <bookmark mark='a'/> "
             f"In 2025 operations grew {C['a2025']} per cent <bookmark mark='b'/> and instrument revenue "
             f"{C['ia_growth']} per cent. <bookmark mark='c'/> In the third quarter of 2026, operations grew "
             f"{C['q3_growth']} per cent and instrument revenue {C['q3_ia_growth']}, to {C['q3_ia']:.2f} billion dollars. "
             "<bookmark mark='d'/> Count the operations and you have most of the business.",
             base=[src], steps=[c[0], c[1], c[2], note])

    def ours(self):
        C = R["called"]
        claim = VGroup(tx("Our call, 27 November 2026", 20, PRICE, bold=True),
                       tx("Intuitive will report 2026 growth in da Vinci operations of 15% or more.", 21, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 22, PRICE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0, 1.7, 0])
        why = bullets([f"for: the first nine months grew {C['nine']}%, and it beat its range in 2025",
                       f"against: the third quarter grew {C['q3_growth']}%, and the company points below the top of its range",
                       f"third quarter of 2026: {C['q3'] / 1e3:,.0f} thousand operations; {C['base_q3']:,} robots installed"],
                      size=18).move_to([0, -0.4, 0])
        rule = tx("scored on the growth Intuitive reports for 2026, as rounded in its January 2027 release", 15, GREY_B).to_edge(DOWN, buff=0.7)
        tag = estimate_tag("this series' call, logged in explainer/industry/calls.py", size=12)
        beat(self,
             "Now ours. <bookmark mark='a'/> We say Intuitive will report growth of fifteen per cent or more in da Vinci "
             f"operations for 2026, as it rounds the number, and give it {100 * C['prob']:.0f} per cent. "
             f"<bookmark mark='b'/> For: the first nine months grew {C['nine']} per cent, and last year it beat its own "
             f"range. Against: growth slowed to {C['q3_growth']} per cent in the third quarter, and the company itself now "
             "points to the middle of its range, fourteen and a half. <bookmark mark='c'/> A little worse than a coin. "
             "Intuitive's release in January will settle it: if it reports fourteen per cent, we were wrong, and the call "
             "stays in the log.",
             base=[tag], steps=[claim, why, rule])
