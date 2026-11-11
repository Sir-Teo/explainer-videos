from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import IMP, LOSS, OPT, PART, QQ, SPOT, VEG, computed, load


class Industry(VoiceoverScene):
    def construct(self):
        self.card()
        self.floor()
        self.vol_quotes()
        self.rule(load("industry"))
        self.plumbing()

    def card(self):
        c = chapter_card(18, r"Industry: the formula at work", r"How is it actually used for a living?",
                         lit=(1973, 1987), part=PART)
        with self.voiceover("Chapter eighteen. Industry: the formula at work."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def floor(self):
        sheet_title = label(r"a sheet of theoretical values (illustrative)", font_size=22, color=GREY_A)
        strikes, months = (40, 45, 50), (1, 4, 7)
        rows = [VGroup(label(r"strike", font_size=20, color=GREY_B),
                       *[label(rf"{m} months", font_size=20, color=GREY_B) for m in months])]
        for k in strikes:
            rows.append(VGroup(MathTex(str(k), font_size=26, color=QC.STRIKE),
                               *[MathTex(f"{float(bs.price(45, k, m / 12, 0.25, 0.06)):.2f}", font_size=26, color=OPT)
                                 for m in months]))
        tab = VGroup(*rows)
        for i, r_ in enumerate(tab):
            for j, c_ in enumerate(r_):
                c_.move_to([j * 1.5, -i * 0.5, 0])
        frame = SurroundingRectangle(tab, buff=0.25, color=GREY_D, corner_radius=0.08, stroke_width=1.5)
        sheet = VGroup(sheet_title, VGroup(frame, tab)).arrange(DOWN, buff=0.15).to_edge(LEFT, buff=0.6).shift(UP * 1.2)
        firm = firm_card(
            r"O'Connor \& Associates",
            r"A Chicago options trading firm founded in 1977; described in 1989 by the New York Times, as later "
            r"quoted, as the largest market maker on the US financial options exchanges; acquired by Swiss Bank "
            r"Corporation in the early 1990s; its name survived as UBS O'Connor.",
            source=r"public record: Federal Reserve approval of SBC's acquisition (1994); as reported",
            width=6.2, font_size=21).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        mm = wrapped_label(r"MacKenzie and Millo (2003): market makers used the sheets to sell what the model called "
                           r"dear and buy what it called cheap, and their trading pulled prices towards the model.",
                           6.2, 22, GREY_A).next_to(sheet, DOWN, buff=0.5).align_to(sheet, LEFT)
        with self.voiceover(
            "How does the formula earn a living? On the floor of the Chicago Board Options Exchange, Fischer Black "
            "sold printed sheets of theoretical prices, a column per expiry, a row per strike. Pause and predict: "
            "why buy a sheet instead of computing? Speed: in a shouting crowd, reading beats typing five inputs. "
            "<bookmark mark='a'/> Donald MacKenzie and Yuval Millo reconstructed what followed: market makers sold "
            "what the sheets called dear, bought what they called cheap, and pulled prices towards the model. "
            "<bookmark mark='b'/> Firms grew around it. O'Connor and Associates, founded in Chicago in 1977, was "
            "described in 1989 by the New York Times, as later quoted, as the largest market maker on America's "
            "financial options exchanges; Swiss Bank Corporation acquired it in the early 1990s."
        ) as vo:
            self.play(FadeIn(sheet, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(mm))
            vo.wait_until("b")
            self.play(FadeIn(firm, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vol_quotes(self):
        left = VGroup(
            label(r"Desks quote, hedge and limit risk in volatility:", font_size=28, color=IMP),
            label(r"a price is quoted as an implied volatility", font_size=24, color=GREY_A),
            label(r"risk is counted in vega: dollars per vol point", font_size=24, color=VEG),
            label(r"the formula translates one into the other", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UL, buff=0.6)
        quote = wrapped_label(r"Implied volatility is ``the wrong number to put in the wrong formula to get the right "
                              r"price'' (Riccardo Rebonato)", 6.0, 26, GREY_A).next_to(left, DOWN, buff=0.6)
        quote.align_to(left, LEFT)
        dissent = VGroup(
            label(r"The counter-view (an argument, not a fact):", font_size=24, color=LOSS),
            wrapped_label(r"Haug and Taleb (2011): traders priced options with heuristics and put--call parity long "
                          r"before 1973, and use the formula only as a quoting convention, never as a model.",
                          5.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "On a modern desk the formula is less a model than a language. Prices are quoted as implied "
            "volatilities, positions are counted in vega, dollars per volatility point, and limits are set in "
            "Greeks. The formula is the dictionary that translates between volatility and money. Riccardo "
            "Rebonato's line is the one desks repeat: implied volatility is the wrong number to put in the wrong "
            "formula to get the right price. <bookmark mark='a'/> There is a sharper dissent. Espen Haug and "
            "Nassim Taleb argued in 2011 that traders priced options with heuristics and parity long before 1973, "
            "and that nobody uses the formula as a model at all. Take it as an argument, not a measurement; the "
            "smile of chapter twelve is the evidence both sides point to."
        ) as vo:
            self.play(FadeIn(left, shift=RIGHT * 0.2))
            self.play(FadeIn(quote))
            vo.wait_until("a")
            self.play(FadeIn(dissent, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self, ind):
        T = np.asarray(ind["T"], float) * 365
        rel = np.asarray(ind["rel"], float) * 100
        g = axes([0, 2.6], [0, 1.2], x_length=7.4, y_length=4.0, xlabel=r"days to expiry (log)",
                 ylabel=r"$0.4\,F\sigma\sqrt T$ over the exact price, $-1$, in \%", xticks=[0, 1, 2],
                 yticks=[0, 0.5, 1.0], xfmt=lambda v: f"{10 ** v:.0f}", font_size=18).to_edge(LEFT, buff=0.7)
        g.shift(DOWN * 0.4)
        bars = VGroup(*[Rectangle(width=0.16, height=max(abs(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1]), 0.01),
                                  stroke_width=0, fill_color=OPT, fill_opacity=0.85)
                        .move_to(g.ax.c2p(np.log10(t_), v / 2)) for t_, v in zip(T, rel)])
        base = DashedLine(g.ax.c2p(0, 0.27), g.ax.c2p(2.6, 0.27), color=GREY_B, stroke_width=1.5)
        base_l = label(r"0.4 instead of $1/\sqrt{2\pi} = 0.3989$: $+0.27\%$", font_size=20, color=GREY_B)
        base_l.next_to(g.ax.c2p(0.1, 0.27), UP, buff=0.05).align_to(g.ax.c2p(0.1, 0), LEFT)
        C = {r"C": OPT, r"F": QQ, r"\sigma": IMP}
        eqs = VGroup(
            cmath(r"C", r"=", r"F\big[2N(\tfrac12\sigma\sqrt T) - 1\big]", font_size=32, colors=C),
            cmath(r"C", r"\approx", r"F\,\tfrac{\sigma\sqrt T}{\sqrt{2\pi}}\Big(1 - \tfrac{\sigma^2 T}{24}\Big)",
                  font_size=32, colors=C),
            cmath(r"C", r"\approx", r"0.4\,F\sigma\sqrt T", font_size=36, colors=C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
        notes_ = VGroup(*[note(t, font_size=18) for t in (r"at the forward, undiscounted (Black-76)",
                                                          r"Taylor in $\sigma\sqrt T$",
                                                          r"Brenner and Subrahmanyam (1988)")])
        for e_, n_ in zip(eqs, notes_):
            n_.next_to(e_, DOWN, buff=0.05).align_to(e_, LEFT)
        with self.voiceover(
            f"""At the forward, the undiscounted Black call value is F times the quantity two N of half sigma root T minus one. Its small-total-volatility approximation is point four F sigma root T. <bookmark mark='a'/> Evaluate both formulas using each Surface expiry's interpolated ATM IV. At total volatility {ind['s_max']:.2f}, the largest relative discrepancy here is {100 * ind['max_abs_rel']:.1f} percent. This compares an approximation with a Black model value, not with independent executable ATM prices. Discount both consistently when a present value is needed."""
        ) as vo:
            self.play(FadeIn(eqs[0]), FadeIn(notes_[0]))
            self.play(FadeIn(eqs[1]), FadeIn(notes_[1]))
            self.play(FadeIn(eqs[2]), FadeIn(notes_[2]))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(base), FadeIn(base_l))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15, run_time=2.5),
                      FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plumbing(self):
        rows = VGroup(*[VGroup(label(a, font_size=24, color=c), label(b, font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for a, b, c in (
            (r"Options on futures", r"Black-76, the exchanges' standard formula for decades", QQ),
            (r"Negative prices, April 2020", r"CME switched some energy options to Bachelier's model (Part 5)", LOSS),
            (r"The VIX", r"a strip of options, priced in volatility (Part 12)", IMP),
            (r"Employee stock options", r"a fair value at grant, from an option model (Part 3)", OPT),
            (r"Deribit, Bitcoin options", r"Black-76, settled in coin; Coinbase acquisition completed 14 August 2025", SPOT),
            (r"IBIT options, Nasdaq", r"first day 19 November 2024: 353,716 contracts", SPOT),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(LEFT, buff=0.8)
        if rows.height > 6.8:
            rows.scale_to_fit_height(6.8).to_edge(LEFT, buff=0.8)
        src = note(r"sources: Coinbase and Deribit's announcement (14 Aug 2025); Nasdaq (19 Nov 2024)", font_size=18)
        src.to_corner(DR, buff=0.25)
        with self.voiceover(
            """The formula sits in the plumbing. Futures options often use Black's lognormal convention; negative underlyings require a compatible model, such as Bachelier or a shifted model. The VIX instead uses a strip of option prices. <bookmark mark='a'/> Coinbase completed its acquisition of Deribit in August 2025. Options on the iShares Bitcoin Trust opened on Nasdaq on the nineteenth of November 2024; Nasdaq reports 353,716 contracts on day one. Those are dated industry facts. They do not validate a particular pricing model."""
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:4]], lag_ratio=0.5, run_time=5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[4:]], lag_ratio=0.5, run_time=3),
                      FadeIn(src))
        self.wait(0.4)
        self.clear_scene()
