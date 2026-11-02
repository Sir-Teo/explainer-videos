from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE

RA, RD = 0.08, 0.04


class MM(VoiceoverScene):
    def construct(self):
        self.card()
        self.arbitrage()
        self.prop2()
        self.tradeoff()

    def card(self):
        c = chapter_card(5, r"Modigliani and Miller", r"Can borrowing make a firm worth more?", lit=(1958,), part=PART)
        with self.voiceover("Chapter five. Modigliani and Miller."):
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
            "In 1958 Franco Modigliani and Merton Miller asked whether a firm can make itself more valuable by "
            "how it is financed. Take two firms with identical assets, throwing off the same cash X each year. Firm "
            "U has no debt: its owners get all of X. Firm L has borrowed D at a rate r D: its lenders are paid "
            "first, and its owners get what is left. <bookmark mark='a'/> Owning a fraction alpha of L's shares pays "
            "alpha times X minus the interest. <bookmark mark='b'/> But you could build that payoff yourself: buy "
            "alpha of the unlevered firm and borrow alpha times D on your own account. You receive alpha X and pay "
            "alpha times the interest. The same cash, in every state of the world. <bookmark mark='c'/> Two "
            "identical payoffs must cost the same, or there is an arbitrage. So L's equity is worth U's value minus "
            "the debt, and the levered firm is worth exactly the unlevered one. Leverage you can do at home is not "
            "worth paying a firm to do. Both men later won the Nobel prize, partly for this argument, the first "
            "no-arbitrage proof in finance, and a preview of Part nine."
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
            "The second proposition is about returns. If the whole firm earns r A, eight percent here, and the "
            "debt costs four, then the owners of a levered firm earn more on average, because they keep the "
            "spread on the borrowed money. <bookmark mark='a'/> Their required return rises in a straight line with "
            "leverage. But so does their risk, by exactly as much. The blend, the cost of capital of the whole "
            "firm, does not move. Cheap debt is not cheap: every dollar of it makes the equity more expensive."
        ) as vo:
            self.play(FadeIn(g), Create(lA), Create(lD), FadeIn(leg[1:]))
            vo.wait_until("a")
            self.play(Create(lE), FadeIn(leg[0]), Write(f))
            self.play(FadeIn(nt))
        self.wait(0.4)
        self.clear_scene()

    def tradeoff(self):
        d = np.linspace(0, 0.65, 131)
        shield = 0.21 * d
        distress = 0.8 * d ** 3
        V = 1 + shield - distress
        dstar = float(np.sqrt(0.21 / 2.4))
        g = axes([0, 0.65], [0.9, 1.2], x_length=6.2, y_length=4.6, xlabel=r"debt as a fraction of the unlevered value",
                 ylabel=r"firm value / unlevered value", xticks=[0, 0.2, 0.4, 0.6], yticks=[0.9, 1.0, 1.1, 1.2],
                 yfmt=lambda u: f"{u:.1f}", font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        l0 = curve(ax, d, np.ones_like(d), GREY_B, stroke_width=2.5)
        l1 = curve(ax, d, 1 + shield, CASH, stroke_width=3)
        l2 = curve(ax, d, V, VALUE, stroke_width=4)
        peak = Dot(ax.c2p(dstar, 1 + 0.21 * dstar - 0.8 * dstar ** 3), radius=0.09, color=YELLOW)
        leg = legend([(GREY_B, r"Modigliani--Miller, no taxes"), (CASH, r"with the interest tax shield, $V_U + tD$"),
                      (VALUE, r"less the expected costs of distress")], font_size=21).to_edge(RIGHT, buff=0.5)
        leg.shift(UP * 2.0)
        notes = VGroup(
            label(r"illustrative: tax rate 21\%, distress cost $0.8\,d^3$", font_size=19, color=GREY_B),
            wrapped_label(r"the trade-off theory: borrow until the next dollar's tax saving equals its expected "
                          r"cost of distress", 4.8, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(leg, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The proof's power is in its assumptions: when financing does change value, one of them has failed, "
            "and you know which to look for. The first is taxes. Interest is deducted before corporate tax, so "
            "debt shields income, and in their 1963 correction Modigliani and Miller added the tax shield: each "
            "dollar of permanent debt adds the tax rate to the firm's value. <bookmark mark='a'/> Taken alone, that "
            "says borrow everything. What stops it is the cost of distress: lawyers, lost customers, investment "
            "forgone when a firm might not pay its debts. Those costs rise faster than the debt. "
            "<bookmark mark='b'/> The value peaks where the next dollar's tax saving equals its expected cost of "
            "distress. That is the trade-off theory, and in Part twenty we will price the distress itself, with "
            "Merton's model of default."
        ) as vo:
            self.play(FadeIn(g), Create(l0), FadeIn(leg[0]))
            self.play(Create(l1), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(l2), FadeIn(leg[2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(peak), FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()
