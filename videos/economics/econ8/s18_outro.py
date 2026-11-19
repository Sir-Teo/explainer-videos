from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403

PROBLEMS = [
    r"The yard: \ $q = 2K^{0.25}L^{0.5}$. \ Find $MP_L$, $MP_K$ and the technical rate of substitution at $K = L = 4$, "
    r"\ and the returns to scale.",
    r"Cost minimization: \ $w = 1000$, $r = 400$, $q = 8$. \ Find the least-cost $K$ and $L$, the cost, \ and check "
    r"Shephard's lemma for $L$.",
    r"Show that marginal cost cuts average cost at its minimum. \ For $TC = 4000 + 200q + 50q^2$ find the break-even "
    r"and shut-down prices.",
    r"Play it: \ with 4 slipways, a price of \$1{,}200 and a wage of \$1{,}000, \ how many shipwrights maximize "
    r"profit? \ How does the answer change if the wage falls to \$800?",
    r"Supply: \ for Cobb--Douglas with $a + b < 1$, \ show that the long-run supply elasticity is $(a+b)/(1-a-b)$ "
    r"and the short-run $b/(1-b)$.",
    r"Free entry: \ demand $Q = 400 - 0.2p$ and the cost above. \ Find the long-run price, each yard's output and the "
    r"number of yards.",
    r"Hold-up: \ value $2V\sqrt{i}$, cost $i$, the investor gets a share $\theta$ ex post. \ Find its investment and "
    r"the surplus lost, \ as a function of $\theta$.",
    r"$\bigstar$ \ Refit Cobb and Douglas's 1899--1922 data with a time trend and with growth rates. \ Why does "
    r"capital's coefficient turn negative, \ and what would you need to estimate it credibly?",
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
        a = wrapped_label(r"At the margin. \ A firm hires each input until the last unit earns what it costs, \ "
                          r"builds where price equals marginal cost, \ and, with free entry, \ the industry settles "
                          r"where profits vanish. \ And it exists because using the market has costs: \ it draws its "
                          r"boundary where organizing one more transaction inside costs as much as buying it "
                          r"outside, \ and ownership goes where investment matters most.", 11.6, 29, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        logo = slipway(1.4).next_to(a, DOWN, buff=0.45)
        with self.voiceover(
            "So: how does a firm decide what to make and how, and why is there a firm at all? "
            "<bookmark mark='a'/> At the margin. It hires each input until the last unit earns what it costs, builds "
            "until price equals marginal cost, and, with free entry, the industry settles where profits disappear. "
            "And the firm exists because using the market has costs. It draws its boundary where organizing one more "
            "transaction inside costs as much as buying it outside, and ownership goes to whoever's investment matters "
            "most."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(logo[0]), Create(logo[1]))
        self.clear_scene()

    def recap(self):
        d, t, c, cu, p, s, i, se, b = (load(x) for x in ("douglas", "techs", "costmin", "curves", "playit", "supply",
                                                          "industry", "selection", "boundary"))
        items = [
            (rf"Douglas's chart: \ output a quarter of the way from labour to capital ({d['where_mean']:.2f})", OUT),
            (rf"$P' = {d['A']:.2f}\,L^{{3/4}}C^{{1/4}}$ refitted; \ with a trend, capital's exponent "
             rf"{signed(d['trend']['capital'])}", OUT),
            (r"the labour share: \ about 62\% for fifty years, \ then falling", LAB),
            (rf"technology: \ isoquants, \ $MP_L$ falling ({t['inc'][0]:.2f}, {t['inc'][1]:.2f}, {t['inc'][2]:.2f}), "
             rf"\ TRS {t['trs_at']['trs']:.0f}", ISO),
            (r"CES and $\sigma$: \ Cobb--Douglas is $\sigma = 1$; \ shares move when $\sigma \neq 1$", LAB),
            (r"returns to scale: \ pipelines, \ the six-tenths rule", CAP),
            (rf"least cost: \ TRS = $w/r$; \ 8 boats for \${c['cost']:,.0f}".replace(",", "{,}"), COST),
            (rf"cost curves: \ the U, \ marginal cost through its bottom; \ the long-run envelope", ATC),
            (rf"the boatyard: \ hire {p['hired']}, \ where $p \cdot MP_L = w$; \ supply elastic {s['le_chatelier']['short']:.0f} "
             rf"short run, {s['le_chatelier']['long']:.0f} long run", PRICE),
            (rf"free entry: \ price \${i['same']['price']:,.0f}, \ about {i['same']['firms']:.0f} yards; \ with "
             rf"differences, rents".replace(",", "{,}"), PRICE),
            (rf"survival: \ markups converge on the optimum, \ {se['total_closed']} closures later", COST),
            (r"Coase, \ Williamson, \ hold-up, \ Fisher Body's record, \ and who should own", FIRM),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {txt}", font_size=28, color=col) for k, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 8, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part eight in twelve lines. <bookmark mark='a'/> Douglas saw output sitting a quarter of the way from "
            "labour to capital, and Cobb gave him a formula that refits exactly, and falls apart with a time trend. "
            "Labour's share held near sixty-two percent for half a century, then fell. Technology is isoquants and "
            "marginal products, substitution measured by sigma, and returns to scale that come from geometry. Least "
            "cost sets the rate of substitution equal to relative prices, and from it come the cost curves, short "
            "run and long. You hired three shipwrights in the boatyard; supply is marginal cost, more elastic in the "
            "long run; free entry drives profit to zero, except where something scarce earns a rent; and survival "
            "can stand in for maximizing, slowly. Coase explained why firms exist at all, Williamson when to make "
            "rather than buy, and the record of Fisher Body why to check the story."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. The yard's technology; its least-cost inputs and Shephard's lemma; why marginal cost cuts "
            "average cost at its bottom; the boatyard at a lower wage; supply elasticities, short and long; the "
            "free-entry equilibrium; hold-up as a function of bargaining power; and a research problem, marked with "
            "a star, on refitting Cobb and Douglas's data. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Hal Varian, \emph{Intermediate Microeconomics}, chs.\ 19--24",
             r"Andreu Mas-Colell, Michael Whinston and Jerry Green, \emph{Microeconomic Theory}, ch.\ 5",
             r"Oliver Williamson, \emph{The Economic Institutions of Capitalism} (1985)",
             r"Oliver Hart, \emph{Firms, Contracts, and Financial Structure} (1995)"],
            [r"Cobb and Douglas (1928), \emph{AER}; \ Douglas (1976), \emph{JPE}; \ Felipe and Adams (2005)",
             r"Arrow, Chenery, Minhas and Solow (1961); \ Chenery (1949); \ Samuelson's Le Chatelier principle",
             r"Hall and Hitch (1939); \ Alchian (1950); \ Friedman (1953)",
             r"Coase (1937), \emph{Economica}; \ Williamson (1975, 1985); \ Klein, Crawford and Alchian (1978)",
             r"Coase (2000), Klein (2000), Freeland (2000), Casadesus-Masanell and Spulber (2000), \emph{JLE}",
             r"Grossman and Hart (1986); \ Hart and Moore (1990), \emph{JPE}; \ Gollin (2002); \ Karabarbounis and "
             r"Neiman (2014)",
             r"Haskel and Westlake (2018); \ Brynjolfsson, Li and Raymond (2025); \ Shahidi et al.\ (2025)"])
        with self.voiceover(
            "The reading: Varian's chapters on technology, costs and supply; chapter five of Mas-Colell, Whinston "
            "and Green; Williamson's Economic Institutions of Capitalism; and Oliver Hart's Firms, Contracts, and "
            "Financial Structure. Then the papers, from Cobb and Douglas to the Coasean singularity."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1954, r"Kenneth Arrow \ and G\'erard Debreu", r"a proof that a competitive economy has a "
                          r"set of prices clearing every market at once, \ and the conditions it needs",
                          color=E.ACCENT, width=9.0, font_size=26).move_to(UP * 0.6)
        lead = label(r"from one firm and one market \ to all of them at once", font_size=40, color=GREY_A)
        nxt = VGroup(label(r"Next: \ Part 9 \ $\cdot$ \ Act III, Markets", font_size=30, color=GREY_B),
                     label(r"The Invisible Hand, Proved", font_size=56, color=WHITE),
                     label(r"can a whole economy of selfish traders reach a state nobody could improve on, \ and "
                           r"will it?", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.15).next_to(hc, DOWN,
                                                                                                    buff=0.6)
        with self.voiceover(
            "Act Two is done: the consumer, time and risk, and now the firm. Act Three puts them together in "
            "markets. <bookmark mark='a'/> In 1954 Kenneth Arrow and Gerard Debreu proved that a competitive economy "
            "has a set of prices that clears every market at once, and said exactly what that requires. "
            "<bookmark mark='b'/> Part nine: the invisible hand, proved."
        ) as vo:
            self.play(FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
