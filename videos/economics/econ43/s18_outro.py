from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403

PROBLEMS = [
    r"Cournot: \ three firms with shares 50\%, \ 30\% and 20\%; \ market demand has elasticity 2. \ Find each firm's "
    r"margin, \ the Herfindahl index and the industry's margin.",
    r"Logit: \ two products with shares 0.2 and 0.3 \ (outside good 0.5), \ $\alpha$ = 0.5, \ $p_1$ = 4. \ Find "
    r"product 1's own-price elasticity and product 2's elasticity with respect to $p_1$.",
    r"The red bus: \ a car and a blue bus each take half. \ A red bus identical to the blue appears. \ Find the shares "
    r"under plain logit, \ and under nested logit with the buses in one nest as $\sigma \to 1$.",
    r"Upward pricing pressure: \ diversion from product 1 to product 2 is 0.4, \ product 2's margin is \$3, \ product "
    r"1's cost is \$10. \ With a 5\% cost credit, \ is there upward pressure?",
    r"Berry's inversion: \ with plain logit, \ a product's share is 0.2 and the outside share 0.5. \ Find its mean "
    r"utility, \ and show that, started there, \ the contraction does not move when $\sigma$ = 0.",
    r"De Loecker and Warzynski: \ materials' output elasticity is 0.6 and materials are 40\% of revenue. \ Find the "
    r"markup. \ What if the elasticity were mis-estimated as 0.7?",
    r"Entry: \ a town needs 1,000 people for one dentist and 3,333 for two. \ Find the ratio of per-firm thresholds, "
    r"\ and what it says about the duopoly's margin per resident.",
    r"$\bigstar$ \ Derive the multi-product first-order conditions and show that $p - c = -(\Omega \circ "
    r"\partial s/\partial p')^{-1} s$; \ for single-product logit firms, \ show $p_j - c_j = 1/(\alpha(1 - s_j))$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Not from concentration alone. \ Estimate how buyers substitute, \ from prices, \ shares "
                          r"and characteristics with good instruments, \ and the markups and the conduct that fit "
                          r"follow; \ or read markups from production data, \ or from how many firms a town can "
                          r"support.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1947, 2027], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, PROFIT, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: how do you tell whether a market is competitive when you cannot see anyone's costs? "
            "<bookmark mark='a'/> Not from concentration alone. Estimate how buyers substitute between products, "
            "from prices, shares and characteristics, with instruments that move prices but not unseen quality; "
            "then the markups, and the conduct that fits them, follow. Or read markups from production data, with a "
            "carefully estimated production function. Or count how many firms towns of different sizes can support."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        S, G, C, B, R, M, Pl, D, E_ = (load(x) for x in ("scp", "playit", "cars", "blpdata", "cereal", "merger",
                                                         "plants", "dlw", "entry"))
        items = [
            (r"the aisle: \ four firms, \ high margins, \ a `shared monopoly' case dismissed in 1981", PRICE),
            (rf"structure: \ concentration and margins correlate ({S['corr']:.2f}) with no collusion", LOSS),
            (rf"the game: \ the bran twins +{100 * G['x']['merged']:.0f}\%, \ the two largest "
             rf"+{100 * G['y']['merged']:.0f}\%: \ diversion, \ not shares", NEST[2]),
            (r"conduct: \ parallel shifts cannot reveal it; \ a rotation of demand can", THEORY),
            (r"logit: \ substitution in proportion to share; \ the red bus; \ nests", IV_C),
            (rf"BLP: \ shares as integrals, \ Berry's contraction, \ moments; \ $\alpha$ = "
             rf"{C['mean']['blp_alpha']:.2f} against {C['alpha']}", BLP_C),
            (rf"real cars: \ plain logit leaves {B['iv']['inelastic']} impossible answers, \ even by IV", OLS_C),
            (rf"Nevo's test: \ portfolios, \ not a cartel: \ {100 * R['avg']['actual']:.0f}\% against "
             rf"{100 * R['avg']['joint']:.0f}\%", PRICE),
            (rf"mergers: \ +{100 * M['dp_merged']:.1f}\% without savings; \ "
             rf"{100 * M['cmcr_merged']:.0f}\% savings to offset; \ new goods", LOSS),
            (rf"production: \ OLS {Pl['ols']['bl']:.2f}, \ ACF {Pl['acf']['bl']:.2f}, \ truth "
             rf"{TRUTH['plants']['bl']}", BLP_C),
            (rf"markups from accounts: \ 1.21 $\to$ 1.61, \ contested; \ a wrong elasticity gives "
             rf"{D['median']['ols']:.2f}", HOLD),
            (rf"entry: \ the 2nd and 3rd firm bring competition \ ({E_['est']['ratio'][0]:.2f}, \ "
             rf"{E_['est']['ratio'][1]:.2f}, \ then about 1)", DEMAND),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 43, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-three in twelve lines. <bookmark mark='a'/> A few firms make most of America's cereal at "
            "high margins, and a decade-long case could not prove collusion. Concentration and margins move "
            "together even when every firm competes, because efficient firms grow large. In the game, the merger "
            "that barely moved the concentration index raised prices most, because what matters is where lost "
            "buyers go. Conduct can be identified when something rotates demand. The plain logit makes substitution "
            "follow market shares, which the red bus mocks and nests partly repair. Berry, Levinsohn and Pakes let "
            "tastes differ across buyers, invert shares with a contraction, and estimate by moments, and on the "
            "Island their estimator finds the truth. On the real cars, plain logit leaves hundreds of impossible "
            "answers. Nevo's test finds the cereal margins explained by brands and portfolios, not a cartel. "
            "Simulations predict a merger's price rises and the savings that would offset them, and the logit "
            "overvalues new goods. Production functions need proxies for unseen productivity, and markups from "
            "accounts hinge on the elasticity, which is why their rise is contested. And counting firms in towns "
            "shows competition arriving with the second and third."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Cournot margins and the Herfindahl index; logit elasticities; the red bus; upward pricing "
            "pressure; Berry's inversion; a markup from accounts; entry thresholds; and a starred derivation of "
            "multi-product markups. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Jean Tirole, \emph{The Theory of Industrial Organization} (1988)",
             r"Kenneth Train, \emph{Discrete Choice Methods with Simulation} (2nd edition, 2009)",
             r"Aviv Nevo, \ `A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand', \ "
             r"\emph{JEMS} (2000)",
             r"Steven Berry and Philip Haile, \ `Foundations of Demand Estimation', \ \emph{Handbook of Industrial "
             r"Organization} 4 (2021)"],
            [r"Bain (1951); \ Lancaster (1966); \ Demsetz (1973); \ McFadden (1974); \ Bresnahan (1982); \ Lau (1982)",
             r"Bresnahan and Reiss (1991); \ Berry (1994); \ Berry, \ Levinsohn and Pakes (1995, \ 2004)",
             r"Olley and Pakes (1996); \ Werden (1996); \ Nevo (2001); \ Axtell (2001); \ Petrin (2002)",
             r"Levinsohn and Petrin (2003); \ Farrell and Shapiro (2010); \ Syverson (2011); \ De Loecker and "
             r"Warzynski (2012)",
             r"Ackerberg, \ Caves and Frazer (2015); \ Ashenfelter, \ Hosken and Weinberg (2015); \ Miller and "
             r"Weinberg (2017)",
             r"Traina (2018); \ Basu (2019); \ De Loecker, \ Eeckhout and Unger (2020); \ Bond et al.\ (2021)"])
        with self.voiceover(
            "The reading: Tirole's text on industrial organization; Kenneth Train's book on discrete choice; Nevo's "
            "practitioner's guide to the random-coefficient estimator; and Berry and Haile's survey of what demand "
            "data can identify. Then the papers, from Bain to the debate over rising markups."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1987, r"John Rust", r"recovers, \ from a decade of a bus superintendent's decisions about "
                          r"when to rebuild engines, \ what the superintendent must have believed a breakdown costs",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 44 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Dynamics, \ Platforms and Antitrust", font_size=46),
                     label(r"how do firms compete over time, \ and what is different when the product is a network?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from markets at a moment \ to markets over time", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Everything in this part happened at a moment: prices set, demand estimated, a merger simulated. "
            "<bookmark mark='a'/> In 1987 John Rust took the records of Harold Zurcher, who decided month by month "
            "whether to rebuild the engines of the buses in Madison, Wisconsin, and recovered from those decisions "
            "what Zurcher must have believed a breakdown costs. <bookmark mark='b'/> Part forty-four: dynamics, "
            "platforms and antitrust. How do firms compete over time, and what is different when the product is a "
            "network?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
