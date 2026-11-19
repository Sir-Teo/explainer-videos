from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403

TOP = 200.0


def seasons(center=LEFT * 3.0 + DOWN * 0.3):
    return plane([0, TOP], [0, TOP], center=center, x_length=5.6, y_length=5.6, xticks=[0, 50, 100, 150, 200],
                 yticks=[0, 50, 100, 150, 200], xlabel=r"$c_1$: \ this season (\$)", ylabel=r"$c_2$: \ next season (\$)",
                 font_size=18)


def budget(ax, y1, y2, r, color=TODAY, width=3.2):
    a = ax.ax
    w = y1 + y2 / (1 + r)
    return Line(a.c2p(w, 0), a.c2p(0, min(w * (1 + r), TOP)) if w * (1 + r) <= TOP else
                a.c2p(w - TOP / (1 + r), TOP), color=color, stroke_width=width)


class Fisher(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Fisher's two periods", r"What does an interest rate do to what people spend now and save for "
             r"later?", "Chapter one. Fisher's two periods.", lit={1930: r"Fisher's \emph{Theory of Interest}"},
             scale=("person", "household"))
        self.setup_plane()
        self.euler()
        self.rate_rises()
        self.three_savers()

    def base(self):
        f = load("fisher")
        ax = seasons()
        a = ax.ax
        y1, y2 = f["y"]
        E_ = Dot(a.c2p(y1, y2), radius=0.1, color=WHO["chidi"])
        El = label(r"E: \ the harvest", font_size=19, color=WHO["chidi"]).next_to(E_, UR, buff=0.06)
        bl = budget(ax, y1, y2, f["r0"])
        ic0 = path(ax, f["c1s"], f["ic0"], color=LATER, width=3, xr=(0, TOP), yr=(0, TOP))
        A = Dot(a.c2p(f["f0"]["c1"], f["f0"]["c2"]), radius=0.1, color=CHOICE)
        Al = label(r"A", font_size=24).next_to(A, DL, buff=0.06)
        return f, ax, a, E_, El, bl, ic0, A, Al

    def setup_plane(self):
        f, ax, a, E_, El, bl, ic0, A, Al = self.base()
        y1, y2 = f["y"]
        w = f["f0"]["wealth"]
        side = VGroup(
            label(r"Chidi's coconuts: \ \$120 this season, \\ \$40 the next (the dry season)", font_size=25),
            label(r"Dara lends and borrows at \ $r$ = 10\% a season", font_size=25, color=TODAY),
            label(r"one dollar now trades for \$1.10 later: \\ the interest rate is a price, \ the price of now",
                  font_size=24, color=TODAY),
            label(rf"what he can have: \ $c_1 + \dfrac{{c_2}}{{1+r}} = {y1:.0f} + \dfrac{{{y2:.0f}}}{{1.1}} = "
                  rf"{w:.2f}$", font_size=25),
            label(r"what he likes: \ $u(c_1) + \beta\,u(c_2)$, \ $\beta = 0.9$", font_size=25, color=LATER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        hc = history_card(1930, r"Irving Fisher, \ \emph{The Theory of Interest}", r"interest comes from two "
                          r"things: \ impatience, \ and the opportunity to invest", color=TODAY, width=5.6,
                          font_size=22).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        with self.voiceover(
            "In 1930 Irving Fisher published The Theory of Interest, and in it a diagram that became the atom of "
            "macroeconomics. Put this season's consumption across and next season's up. <bookmark mark='a'/> Chidi's "
            "coconut harvest is worth a hundred and twenty dollars this season and forty the next, the dry season. "
            "Without trade, that's what he eats: the point E. <bookmark mark='b'/> But Dara now lends and borrows at "
            "ten percent a season. <bookmark mark='c'/> A dollar given up now buys a dollar ten later, so the "
            "interest rate is a price: the price of having things now, in units of having them later. "
            "<bookmark mark='d'/> Everything Chidi can reach lies on a line through his harvest with slope minus one "
            "point one. Its equation says the present value of what he eats equals the present value of what he "
            "earns: a hundred and fifty-six dollars thirty-six. <bookmark mark='e'/> What he likes is utility now "
            "plus utility later, discounted by a factor beta of nought point nine: he is a little impatient."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hc), FadeIn(E_), FadeIn(El), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(bl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Create(ic0), FadeIn(A), FadeIn(Al))
        self.clear_scene()

    def euler(self):
        f, ax, a, E_, El, bl, ic0, A, Al = self.base()
        f0 = f["f0"]
        lend = Arrow(a.c2p(f["y"][0], 18), a.c2p(f0["c1"], 18), color=TODAY, buff=0.05, stroke_width=4,
                     max_tip_length_to_length_ratio=0.2)
        lend_l = label(rf"lends \${f0['saving']:.2f}", font_size=19, color=TODAY).next_to(lend, UP, buff=0.08)
        eq = VGroup(
            MathTex(r"u'(c_1) \;=\; \beta\,(1+r)\,u'(c_2)", font_size=44, color=WHITE),
            label(r"the Euler equation: \ a dollar eaten now is worth \\ the same as \$1.10 eaten later", font_size=24,
                  color=GREY_A),
            MathTex(r"u(c) = \frac{c^{1-\gamma}}{1-\gamma}: \qquad \frac{c_2}{c_1} = \bigl(\beta(1+r)\bigr)^{1/\gamma}",
                    font_size=34, color=LATER),
            label(rf"$\gamma = 2$: \ $c_1 = {f0['c1']:.1f}$, \ $c_2 = {f0['c2']:.1f}$", font_size=27),
            label(r"$1/\gamma$: \ the elasticity of intertemporal substitution \\ (the EIS): \ how much the growth "
                  r"of consumption \\ answers the interest rate", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Chidi's best choice is where his indifference curve just touches the line: the point A. He eats "
            "eighty-two dollars' worth this season and lends the rest, <bookmark mark='a'/> thirty-seven dollars "
            "ninety, to have eighty-two next season too. <bookmark mark='b'/> At that point the slope of the curve "
            "equals the slope of the line, which in symbols is the Euler equation: the marginal utility of a dollar "
            "now equals beta times one plus r times the marginal utility of a dollar later. Give up a dollar now, "
            "get a dollar ten later, and at the best choice it's a wash. <bookmark mark='c'/> With the usual utility "
            "function, the power function with curvature gamma, the Euler equation says how fast consumption grows: "
            "the ratio of later to now is beta times one plus r, to the power one over gamma. "
            "<bookmark mark='d'/> Chidi's gamma is two. Beta times one point one is nought point nine nine, so his "
            "consumption is almost flat: eighty-two point one, then eighty-one point seven. "
            "<bookmark mark='e'/> One over gamma has a name: the elasticity of intertemporal substitution. It says "
            "how much the growth of consumption responds to the interest rate. Remember it; it comes back several "
            "times in this part."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(E_), FadeIn(El), Create(bl), Create(ic0), FadeIn(A), FadeIn(Al))
            vo.wait_until("a")
            self.play(GrowArrow(lend), FadeIn(lend_l))
            vo.wait_until("b")
            self.play(FadeIn(eq[0]), FadeIn(eq[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq[2]))
            vo.wait_until("d")
            self.play(FadeIn(eq[3]))
            vo.wait_until("e")
            self.play(FadeIn(eq[4]))
        self.clear_scene()

    def rate_rises(self):
        f, ax, a, E_, El, bl, ic0, A, Al = self.base()
        f1 = f["f1"]
        y1, y2 = f["y"]
        new = budget(ax, y1, y2, f["r1"], color=RISKY)
        ic1 = path(ax, f["c1s"], f["ic1"], color=LATER, width=3, xr=(0, TOP), yr=(0, TOP))
        C = Dot(a.c2p(f1["c1"], f1["c2"]), radius=0.08, color=RISKY)
        # a magnified view round A, where the three points sit close together
        lo1, hi1, lo2, hi2 = 72.0, 92.0, 74.0, 94.0
        zx = plane([lo1, hi1], [lo2, hi2], center=RIGHT * 3.9 + DOWN * 1.85, x_length=3.2, y_length=3.2,
                   xticks=[75, 80, 85, 90], yticks=[75, 80, 85, 90], font_size=14)
        z = zx.ax
        frame = SurroundingRectangle(VGroup(Dot(a.c2p(lo1, lo2)), Dot(a.c2p(hi1, hi2))), buff=0.0, color=GREY_B,
                                     stroke_width=1.5)
        link = DashedLine(frame.get_right(), zx.get_left(), color=GREY_C, stroke_width=1.5)

        def zline(r_, color):
            w = y1 + y2 / (1 + r_)
            xs = np.linspace(lo1, hi1, 50)
            ys = (w - xs) * (1 + r_)
            return path(zx, xs, ys, color=color, width=3, xr=(lo1, hi1), yr=(lo2, hi2), smooth=False)

        zb0, zb1 = zline(f["r0"], TODAY), zline(f["r1"], RISKY)
        zi0 = path(zx, f["c1s"], f["ic0"], color=LATER, width=2.5, xr=(lo1, hi1), yr=(lo2, hi2))
        zi1 = path(zx, f["c1s"], f["ic1"], color=LATER, width=2.5, xr=(lo1, hi1), yr=(lo2, hi2))
        # Hicks's compensated line: the new slope, tangent to the old curve at B
        hb = f["hicks_c1"] + f["hicks_c2"] / (1 + f["r1"])
        xs = np.linspace(lo1, hi1, 50)
        zh = DashedVMobject(path(zx, xs, (hb - xs) * (1 + f["r1"]), color=UTIL, width=2.5, xr=(lo1, hi1),
                                 yr=(lo2, hi2), smooth=False), num_dashes=18)
        pa = z.c2p(f["f0"]["c1"], f["f0"]["c2"])
        pb = z.c2p(f["hicks_c1"], f["hicks_c2"])
        pc = z.c2p(f1["c1"], f1["c2"])
        zA = VGroup(Dot(pa, radius=0.08, color=CHOICE), label(r"A", font_size=19).next_to(pa, DR, buff=0.04))
        zB = VGroup(Dot(pb, radius=0.08, color=UTIL), label(r"B", font_size=19, color=UTIL).next_to(pb, LEFT,
                                                                                                    buff=0.06))
        zC = VGroup(Dot(pc, radius=0.08, color=RISKY), label(r"C", font_size=19, color=RISKY).next_to(pc, RIGHT,
                                                                                                      buff=0.06))
        sub_ = Arrow(pa, pb, color=UTIL, buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        inc_ = Arrow(pb, pc, color=RISKY, buff=0.08, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        ds = f["hicks_c1"] - f["f0"]["c1"]
        di = f1["c1"] - f["hicks_c1"]
        side = VGroup(
            label(r"Dara raises the rate: \ 10\% $\to$ 30\%; \ the line pivots \\ through the harvest", font_size=23,
                  color=RISKY),
            label(rf"substitution, A $\to$ B: \ now is dearer: \ $c_1$ {signed(ds, 1)}", font_size=22, color=UTIL),
            label(rf"income, B $\to$ C: \ a lender is richer: \ $c_1$ {signed(di, 1)}", font_size=22, color=RISKY),
            label(rf"together: \ $c_1$ {signed(f1['c1'] - f['f0']['c1'], 1)}; \ saving barely moves", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        borrower = label(r"for a borrower the income effect turns round, \\ and both push saving up", font_size=20,
                         color=GREY_A).next_to(side, DOWN, buff=0.2).align_to(side, LEFT)
        with self.voiceover(
            "Now Dara raises the interest rate, from ten percent to thirty. <bookmark mark='a'/> The line pivots "
            "around the harvest point, because Chidi can always just eat his harvest. It gets steeper: now is "
            "dearer. The three points that matter sit close together, so here they are magnified. "
            "<bookmark mark='b'/> As in Part six, the change does two things. Now is more expensive relative to "
            "later, so Chidi substitutes toward later: holding his satisfaction fixed, he would eat three dollars "
            "less this season. <bookmark mark='c'/> But Chidi is a lender, and a higher rate makes a lender richer: "
            "that income effect pushes his consumption now back up, by a little over three dollars. "
            "<bookmark mark='d'/> The two almost cancel. His saving barely moves. <bookmark mark='e'/> For a "
            "borrower the income effect turns round, and both effects push saving up. Whether a higher interest rate "
            "makes people save more is not something theory can tell you."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(E_), FadeIn(El), Create(bl), Create(ic0), FadeIn(A), FadeIn(Al))
            self.play(FadeIn(side[0]))
            vo.wait_until("a")
            self.play(TransformFromCopy(bl, new), Create(ic1), FadeIn(C))
            self.play(Create(frame), Create(link), FadeIn(zx), Create(zb0), Create(zb1), Create(zi0), Create(zi1),
                      FadeIn(zA))
            vo.wait_until("b")
            self.play(Create(zh), FadeIn(zB), GrowArrow(sub_), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(zC), GrowArrow(inc_), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(borrower))
        self.clear_scene()

    def three_savers(self):
        f = load("fisher")
        rates = np.array(f["rates"])
        ax = plane([0, 0.5], [25, 60], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.0, y_length=5.0,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[30, 40, 50, 60],
                   xlabel=r"interest rate a season", ylabel=r"saving this season, \ \$", font_size=18,
                   xfmt=lambda v: f"{100 * v:.0f}\\%")
        cols = {"0.5": SAFE, "2": LATER, "8": RISKY}
        names = {"0.5": r"EIS 2", "2": r"EIS $\tfrac12$ (Chidi)", "8": r"EIS $\tfrac18$"}
        curves, labs = VGroup(), VGroup()
        for k, c in cols.items():
            ys = np.array(f["saving"][k])
            curves.add(path(ax, rates, ys, color=c, width=3.5))
            labs.add(label(names[k], font_size=20, color=c).next_to(ax.ax.c2p(0.5, ys[-1]), RIGHT, buff=0.12))
        side = VGroup(
            label(r"the same harvest and patience, \\ three elasticities of substitution", font_size=25),
            label(r"a high EIS: \ substitution wins, \\ saving rises with the rate", font_size=23, color=SAFE),
            label(r"a low EIS: \ the income effect wins, \\ saving falls", font_size=23, color=RISKY),
            label(r"how big is the EIS? \\ an empirical question: \ the intermission \\ and chapter 10 come back to "
                  r"it", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here's that point as a picture. Three choosers with Chidi's harvest and Chidi's patience, but different "
            "elasticities of substitution. <bookmark mark='a'/> With an elasticity of two, substitution wins: as the "
            "rate rises from zero to fifty percent, saving climbs from about thirty-two dollars to fifty-four. "
            "<bookmark mark='b'/> With Chidi's elasticity of a half, saving is nearly flat. With an eighth, the "
            "income effect wins and saving falls as the rate rises. <bookmark mark='c'/> So the effect of interest "
            "rates on saving, which every central bank and every tax on savings depends on, comes down to one number. "
            "We'll look for it in the data in the intermission, and again in chapter ten."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(labs[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(labs[1]), Create(curves[2]), FadeIn(labs[2]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
