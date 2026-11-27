from __future__ import annotations

from videos.industry.industry26.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.index()
        self.office()
        self.formula()
        self.title()

    def index(self):
        H = R["hook"]
        q = H["q"]
        idx = H["idx"]
        ch = line_chart({"commercial property prices": (idx, VALUE)}, x=(1990, 2026.5), y=(50, 250),
                        xticks=[1990, 2000, 2007, 2010, 2016, 2023, 2026], yticks=[50, 100, 150, 200, 250],
                        yfmt=lambda v: f"{v:.0f}", ylabel="American commercial property prices, 2001 = 100 (not adjusted for inflation)",
                        width=9.6, height=4.4, center=(-0.5, -0.45), label_end=False)
        a, b, c, d, e = (q[H[k]] for k in ("pk1", "lo1", "pk2", "lo2", "last"))
        m1 = marker(ch.ax, a, idx[a], f"{H['pk1'][:4]}: {idx[a]:.0f}", VALUE, side=UP)
        m2 = marker(ch.ax, b, idx[b], f"{H['lo1'][:4]}: {idx[b]:.0f}  ({100 * H['fall1']:.0f}%)", BAD, side=DOWN)
        m3 = marker(ch.ax, c, idx[c], f"{H['pk2'][:4]}: {idx[c]:.0f}", VALUE, side=UP)
        m4 = marker(ch.ax, d, idx[d], f"{H['lo2'][:4]}: {idx[d]:.0f}  ({100 * H['fall2']:.0f}%)", BAD, side=DOWN)
        tower = draw.office_tower(0.9).move_to([5.6, 0.4, 0])
        draw.light(tower.windows, 0.9)
        src = source("Federal Reserve, Financial Accounts of the United States (Z.1): commercial real estate price index, quarterly, via FRED", size=12)
        beat(self,
             "Every quarter the Federal Reserve publishes an index of what American commercial buildings sell for: offices, "
             "shops, warehouses, flats. <bookmark mark='a'/> In the summer of 2007 it stood at "
             f"{idx[a]:.0f}, against 100 in 2001. <bookmark mark='b'/> By the end of 2009 it had fallen "
             f"{abs(100 * H['fall1']):.0f} per cent. <bookmark mark='c'/> It climbed to a new high in the spring of 2023, "
             f"<bookmark mark='d'/> then fell {abs(100 * H['fall2']):.0f} per cent in two years, before recovering "
             f"{100 * H['since']:.0f} per cent by mid-2026. The buildings themselves barely changed: the same floors, the same "
             "lifts, the same addresses. Something else moved their price.",
             base=[ch.frame, tower, src], steps=[[ch.lines["commercial property prices"], m1], m2, m3, m4])

    def office(self):
        G = R["hook"]["gmv"]
        t0 = draw.office_tower(1.1).move_to([-4.8, -0.3, 0])
        t1 = draw.office_tower(1.1, seed=11).move_to([-2.6, -0.3, 0])
        draw.light(t0.windows, 0.93)
        draw.light(t1.windows, 0.6)
        c = VGroup(*[VGroup(tx(a, 40, col, bold=True), tx(b, 17, GREY_A)).arrange(DOWN, buff=0.12)
                     for a, b, col in ((f"{G['short']:.0f}%", "New York office values, 2020", BAD),
                                       (f"{G['long']:.0f}%", "New York office values, the long run", BAD),
                                       (f"${G['us']:.0f}bn", "the long-run loss, all American offices", VALUE))]
                   ).arrange(DOWN, buff=0.45).move_to([2.6, 0.3, 0])
        src = source("Gupta, Mittal and Van Nieuwerburgh, 'Work From Home and the Office Real Estate Apocalypse', NBER Working "
                     "Paper 30526, September 2022", size=12)
        tag = estimate_tag("a model's estimate, not a price index", size=12)
        beat(self,
             "And the average hides the office. <bookmark mark='a'/> In 2022 three finance professors, Arpit Gupta, Vrinda "
             "Mittal and Stijn Van Nieuwerburgh, revalued New York's office buildings for a world that works from home: "
             f"lower rents, emptier floors, a higher risk. They estimated a fall of about {abs(G['short']):.0f} per cent in "
             f"2020, <bookmark mark='b'/> and {abs(G['long']):.0f} per cent in the long run. <bookmark mark='c'/> Extrapolated "
             f"to every office in America, a loss of about {G['us']:.0f} billion dollars of value. Not a building had fallen "
             "down.",
             base=[t0, t1, src, tag], steps=[c[0], c[1], c[2]])

    def formula(self):
        eq = MathTex(r"\text{value} = \frac{\text{net operating income}}{\text{capitalization rate}}", font_size=52,
                     color=WHITE).move_to([0, 1.7, 0])
        ex = VGroup(tx("$10m of income a year, at 5%:   $200m", 22, INCOME, bold=True),
                    tx("the same $10m, at 7.5%:   $133m", 22, RATE, bold=True),
                    tx("a third of the tenants gone, $3m, at 7.5%:   $40m", 22, BAD, bold=True)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.6, 0])
        tag = estimate_tag("the Works' office, chapter one", size=12)
        beat(self,
             "Here is what moved it. <bookmark mark='a'/> A commercial building is worth the income it earns, after its "
             "running costs, divided by a rate: the yield a buyer demands. <bookmark mark='b'/> Ten million dollars of income "
             "a year, at five per cent, is a two hundred million dollar building. <bookmark mark='c'/> The same income, when "
             "buyers want seven and a half, is worth a third less. <bookmark mark='d'/> And if a third of the tenants leave, "
             "the income can fall much further than the rent, because the building's costs do not leave with them. Two "
             "numbers set the price, and both can move while the building stands still.",
             base=[tag], steps=[eq, ex[0], ex[1], ex[2]])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-six: property. What is a building worth, and why does that number "
                            "move so much when the building does not?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
