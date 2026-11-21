from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

PROBLEMS = [
    r"Year-on-year differences: \ show that comparing each month with the same month a year before removes a "
    r"seasonal factor common to both groups, \ and what it does to a linear trend specific to one group.",
    r"Placebo subtraction: \ with a group-specific drift $\delta$ a year and an effect $\tau$, \ show that the 2025 "
    r"comparison estimates $\tau + \delta$ and the 2024 placebo $\delta$.",
    r"The clock: \ explain why a jump in entries at 9 pm measures retiming, \ and what extra data would be needed to "
    r"count the trips given up.",
    r"The externality: \ with $T(V) = T_0(1 + a v^b)$, \ show that $V\,T'(V) = e\,T$ with $e = b\,s$, \ and that "
    r"the marginal external cost is $e \times T \times$ the value of time.",
    r"Demand: \ with $V = A P^{\eta}$, \ compute $\eta$ from a 3.9\% fall in traffic when the full price of a trip "
    r"rises from \$31 to \$39.9.",
    r"$\bigstar$ \ Diversion: \ if a share $d$ of the trips lost on the tolled crossings appears on the comparison "
    r"crossings, \ derive the bias of the difference in differences, \ and its sign.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.last_market()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.5)
        a = wrapped_label(r"From a question that matters and can be answered, \ data described before they are "
                          r"used, \ a design whose threats are written down first, \ the smallest model that speaks "
                          r"to the estimates, \ a counterfactual with its uncertainty, \ and the honesty to say what "
                          r"the design cannot show. \ Then others check it, \ and the record grows.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        with self.voiceover(
            "So: how is a new piece of economics made? <bookmark mark='a'/> From a question that matters and can be "
            "answered; data described before they are used; a design whose threats are written down first; the "
            "smallest model that speaks to the estimates; a counterfactual that carries its uncertainty; and the "
            "honesty to say what the design cannot show. Then others check it, and the record grows."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
        self.clear_scene()

    def recap(self):
        E_, D, Bu, V, C, M, R, I, S, Dl, Ca = (load(x) for x in (
            "entries", "did", "buses", "vmt", "clock", "model", "cf", "island", "scorecard", "dials", "calls"))
        items = [
            (r"the question: \ what did New York's charge do?", TOLL),
            (rf"the data: \ about {E_['weekday_all'] / 1000:.0f},000 entries a weekday; \ no before in that file",
             DATA),
            (r"the design: \ year-on-year comparisons with placebo years", TRUE),
            (rf"tunnels: \ {100 * D['effect']:.1f}\%, \ net of their drift {100 * D['adjusted']:.1f}\%".replace(
                "-", "{-}"), CTRL),
            (rf"buses: \ {100 * Bu['effect']:+.1f}\% against outside; \ miles in the zone "
             rf"{100 * V['crz_change']:+.1f}\%".replace("-", "{-}"), BUS),
            (rf"the clock: \ +{100 * (np.exp(C['nine']['jump']) - 1):.0f}\% at 9 pm, \ "
             rf"{100 * (np.exp(C['five']['jump']) - 1):.0f}\% at 5 am".replace("-", "{-}"), DATA),
            (rf"the model: \ $\eta = {M['eta']:.2f}$, \ a car's delay to others \${M['mec_old']:.2f}".replace("-",
                                                                                                         "{-}"),
             MODEL),
            (rf"\$15: \ traffic {100 * (np.exp(R['lnV'][1]) - 1):.1f}\% \ [{100 * (np.exp(R['lnV'][0]) - 1):.1f}, \ "
             rf"{100 * (np.exp(R['lnV'][2]) - 1):.1f}]".replace("-", "{-}"), TOLL),
            (rf"the Island: \ a 1.5\% drift turns {100 * I['trend']['truth']:.0f}\% into "
             rf"{100 * I['trend']['mean']:.1f}\%; \ the placebo fixes it".replace("-", "{-}"), ROW),
            (rf"the Facts: \ {S['filled']} of {S['n']} reproduced", TRUE),
            (rf"the Dials: \ {Dl['statuses'].get('settled within a range', 0)} settled of {Dl['n']}", DATA),
            (rf"Called it?: \ {Ca['verdicts'].get('right', 0)} right of {Ca['n']}", TOLL),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 68, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-eight in twelve lines. <bookmark mark='r1'/> A question with a date and a law. <bookmark "
            "mark='r2'/> Data, described first, and a file with no before. <bookmark mark='r3'/> Comparisons with "
            "placebo years. <bookmark mark='r4'/> The tunnels' small effect, once their drift is removed. <bookmark "
            "mark='r5'/> Slightly faster buses, fewer miles. <bookmark mark='r6'/> A large jump at the minute the "
            "price changes. <bookmark mark='r7'/> A very inelastic demand, and a modest cost of a car's delay. "
            "<bookmark mark='r8'/> A counterfactual with its range. <bookmark mark='r9'/> The method checked where "
            "the truth is known. <bookmark mark='r10'/> The Facts, nearly all reproduced. <bookmark mark='r11'/> "
            "The Dials, mostly open. <bookmark mark='r12'/> And the calls, honestly scored."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The last problems: year-on-year differences; subtracting a placebo; what the clock measures; the "
            "external cost of a trip; the elasticity of demand; and a starred problem on the bias from diversion. "
            "Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"William Thomson, \ \emph{A Guide for the Young Economist} (2nd ed., \ 2011)",
             r"Hal Varian, \ `How to Build an Economic Model in Your Spare Time' (1997)",
             r"John Cochrane, \ `Writing Tips for Ph.D.\ Students' (2005); \ Jesse Shapiro, \ `How to Give an "
             r"Applied Micro Talk'"],
            [r"Vickrey (1963); \ Walters (1961); \ Small and Verhoef, \ \emph{The Economics of Urban Transportation}",
             r"Angrist and Pischke (2009); \ Cattaneo, \ Idrobo and Titiunik on regression discontinuity",
             r"the MTA's open data; \ the Office of the Governor (2024, \ 2026)",
             r"and the sixty-seven parts before this one"])
        with self.voiceover(
            "The reading for a dissertation: William Thomson's guide for the young economist; Hal Varian on building "
            "a model in your spare time; John Cochrane's writing tips and Jesse Shapiro on giving a talk. Then the "
            "economics of congestion, from Walters and Vickrey on, and the methods. And the sixty-seven parts "
            "before this one."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def last_market(self):
        ax = plane([0, 10], [0, 10], center=LEFT * 2.6 + DOWN * 0.2, x_length=5.6, y_length=5.0, xticks=[],
                   yticks=[], xlabel=r"quantity", ylabel=r"price", font_size=16)
        dem = path(ax, [0.5, 9.5], [9.0, 1.0], E.ACCENT, 3.4, smooth=False)
        sup = path(ax, [0.5, 9.5], [1.0, 9.0], FIRST, 3.4, smooth=False)
        meet = Dot(ax.ax.c2p(5, 5), radius=0.12, color=WHITE)
        stats = VGroup(
            label(r"68 parts", font_size=26, color=WHITE),
            label(rf"{load('dials')['n']} Dials, \ {load('dials')['estimates']} estimates", font_size=22, color=DATA),
            label(rf"{load('scorecard')['n']} Facts, \ {load('scorecard')['filled']} reproduced", font_size=22,
                  color=TRUE),
            label(rf"{load('calls')['n']} calls, \ scored", font_size=22, color=TOLL),
            label(r"one economy, \ built", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax.ax, RIGHT, buff=1.0)
        end = label(r"Economics, Built", font_size=54).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The series began with a market: traders in a pit, calling bids and asks, and a price nobody chose. "
            "<bookmark mark='a'/> Demand, and supply, the two blades of Marshall's scissors that the score has "
            "carried through every part. <bookmark mark='b'/> Where they meet, a price, and behind it everything "
            "this series has tried to build: the choices, the institutions, the money and the states that make the "
            "meeting possible, and the evidence that tells us when we have it right. <bookmark mark='c'/> Sixty-"
            "eight parts, the Dials, the Facts, the calls, and one economy, built. <bookmark mark='d'/> Thank you "
            "for building it with us."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(dem), Create(sup), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(meet, scale=2.0), Flash(meet, color=WHITE))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in stats], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.wait(9.5)
