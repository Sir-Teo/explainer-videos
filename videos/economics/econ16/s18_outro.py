from __future__ import annotations

from videos.economics.econ16.common import *  # noqa: F403

PROBLEMS = [
    r"Vickrey: \ show that bidding your value is weakly dominant in a second-price auction, \ and give a case "
    r"where it is not strictly better than some other bid.",
    r"Shading: \ with $n$ bidders and values uniform on $[0, 1]$, \ verify that $b(v) = \tfrac{n-1}{n}v$ is an "
    r"equilibrium of the first-price auction, \ and that revenue is $\tfrac{n-1}{n+1}$.",
    r"All-pay: \ use the envelope formula to derive the all-pay equilibrium bid $\tfrac{n-1}{n}v^n$, \ and check "
    r"its revenue.",
    r"Myerson: \ with two bidders, \ show revenue with reserve $r$ is $\tfrac13 + r^2 - \tfrac43 r^3$, \ "
    r"maximized at $r = \tfrac12$ with $\tfrac{5}{12}$; \ compare three bidders with no reserve.",
    r"The winner's curse: \ with estimates $V + e$, \ $e$ uniform on $[-s, s]$, \ show the highest of $n$ "
    r"overstates $V$ by $s\,\tfrac{n-1}{n+1}$ on average.",
    r"Slots: \ with values (10, 8, 6, 4) and clicks (200, 120, 60), \ compute Vickrey's payments, \ and check "
    r"that bids of 6.2, 5 and 4 below the top form an equilibrium of the second-price auction for slots.",
    r"Exposure: \ with Bo's pair worth 10 and either right 1, \ find for which local values a bold Bo loses money.",
    r"$\bigstar$ \ Demand reduction: \ two units, \ values (10, 10) and 6; \ show that under one price the big "
    r"bidder bids for one unit, \ and find Vickrey's payments.",
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
        a = wrapped_label(r"Let the bidders compete, \ and design the sale around who they are. \ With independent "
                          r"private values, \ any standard format raises the same money, \ and a reserve adds a "
                          r"little. \ What really matters is getting bidders to come and stopping them from "
                          r"colluding, \ guarding winners against the curse of shared values, \ and choosing rules "
                          r"bidders can trust and follow.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = gavel(height=0.9).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: how should something be sold, when nobody knows what it is worth to the buyers? "
            "<bookmark mark='a'/> Let the bidders compete, and design the sale around who they are. When each knows "
            "its own value and nothing about the others, any of the standard formats raises the same money, and a "
            "reserve price adds a little. What really matters is getting bidders to come, and stopping them from "
            "colluding; protecting winners from the curse of shared values; and choosing rules that bidders can "
            "trust, and can follow."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo, shift=UP * 0.2))
        self.clear_scene()

    def recap(self):
        p, m, c, uk = load("playit"), load("myerson"), load("curse"), load("spectrum")["uk"]
        items = [
            (rf"Britain's airwaves: \ \pounds{uk['revenue_bn_gbp']} billion; \ the Dutch: \ a third of the forecast",
             PRICE),
            (rf"Play it: \ bid {p['best_first']:.1f} when you pay your bid, \ 70 when you pay the next one", YOU),
            (r"four formats, \ two games: \ Dutch is a sealed bid; \ English is nearly Vickrey's", SECOND),
            (r"Vickrey: \ when the price isn't your bid, \ bid your value, \ whatever others do", SECOND),
            (r"shading: \ $\tfrac{n-1}{n}$ of your value; \ more rivals, \ less shading", FIRST),
            (r"revenue equivalence: \ who wins fixes what is paid; \ six shells either way", PRICE),
            (r"risk, \ linked values, \ asymmetry, \ collusion and entry break it", HOLD),
            (rf"Myerson's reserve: \ +{m['gain'] * 100:.0f}\% with two bidders; \ a third bidder is worth more",
             RESERVE),
            (rf"the winner's curse: \ the highest estimate wins; \ the jar's winners lost \${c['jar']['mean_loss']:.2f}",
             CURSE),
            (r"the airwaves: \ simultaneous rounds, \ the exposure problem, \ packages; \ signals in the digits",
             SECOND),
            (r"slots: \ not Vickrey's, \ but Vickrey's prices in equilibrium; \ one price invites demand reduction",
             FIRST),
            (r"reserves in practice: \ +2.7\%, \ depending on the setting; \ credible auctions, \ machines that bid",
             E.ACCENT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 16, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixteen in twelve lines. <bookmark mark='a'/> Britain sold its airwaves for twenty-two and a half "
            "billion pounds, and the Netherlands, with as many licences as incumbents, raised a third of its "
            "forecast. In Play it, the best bids were fifty-two and a half when you pay your bid, and seventy when "
            "you pay the next one. The four formats are two games. Vickrey showed that when the price isn't your own "
            "bid, you should bid your value. In a first-price auction you shade, less with more rivals. Revenue "
            "equivalence says who wins fixes what is paid, which is why you expected six shells either way. Risk, "
            "linked values, unequal bidders, collusion and entry break it. Myerson's reserve adds a quarter with two "
            "bidders, but a third bidder adds more. The highest estimate wins a common-value auction, which is the "
            "winner's curse, and the jar's winners lost two dollars each. Selling the airwaves needed simultaneous "
            "rounds, raised the exposure problem, and invited signals in the digits. The auction for search slots is "
            "not Vickrey's, but reaches Vickrey's prices, and a single price for many units invites demand "
            "reduction. And in a real market, reserves added a few percent, depending on the setting, while the "
            "frontier asks for auctions the seller can't cheat in, and bidders that are machines."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Vickrey's dominance; the first-price equilibrium and its revenue; the all-pay auction by "
            "the envelope formula; Myerson's reserve and Bulow and Klemperer's extra bidder; the winner's curse; "
            "prices for slots; the exposure problem; and a starred problem on demand reduction. Full solutions are "
            "in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Vijay Krishna, \emph{Auction Theory} (2nd ed., 2010)",
             r"Paul Klemperer, \emph{Auctions: Theory and Practice} (2004)",
             r"Paul Milgrom, \emph{Putting Auction Theory to Work} (2004)",
             r"John Kagel and Dan Levin, \emph{Common Value Auctions and the Winner's Curse} (2002)"],
            [r"Vickrey (1961); \ Myerson (1981); \ Riley and Samuelson (1981); \ Milgrom and Weber (1982)",
             r"Capen, Clapp and Campbell (1971); \ Bazerman and Samuelson (1983); \ Kagel, Harstad and Levin (1987); "
             r"\ Cox, Smith and Walker (1988)",
             r"Bulow and Klemperer (1996); \ Maskin and Riley (2000); \ Guerre, Perrigne and Vuong (2000)",
             r"Cramton and Schwartz (2000); \ Binmore and Klemperer (2002); \ Klemperer (2002a, 2002b)",
             r"Edelman, Ostrovsky and Schwarz (2007); \ Varian (2007); \ Ostrovsky and Schwarz (2009)",
             r"Garbade and Ingber (2005); \ Akbarpour and Li (2020); \ Milgrom and Segal (2020)"])
        with self.voiceover(
            "The reading: Vijay Krishna's Auction Theory, the graduate text; Paul Klemperer's Auctions, Theory and "
            "Practice; Paul Milgrom's Putting Auction Theory to Work; and Kagel and Levin on the winner's curse. "
            "Then the papers, from Vickrey to the incentive auction."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1945, r"American hospitals", r"offering internships to medical students two years before "
                          r"they graduate, \\ with hours to decide", color=E.ACCENT, width=10.6, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 17 \ $\cdot$ \ Act IV, \ Failure and Design", font_size=30, color=GREY_B),
                     label(r"Markets by Design", font_size=46),
                     label(r"can a market be engineered, \ when prices cannot do the work?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ markets with prices, \ designed; \ next: \ markets without them", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hc.next_to(head, DOWN, buff=0.45)
        nxt.next_to(hc, DOWN, buff=0.5)
        with self.voiceover(
            "This part designed markets with prices. The next designs markets where prices can't be used. "
            "<bookmark mark='a'/> By 1945, American hospitals were offering internships to medical students two "
            "years before they graduated, and giving them hours to decide. The market for young doctors was "
            "unravelling. <bookmark mark='b'/> Part seventeen: markets by design."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)          # the score's close plays here, after the last line, not under it
        self.clear_scene()
