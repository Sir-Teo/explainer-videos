from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class TranscriptComplete(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. The transcript, complete.", 9, r"The transcript", r"The degree in one picture")
        self.transcript()
        self.timeline_()
        self.instruments()
        self.stages()
        self.numbers()

    def transcript(self):
        tr = transcript_card(done=64, current=65)
        tr.move_to([0, 0.6, 0])
        caps = fit_rows(VGroup(
            label(r"sixty-five parts; \ four milestones", font_size=26, color=GREY_A),
            label(r"the BSc at Part 20, \ the MSc at Part 42, \ candidacy at Part 55, \ the PhD at Part 65", font_size=26, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The transcript has tracked the degree since Part one: a cell for each part. <bookmark "
            "mark='b'/> Sixty-four filled. <bookmark mark='c'/> The last one fills now. <bookmark mark='d'/> Four "
            "milestones along the way: the bachelor's analysis at Part twenty, the comprehensive exam at Part forty-two, the "
            "qualifying exam at Part fifty-five, and this dissertation."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(64)])
            vo.wait_until("c")
            self.play(tr.cells[64].animate.set_fill(S.ACCENT, opacity=1.0), Flash(tr.cells[64], color=S.ACCENT))
            vo.wait_until("d")
            self.play(FadeIn(caps[0]), FadeIn(caps[1]))
        self.wait(1.5)
        self.clear_scene()

    def timeline_(self):
        years = tuple(range(1600, 2027))
        tl = timeline(lit=years, show_labels=False).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(r"1662: \ Graunt's Bills", font_size=26, color=GREY_A),
            label(r"1900s: \ Pearson, \ Fisher, \ Neyman, \ the experiment and the interval", font_size=26, color=GREY_A),
            label(r"1970s--2000s: \ the bootstrap, \ MCMC, \ the lasso, \ causal graphs", font_size=26, color=GREY_A),
            label(r"now: \ conformal, \ anytime-valid, \ privacy, \ statistics for AI", font_size=26, color=S.ACCENT),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The timeline, every entry lit, from 1662 to now. <bookmark mark='b'/> Graunt's lists of "
            "the dead. <bookmark mark='c'/> The twentieth century's foundations: Pearson's chi-squared, Fisher's likelihood "
            "and experiments, Neyman's intervals and tests. <bookmark mark='d'/> The computer's century: the bootstrap, Markov "
            "chain Monte Carlo, the lasso, causal graphs. <bookmark mark='e'/> And the frontier the last ten parts reached: "
            "conformal prediction, anytime-valid inference, privacy, and statistics for a world of machine predictions."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def stages(self):
        f = load("fullboard")
        bs = f["by_stage"]
        self.list_voiceover(
            "<bookmark mark='a'/> The five stages, by what they taught. <bookmark mark='b'/> Stage one, the foundations: "
            "probability, sampling, estimation and the first intervals. <bookmark mark='c'/> Stage two, the methods: "
            "regression, experiments, counts, Bayes, the bootstrap, time series, surveys, learning, and the bachelor's "
            "analysis. <bookmark mark='d'/> Stage three, the master's: likelihood and models in depth, borrowing strength, "
            "computation, smoothing, robustness, many variables and many questions, causes, space and time. <bookmark "
            "mark='e'/> Stage four, the theory a doctorate rests on; and stage five, the research frontier and this "
            "dissertation.",
            [(r"the five stages:", GREY_A),
             (r"I \ (1--10): \ foundations", S.EST),
             (r"II \ (11--20): \ methods, \ and the BSc", S.KEPT),
             (r"III \ (21--42): \ the MSc", S.ALT),
             (r"IV--V \ (43--65): \ theory, \ the frontier, \ the PhD", S.ACCENT)],
            buff=0.42, font_size=25, head_size=32)

    def instruments(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The instruments built along the way, a few of the many. <bookmark mark='b'/> The World, "
            "a simulated population that every part could sample from, and the Museum, the real datasets from Graunt's "
            "Bills to ProPublica's COMPAS data. <bookmark mark='c'/> The Coverage Board, and the exact probability engine of "
            "Part two. <bookmark mark='d'/> Machines for single ideas: the Galton board, the tank factory, the interval "
            "rain, the permutation machine, the likelihood landscape, the trade-off plot, the leaderboard. <bookmark "
            "mark='e'/> And statkit, a statistics library of more than fifty modules, from random number generators to "
            "conformal prediction and privacy accounting, with numerical tests and audits of the examples used in this series. Tests can be incomplete and do not prove every function correct.",
            [(r"the instruments:", GREY_A),
             (r"the World \ and the Museum", S.EST),
             (r"the Coverage Board; \ the exact probability engine", S.KEPT),
             (r"Galton board, \ tank factory, \ interval rain, \ trade-off plot, \ leaderboard", S.ALT),
             (r"\texttt{statkit}: \ more than fifty tested modules", S.ACCENT)],
            buff=0.42, font_size=25, head_size=32)

    def numbers(self):
        f = load("fullboard")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The series by its numbers. <bookmark mark='b'/> Sixty-five parts, each about an hour of "
            f"narration: well over sixty hours, a substantial teaching sequence rather than an accredited degree or a substitute for supervised research. <bookmark mark='c'/> {f['n']} promises "
            f"tested on the Coverage Board, across {f['parts']} parts. <bookmark mark='d'/> Dozens of instruments, more than "
            f"fifty statkit modules with their tests, and the Museum's real datasets, every one of them a reason to believe "
            f"a number rather than to take it on trust.",
            [(r"\text{parts}", r":", r"65, \ \text{about an hour each}", 40),
             (r"\text{Board rows}", r":", rf"{f['n']}, \ \text{{from {f['parts']} parts}}", 40),
             (r"\text{statkit}", r":", r"\text{more than fifty tested modules}", 40),
             (r"\text{the point}", r":", r"\text{numbers you can check}", 40)],
            [r"the scale", r"the evidence", r"the code", r"the ethic"],
            colors=[(3, S.ACCENT)])
