from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

DEM = "#FFFFFF"
AC = "#F2A65A"
MC = "#7EC8F5"


class Diagram(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Selection in pictures: \ the Einav--Finkelstein diagram", r"Can adverse selection be measured "
             r"with nothing but a demand curve and a cost curve?", "Chapter eight. Selection in pictures: the "
             "Einav-Finkelstein diagram.", lit={2010: r"Einav, Finkelstein and Cullen"}, scale=("person", "firm",
                                                                                                 "market"),
             horizon=("a year",))
        self.picture()
        self.alcoa()
        self.policy()

    def curves(self, e, center=LEFT * 2.9 + DOWN * 0.3):
        D = np.array(e["D"])
        ax = plane([0.3, 0.95], [0, 1000], center=center, x_length=6.2, y_length=4.8,
                   xticks=[0.4, 0.6, 0.8], yticks=[0, 250, 500, 750, 1000], xlabel=r"share of employees buying the "
                   r"generous plan", ylabel=r"\$ a year", font_size=16, xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.0f}")
        keep = D >= 0.3
        dem = path(ax, D[keep], np.array(e["demand"])[keep], color=DEM, width=3.2, smooth=False, yr=(0, 1000))
        ac = path(ax, D[keep], np.array(e["ac"])[keep], color=AC, width=3.2, smooth=False, yr=(0, 1000))
        mc = path(ax, D[keep], np.array(e["mc"])[keep], color=MC, width=3.2, smooth=False, yr=(0, 1000))
        return ax, dem, ac, mc

    def picture(self):
        e = load("efc")
        ax, dem, ac, mc = self.curves(e)
        a = ax.ax
        dl = label(r"demand: \ willingness to pay", font_size=15, color=DEM).next_to(a.c2p(0.36, 900), RIGHT, buff=0.05)
        acl = label(r"average cost of those who buy", font_size=15, color=AC).next_to(a.c2p(0.85, 420), DOWN, buff=0.1)
        mcl = label(r"marginal cost: \ the cost of the marginal buyer", font_size=15, color=MC).next_to(
            a.c2p(0.62, 230), DOWN, buff=0.2)
        side = VGroup(
            label(r"Liran Einav and Amy Finkelstein: \\ selection is a cost curve that slopes", font_size=21),
            label(r"the first to buy at a high price \\ are those who expect to need it most: \\ so average cost "
                  r"falls as more buy", font_size=21, color=AC),
            label(r"marginal cost: \ the cost of the last buyer \\ to join, \ below the average", font_size=21,
                  color=MC),
            label(r"competitive insurers price at average cost: \\ C, \ where demand meets average cost", font_size=21,
                  color=EQ),
            label(r"efficiency needs price at marginal cost: \\ E; \ the shaded triangle is the waste", font_size=21,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        Ds = np.linspace(e["D_eq"], e["D_eff"], 40)
        b = -0.00070
        Pd = (Ds - 0.940) / b
        mcd = np.interp(Ds, np.array(e["D"]), np.array(e["mc"]))
        tri = Polygon(*[a.c2p(x, y) for x, y in zip(Ds, Pd)], *[a.c2p(x, y) for x, y in zip(Ds[::-1], mcd[::-1])],
                      stroke_width=0, fill_color=LOSS, fill_opacity=0.5)
        C = Dot(a.c2p(e["D_eq"], e["p_eq"]), radius=0.09, color=EQ)
        Cl = label(r"C", font_size=18, color=EQ).next_to(C, UR, buff=0.05)
        E_ = Dot(a.c2p(e["D_eff"], e["p_eff"]), radius=0.09, color=LOSS)
        El = label(r"E", font_size=18, color=LOSS).next_to(E_, UR, buff=0.05)
        tag = published_tag(r"Einav and Finkelstein, JEP 25(1) (2011); \ Einav, Finkelstein and Cullen, QJE 125(3) "
                            r"(2010)", corner=DR, font_size=12)
        with self.voiceover(
            "In 2010 Liran Einav, Amy Finkelstein and Mark Cullen showed how to measure all this with two curves. "
            "<bookmark mark='a'/> Plot the share of people buying generous insurance against its price. Demand is the "
            "familiar downward-sloping curve. Selection shows up in the other curve: the people who buy at a high "
            "price are those who expect to need it most, so as the price falls and more people buy, the average cost "
            "of the insured falls too. <bookmark mark='b'/> The marginal cost, the cost of the last buyer to join, "
            "lies below the average. <bookmark mark='c'/> Competitive insurers must cover their average cost, so the "
            "market settles at C, where demand meets average cost. <bookmark mark='d'/> Efficiency needs everyone to "
            "buy whose value exceeds their own cost: point E, where demand meets marginal cost. Between C and E are "
            "people who value the cover more than it would cost to give them, but less than the price. The shaded "
            "triangle is the waste."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(dl), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ac), FadeIn(acl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(mc), FadeIn(mcl), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(C, scale=1.5), FadeIn(Cl), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(E_, scale=1.5), FadeIn(El), FadeIn(tri), FadeIn(side[4]))
        self.clear_scene()

    def alcoa(self):
        e = load("efc")
        p = e["paper"]
        ax, dem, ac, mc = self.curves(e)
        a = ax.ax
        C = Dot(a.c2p(e["D_eq"], e["p_eq"]), radius=0.09, color=EQ)
        E_ = Dot(a.c2p(e["D_eff"], e["p_eff"]), radius=0.09, color=LOSS)
        side = VGroup(
            label(rf"Alcoa: \ the extra premium for its generous plan \\ varied across the company's divisions, \\ "
                  rf"from \${p['price_range'][0]} to \${p['price_range'][1]}", font_size=20),
            label(rf"demand: \ ${p['demand'][0]:.3f} {p['demand'][1]:.5f}\,p$ \\ cost: \ ${p['cost'][0]:.1f} + "
                  rf"{p['cost'][1]:.3f}\,p$ \ (they estimated both)", font_size=20, color=AC),
            label(rf"C: \ \${e['p_eq']:.0f}; \ E: \ \${e['p_eff']:.0f}; \\ {100 * e['share_drop']:.0f} points fewer buy "
                  r"than should", font_size=21, color=EQ),
            label(rf"the triangle: \ \${e['loss']:.2f} a year per employee \\ (the paper: \${p['loss']:.2f}), \ about "
                  rf"{100 * p['loss_share_surplus']:.0f}\% of what's at stake", font_size=21, color=LOSS),
            label(r"adverse selection is real, \ and its cost is small", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Einav, Finkelstein and Cullen, NBER WP 14414 (2008), Table 4; \ the rebuild: \ Agora",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The curves are the paper's own. <bookmark mark='a'/> At the aluminium company Alcoa, the extra premium "
            "an employee paid for the generous plan differed across the company's divisions, from three hundred and "
            "eighty-four to six hundred and fifty-nine dollars a year, in ways the authors show were unrelated to "
            "what the managers setting them could see about their employees. "
            "<bookmark mark='b'/> That variation traced out both curves: the share choosing the generous plan, and the "
            "average extra cost of those who did, which rose with the price, the signature of adverse selection. "
            "<bookmark mark='c'/> Agora rebuilds the diagram from their two estimated lines. The market settles at "
            "about four hundred and sixty-four dollars; the efficient price is about two hundred and sixty-six; and "
            "fourteen percentage points fewer employees buy than should. <bookmark mark='d'/> The triangle comes to "
            "nine dollars and forty-six cents a year per employee, against the nine fifty-five they report, about "
            "three percent of the surplus at stake. <bookmark mark='e'/> So adverse selection is real and measurable, "
            "and in this market its cost is small."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), Create(ac), Create(mc), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(C, scale=1.5), FadeIn(E_, scale=1.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def policy(self):
        e = load("efc")
        p = e["paper"]
        rows = VGroup(
            label(r"could policy close the triangle?", font_size=27, color=E.ACCENT),
            label(r"a subsidy that lowers the price from C to E would get the right people insured", font_size=23),
            label(rf"but each dollar of tax costs more than a dollar: \ at the usual 30 cents extra, \ the subsidy "
                  rf"costs about \${e['subsidy_cost']:.0f} a head", font_size=23, color=LOSS),
            label(rf"to save \${e['loss']:.2f}: \ about five times the gain \ (the paper: \${p['subsidy_cost']} "
                  rf"against \${p['loss']:.2f})", font_size=23, color=LOSS),
            label(r"a mandate to buy the generous plan could cost more still: \ many value it below its cost",
                  font_size=23, color=GREY_A),
            label(r"the lesson: \ measure the triangle before reaching for a remedy", font_size=24, color=EQ),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"Einav, Finkelstein and Cullen (2008), section 4.3", corner=DR, font_size=13)
        with self.voiceover(
            "Could policy close the triangle? <bookmark mark='a'/> A subsidy that cut the price from C to E would get "
            "exactly the right people insured. <bookmark mark='b'/> But every dollar raised in tax costs society more "
            "than a dollar, because taxes distort; at the conventional thirty cents extra per dollar, that subsidy "
            "would cost about forty-five dollars a head, <bookmark mark='c'/> to save nine and a half: some five times "
            "the gain. <bookmark mark='d'/> A mandate to buy the generous plan could cost more still, since many "
            "employees value it below what it costs to cover them. <bookmark mark='e'/> The lesson of the diagram is "
            "to measure the triangle before reaching for a remedy."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
