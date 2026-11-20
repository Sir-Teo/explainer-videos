from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Crises(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Currency crises, \ three generations", r"Why do pegs break, and why so suddenly?",
             "Chapter eight. Currency crises, three generations.",
             lit={1979: r"Krugman", 1996: r"Obstfeld", 1999: r"Kaminsky and Reinhart"}, scale=("nation", "world"),
             horizon=("a day", "years"))
        self.first()
        self.later()

    def first(self):
        K = load("crises")["krugman"]
        t = np.array(K["t"])
        ax = plane([0, 25], [0, 130], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 25, 50, 75, 100, 125], xlabel=r"years",
                   ylabel=r"reserves; \ the exchange rate", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        res = path(ax, t, K["reserves"], RES, 3.2, smooth=False)
        shadow = path(ax, t, K["shadow"], GREY_B, 2.4, smooth=False)
        peg = seg(ax, 0, K["peg"], 25, K["peg"], DEM, 2.0, dashed=True)
        s = path(ax, t[t >= K["T_attack"]], np.array(K["s"])[t >= K["T_attack"]], GBP, 3.2, smooth=False)
        att = vline(ax, K["T_attack"], 0, 130, CRISIS, 2.0)
        exh = vline(ax, K["T_exhaust"], 0, 130, GREY_B, 1.5)
        side = VGroup(
            label(r"purple: \ reserves, \ draining \\ to pay for a deficit", font_size=18, color=RES),
            label(r"grey: \ the shadow rate, \\ where the currency would float", font_size=18, color=GREY_B),
            label(rf"the attack: \ year {K['T_attack']:.0f}, \\ when the shadow rate \\ reaches the peg", font_size=18,
                  color=CRISIS),
            label(rf"not year {K['T_exhaust']:.0f}, \ when reserves \\ would have run out: \\ the last "
                  rf"{K['jump_reserves']:.0f} go in a day", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Krugman, \ \emph{JMCB} 11(3) (1979); \ Flood and Garber, \ \emph{JIE} 17 (1984); \ "
                            r"the Island", corner=DR, font_size=12)
        with self.voiceover(
            "The first generation of models, Paul Krugman's of 1979, explains crises in Latin America. "
            "<bookmark mark='a'/> A government pegs its currency but prints money to pay for a deficit; the new money "
            "is swapped for foreign currency at the central bank, and reserves drain, steadily. "
            "<bookmark mark='b'/> At every moment there is a shadow exchange rate: where the currency would float if "
            "reserves were gone. It rises as money is printed. <bookmark mark='c'/> Speculators do not wait for "
            "reserves to run out. The moment the shadow rate reaches the peg, holding the currency becomes a losing "
            f"bet, and they buy the remaining reserves in a single attack: here in year {K['T_attack']:.0f}, "
            f"<bookmark mark='d'/> not year {K['T_exhaust']:.0f}, when the drain would have finished on its own. The "
            "crisis looks sudden; its cause was years old. And the peg falls without any jump in the exchange rate, "
            "because the attack comes exactly when there is none to profit from."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(peg), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(res), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(shadow), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(att), Create(s), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(exh), FadeIn(side[3]))
        self.clear_scene()

    def later(self):
        cards = point_cards([
            (r"first generation", r"bad fundamentals: \\ a deficit paid in money \\ drains reserves until \\ a "
                                  r"predictable attack \\ (Latin America, \ 1970s--80s)", RES),
            (r"second generation", r"a government that could \\ defend but may not: \\ self-fulfilling attacks \\ "
                                   r"(the ERM, \ 1992--93; \\ chapter 2)", DEM),
            (r"third generation", r"balance sheets: \ dollar debts \\ and fragile banks turn \\ a devaluation into "
                                  r"\\ a collapse (Asia, \ 1997; \\ Part 33)", CRISIS),
        ], width=12.8, cols=3, font_size=20).move_to(DOWN * 0.1)
        head = label(r"three generations of models, \ each written after the crises it explains", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        foot = label(r"1992: \ second generation: \ Britain could have held on, \ at a price in jobs markets "
                     r"judged it would not pay", font_size=20, color=WHITE).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Krugman (1979); \ Obstfeld (1996); \ Kaminsky and Reinhart, \ \emph{AER} 89(3) (1999)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Each generation of models was written after the crises it explains. <bookmark mark='a'/> The first: bad "
            "fundamentals, a predictable attack. <bookmark mark='b'/> The second, after 1992: governments that could "
            "defend a peg but might choose not to, so that attacks can succeed because they are expected. In "
            "September 1992 Sweden's central bank raised its overnight rate to five hundred percent for a few days "
            "to defend the krona; by November it had let it float too. <bookmark mark='c'/> The third, after Asia "
            "in 1997: balance sheets. Firms and banks with debts in dollars are bankrupted by the devaluation "
            "itself, so currency crises and banking crises arrive together, the twin crises Graciela Kaminsky and "
            "Carmen Reinhart documented. <bookmark mark='d'/> Black Wednesday belongs to the second generation. "
            "Britain's reserves and credit were not exhausted. Holding the peg would have meant still higher "
            "interest rates in a recession, and the markets judged, correctly, that the government would not pay "
            "that price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
