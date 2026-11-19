from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403

PROBLEMS = [
    r"Lemons: \ quality uniform on $[0, H]$, \ worth $q$ to sellers and $q + a$ to buyers; \ show the price is $2a$ "
    r"(if $2a \le H$) \ and the share traded $2a/H$; \ check \$60 and 60\%.",
    r"Akerlof's example: \ buyers value a car at $m$ times its worth to the seller; \ show nothing trades if $m < 2$ "
    r"and everything if $m \ge 2$.",
    r"Play it: \ show a single buyer's best offer is $p = a$, \ with expected gain $a^2 / 2H$; \ check \$30 and \$4.50.",
    r"The guarantee: \ with chapter 3's numbers, \ check that good sellers gain by offering it \ and bad sellers don't "
    r"gain by copying.",
    r"Spence: \ derive the separating range $[1, 2]$ for chapter 4's fishers, \ and show the strong prefer pooling when "
    r"90\% are strong.",
    r"Rothschild and Stiglitz: \ verify that the careless are indifferent between full cover at 0.4 \ and \$12.57 of "
    r"cover at 0.1.",
    r"Einav, \ Finkelstein and Cullen: \ from $D = 0.94 - 0.0007p$ and $AC = 391.69 + 0.155p$, \ derive the "
    r"competitive and efficient prices.",
    r"$\bigstar$ \ Stiglitz and Weiss: \ show the bank's expected repayment falls when the safe borrowers leave at "
    r"\$177.78, \ and find its maximum.",
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
        a = wrapped_label(r"The good is driven out by the bad, \ and trades that would benefit both sides don't "
                          r"happen; \ in the extreme the market vanishes. \ The informed respond with signals that are "
                          r"cheap only for the truthful, \ the uninformed with screens that sort; \ markets grow "
                          r"guarantees, \ reputations and inspectors. \ All of it costs something, \ and in the "
                          r"insurance markets where it has been measured \ the cost is real but modest.", 11.6, 29,
                          WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = pair(height=0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: what happens to a market when one side knows more than the other? <bookmark mark='a'/> The good is "
            "driven out by the bad, and trades that would benefit both sides don't happen; in the extreme, the market "
            "vanishes. The informed respond with signals that are cheap only for those telling the truth, and the "
            "uninformed with screens that sort. Markets grow guarantees, reputations and inspectors. All of it costs "
            "something, and in the insurance markets where it has been measured, the cost is real but modest."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        L, o, s, sc, e, t = (load(x) for x in ("lemons", "offers", "spence", "screen", "efc", "tests"))
        items = [
            (r"Akerlof's paper: \ rejected three times as trivial or wrong; \ a Nobel prize", LEMON),
            (rf"your blind offer: \ \${o['best']:.0f} at best, \ and 70\% of boats stay unsold", GOOD),
            (rf"the market: \ \${L['add_p']:.0f}, \ {100 * L['add_share']:.0f}\% trade; \ with Akerlof's 1.5, \ "
             r"nothing", LEMON),
            (r"guarantees, \ brands, \ chains, \ inspectors, \ licences: \ cheap only for the honest", SIGNAL),
            (rf"Spence: \ school from {s['e_min']:.0f} to {s['e_max']:.0f} seasons separates; \ the cheapest survives",
             POOL),
            (r"the GED: \ 10 to 19\% for the same skills; \ school is both skill and signal", USED),
            (rf"Rothschild--Stiglitz: \ menus that sort; \ no equilibrium below {100 * sc['share_threshold']:.0f}\% "
             r"careless", LOSS),
            (r"Harvard's PPO: \ \$450, \ \$1{,}000, \ \$2{,}000, \ gone, \ in three years", SIGNAL),
            (rf"Alcoa: \ \${e['p_eq']:.0f} against \${e['p_eff']:.0f}; \ a triangle of \${e['loss']:.2f} a head",
             LOSS),
            (rf"the test: \ positive, \ zero or negative ({t['results']['advantageous']['corr']:.3f}) \ with caution",
             GOOD),
            (r"credit rationing; \ mandates, \ subsidies, \ risk adjustment; \ reviews", POOL),
            (r"the dial: \ a few percent; \ selection on moral hazard; \ the end of pooling", E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 13, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirteen in twelve lines. <bookmark mark='a'/> Akerlof's paper was rejected three times, as trivial "
            "or as wrong, and won a Nobel prize. Your best blind offer for Bo's boat was thirty dollars, and most boats "
            "stayed unsold. With many buyers the market settles at sixty dollars, and the best boats never trade; "
            "with Akerlof's own numbers, nothing trades at all. Guarantees, brands, chains, inspectors and licences "
            "work because they are cheap only for the honest. Spence's schooling sorts the strong from the weak while "
            "teaching nothing, and the cheapest sort survives. The GED shows a certificate paying for the same skills, "
            "so school is both skill and signal. Rothschild and Stiglitz's menus sort the careful from the careless, "
            "and may have no equilibrium. Harvard's generous plan died in three years. At Alcoa, adverse selection "
            "cost under ten dollars a head. The positive-correlation test can come out positive, zero or negative. "
            "Banks ration credit; policy has mandates, subsidies and risk adjustment; platforms have reviews. And the "
            "dial says selection costs a few percent, while the frontier asks what happens when insurers know more "
            "than we do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The lemons market's price; Akerlof's example; your best blind offer; the guarantee's "
            "separation; Spence's range; the careless owners' indifference; the Einav-Finkelstein prices; and a "
            "starred problem on credit rationing. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Patrick Bolton and Mathias Dewatripont, \emph{Contract Theory} (2005), chs.\ 2--3; \ Mas-Colell, "
             r"Whinston and Green, ch.\ 13",
             r"Jean-Jacques Laffont and David Martimort, \emph{The Theory of Incentives} (2002); \ Salani\'e, "
             r"\emph{The Economics of Contracts}",
             r"Liran Einav, Amy Finkelstein and Ray Fisman, \emph{Risky Business} (2023); \ Einav and Finkelstein, "
             r"JEP 25(1) (2011)",
             r"Bryan Caplan, \emph{The Case against Education} (2018)"],
            [r"Akerlof (1970); \ Spence (1973); \ Rothschild and Stiglitz (1976); \ Riley (1979); \ Stiglitz and "
             r"Weiss (1981)",
             r"Cho and Kreps (1987); \ Hungerford and Solon (1987); \ Tyler, Murnane and Willett (2000)",
             r"Cutler and Reber (1998); \ Cutler and Zeckhauser (1998); \ Chiappori and Salani\'e (2000)",
             r"Finkelstein and Poterba (2004); \ Finkelstein and McGarry (2006); \ Cabral and Horta\c{c}su (2010)",
             r"Einav, Finkelstein and Cullen (2010); \ Handel (2013); \ Einav, Finkelstein, Ryan, Schrimpf and Cullen "
             r"(2013)",
             r"Hackmann, Kolstad and Kowalski (2015); \ Angrist and Krueger (1991)"])
        with self.voiceover(
            "The reading: Bolton and Dewatripont's Contract Theory and chapter thirteen of Mas-Colell, Whinston and "
            "Green; Laffont and Martimort's Theory of Incentives; Risky Business, by Einav, Finkelstein and Ray Fisman, and "
            "their paper of pictures; and, for the case against school, Bryan Caplan. Then the papers, from Akerlof "
            "to the Massachusetts mandate."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1978, r"Xiaogang, \ Anhui", r"eighteen farmers put their thumbprints on a secret contract: \\ "
                          r"divide the commune's land, \ and keep what each household grows above the quota",
                          color=E.ACCENT, width=10.4, font_size=24).move_to(UP * 1.2)
        nxt = VGroup(label(r"Next: \ Part 14 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Incentives", font_size=46),
                     label(r"how do you get someone to work for you \ when you can't see what they do?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ hidden information; \ next: \ hidden action", font_size=30, color=GREY_A
                     ).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part was about hidden information: what people know. The next is about hidden action: what people "
            "do. <bookmark mark='a'/> In the winter of 1978, eighteen farmers in the village of Xiaogang, in Anhui "
            "province, put their thumbprints on a secret contract to divide their commune's land, and to keep "
            "whatever each household grew above the quota. <bookmark mark='b'/> Part fourteen: incentives."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
