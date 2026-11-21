from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403

PROBLEMS = [
    r"Hotelling: \ the interest rate is 5\%, \ extraction costs 2 a ton and the price today is 5. \ What does the rule "
    r"predict for the price in ten years? \ What if the cost falls 4\% a year?",
    r"The fishery: \ stock grows $0.5\,S(1-S)$, \ catch is $E\,S$, \ fish sell at 1 and effort costs 0.2. \ Find the "
    r"open-access effort and stock, \ the rent-maximizing effort and its rent, \ and the maximum sustainable yield.",
    r"Discounting: \ what is a dollar of damage in 75 years worth today at 1\%, \ 3\% and 5\%? \ And 5 dollars a "
    r"year forever?",
    r"Ramsey: \ with growth of 1.75\% a year, \ find the discount rate for $\rho$ = 0.1\%, \ $\eta$ = 1 and for "
    r"$\rho$ = 1.5\%, \ $\eta$ = 1.45.",
    r"Prices or quantities: \ damage is a flat 50 a tonne; \ the cost of cutting $q$ tonnes is $\theta + q$ at the "
    r"margin, \ with $\theta$ = 30 or 50, \ equally likely. \ Compare a tax of 50 with a cap at the expected optimum.",
    r"Learning: \ with a learning rate of 20\%, \ how far has the price fallen after five doublings of output?",
    r"Withholding: \ using the Island's power plants and a load of 35 GW, \ find Dynamo's profit when it offers "
    r"everything and when it holds back 2 GW of gas B.",
    r"$\bigstar$ \ A tonne's damage starts at $D_0$ a year and grows at $g$ forever. \ Find its social cost at a "
    r"discount rate $r > g$, \ and explain why the answer is so sensitive when $r$ is close to $g$.",
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
        a = wrapped_label(r"Between about 30 and 200 dollars on most estimates, \ and the answer turns above all "
                          r"on the discount rate, \ then on how large and how lasting the damage is, \ and on the "
                          r"risk of the worst. \ Where things have owners, \ prices manage scarcity; \ where they do "
                          r"not, \ a price on carbon has to be built.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1850, 2025], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, HEAT, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what is a tonne of carbon dioxide worth, and what does the answer turn on? <bookmark mark='a'/> "
            "Between about thirty and two hundred dollars on most estimates, and more if the newest work on global "
            "damage is right. The answer turns above all on the discount rate, a judgment about how much the future "
            "counts; then on how large and how lasting the damage is, which the data are only beginning to tell us; "
            "and on the risk of the worst. Where things have owners, like Simon's metals, prices manage scarcity. "
            "Where they do not, like fish in the open sea and the air, a price has to be built."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        M, B, Fi, Fa, C, D, S, L, Cl, So, P, Pw = (load(x) for x in (
            "metals", "bet", "fishery", "fao", "climate", "dice", "scc", "tails", "club", "solar", "panel", "power"))
        O = D["opt"]
        st = Pw["steps"]
        items = [
            (rf"the bet: \ 1980--90, \ {100 * M['bundle_8090']:+.0f}\%; \ Ehrlich wins about half of all decades"
             .replace("-", "{-}"), METAL),
            (r"Hotelling: \ the rent rises at the rate of interest; \ prices need not, \ and mostly did not", METAL),
            (rf"the fishery: \ open access, \ stock {Fi['open_end']:.1f}; \ a quota, \ {Fi['quota_end']:.1f}; \ "
             rf"overexploited: \ {Fa['first']:.0f}\% to {Fa['last']:.0f}\%", FISH),
            (rf"the climate: \ four equations, \ {C['decade_model']:.2f}\textdegree \ against "
             rf"{C['decade_obs']:.2f}\textdegree", HEAT),
            (rf"the model: \ optimal warming {O['T2100']:.1f}\textdegree \ in 2100, \ \${O['price2050']:.0f} a tonne "
             r"in 2050", OPT),
            (rf"the discount rate: \ \${S['by_rate'][0]:.0f} \ at 1\%, \ \${S['by_rate'][4]:.0f} \ at 3\%, \ "
             rf"\${S['by_rate'][8]:.0f} \ at 5\%", STERN),
            (rf"ethics: \ near-zero time preference, \ \${S['stern']:.0f}; \ modest, \ \${S['ramsey']:.0f}", STERN),
            (rf"fat tails: \ the answer follows the cut-off, \ {100 * L['fat'][1]:.0f}\% to {100 * L['fat'][-1]:.0f}\%",
             HEAT),
            (r"instruments: \ flat damage favours a price; \ British Columbia, \ 2008--2025; \ the EU above 100",
             POLICY),
            (rf"clubs: \ no tariff, \ nobody; \ {100 * Cl['full']:.0f}\%, \ all {Cl['n']}; \ solar: \ "
             rf"{100 * So['learning_rate']:.0f}\% cheaper each doubling", CLEAN),
            (rf"damages: \ growth peaks near {P['optimum']:.0f}\textdegree C; \ hot, \ poor places lose", HEAT),
            (rf"power: \ holding back 2 GW, \ {st[1]['profit'] / st[0]['profit']:.0f} times the profit; \ California, "
             r"\ 59\% market power", POWER),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 48, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del B
        with self.voiceover(
            "Part forty-eight in twelve lines. <bookmark mark='a'/> Simon won his bet, but a decade of metal prices "
            "is close to a coin toss. Hotelling's rent rises at the rate of interest, while the prices of metals "
            "barely rose, because costs fell and supply grew. Fish without owners are overfished; quotas that can be "
            "traded save them. Four equations, fitted to the record, reproduce the warming so far. A climate-economy "
            "model built on them finds an optimal path to about two and a half degrees, with a carbon price near a "
            "hundred dollars by 2050. The social cost of carbon falls from hundreds of dollars to tens as the "
            "discount rate rises, and the rate is partly an ethical choice. With fat tails, the answer depends on "
            "the worst case allowed. A flat damage favours a price over a cap. A club with a penalty tariff can "
            "hold together where goodwill cannot. Solar power got cheaper the more was built. Hot, poor places lose "
            "the most from warm years. And in electricity, holding back a little capacity can pay a great deal."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Hotelling's price in ten years; the fishery's three efforts; discounting a dollar and a "
            "stream; Ramsey's rate; prices against quantities when costs are uncertain; a learning curve; Dynamo's "
            "withholding; and a starred problem on why the social cost of carbon is so sensitive to the discount "
            "rate. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"William Nordhaus, \emph{A Question of Balance} (2008) and \emph{The Climate Casino} (2013)",
             r"Nicholas Stern, \emph{The Economics of Climate Change: The Stern Review} (2007)",
             r"Paul Sabin, \emph{The Bet} (2013)",
             r"Tom Tietenberg and Lynne Lewis, \emph{Environmental and Natural Resource Economics}"],
            [r"Hotelling (1931); \ Gordon (1954); \ Smith (1969); \ Weitzman (1974); \ Slade (1982); \ Nordhaus (1992)",
             r"Borenstein et al. (2002); \ Hughes et al. (2008); \ Costello et al. (2008); \ Weitzman (2009)",
             r"Kiel et al. (2010); \ Acemoglu et al. (2012); \ Dell et al. (2012); \ Chen et al. (2013)",
             r"Burke et al. (2015); \ McGlade and Ekins (2015); \ Nordhaus (2015, 2017); \ Barreca et al. (2016)",
             r"Ebenstein et al. (2017); \ Deryugina et al. (2020); \ Dietz et al. (2021); \ Rennert et al. (2022)",
             r"Barrage and Nordhaus (2024); \ Bilal and K\"anzig (2024)"])
        with self.voiceover(
            "The reading: William Nordhaus's A Question of Balance and The Climate Casino; the Stern Review; Paul "
            "Sabin's history of the bet; and Tom Tietenberg and Lynne Lewis's textbook on environmental and natural "
            "resource economics. Then the papers, from Hotelling's rule to the newest estimates of global damage."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1968, r"Gary Becker", r"late for a student's oral exam, \ he weighs a car park against the "
                          r"chance of a ticket, \ parks in the street, \ and sees crime as a choice", color=E.ACCENT,
                          width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 49 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"The Economic Approach", font_size=46),
                     label(r"how far can the model of choice under constraint be pushed into the rest of life?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from the planet \ to the rest of life", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Next time, the economic approach to everything else. <bookmark mark='a'/> In the 1960s Gary Becker, "
            "late for a student's oral examination, had to choose between a car park and the street. He weighed "
            "the chance of a ticket and the fine against the cost of the car park, parked in the street, and did "
            "not get a ticket. By the time he reached the room he was thinking of crime as a choice, the idea of "
            "his 1968 paper. <bookmark mark='b'/> Part forty-nine asks how far the model of choice under "
            "constraint can be pushed into the rest of life, and where it breaks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
