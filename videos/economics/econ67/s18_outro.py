from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

PROBLEMS = [
    r"The caliper: \ with no selection, \ the density of $|z|$ is smooth near 1.96; \ explain why the counts just "
    r"above and just below should be nearly equal, \ and what a ratio of 3 implies.",
    r"The winner's curse: \ with true $z = 1$ and noise $N(0, 1)$, \ compute the mean of the estimate given that "
    r"it is significant, \ and the power of a replication sized for that mean.",
    r"Forking paths: \ for $k$ independent tests at 5\%, \ show that the chance of at least one false positive is "
    r"$1 - 0.95^k$; \ why is it lower when the tests are correlated?",
    r"Selection: \ with latent $z \sim N(\mu, \sigma^2)$ and publication probability $\beta$ below 1.96, \ write "
    r"the density of published $z$ and its normalizing constant.",
    r"Many analysts: \ take the seven teams' estimates and standard errors; \ compute their spread over the mean "
    r"standard error, \ and say what a ratio of 2 means for a reader.",
    r"$\bigstar$ \ Brock and Hommes: \ show that the steady state of the switching cobweb loses stability when "
    r"$(1 - n^\ast)\,b = B + n^\ast b$, \ and find the $\beta$ at which this happens for $b/B = 1.35$, \ $C = 1$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).move_to(UP * 2.5)
        a = wrapped_label(r"More than its critics say, \ less than its journals print. \ Published results are "
                          r"selected, \ so they are exaggerated and replicate about three times in five; \ the "
                          r"selection can be seen and partly corrected. \ The field is changing how it finds out: \ "
                          r"plans before data, \ code checked before print, \ many analysts and whole specification "
                          r"curves instead of one, \ and records that accumulate. \ Machines speed every step, \ the "
                          r"errors included.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.45)
        with self.voiceover(
            "So: how much of what economics says is true? <bookmark mark='a'/> More than its critics say, and less "
            "than its journals print. Published results are selected, so they are exaggerated, and in the "
            "laboratories they replicate about three times in five; the selection can be seen, and partly "
            "corrected. And the field is changing how it finds out: plans before data, code checked before "
            "publication, many analysts and whole specification curves instead of a single estimate, and records "
            "that accumulate. Machines will speed every step, the errors included."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
        self.clear_scene()

    def recap(self):
        C, R, Mv, Dd, Me, F, H, A, An, B, Mc = (load(x) for x in (
            "camel", "replication", "multiverse", "designs", "meta", "forking", "turn", "audit", "analysts", "abm",
            "machine"))
        d = Dd["designs"]
        items = [
            (rf"the camel: \ published {C['caliper']['ratio']:.1f} to 1 at 1.96, \ first tries "
             rf"{C['caliper_first']['ratio']:.1f}", PUB),
            (r"Play it: \ results just past the line replicate about half the time", TRUE),
            (rf"the laboratories: \ 11 of 18, \ effects 66\%; \ the simulated field {100 * R['rate']:.0f}\%", FIRST),
            (rf"Reinhart and Rogoff, \ {Mv['n']} ways: \ the sign holds, \ the size does not, \ the cause is "
             r"unknown", STATE),
            (rf"designs: \ missing insignificant results {100 * (1 - d['RCT']['beta']):.0f}\% for trials, \ "
             rf"{100 * (1 - d['IV']['beta']):.0f}\% for instruments", FAIL),
            (rf"correction: \ {Me['ak']['theta']:.3f} recovered, \ truth {Me['theta']:.3f}, \ naive "
             rf"{Me['naive']:.3f}".replace("-", "{-}"), ROW),
            (rf"forking paths: \ five tries, \ {100 * F['curves']['0.6'][3]:.0f}\% false positives", FAIL),
            (rf"the turn: \ theory {H['shares'][2][0]:.0f}\% of articles in 1983, \ {H['shares'][5][0]:.0f}\% in "
             r"2011", STATE),
            (rf"the audit: \ {A['n_dials']} Dials, \ {A['statuses']['contested']} contested, \ "
             rf"{A['statuses']['settled within a range']} settled within a range", TEXT),
            (rf"many analysts: \ spread {An['ratio']:.1f} times the standard error", PUB),
            (r"Brock and Hommes: \ switching forecasters, \ chaos from inside", FIRST),
            (rf"machines: \ a thousand specifications, \ {100 * Mc['fp'][3]:.0f}\% false positives", FAIL),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 67, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-seven in twelve lines. <bookmark mark='r1'/> Selection leaves a camel in the published "
            "record. <bookmark mark='r2'/> Results just past the line are coin tosses. <bookmark mark='r3'/> Three "
            "in five laboratory results replicate, smaller. <bookmark mark='r4'/> A robust correlation can still "
            "miss the cause. <bookmark mark='r5'/> Designs that allow choices invite search. <bookmark mark='r6'/> "
            "Selection can be modelled, and partly undone. <bookmark mark='r7'/> Forking paths need no cheating. "
            "<bookmark mark='r8'/> Economics turned from theory to data. <bookmark mark='r9'/> Its own ledger is "
            "mostly open. <bookmark mark='r10'/> Analysts are a source of uncertainty. <bookmark mark='r11'/> "
            "Markets can fluctuate from inside. <bookmark mark='r12'/> And machines multiply both the search and "
            "the checks."
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
            "The problems: the caliper test; the winner's curse and a replication's power; forking paths; the "
            "density of a selected literature; the many-analysts ratio; and a starred problem on the stability of "
            "Brock and Hommes's market. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Garret Christensen, \ Jeremy Freese and Edward Miguel, \ \emph{Transparent and Reproducible Social "
             r"Science Research} (2019)",
             r"Dani Rodrik, \ \emph{Economics Rules} (2015)",
             r"Joshua Angrist and J\"orn-Steffen Pischke, \ \emph{Mastering 'Metrics} (2015)"],
            [r"Leamer (1983); \ Angrist and Pischke (2010); \ Hamermesh (2013); \ Christensen and Miguel (2018)",
             r"Brodeur et al.\ (2016, 2020); \ Camerer et al.\ (2016, 2018); \ Andrews and Kasy (2019)",
             r"Ioannidis, \ Stanley and Doucouliagos (2017); \ Huntington-Klein et al.\ (2021); \ DellaVigna and "
             r"Pope (2018)",
             r"Brock and Hommes (1997); \ Heckman and Moktan (2020); \ Akerlof (2020); \ Ludwig and Mullainathan "
             r"(2024)"])
        with self.voiceover(
            "The reading: Garret Christensen, Jeremy Freese and Edward Miguel on transparent and reproducible "
            "social science; Dani Rodrik's Economics Rules, on what models are for; and Joshua Angrist and "
            "Jörn-Steffen Pischke's Mastering Metrics, on designs. Then the papers, from Leamer's con to the "
            "machines."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(r"1845", r"who feeds Paris?", r"Bastiat asks how a city of a million is fed every day "
                          r"without anyone planning it: \ the question of Part 1", color=E.ACCENT, width=10.4,
                          font_size=23)
        nxt = VGroup(label(r"Next: \ Part 68 \ $\cdot$ \ Act XII, \ The Frontier \ (the last part)", font_size=30,
                           color=GREY_B),
                     label(r"The Dissertation", font_size=46),
                     label(r"how is a new piece of economics made?", font_size=24, color=E.ACCENT)).arrange(
            DOWN, buff=0.22)
        head = label(r"from checking economics to making it", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"a question", FIRST), (r"a design", TRUE), (r"a model", STATE),
                                         (r"the accounts closed", PUB))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from checking economics to making it. <bookmark mark='a'/> The series began with Bastiat's "
            "question: who feeds Paris? It ends in a city too. <bookmark mark='b'/> One research question, carried "
            "from idea to paper with everything this part asked of others: a design, a model, a plan written "
            "before the results, and the series' accounts closed, the Dials, the Facts and the Tableau. <bookmark "
            "mark='c'/> Part sixty-eight, the last: the dissertation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
