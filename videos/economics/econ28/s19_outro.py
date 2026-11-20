from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403

PROBLEMS = [
    r"Phillips: \ from $\dot w + 0.900 = 9.638\,u^{-1.394}$, \ find the unemployment rate at which wages are "
    r"stable, \ and the slope there.",
    r"Acceleration: \ with $\pi_t = \pi_{t-1} - \beta(u_t - u^*)$, \ show that holding $u$ one point below $u^*$ "
    r"raises inflation by $\beta$ every year.",
    r"Adaptive expectations: \ show that $\pi^e_{t+1} = \lambda \sum_k (1-\lambda)^k \pi_{t-k}$; \ what is the mean "
    r"lag?",
    r"Lucas's islands: \ with $p_i = m + z_i$, \ derive $\mathbb{E}[z_i \mid p_i] = \theta p_i$ with $\theta = "
    r"\sigma_z^2/(\sigma_z^2 + \sigma_m^2)$.",
    r"The critique: \ fit $y = a + c\pi$ under a 2\% rule; \ why does it fail at 6\%? \ What \emph{is} stable?",
    r"Barro--Gordon: \ derive discretionary inflation $\lambda b k$, \ and show society's loss is higher than "
    r"under the rule $\pi = 0$.",
    r"Sacrifice: \ output is 2\%, 4\%, 3\%, 1\% below potential over four years while inflation falls from 9\% to "
    r"4\%; \ find the ratio.",
    r"$\bigstar$ \ Rogoff: \ with supply shocks of variance $\sigma^2$, \ find the banker's weight $w$ that minimizes "
    r"society's loss, \ and show $0 < w < \lambda$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 42, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Only for a while, \ and only by surprise. \ Unemployment falls below its natural rate "
                          r"only while inflation runs ahead of what people expect, \ and expectations catch up, \ so "
                          r"a permanent gain would take ever faster inflation. \ Bringing inflation down costs output "
                          r"unless the central bank is believed, \ which is why central banks are now independent, "
                          r"\ with targets, \ and judged by whether expectations stay anchored.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.55)
        u = load("us")
        ys = np.array(u["years"])
        k = (ys >= 1960) & (ys <= 1983)
        mini = plane([2, 11], [0, 15], x_length=4.2, y_length=1.4)
        logo = VMobject(stroke_color=INFL, stroke_width=3).set_points_as_corners(
            [mini.ax.c2p(x, y) for x, y in zip(np.array(u["unemployment"])[k], np.array(u["inflation"])[k])])
        logo.next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: can a country buy lower unemployment with higher inflation? <bookmark mark='a'/> Only for a while, "
            "and only by surprise. Unemployment falls below its natural rate only while inflation runs ahead of "
            "what people expect, and expectations catch up, so a lasting gain would take ever faster inflation. "
            "Bringing inflation down costs output, unless the central bank is believed. That is why central banks "
            "are now independent, with targets, and judged above all by whether expectations stay anchored."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        u, A, ad, I, C, B, V, F, S = (load(x) for x in ("us", "accelerate", "adaptive", "islands", "critique", "bg",
                                                        "volcker", "flat", "surge"))
        items = [
            (rf"Friedman, \ 1967; \ by 1975, \ {u['u1975']:.1f}\% unemployed with {u['pi1975']:.0f}\% inflation",
             INFL),
            (r"Phillips's curve, \ and Samuelson and Solow's menu", WAGE),
            (r"Play it: \ 1973 brought 6\%, \ 1974 brought 11\%", EXPECT),
            (rf"the natural rate: \ inflation climbs {A['fast']['step']} a point a year", OUTPUT),
            (r"the Great Inflation: \ loops that start higher, \ and two oil shocks", INFL),
            (rf"adaptive expectations: \ errors that run one way for years \ (RMSE {ad['fits']['1.0']['rmse']:.1f})",
             EXPECT),
            (r"rational expectations: \ no predictable errors", SURPRISE),
            (rf"Lucas's islands: \ output's response {I['calm']['slope']:.2f} with calm money, \ "
             rf"{I['wild']['slope']:.2f} with wild", WAGE),
            (rf"the critique: \ a slope of {C['slope']:.1f} that vanishes; \ the inflation bias "
             rf"{B['game']['pi_discretion']:.0f}\%", CB),
            (rf"Volcker: \ a sacrifice ratio of {V['sac_ratio']:.1f}; \ conservative bankers, \ independence, \ "
             r"targets", CB),
            (rf"the flat curve: \ {F['early']['slope']:.2f} to {F['late']['slope']:.2f}; \ 2021--23 and a bent "
             rf"curve", INFL),
            (r"two dials; \ persistence; \ Friedman right, \ team transitory wrong; \ how people really forecast",
             OUTPUT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 28, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del S
        with self.voiceover(
            "Part twenty-eight in twelve lines. <bookmark mark='a'/> Friedman said the trade-off would vanish, and "
            "within a decade it had. Phillips's curve became Samuelson and Solow's menu. You forecast 1973, and the "
            "1970s outran everyone looking back. Holding unemployment below its natural rate makes inflation "
            "accelerate. The Great Inflation moved in loops that started higher each time. Adaptive forecasts made "
            "errors that ran one way for years; rational expectations rule that out. On Lucas's islands, output "
            "responds less when money is wild, and an estimated trade-off vanishes when policy changes. A central "
            "bank that cannot commit ends up with inflation and nothing for it. Volcker's cure cost about two "
            "point-years of output per point, and conservative bankers, independence and targets were built to "
            "make the cure unnecessary. The curve flattened, then bent in 2021. And two dials, persistence, two "
            "forecasts scored, and what surveys show."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=46.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems. Phillips's curve; acceleration; adaptive expectations as a weighted average of the past; "
            "Lucas's signal extraction; the critique; Barro and Gordon's inflation bias; a sacrifice ratio; and a "
            "starred problem on Rogoff's conservative banker. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"David Romer, \emph{Advanced Macroeconomics} (5th ed., 2019), \ chs.\ 6 and 12",
             r"Thomas Sargent, \emph{The Conquest of American Inflation} (1999)",
             r"Olivier Blanchard, \emph{Macroeconomics} (8th ed., 2021), \ chs.\ 8--9",
             r"Robert Lucas, \emph{Studies in Business-Cycle Theory} (1981)"],
            [r"Phillips (1958); \ Samuelson and Solow (1960); \ Phelps (1967); \ Friedman (1968); \ Muth (1961)",
             r"Lucas (1972, 1973, 1976); \ Sargent and Wallace (1975); \ Kydland and Prescott (1977)",
             r"Barro and Gordon (1983); \ Rogoff (1985); \ Alesina and Summers (1993); \ Ball (1994)",
             r"Hazell, \ Herre\~no, \ Nakamura and Steinsson (2022); \ Bernanke and Blanchard (2023)",
             r"Benigno and Eggertsson (2023); \ Coibion, \ Gorodnichenko and Kumar (2018); \ Weber et al.\ (2022)"])
        with self.voiceover(
            "The reading: David Romer's Advanced Macroeconomics, the graduate text this part follows; Thomas "
            "Sargent's Conquest of American Inflation, on how policymakers learned; Blanchard's chapters on the "
            "Phillips curve; and Lucas's collected papers. Then the papers, from Phillips to the surveys of today."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1982, r"Kydland and Prescott", r"they take the growth model, \ add random shocks to "
                          r"technology, \ and claim that the result looks like the American business cycle",
                          color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 29 \ $\cdot$ \ Act VI, \ Money and the Cycle", font_size=30, color=GREY_B),
                     label(r"The Cycle as Equilibrium", font_size=46),
                     label(r"could booms and slumps be an economy's best response to shocks?", font_size=26,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"this part: \ expectations; \ next: \ a cycle built from them", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part put expectations at the centre. The next builds a whole business cycle on them. "
            "<bookmark mark='a'/> In 1982, Finn Kydland and Edward Prescott took the growth model, added random "
            "shocks to technology, and claimed that the result looked like the American business cycle. If they "
            "were right, recessions were not failures at all. <bookmark mark='b'/> Part twenty-nine: the cycle as "
            "equilibrium. Could booms and slumps be an economy's best response to shocks it cannot avoid?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
