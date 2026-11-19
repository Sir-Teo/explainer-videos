from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

PROBLEMS = [
    r"The kiln: \ with demand $a - bQ$, \ private cost $c + eQ$ \ and damage $dQ$, \ derive the market and efficient "
    r"outputs, \ Pigou's tax and the triangle; \ check 45, 36, 18, 101.25.",
    r"Coase: \ with his table and Agora's values for the steers, \ show the herd is 2 under either rule, \ and the "
    r"farmer pays between \$1.50 and \$3.",
    r"The shared pot: \ show that giving nothing is best for each player when the return per shell $m < 1$, \ and "
    r"giving everything best for the group when $nm > 1$.",
    r"Samuelson and Lindahl: \ for values $\theta_i \ln(1 + G)$ with $\theta = (4, 3, 2, 1)$ and cost 1, \ find the "
    r"efficient $G$, \ voluntary provision, \ and Lindahl's prices.",
    r"Gordon's fishery: \ with Schaefer's growth, \ derive open-access effort, \ maximum economic yield and maximum "
    r"sustainable yield; \ check 35, 17.5, 25.",
    r"Weitzman: \ derive the expected losses of a tax and a quota, \ and show their difference is "
    r"$\sigma^2(C'' - B'')/(2C''^2)$.",
    r"Vickrey's bottleneck: \ show the equilibrium cost per commuter is $\delta N/s$ with $\delta = \beta\gamma/("
    r"\beta+\gamma)$, \ and that half of the total is time in the queue.",
    r"$\bigstar$ \ Arthur's lock-in: \ show that once one technology leads by more than taste/network adopters, \ "
    r"every later adopter chooses it.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.0)
        a = wrapped_label(r"The market makes too much of what harms others and too little of what helps them, \ because "
                          r"no price carries the spillover. \ Where the people involved are few and contracts cheap, \ "
                          r"they bargain it away, \ as the beekeepers did. \ Where they are many, \ the remedy is a "
                          r"price on the spillover, \ a cap on it with permits to trade, \ or rules made by the "
                          r"users; \ each works only as well as the damage is measured \ and the rules are kept.",
                          11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = pair(height=0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: what happens when my choice lands on you, and nobody pays? <bookmark mark='a'/> The market makes too "
            "much of what harms others, and too little of what helps them, because no price carries the spillover. "
            "Where the people involved are few and contracts are cheap, they bargain it away, as the beekeepers did. "
            "Where they are many, the remedy is a price on the spillover, a cap with permits to trade, or rules made "
            "by the users themselves. And each works only as well as the damage is measured, and the rules are kept."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        k, lh, f, b, ac = (load(x) for x in ("kiln", "lighthouse", "fishery", "bottleneck", "acid"))
        items = [
            (r"Meade's fable, \ and Cheung's beekeepers: \ the spillover had a price", DEMAND),
            (r"the shared pot: \ keep your shells, \ and all end with 20 instead of 32", POT),
            (rf"the kiln: \ {k['q_market']:.0f} pots, \ not {k['q_social']:.0f}; \ a triangle of "
             rf"{k['dwl']:.0f} shells", SOCIAL),
            (rf"Pigou: \ a tax of {k['tax']:.0f} a pot; \ the right amount of smoke isn't zero", GOOD),
            (r"Coase: \ bargaining makes the rule irrelevant, \ unless bargaining is costly", DEMAND),
            (rf"public goods: \ add the values; \ {lh['g_star']:.0f} hours of light, \ not {lh['g_nash']:.0f}; \ "
             r"the lighthouse's harbour", PRIVATE),
            (r"free riding decays; \ punishment restores it, \ where norms aim it well", POT),
            (rf"the commons: \ {f['e_oa']:.0f} boats and no rent; \ cod in 1992; \ Ostrom's principles", FISH),
            (r"the acid-rain market: \ a third less sulphur, \ cheaply; \ benefits fifty times the costs", SOCIAL),
            (r"Weitzman: \ a price when cost is steeper, \ a cap when benefit is", GOOD),
            (rf"the bottleneck: \ a {b['max_wait_min']:.0f}-minute queue; \ a toll halves the cost; \ Stockholm",
             ROAD),
            (r"networks lock in; \ ideas spill over; \ new roads fill; \ the damage, \ measured", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 15, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fifteen in twelve lines. <bookmark mark='a'/> Meade's fable of the bees was wrong as an example: "
            "Cheung found the beekeepers' contracts. In the shared pot, keeping your shells is best for you, and "
            "leaves everyone with twenty instead of thirty-two. Bo's kiln made forty-five pots where thirty-six were "
            "best, losing a hundred shells a season. Pigou's tax of eighteen a pot fixes it, and the right amount of "
            "smoke is not zero. With cheap bargaining, Coase showed, the liability rule doesn't change what happens; "
            "with costly bargaining, it does. A public good's values are added up, and voluntary giving provides "
            "three hours of light where nine are worth it. Free riding decays, and punishment restores giving where "
            "norms aim it well. Open access dissipates the lagoon's rent, the cod collapsed, and Ostrom found commons "
            "that last. The acid-rain market cut sulphur cheaply, and its benefits were fifty times its costs. "
            "Weitzman says set a price when costs are steeper, a cap when benefits are. Vickrey's toll halves the cost "
            "of a rush hour, and Stockholm proved it. And networks lock in, ideas spill over, new roads fill, and "
            "the damage can be measured."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The kiln's numbers; Coase's herd; the shared pot's dilemma; Samuelson's and Lindahl's "
            "lighthouse; Gordon's fishery; Weitzman's formula; Vickrey's bottleneck; and a starred problem on "
            "lock-in. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jonathan Gruber, \emph{Public Finance and Public Policy}, chs.\ 5--9",
             r"Mas-Colell, Whinston and Green, \emph{Microeconomic Theory} (1995), ch.\ 11",
             r"Elinor Ostrom, \emph{Governing the Commons} (1990)",
             r"Tom Tietenberg and Lynne Lewis, \emph{Environmental and Natural Resource Economics}"],
            [r"Pigou (1920); \ Meade (1952); \ Coase (1959, 1960, 1974); \ Samuelson (1954); \ Gordon (1954)",
             r"Hardin (1968); \ Dales (1968); \ Montgomery (1972); \ Cheung (1973); \ Weitzman (1974)",
             r"Vickrey (1969); \ Arnott, de Palma and Lindsey (1990); \ Duranton and Turner (2011)",
             r"Fehr and Gächter (2000); \ Fischbacher, Gächter and Fehr (2001); \ Herrmann, Thöni and Gächter (2008)",
             r"Rohlfs (1974); \ Katz and Shapiro (1985); \ David (1985); \ Arthur (1989); \ Jaffe, Trajtenberg and "
             r"Henderson (1993)",
             r"Schmalensee and Stavins (2013); \ Chay and Greenstone (2003); \ Currie and Walker (2011); \ Deryugina "
             r"et al.\ (2019)"])
        with self.voiceover(
            "The reading: Jonathan Gruber's Public Finance and Public Policy; chapter eleven of Mas-Colell, Whinston "
            "and Green; Elinor Ostrom's Governing the Commons; and Tietenberg and Lewis on environmental economics. "
            "Then the papers, from Pigou to the wind."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2000, r"London, \ March and April", r"five licences for the airwaves, \ sold in an auction "
                          r"designed by game theorists: \\ 150 rounds, \ \pounds22.5 billion", color=E.ACCENT, width=10.4,
                          font_size=24)
        nxt = VGroup(label(r"Next: \ Part 16 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Auctions", font_size=46),
                     label(r"how should something be sold \ when nobody knows what it is worth to the buyers?",
                           font_size=26, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ spillovers no market priced; \ next: \ markets built on purpose", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about what markets leave out. The next is about markets built on purpose. "
            "<bookmark mark='a'/> In the spring of 2000 the British government sold five licences to use the "
            "airwaves for mobile phones, in an auction designed by game theorists. It ran for a hundred and fifty "
            "rounds and raised twenty-two and a half billion pounds. <bookmark mark='b'/> Part sixteen: auctions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
