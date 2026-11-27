from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Boom(VoiceoverScene):
    def construct(self):
        card(self, 9, "A boom: the weight-loss drugs", "What does it look like when a drug works for millions?",
             "Chapter nine. A boom. What does it look like when a new class of drug works for millions of people?",
             lit=("change",))
        self.lilly()
        self.abroad()
        self.build()
        self.q3()

    def abroad(self):
        Mj = R["mounjaro"]
        items = [("outside the US, 2024", Mj["ex24"], BIO, f"${Mj['ex24']:.1f}bn"), ("outside the US, 2025", Mj["ex"], BIO, f"${Mj['ex']:.1f}bn"),
                 ("in the US, 2025", Mj["us"], LAB, f"${Mj['us']:.1f}bn")]
        rows = hbars(items, max_value=15, x0=-0.4, top=1.4, row=1.0, length=6.0, size=17, bar_h=0.5)
        src = source("Eli Lilly and Company, Form 10-K 2025: Mounjaro revenue in and outside the US", size=12)
        beat(self,
             "And it is spreading. <bookmark mark='a'/> Mounjaro sold "
             f"{Mj['ex24']:.1f} billion dollars outside America in 2024, <bookmark mark='b'/> and {Mj['ex']:.1f} billion "
             f"in 2025, more than three times as much. <bookmark mark='c'/> In America it sold {Mj['us']:.1f} billion. "
             "The boom that began in America is now spreading around the world. Its twin, Zepbound, the same molecule "
             f"sold for obesity, is another matter: of its {Mj['zep']:.1f} billion dollars in 2025, {Mj['zep_us']:.1f} "
             "billion came from America, where it is paid for by insurers and, a growing share, by patients themselves "
             "through Lilly's own direct-to-patient platform.",
             base=[rows.axis, head("Mounjaro, in and outside the United States"), src], steps=[rows[0], rows[1], rows[2]])

    def lilly(self):
        H = R["hook"]
        C = R["called"]
        t = H["tirz"]
        items = [("2024: tirzepatide", t[2024], LAB, f"${t[2024]:.1f}bn"), ("2025: tirzepatide", t[2025], LAB, f"${t[2025]:.1f}bn")]
        rows = hbars(items, max_value=40, x0=-0.6, top=1.4, row=1.1, length=6.0, size=17, bar_h=0.55)
        rev = tx(f"Lilly's total revenue: ${R['rnd']['lly_rev']:.1f}bn in 2025, up 45%", 18, WHITE, bold=True).to_edge(DOWN, buff=0.9)
        inj = draw.vial(1.4, LAB).move_to([-5.4, -1.2, 0])
        src = source("Eli Lilly and Company, Form 10-K 2025: revenue by product", size=12)
        beat(self,
             "The newest blockbusters are a class of injected drugs for diabetes and for weight loss. "
             "<bookmark mark='a'/> Lilly's version, tirzepatide, sold "
             f"{t[2024]:.1f} billion dollars in 2024 <bookmark mark='b'/> and {t[2025]:.1f} billion in 2025. "
             "<bookmark mark='c'/> Lilly's revenue rose forty-five per cent in a year. A protected drug that works for a "
             "common condition can grow very fast indeed.",
             base=[rows.axis, inj, head("Eli Lilly: a boom in one molecule"), src], steps=[rows[0], rows[1], rev])

    def build(self):
        Bd = R["build"]
        cx = Bd["capex"]
        items = [(str(y), v, PRICE, f"${v:.1f}bn") for y, v in sorted(cx.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.2, width=1.2, gap=0.7, x0=-5.0)
        fac = VGroup(*[draw.factory(0.9, LAB).move_to([0.9 + 1.25 * (i % 5), 1.5 - 1.2 * (i // 5), 0]) for i in range(int(Bd["sites"]))])
        sl = tx(f"{Bd['sites']:.0f} new sites: North Carolina, Wisconsin, Indiana, Virginia, Texas, Alabama, Pennsylvania, "
                "Ireland, Germany, the Netherlands", 13, GREY_A).to_edge(DOWN, buff=0.75)
        if sl.width > 13:
            sl.scale_to_fit_width(13)
        inv = Bd["inventory"]
        it = tx(f"inventories: ${inv[2023]:.1f}bn (2023) to ${inv[2025]:.1f}bn (2025)", 17, WHITE, bold=True).move_to([3.4, -1.3, 0])
        src = source("Eli Lilly and Company, Form 10-K 2025: purchases of property and equipment; raw materials and product supply", size=12)
        beat(self,
             "A boom in a medicine is also a boom in factories. The molecule is cheap to make once a plant exists, but the "
             "plants take years to build and approve. <bookmark mark='a'/> Lilly spent "
             f"{cx[2023]:.1f} billion dollars on property and equipment in 2023, {cx[2024]:.1f} billion in 2024 "
             f"<bookmark mark='b'/> and {cx[2025]:.1f} billion in 2025, and says the figure will be meaningfully higher in "
             f"the near term. <bookmark mark='c'/> Its report lists {Bd['sites']:.0f} new manufacturing sites, from North "
             "Carolina to the Netherlands. <bookmark mark='d'/> Its stock of drugs and materials more than doubled in two "
             f"years, and it has signed supply contracts that could cost it up to about {Bd['commit']:.0f} billion dollars "
             "if demand falls short. A drug company that guesses demand wrong is left with empty plants; one that guesses it "
             "low is left with patients it cannot supply.",
             base=[head("Lilly builds"), src], steps=[VGroup(*bars_[:2]), bars_[2], [fac, sl], it])

    def q3(self):
        C = R["called"]
        c = stat_cards([(f"${C['q3']:.1f}bn", "Lilly's revenue in the third quarter of 2026, up 39%", LAB),
                        (f"${C['g2026_oct'][0]:.0f}-{C['g2026_oct'][1]:.0f}bn", "its forecast for 2026, raised in October", PRICE)],
                       y=0.6, size=44, span=11)
        note = tx("Prices are already lower in America; the patent's date will come too.", 18, GREY_A).move_to([0, -1.6, 0])
        src = source("Eli Lilly and Company, Form 8-K of 29 October 2026 (third-quarter results)", size=12)
        beat(self,
             f"And the boom continues. <bookmark mark='a'/> In the third quarter of 2026 Lilly's revenue was "
             f"{C['q3']:.1f} billion dollars, thirty-nine per cent more than a year earlier. <bookmark mark='b'/> It now "
             f"expects {C['g2026_oct'][0]:.0f} to {C['g2026_oct'][1]:.0f} billion dollars for the year. "
             "<bookmark mark='c'/> Lilly's own report notes lower realized prices for these drugs in America, and every "
             "patent has its date. The same economics that make the boom will, one day, make the cliff.",
             base=[src], steps=[c[0], c[1], note])
