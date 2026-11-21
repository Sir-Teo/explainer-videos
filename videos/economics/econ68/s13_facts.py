from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

SHORT = {
    "engel": r"food's share falls with income", "demand_slopes": r"demand slopes down",
    "smooth_consumption": r"consumption smoother than income", "zipf_firms": r"firm sizes follow Zipf",
    "dispersion": r"productivity dispersion", "sticky_prices": r"most prices change rarely",
    "auctions_converge": r"double auctions converge", "one_price": r"one price for gold, not haircuts",
    "winners_curse": r"the winner's curse", "passthrough": r"pass-through is incomplete",
    "flat_for_millennia": r"flat for millennia, then growth", "kaldor": r"Kaldor's facts",
    "conditional_convergence": r"conditional convergence", "labour_share": r"the labour share fell",
    "price_of_light": r"the price of light", "okun": r"Okun's law", "beveridge": r"the Beveridge curve",
    "volatility": r"investment most volatile", "hours": r"hours move with output", "hump": r"hump-shaped responses",
    "persistence": r"inflation persists", "asymmetry": r"long expansions, short recessions",
    "quantity": r"money and prices in the long run", "equity_premium": r"the equity premium",
    "unpredictable": r"returns hard to predict", "yield_curve": r"inversions before recessions",
    "credit_booms": r"credit booms before crises", "gravity": r"gravity", "random_walk": r"exchange rates wander",
    "intra_industry": r"intra-industry trade", "few_exporters": r"few firms export", "zipf_cities": r"Zipf's cities",
    "mincer": r"Mincer's wage curve", "pareto": r"Pareto's top tail", "gatsby": r"the Great Gatsby curve",
    "child_penalty": r"the child penalty",
}


class Facts(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Agora against the Facts", r"Of the regularities any account of an economy must reproduce, \ "
             r"how many does the economy the series built produce?", "Chapter eleven. Agora against the Facts.",
             scale=("world",), horizon=("a century",))
        self.grid()
        self.open_ones()

    def grid(self):
        S = load("scorecard")
        cells = VGroup()
        for r in S["rows"]:
            ok = bool(r["agora"])
            col = TRUE if ok else GREY_B
            box = RoundedRectangle(width=3.05, height=0.5, corner_radius=0.06, stroke_color=col, stroke_width=1.6,
                                   fill_color=col, fill_opacity=0.16 if ok else 0.04)
            t = label(SHORT.get(r["key"], tex_safe(r["key"])), font_size=13, color=WHITE if ok else GREY_B)
            if t.width > 2.85:
                t.scale_to_fit_width(2.85)
            t.move_to(box)
            cells.add(VGroup(box, t))
        cells.arrange_in_grid(rows=9, cols=4, buff=(0.12, 0.1), flow_order="dr").move_to(DOWN * 0.25)
        head = label(rf"{S['filled']} of {S['n']} Facts reproduced by Agora", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.35)
        tag = published_tag(r"explainer/economics/facts.py: \ the Facts and Agora's column", corner=DL, font_size=12)
        with self.voiceover(
            f"Part one fixed {S['n']} Facts that any account of an economy has to reproduce, from Engel's law to the "
            "child penalty. Each had three columns: your guess, the data, and Agora, the economy the series built, "
            "filled in by the part that built the mechanism. <bookmark mark='a'/> Here is the whole list. <bookmark "
            f"mark='b'/> {S['filled']} of the {S['n']} are reproduced: Agora's households smooth consumption, its "
            "firms set sticky prices, its traders converge, its bidders suffer the winner's curse, its growth is "
            "flat for millennia and then takes off, its banks lend into crises, its cities and incomes follow "
            "Zipf and Pareto."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(c[0]) for c in cells], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(head), *[Indicate(c[0], color=TRUE, scale_factor=1.02) for c, r in
                                      zip(cells, S["rows"]) if r["agora"]])
        self.clear_scene()

    def open_ones(self):
        S = load("scorecard")
        cards = point_cards([
            (r"firm sizes follow Zipf", r"shown in Part 43; \ the random-growth mechanism was built for cities "
             r"(Part 37), \ never run for firms", GREY_B),
            (r"long expansions, \ short recessions", r"shown in Part 27; \ the equilibrium cycle of Part 29 is "
             r"symmetric, \ and a switching model only describes it", TOLL),
            (r"the yield curve inverts before recessions", r"shown in Part 57's probit; \ no part built the "
             r"expectations that would make it", DATA),
            (r"what that means", r"three Facts the series could show but not yet explain: \ the next economics' "
             r"work, \ listed in the open", MODEL),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(rf"the {S['n'] - S['filled']} that stayed open", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                       buff=0.5)
        with self.voiceover(
            f"And the {S['n'] - S['filled']} that stayed open. <bookmark mark='a'/> Firm sizes follow Zipf's law; "
            "the random growth that produces it was built for cities in Part thirty-seven, and never run for firms. "
            "<bookmark mark='b'/> Expansions are long and recessions short; the equilibrium cycle of Part "
            "twenty-nine is symmetric, and a switching model only describes the asymmetry. <bookmark mark='c'/> The "
            "yield curve inverts before most recessions; Part fifty-seven measured it, but no part built the "
            "expectations that would produce it. <bookmark mark='d'/> Three Facts the series could show and not "
            "explain. A scorecard that admits its gaps is worth more than one that hides them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
