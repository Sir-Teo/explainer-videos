from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE, live

RA, RD = 0.08, 0.04


class MM(VoiceoverScene):
    def construct(self):
        self.card()
        self.arbitrage()
        self.prop2()
        self.taxes()
        self.pie()
        self.survey()

    def card(self):
        c = chapter_card(10, r"Modigliani and Miller, with taxes and distress", r"Can borrowing make a firm worth more?",
                         lit=(1958,), part=PART)
        with self.voiceover("Chapter ten. Modigliani and Miller, with taxes and distress."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def firm(self, name, debt):
        box = RoundedRectangle(width=3.6, height=2.6, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2)
        assets = Rectangle(width=1.4, height=2.0, stroke_width=0, fill_color=VALUE, fill_opacity=0.7)
        al = MathTex(r"X", font_size=34).move_to(assets)
        claims = VGroup()
        if debt:
            d = Rectangle(width=1.4, height=0.8, stroke_width=0, fill_color=DEBT, fill_opacity=0.75)
            e = Rectangle(width=1.4, height=1.2, stroke_width=0, fill_color=EQUITY, fill_opacity=0.75)
            claims = VGroup(e, d).arrange(DOWN, buff=0)
            claims.add(MathTex(r"X - r_D D", font_size=24).move_to(e), MathTex(r"r_D D", font_size=24).move_to(d))
        else:
            e = Rectangle(width=1.4, height=2.0, stroke_width=0, fill_color=EQUITY, fill_opacity=0.75)
            claims = VGroup(e, MathTex(r"X", font_size=28).move_to(e))
        body = VGroup(VGroup(assets, al), claims).arrange(RIGHT, buff=0.3).move_to(box)
        claims.align_to(assets, DOWN)
        nm = label(name, font_size=24).next_to(box, UP, buff=0.15)
        caps = VGroup(label(r"assets", font_size=17, color=GREY_B).next_to(assets, DOWN, buff=0.08),
                      label(r"claims", font_size=17, color=GREY_B).next_to(claims, DOWN, buff=0.08))
        box.stretch_to_fit_height(box.height + 0.25).shift(DOWN * 0.1)
        return VGroup(box, body, nm, caps)

    def arbitrage(self):
        U = self.firm(r"firm U: no debt", False)
        L = self.firm(r"firm L: debt $D$ at $r_D$", True)
        VGroup(U, L).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.6)
        cap = label(r"the same assets, the same cash flow $X$ each year; only the claims differ", font_size=22,
                    color=GREY_B).next_to(VGroup(U, L), DOWN, buff=0.25)
        a = MathTex(r"\text{own } \alpha \text{ of L's equity:}", r"\quad \alpha\,(X - r_D D)", font_size=32)
        b = MathTex(r"\text{own } \alpha \text{ of U, borrow } \alpha D \text{ yourself:}", r"\quad \alpha X - \alpha\,r_D D",
                    font_size=32)
        a[1].set_color(EQUITY)
        b[1].set_color(EQUITY)
        c = cmath(r"E_L", r"=", r"V_U - D", r"\;\Rightarrow\;", r"V_L = E_L + D = V_U", font_size=40,
                  colors={r"V_L = E_L + D = V_U": VALUE})
        VGroup(a, b, c).arrange(DOWN, buff=0.35).next_to(cap, DOWN, buff=0.45)
        tag = why(r"Proposition I (1958): in a market without taxes or frictions, financing does not change value")
        tag.next_to(c, DOWN, buff=0.2)
        with self.voiceover(
            "In 1958 Franco Modigliani and Merton Miller asked whether a firm can make itself more valuable by how it is financed. "
            "Take two firms with identical assets, throwing off the same cash X each year. Firm U has no debt: its owners get all of "
            "X. Firm L has borrowed D at a rate r D: its lenders are paid first, and its owners get what is left. "
            "<bookmark mark='a'/> Owning a fraction alpha of L's shares pays alpha times X minus the interest. "
            "<bookmark mark='b'/> But you could build that payoff yourself: buy alpha of the unlevered firm and borrow alpha times D "
            "on your own account. You receive alpha X and pay alpha times the interest: the same cash, in every state of the world. "
            "<bookmark mark='c'/> Two identical payoffs must cost the same, or there is an arbitrage. So the levered firm is worth "
            "exactly the unlevered one. Leverage you can do at home is not worth paying a firm to do. It was the first no-arbitrage "
            "proof in finance, and a preview of Part nine."
        ) as vo:
            self.play(FadeIn(U), FadeIn(L), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(Write(c))
            self.play(FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def prop2(self):
        de = np.linspace(0, 3, 121)
        rE = valuation.mm_cost_of_equity(RA, RD, de)
        g = axes([0, 3], [0, 0.22], x_length=6.2, y_length=4.6, xlabel=r"leverage $D/E$", ylabel=r"required return",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.04, 0.08, 0.12, 0.16, 0.20], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lE = curve(ax, de, rE, EQUITY, stroke_width=3.5)
        lD = curve(ax, de, np.full_like(de, RD), DEBT, stroke_width=3)
        lA = curve(ax, de, np.full_like(de, RA), VALUE, stroke_width=3)
        leg = legend([(EQUITY, r"equity, $r_E$"), (VALUE, r"the whole firm (WACC)"), (DEBT, r"debt, $r_D$")],
                     font_size=22).to_edge(RIGHT, buff=0.8).shift(UP * 2.0)
        f = cmath(r"r_E", r"=", r"r_A", r"+", r"(r_A - r_D)\,\frac{D}{E}", font_size=40,
                  colors={r"r_E": EQUITY, r"r_A": VALUE})
        nt = wrapped_label(r"borrowing raises the owners' expected return, and exactly as much risk; the blend stays "
                           r"put.  (Real debt costs more as leverage rises; the blend still stays put.)", 5.2, 22,
                           GREY_A)
        VGroup(leg, f, nt).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The second proposition is about returns. If the whole firm earns eight percent and debt costs four, the owners of a "
            "levered firm keep the spread on the borrowed money, so their required return rises in a straight line with leverage. "
            "<bookmark mark='a'/> But so does their risk, by exactly as much, and the blend, the cost of capital of the whole firm, "
            "does not move. Cheap debt is not cheap: every dollar of it makes the equity dearer."
        ) as vo:
            self.play(FadeIn(g), Create(lA), Create(lD), FadeIn(leg[1:]))
            vo.wait_until("a")
            self.play(Create(lE), FadeIn(leg[0]), Write(f))
            self.play(FadeIn(nt))
        self.wait(0.4)
        self.clear_scene()

    def taxes(self):
        tc, te, td = 0.21, 0.20, 0.37
        rows = [
            cmath(r"\text{PV(shield)}", r"=", r"\sum_{t \ge 1} \frac{T_c\, r_D D}{(1 + r_D)^t}", r"=", r"T_c D",
                  font_size=38, colors={r"T_c D": CASH}),
            cmath(r"V_L", r"=", r"V_U + T_c D", font_size=40, colors={r"V_L": VALUE}),
            cmath(r"r_E", r"=", r"r_A + (r_A - r_D)(1 - T_c)\,\frac{D}{E}", font_size=40, colors={r"r_E": EQUITY}),
            cmath(r"T^*", r"=", r"1 - \frac{(1 - T_c)(1 - T_E)}{1 - T_D}", font_size=40, colors={r"T^*": CASH}),
            cmath(rf"T_c = {100 * tc:.0f}\%,\ T_E = {100 * te:.0f}\%,\ T_D = {100 * td:.0f}\%", r":",
                  rf"\ T^* = {100 * valuation.miller_gain(tc, te, td):.1f}\%", font_size=34),
        ]
        whys = [why(r"permanent debt saves $T_c r_D D$ a year, as risky as the debt itself, so discount at $r_D$"),
                why(r"Modigliani and Miller (1963): each dollar of permanent debt adds $T_c$ of value"),
                why(r"value balance with the shield: owners' required return rises more slowly with leverage"),
                why(r"Miller (1977): investors pay $T_D$ on interest but $T_E$ on equity income; the net gain per dollar"),
                why(r"the US top statutory rates since 2018 (corporate; dividends and gains; interest): about zero")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.8, edge=6.9)
        with self.voiceover(
            "The proof's power is in its assumptions: when financing does change value, one of them has failed. The first is "
            "taxes. Interest is paid before corporate tax, so permanent debt saves the tax rate times the interest every year. "
            "Discount those savings at the debt's own rate, and the shield is worth the tax rate times the debt. "
            "<bookmark mark='a'/> That was Modigliani and Miller's correction of 1963: the levered firm is worth the unlevered firm "
            "plus T times D. <bookmark mark='b'/> The owners' required return still rises with leverage, but more slowly. "
            "<bookmark mark='c'/> In 1977 Miller added the other side: investors pay personal tax on interest at one rate and on "
            "equity income at another, and the net gain from a dollar of debt is one minus this ratio. <bookmark mark='d'/> At "
            f"America's top rates since 2018 it is {100 * valuation.miller_gain(tc, te, td):.1f} percent: at the margin, the "
            "corporate saving is roughly cancelled by what bondholders pay."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def pie(self):
        d = ValueTracker(0.0)
        R0 = 2.0
        center = LEFT * 3.4 + DOWN * 0.2

        def value(x):
            return 1 + 0.21 * x - 0.8 * x ** 3

        def draw():
            x = d.get_value()
            gov = 0.21 * (1 - x) / 1.21          # the tax the government takes falls as interest replaces profit
            dist = 0.8 * x ** 3 / 1.21
            debt = x / 1.21
            eq = 1 - gov - debt - dist
            g = VGroup()
            a0 = PI / 2
            for frac, col in ((eq, EQUITY), (debt, DEBT), (gov, GREY_D), (dist, QC.LOSS)):
                ang = TAU * max(frac, 0)
                if ang > 1e-4:
                    g.add(AnnularSector(inner_radius=0, outer_radius=R0, angle=ang, start_angle=a0, fill_color=col,
                                        fill_opacity=0.85, stroke_width=1, stroke_color=BLACK).move_arc_center_to(center))
                a0 += ang
            rd = VGroup(live(r"\text{debt}", 100 * x, 0, r"\%\ \text{of}\ V_U", font_size=30),
                        live(r"\text{investors}", value(x), 3, font_size=30)).arrange(RIGHT, buff=0.5)
            rd.next_to(center, DOWN, buff=R0 + 0.35)
            return VGroup(g, rd)

        pie = always_redraw(draw)
        gx = axes([0, 0.65], [0.95, 1.06], x_length=5.4, y_length=3.4, xlabel=r"debt / unlevered value",
                  ylabel=r"investors' value / $V_U$", xticks=[0, 0.2, 0.4, 0.6], yticks=[0.96, 1.0, 1.04],
                  yfmt=lambda v: f"{v:.2f}", font_size=17).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        ax = gx.ax
        xs = np.linspace(0, 0.65, 66)
        k = ValueTracker(0)
        tr = tracing(ax, xs, value(xs), k, VALUE)
        leg = legend([(EQUITY, r"equity"), (DEBT, r"debt"), (GREY_D, r"government (taxes)"),
                      (QC.LOSS, r"expected distress costs")], font_size=19).next_to(gx, DOWN, buff=0.35).align_to(gx, LEFT)
        illus = label(r"illustrative: tax 21\%, distress cost $0.8\,d^3$", font_size=18, color=GREY_B).to_corner(DL, buff=0.3)
        dstar = float(np.sqrt(0.21 / 2.4))
        with self.voiceover(
            "Picture the firm's pre-tax value as a pie whose size financing cannot change. Without debt, the owners get one slice "
            "and the government, through corporate tax, gets the grey one. <bookmark mark='a'/> Add debt. Interest is deducted, so "
            "the grey slice shrinks and the investors' share of the same pie grows: that is all the tax shield is. "
            "<bookmark mark='b'/> But a red slice appears too: the expected costs of distress, lawyers, lost customers, investment "
            "forgone when the firm might not pay. It grows faster than the debt. <bookmark mark='c'/> The investors' total peaks "
            f"where the next dollar of debt saves as much tax as it adds expected distress, here at about {100 * dstar:.0f} percent: "
            "the trade-off theory, read straight off the pie."
        ) as vo:
            self.add(pie)
            self.play(FadeIn(gx), FadeIn(leg), FadeIn(illus))
            self.add(tr)
            vo.wait_until("a")
            self.play(d.animate.set_value(0.3), k.animate.set_value(30), run_time=4)
            vo.wait_until("b")
            self.play(d.animate.set_value(0.65), k.animate.set_value(65), run_time=4)
            vo.wait_until("c")
            self.play(d.animate.set_value(dstar), run_time=2)
            self.play(FadeIn(Dot(ax.c2p(dstar, value(dstar)), radius=0.09, color=YELLOW)))
        pie.clear_updaters()
        tr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def survey(self):
        card = firm_card(r"How CFOs decide: 392 of them",
                         r"Graham and Harvey surveyed chief financial officers in 1999 about how they set capital "
                         r"structure. Share saying each factor is important or very important for debt policy:",
                         numbers=[(r"59.4\%", r"financial flexibility"), (r"57.1\%", r"credit rating"),
                                  (r"44.9\%", r"tax advantage of interest"), (r"21.4\%", r"distress costs")],
                         source=r"Graham and Harvey, JFE 60 (2001); JACF 15 (2002)", width=9.6, font_size=22)
        card.move_to(UP * 0.5)
        pp = desk_question(r"Pause and predict: tax 21\%, permanent debt of 100. How much value does the debt add, "
                           r"and who loses it?", width=9.6, font_size=21).next_to(card, DOWN, buff=0.35)
        with self.voiceover(
            "Do firms think this way? Graham and Harvey asked three hundred and ninety-two CFOs: fewer than half called the tax "
            "advantage important and a fifth called distress costs important; most cited flexibility and credit ratings. "
            "<bookmark mark='a'/> Pause and predict: twenty-one percent tax, permanent debt of a hundred. What does the debt add, "
            "and who loses it? Twenty-one, from the government."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()
