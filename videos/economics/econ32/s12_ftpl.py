from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class FTPL(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Who backs the money? \ The fiscal theory", r"Can a budget set the price level?",
             "Chapter ten. Who backs the money? The fiscal theory.",
             lit={1981: r"Sargent and Wallace", 1994: r"Sims", 2023: r"Cochrane"}, scale=("nation",),
             horizon=("a year", "decades"))
        self.ftpl()
        self.unpleasant()

    def ftpl(self):
        U = load("unpleasant")
        F = U["ftpl"]
        rows = VGroup(
            label(r"the government's debt is promised in money", font_size=25, color=E.ACCENT),
            MathTex(r"\frac{B}{P} \;=\; \text{present value of future real surpluses}", font_size=40, color=DEBT),
            label(rf"nominal debt {F['B']:.0f}; \ a surplus of {F['surplus']:.1f} a year at {100 * F['r']:.0f}\%: "
                  rf"\ $P = {F['P']:.2f}$", font_size=23, color=TAX),
            label(rf"people come to expect surpluses of only {F['surplus_low']:.1f}: \ $P = {F['P_low']:.2f}$ \ "
                  rf"--- prices rise {100 * (F['P_low'] / F['P'] - 1):.0f}\%", font_size=23, color=INFL),
            label(r"the fiscal theory: \ if surpluses do not adjust, \ the price level must", font_size=23,
                  color=WHITE),
            label(r"a central bank can control inflation only if the treasury backs it", font_size=22, color=CB),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Sims, \ \emph{Economic Theory} 4(3) (1994); \ Cochrane, \ \emph{The Fiscal Theory of "
                            r"the Price Level} (2023); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Now a theory in which the budget sets the price level. <bookmark mark='a'/> Government bonds promise "
            "money, not goods. <bookmark mark='b'/> Their real value, nominal debt over the price level, must equal "
            "what the government will raise to pay them: the present value of its future surpluses. "
            f"<bookmark mark='c'/> Nominal debt of {F['B']:.0f}, a real surplus of {F['surplus']:.0f} a year, a "
            f"real interest rate of {100 * F['r']:.0f} percent: the price level is {F['P']:.0f}. "
            f"<bookmark mark='d'/> If people come to expect surpluses of only {F['surplus_low']:.1f}, the same "
            f"debt is worth less in goods, and with the debt fixed in money, prices must rise "
            f"{100 * (F['P_low'] / F['P'] - 1):.0f} percent. <bookmark mark='e'/> That is the fiscal theory of the "
            "price level, from Christopher Sims, Michael Woodford and John Cochrane: if surpluses do not adjust to "
            "the debt, the price level does. <bookmark mark='f'/> A central bank controls inflation only as long "
            "as the treasury stands behind its debts."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def unpleasant(self):
        U = load("unpleasant")
        yrs = np.array(U["years"])
        ax = plane([0, 30], [0, 0.16], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[0, 10, 20, 30], yticks=[0, 0.04, 0.08, 0.12, 0.16], xlabel=r"years",
                   ylabel=r"money growth", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        ax2 = plane([0, 30], [0.4, 0.75], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0, 10, 20, 30], yticks=[0.4, 0.5, 0.6, 0.7], xlabel=r"years",
                    ylabel=r"debt, \ share of output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                    font_size=14)
        ml = path(ax, yrs, U["loose"]["mu"], SPEND, 3, smooth=False)
        mt = path(ax, yrs, U["tight"]["mu"], INFL, 3.5, smooth=False)
        dl = path(ax2, list(range(len(U["loose"]["debt"]))), U["loose"]["debt"], SPEND, 3, smooth=False)
        dt = path(ax2, list(range(len(U["tight"]["debt"]))), U["tight"]["debt"], INFL, 3.5, smooth=False)
        head = label(r"Sargent and Wallace, \ 1981: \ some unpleasant monetarist arithmetic", font_size=22,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        k = VGroup(label(r"teal: \ money pays its share of the deficit from the start", font_size=16, color=SPEND),
                   label(rf"red: \ tight money for {U['T']} years, \ then it must pay for more", font_size=16,
                         color=INFL)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(head, DOWN, buff=0.2)
        foot = label(rf"money growth for ever after: \ {100 * U['mu_after_tight']:.1f}\% \ against "
                     rf"{100 * U['mu_loose']:.1f}\%", font_size=21, color=INFL).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Sargent and Wallace, \ FRB Minneapolis \emph{Quarterly Review} 5(3) (1981); \ the "
                            r"Island", corner=DR, font_size=12)
        with self.voiceover(
            "An older warning makes the same point. <bookmark mark='a'/> In 1981 Thomas Sargent and Neil Wallace "
            "imagined a treasury that runs a deficit it will not change, and a central bank that must decide how "
            "much of it to pay for by printing money. <bookmark mark='b'/> If the bank pays its share from the "
            "start, money grows at a steady rate, in teal. <bookmark mark='c'/> If it holds money tight for "
            f"{U['T']} years, the treasury borrows more instead, and debt piles up. <bookmark mark='d'/> When the "
            "bank can no longer refuse, it must pay for the larger debt's interest as well: money growth for ever "
            f"after is {100 * U['mu_after_tight']:.1f} percent instead of {100 * U['mu_loose']:.1f}. Tight money "
            "today means more inflation tomorrow, unless the treasury changes course."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ax), FadeIn(ax2), run_time=0.6)
            vo.wait_until("b")
            self.play(Create(ml), Create(dl), FadeIn(k[0]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(dt), FadeIn(k[1]), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(mt), FadeIn(foot), run_time=1.6)
        self.clear_scene()
