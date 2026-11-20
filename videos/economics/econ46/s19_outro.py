from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403

PROBLEMS = [
    r"The line: \ a household of five spends 360 rupees a day; \ the PPP rate is 22 rupees per international "
    r"dollar. \ Is it below \$3.00 a head? \ What if the poor face prices 20\% above the national average?",
    r"The trap: \ $f(k) = \max(\sqrt{k}, \ 4\sqrt{k} - 11)$, \ $s$ = 0.3, \ $\delta$ = 0.1. \ Find the three steady "
    r"states, \ and say which are stable.",
    r"The moneylender: \ funds cost 10\%, \ 20\% of loans default, \ screening costs 10\% of each loan. \ Find the "
    r"break-even rate. \ What does a fall in defaults to 10\% do?",
    r"The multiplier: \ 60\% of spending stays in the village, \ and sellers spend 75\% of what they earn. \ Find the "
    r"multiplier. \ What if the transfer itself is half saved?",
    r"Townsend: \ with village shocks $v$ and own shocks $e$, \ show that the regression of $\Delta c$ on $\Delta y$ "
    r"without village-year effects is biased toward one.",
    r"Duflo: \ each school per 1,000 children adds 0.15 years and 1.2\% to wages. \ Find the return to a year of "
    r"school. \ What must be true for this to be the return?",
    r"Worms: \ in treated schools, \ treated pupils miss 7 points fewer days than untreated ones, \ who miss 4 fewer "
    r"than pupils in control schools. \ Find the effect on a treated child.",
    r"$\bigstar$ \ The budget: \ two programmes, \ $B_i(x) = a_i s_i (1 - e^{-x/s_i})$, \ and a budget $M$. \ Derive "
    r"the best split, \ and the condition under which one programme gets nothing.",
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
        a = wrapped_label(r"Sometimes because a threshold keeps them there; \ more often because markets for credit, "
                          r"\ insurance and information fail them, \ and small frictions loom large. \ What helps: \ "
                          r"growth above all, \ and programmes whose effects are measured, \ priced at the margin, \ "
                          r"and checked again where they are used.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1981, 2024], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, POOR, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why do the poor stay poor, and what actually helps? <bookmark mark='a'/> Sometimes because a "
            "threshold keeps them there, and a large push can free them. More often because the markets for "
            "credit, insurance and information work worst for the poor, and small frictions, a walk, a price of a "
            "few cents, a trip to town that can wait, loom large. What helps is growth, above all, and programmes "
            "whose effects have been measured, whose money is spent where the next dollar does most, and whose "
            "results are checked again in the places they are used."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        N, P, A, T, L, G, Le, C, M, Pa, R, Th, W, Tw, I, F, Mi, S, Tg = (load(x) for x in (
            "nets", "poverty", "aid", "trap", "lewis", "agrigap", "lender", "credit", "cash", "panes", "inpres",
            "thornton", "worms", "townsend", "insure", "fert", "mita", "sites", "target"))
        Wd = P["WLD"]
        items = [
            (rf"nets: \ demand down {100 * N['drop']:.0f}\% at 60 cents; \ use the same at every price", HEALTH),
            (rf"the count: \ {Wd['first']:.0f}\% to {Wd['last']:.0f}\% of the world below \$3.00 a day, \ "
             rf"{Wd['first_year']}--{Wd['last_year']}", POOR),
            (rf"the budget: \ all on nets {A['all_first']:.1f}, \ equal shares {A['even']:.1f}, \ the best split "
             rf"{A['best']:.1f}", GAIN),
            (rf"the trap: \ a threshold at {T['threshold']:.1f}; \ a transfer of 10 lifts "
             rf"{100 * T['runs']['10']['share_above_end']:.0f}\% for good", TRAP),
            (rf"farm and town: \ the turning point in year {L['turn']}; \ a gap of {G['median_poorest']:.1f} in the "
             r"poorest countries", FARM),
            (rf"credit: \ the lender's {100 * Le['rate']:.0f}\% is mostly cost; \ microcredit +{C['itt']:.1f} on "
             rf"{C['mean_control']:.0f}, \ gains at the top", CREDIT),
            (rf"cash: \ a multiplier of {M['multiplier']:.1f}; \ PANES raised support by "
             rf"{100 * Pa['support']['jump']:.0f} points", CASH),
            (rf"schools: \ the Wald ratio {R['wald']:.3f}, \ planted {R['truth']:.2f}; \ learning is the harder "
             r"problem", SCHOOL),
            (rf"health: \ the within-school comparison misses the spillover; \ results collected "
             rf"{100 * Th['none']:.0f}\% to {100 * Th['any']:.0f}\%", HEALTH),
            (rf"risk: \ Townsend's slope {Tw['main']['within']:.2f}, \ not {Tw['main']['raw']:.2f}; \ a default to "
             rf"buy +{100 * I['default']['diff']:.0f} points", RISK),
            (rf"farms: \ an offer at harvest, \ {100 * F['base']:.0f}\% to {100 * F['harvest_offer']:.0f}\%; \ the "
             r"same later, \ nothing", FARM),
            (rf"history and limits: \ the boundary's jump {Mi['jump']:+.2f}; \ the next site "
             rf"{S['next_lo']:+.2f} to {S['next_hi']:+.2f}".replace("-", "{-}"), HIST),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 46, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del W, Tg
        with self.voiceover(
            "Part forty-six in twelve lines. <bookmark mark='a'/> A price of sixty cents cut the demand for bed nets "
            "by more than half, and paying picked out nobody who would use them more. The share of the world in "
            "extreme poverty has fallen from almost half to a tenth. An aid budget should be spent where its next "
            "dollar does most. Where technology has a fixed cost, a threshold can trap households, and only a large "
            "enough push frees them. Farm workers produce far less than town workers in poor countries, and Lewis's "
            "wages stay flat until the surplus is gone. The moneylender's high rate is mostly the cost of information,"
            " and microcredit helps a few firms a lot and most not at all. Cash raises consumption and spreads through"
            " the village, and governments that pay it gain support. Duflo's schools give the return to schooling; "
            "whether children learn is the harder problem. Spillovers decide how a health trial must be designed, and "
            "the first cents of a price or a prize matter most. Villages insure themselves well but not fully, and a "
            "default sells insurance. A visit at harvest does for fertilizer what a large subsidy does later. And "
            "history leaves boundaries in incomes, while experiments leave honest uncertainty about the next place."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Whether a household is below the line; the trap's three steady states; the "
            "moneylender's rate; the village multiplier; why Townsend's test needs village effects; Duflo's Wald "
            "ratio; the effect of deworming on a treated child; and a starred derivation of the best split of an "
            "aid budget. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Abhijit Banerjee and Esther Duflo, \emph{Poor Economics} (2011)",
             r"Debraj Ray, \emph{Development Economics} (1998)",
             r"Amartya Sen, \emph{Development as Freedom} (1999)",
             r"Angus Deaton, \emph{The Great Escape} (2013)"],
            [r"Lewis (1954); \ Townsend (1994); \ Duflo (2001); \ Miguel and Kremer (2004); \ Schultz (2004)",
             r"Thornton (2008); \ Nunn (2008); \ Cohen and Dupas (2010); \ Dell (2010); \ Deaton (2010)",
             r"Duflo, \ Kremer and Robinson (2011); \ Banerjee et al. (2015); \ Banerjee, \ Karlan and Zinman (2015)",
             r"Haushofer and Shapiro (2016); \ Suri and Jack (2016); \ Muralidharan and Niehaus (2017)",
             r"Balboni et al. (2022); \ Egger et al. (2022); \ Aiken et al. (2022)"])
        with self.voiceover(
            "The reading: Banerjee and Duflo's Poor Economics, the case for the experimental approach in their own "
            "words; Debraj Ray's graduate text, Development Economics; Amartya Sen's Development as Freedom, on "
            "what development is for; and Angus Deaton's The Great Escape. Then the papers, from Lewis to the "
            "satellites."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2007, r"Olken", r"has engineers take core samples from over 600 new village roads in "
                          r"Indonesia to measure how much of the money went missing, \ then randomizes audits and "
                          r"village meetings", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 47 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Political Economy", font_size=46),
                     label(r"why do governments choose policies that economists can show are wasteful?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from programmes that work \ to governments that choose them", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Next time, political economy. <bookmark mark='a'/> Benjamin Olken wanted to know how much of the "
            "money for new roads in Indonesian villages was stolen. He had engineers dig core samples out of "
            "each finished road and price the materials actually in it, then randomized two cures: audits from "
            "above, and village meetings from below. <bookmark mark='b'/> Part forty-seven asks why governments "
            "so often choose policies that economists can show are wasteful."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
