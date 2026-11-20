from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403

PROBLEMS = [
    r"Difference in differences: \ New Jersey's restaurants went from 20.44 to 21.03 employees, \ Pennsylvania's "
    r"from 23.33 to 21.17. \ Find the effect, \ and say what it assumes.",
    r"Slutsky: \ at a high wage the Marshallian elasticity is $-0.11$ and the income effect $-0.40$. \ Find the "
    r"Hicksian elasticity.",
    r"The textbook floor: \ with a demand elasticity of 0.5, \ how much does employment fall when a minimum is set "
    r"19\% above the market wage?",
    r"Monopsony: \ with a labour supply elasticity of 3 facing the firm, \ how far below the value of the marginal "
    r"worker is the wage? \ With 10?",
    r"Mincer: \ with a return of 0.09, \ how much more does someone with four more years of school earn?",
    r"Ability bias: \ least squares gives 0.075; \ adding IQ gives 0.056, \ with 0.0055 per IQ point, \ and IQ is 3.5 "
    r"points higher per year of school. \ Check the omitted-variable formula.",
    r"The Wald estimator: \ near a college, \ 13.53 years of school and log wage 6.311; \ far, \ 12.70 and 6.156. "
    r"\ Estimate the return.",
    r"$\bigstar$ \ Heckman: \ for jointly normal errors, \ derive $E[\varepsilon \mid v > -Z\gamma] = "
    r"\sigma_{\varepsilon v}\,\phi(Z\gamma)/\Phi(Z\gamma)$.",
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
        a = wrapped_label(r"Wages are set by the value of what people produce, \ their skills, \ which schooling "
                          r"raises by six to fifteen percent a year, \ and their choices about how much and where to "
                          r"work; \ but employers often have some power to set pay. \ When the law sets a moderate "
                          r"minimum, \ jobs barely fall; \ how high it can go before they do is still being "
                          r"measured.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1938, 2025], [0, 16], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], WAGE, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: what sets a wage, and what happens when the law sets it instead? <bookmark mark='a'/> Wages are set "
            "by the value of what people produce, by their skills, which a year of school raises by six to fifteen "
            "percent, and by their own choices about how much and where to work. But employers often have some power "
            "to set pay. When the law sets a moderate minimum, jobs barely fall; how high it can go before they do is "
            "still being measured."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        C, S, M, P, B, Mi, R, Ro, F = (load(x) for x in ("ck", "supply", "market", "monopsony", "border", "mincer",
                                                          "returns", "roy", "film"))
        D = tables.CDLZ_2019.data
        items = [
            (rf"New Jersey: \ +{C['did']:.2f} employees per restaurant, \ relative to Pennsylvania", NJ),
            (rf"labour supply: \ bends back above \${S['peak']:.0f}; \ Hicksian 0.3, \ Frisch 0.5", SUPPLY),
            (r"cab drivers: \ targets in 1997, \ standard responses since; \ Uber's Frisch 1.2", WHITE),
            (rf"the textbook floor: \ 19\% higher, \ employment {100 * M['drop19']:.0f}\%", DEMAND),
            (rf"the border: \ the law bound, \ prices +{100 * (C['price_nj'] - C['price_pa']):.0f}\% relative", NJ),
            (rf"bunching: \ {D['events']} increases, \ own-wage elasticity {D['owe']:.2f}; \ Seattle's hours fell",
             WAGE),
            (rf"monopsony: \ a {100 * P['markdown']:.0f}\% markdown; \ a minimum up to \${P['w_c']:.2f} adds jobs",
             MCL),
            (rf"the Island: \ the design finds {B['competitive']['mean_did']:+.2f} or "
             rf"{B['monopsony']['mean_did']:+.2f}",
             E.ACCENT),
            (rf"Mincer: \ {100 * Mi['b'][1]:.1f}\% a year of school \ (1976)", SCHOOL),
            (rf"returns: \ least squares {R['ols']:.3f}, \ college distance {R['iv']:.3f}; \ with IQ {R['w2_iq']:.3f}",
             SCHOOL),
            (rf"Roy: \ seen {Ro['naive']:.2f}, \ true {Ro['truth']:.2f}, \ Heckman {Ro['corrected']:.2f}", FISH),
            (rf"Mariel: \ +7\% labour force; \ no effect, \ or $-$10 to $-$30\%; \ real minimum \${F['peak']:.2f} in "
             rf"{F['peak_y']}", BOAT),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 38, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-eight in twelve lines. <bookmark mark='a'/> New Jersey's higher minimum did not cost its "
            "restaurants jobs. People supply labour according to substitution and income effects, with three "
            "elasticities for three questions, and cab drivers, given the chance, work more when it pays. The "
            "competitive textbook predicts losses from a floor; the border design found none, and bunching across "
            "many increases found few, though Seattle's high minimum cut hours. Monopsony explains why: employers who "
            "set wages can hire more under a minimum, and on the Island the same design tells the two worlds apart. "
            "Schooling pays roughly six to fifteen percent a year, by regressions and natural experiments alike. "
            "Selection hides what people would earn elsewhere, and Heckman's correction can recover it. And the "
            "Mariel boatlift, read three ways, shows how much depends on who is counted."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. The difference in differences; Slutsky's equation; the textbook floor; the monopsony "
            "markdown; Mincer's arithmetic; the omitted-variable formula; the Wald estimator on Card's data; and a "
            "starred derivation of Heckman's correction. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"David Card and Alan Krueger, \emph{Myth and Measurement} (1995)",
             r"Alan Manning, \emph{Monopsony in Motion} (2003)",
             r"George Borjas, \emph{Labor Economics}; \ Pierre Cahuc, \ St\'ephane Carcillo and Andr\'e Zylberberg, "
             r"\emph{Labor Economics}",
             r"Jacob Mincer, \emph{Schooling, Experience, and Earnings} (1974)"],
            [r"Robinson (1933); \ Stigler (1946); \ Roy (1951); \ Becker (1964); \ Heckman (1979)",
             r"Card (1990); \ Angrist and Krueger (1991); \ Card and Krueger (1994); \ Card (1995)",
             r"Camerer et al.\ (1997); \ Neumark and Wascher (2000); \ Oreopoulos (2006); \ Chetty et al.\ (2011)",
             r"Farber (2015); \ Borjas (2017); \ Cengiz et al.\ (2019); \ Peri and Yasenov (2019)",
             r"Angrist, \ Caldwell and Hall (2021); \ Sokolova and Sorensen (2021); \ Jardim et al.\ (2022)"])
        with self.voiceover(
            "The reading: Card and Krueger's Myth and Measurement; Alan Manning's Monopsony in Motion; the labour "
            "textbooks of George Borjas and of Cahuc, Carcillo and Zylberberg; and Mincer's book. Then the papers, "
            "from Joan Robinson to Seattle."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(2001, r"Marianne Bertrand and Sendhil Mullainathan", r"answer help-wanted advertisements in "
                          r"Boston and Chicago with invented r\'esum\'es, \ identical but for the name at the top: \ "
                          r"White-sounding names get 50\% more call-backs", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 39 \ $\cdot$ \ Act VIII, \ Work and the State", font_size=30, color=GREY_B),
                     label(r"The Wage Structure", font_size=46),
                     label(r"why are some people paid so much more than others, \ and how much of the gap is unfair?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from what sets a wage \ to why wages differ", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked what sets a wage. The next asks why wages differ so much. <bookmark mark='a'/> In 2001 "
            "and 2002 Marianne Bertrand and Sendhil Mullainathan answered help-wanted advertisements in Boston and "
            "Chicago with invented résumés, identical except for the name at the top. Résumés with White-sounding "
            "names got fifty percent more calls back. <bookmark mark='b'/> Part thirty-nine: the wage structure. Why "
            "are some people paid so much more than others, and how much of the gap is unfair?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
