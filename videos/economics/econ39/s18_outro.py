from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403

PROBLEMS = [
    r"Call-backs: \ 235 of 2,435 r\'esum\'es with White names, \ 157 of 2,435 with African-American names. \ Find "
    r"each rate, \ their ratio, \ and the number of r\'esum\'es per call-back.",
    r"The canonical model: \ with $\sigma = 1.4$, \ by how much does the college premium fall if relative supply "
    r"rises 10\% and demand does not move?",
    r"The race: \ relative supply grows 2.7\% a year and the premium is flat. \ With $\sigma = 1.41$, \ how fast "
    r"must relative demand be growing?",
    r"Unions: \ least squares gives a premium of 0.182; \ comparing the same men gives 0.080. \ What share of the "
    r"cross-sectional gap is selection, \ and what does the within estimate assume?",
    r"Becker: \ a fifth of workers are in the minority and 30\% of employers have no prejudice. \ What is the "
    r"market gap? \ And if the minority were 40\%?",
    r"Phelps: \ productivity has variance 1 and mean 0 in both groups; \ test noise has variance 0.25 for A and 1 "
    r"for B. \ What is each group's pay at a score of 2?",
    r"Oaxaca-Blinder: \ men average 13.0 years of school, \ women 12.6; \ the return for women is 0.08; \ the gap "
    r"is 0.23. \ How much is `explained' by schooling?",
    r"$\bigstar$ \ AKM: \ show that with $n_j$ movers per firm, \ the plug-in variance of firm effects exceeds the "
    r"true variance by roughly the average sampling variance, \ $\sigma^2_\varepsilon \cdot \overline{2/n_j}$.",
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
        a = wrapped_label(r"Pay differs because skills differ and are rewarded more when technology outruns "
                          r"education, \ because machines took the middle's routine tasks, \ because some firms pay "
                          r"more than others, \ and because some jobs are worse; \ but part of the gap is "
                          r"discrimination, \ which experiments can measure, \ and much of the gender gap opens with "
                          r"children.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1979, 2025], [1.3, 1.9], x_length=4.2, y_length=1.3)
        logo = path(mini, F["t"], F["v"], COLLEGE, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why are some people paid so much more than others, and how much of the gap is unfair? "
            "<bookmark mark='a'/> Pay differs because skills differ, and skills are rewarded more when technology "
            "outruns education; because machines took over the routine tasks of the middle; because some firms pay "
            "more than others; and because some jobs are worse. But part of the gap is discrimination, which "
            "experiments can measure, and much of the gender gap opens with the first child."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        R, W, Rc, T, Ro, Fm, S, U, G = (load(x) for x in ("resume", "wages", "race", "tasks", "robots", "firms",
                                                           "stars", "unions", "gender"))
        items = [
            (rf"the r\'esum\'es: \ {100 * R['white'][0]:.1f}\% against {100 * R['black'][0]:.1f}\% call-backs",
             WHITE_N),
            (rf"the premium: \ {W['ratio'][0]:.2f} in 1979, \ {W['ratio'][-1]:.2f} in 2025; \ the 1980s did most",
             COLLEGE),
            (rf"the race: \ $\sigma$ about 1.4 to 2.5; \ demand growth {100 * Rc['d141_rates']['1992-2000']:.1f}\% "
             rf"$\to$ {100 * Rc['d141_rates']['2010-2025']:.1f}\% a year", DEMAND),
            (r"the game: \ operators, \ crafts and clerks shrank; \ both ends grew", EMP),
            (rf"tasks: \ automating the middle, \ middle/low pay {T['before']['wM_wL']:.2f} $\to$ "
             rf"{T['after']['wM_wL']:.2f}", MIDS),
            (rf"robots: \ $-$0.2 points per robot; \ the Island's naive slope {Ro['naive']:.2f}", MACHINE),
            (rf"firms: \ {100 * Fm['est']['share_psi']:.0f}\% of the variance on the Island; \ Germany 18\% $\to$ "
             r"21\%", FIRM),
            (rf"superstars: \ the labour share down {100 * (1 - S['ls2025'] / S['ls1980']):.0f}\% since 1980", WAGE),
            (rf"unions: \ premium {U['pooled']:.2f}, \ or {U['fe']:.2f} within men; \ membership 20\% $\to$ 10\%",
             UNION),
            (r"differentials: \ risk and rigid hours are paid for", WORKER),
            (r"discrimination: \ Becker's marginal employer, \ Phelps's noisy signals", BLACK_N),
            (rf"the gender gap: \ {100 * G['r1979']:.0f}\% $\to$ {100 * G['r2025']:.0f}\%; \ the child penalty, "
             r"about 20\%", WOMEN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 39, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-nine in twelve lines. <bookmark mark='a'/> Résumés that differed only in the name were "
            "called back half as often again when the name sounded White. The college premium rose steeply in the "
            "1980s and has stalled since; the race between education and technology explains much of it, with an "
            "elasticity of substitution between about one and a half and two and a half. Jobs shrank in the middle "
            "and grew at both ends, and a model of tasks shows why: machines take routine tasks, and middle-skill "
            "workers are pushed to the edges. Robots cost jobs in exposed towns, once other shocks are held fixed. "
            "Where you work matters, and better workers increasingly sort into better-paying firms. Superstar people "
            "and firms pull away, and labour's share has fallen. Unions raise and compress pay, but much of their "
            "measured premium is who joins them. Some pay gaps are prices for risk and rigid hours. Discrimination "
            "can survive competition when it is statistical or comes from customers, and experiments show it has "
            "not faded. And the gender gap opens with the first child."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=44.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Call-back rates and their ratio; the canonical model; the race; selection into unions; "
            "Becker's marginal employer; Phelps's pay lines; an Oaxaca-Blinder split; and a starred derivation of "
            "the limited-mobility bias. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Claudia Goldin and Lawrence Katz, \emph{The Race between Education and Technology} (2008)",
             r"Gary Becker, \emph{The Economics of Discrimination} (1957)",
             r"Claudia Goldin, \emph{Career and Family} (2021)",
             r"David Card, \ `Who Set Your Wage?', \ \emph{AER} (2022)"],
            [r"Rosen (1974, 1981); \ Phelps (1972); \ Arrow (1973); \ Oaxaca (1973); \ Blinder (1973)",
             r"Katz and Murphy (1992); \ Abowd, \ Kramarz and Margolis (1999); \ Goldin and Rouse (2000)",
             r"Autor, \ Levy and Murnane (2003); \ Bertrand and Mullainathan (2004); \ Acemoglu and Autor (2011)",
             r"Autor and Dorn (2013); \ Card, \ Heining and Kline (2013); \ Goldin (2014); \ Mas and Pallais (2017)",
             r"Quillian et al.\ (2017); \ Kleven, \ Landais and S\o{}gaard (2019); \ Acemoglu and Restrepo (2020)",
             r"Autor et al.\ (2020); \ Cullen and Pakzad-Hurson (2023)"])
        with self.voiceover(
            "The reading: Goldin and Katz's The Race between Education and Technology; Becker's The Economics of "
            "Discrimination; Goldin's Career and Family; and David Card's lecture, Who Set Your Wage? Then the "
            "papers, from Rosen's hedonic prices to pay transparency."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1971, r"Jan Pen", r"imagines everyone in the country marching past in an hour, \ each as "
                          r"tall as their income: \ for most of the hour, \ people who barely reach your waist; \ "
                          r"in the last minutes, \ giants", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 40 \ $\cdot$ \ Act VIII, \ Work and the State", font_size=30, color=GREY_B),
                     label(r"Inequality and Mobility", font_size=46),
                     label(r"how unequal are incomes and wealth, \ and do children escape where they started?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from wages \ to incomes, \ wealth and generations", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This part asked why wages differ. The next widens the lens to incomes, wealth and generations. "
            "<bookmark mark='a'/> In 1971 the Dutch economist Jan Pen asked his readers to imagine everyone in the "
            "country marching past in a single hour, each as tall as their income. For most of the hour you watch "
            "people who barely reach your waist; in the last minutes come giants. <bookmark mark='b'/> Part forty: "
            "inequality and mobility. How unequal are incomes and wealth, and do children escape where they started?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(9.5)
        self.clear_scene()
