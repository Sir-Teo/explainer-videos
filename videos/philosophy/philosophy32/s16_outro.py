from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.toolbox()
        self.problems()
        self.payoffs()
        self.references()

    def recap(self):
        items = [
            r"determinism defined; \ Laplace's demon; \ List's levels; \ the dilemma of luck",
            r"the sea battle; \ Chrysippus's cylinder; \ the lazy argument",
            r"the consequence argument, \ with $N$, \ $\alpha$ and $\beta$",
            r"$\beta$ fails on the coin: \ 2 of 64; \ $\beta_\Box$ never \ (the Wall)",
            r"Frankfurt's case: \ no choice, \ yet a flicker; \ compatibilism; \ the Price List",
            r"Kane; \ a torn decision; \ 1000 replays, \ 708 truths; \ Pereboom; \ the Strawsons",
            r"a readiness potential from noise; \ an avoider; \ the self-prediction diagonal",
            r"the free will theorem; \ 6 of 10\,000 drivers, \ two ledgers; \ responsibility gaps",
        ]
        card = objectives_card(items, title=r"What we built", font_size=22)
        with self.voiceover(
            "Let's gather what we built. <bookmark mark='a'/>Determinism, Laplace's demon, a world determined below and "
            "open above, and the dilemma of luck. "
            "<bookmark mark='b'/>The sea battle, the cylinder and the lazy argument. <bookmark mark='c'/>The "
            "consequence argument, with its operator and rules. <bookmark mark='d'/>Rule beta failing on McKay and "
            "Johnson's coin, two instances in sixty four, and the repaired rule failing on none: this part's brick "
            "in the Wall. <bookmark mark='e'/>Frankfurt's case on the same model, compatibilism, and the Price List. "
            "<bookmark mark='f'/>Kane's self-forming actions, a torn decision, a thousand replays with seven "
            "hundred and eight truths, Pereboom's cases, and both Strawsons. <bookmark mark='g'/>A readiness "
            "potential built from nothing but noise, a deterministic avoider, and the diagonal that keeps a mind "
            "from predicting itself. <bookmark mark='h'/>The free will theorem, six careless drivers in ten "
            "thousand and their two ledgers, and the gaps machines open in responsibility."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def toolbox(self):
        head = label(r"The Reasoner, so far", font_size=36, color=CONN).to_edge(UP, buff=0.4)
        mods = [(r"\texttt{freewill.Options, rule\_check}", r"$N$, \ and its rules checked"),
                (r"\texttt{freewill.frankfurt}", r"no choice, \ and a flicker"),
                (r"\texttt{freewill.rollback}", r"replays of one moment"),
                (r"\texttt{freewill.accumulator}", r"a readiness potential from noise"),
                (r"\texttt{freewill.self\_prediction}", r"the contrarian and the diagonal"),
                (r"\texttt{freewill.reasons\_responsive, miracles}", r"compatibilist conditions, \ checked"),
                (r"\texttt{freewill.moral\_luck, blame\_ledgers, responsibility}", r"luck; \ two ledgers; \ degrees"),
                (r"\texttt{freewill.levels, torn\_decision, avoider}", r"levels; \ a torn decision; \ evitability"),
                (r"\texttt{consciousness.*}, \ \texttt{mind.*}, \ \dots", r"Parts 1--31")]
        lefts = [label(a, font_size=20, color=P.WORLD) for a, _ in mods]
        rights = [label(b, font_size=20, color=GREY_A) for _, b in mods]
        x0, y0 = -6.4, head.get_bottom()[1] - 0.5
        rows = VGroup()
        for i, (a, b) in enumerate(zip(lefts, rights)):
            y = y0 - i * 0.48
            if a.width > 7.4:
                a.width = 7.4
            a.move_to([x0 + a.width / 2, y, 0])
            if b.width > 4.6:
                b.width = 4.6
            b.move_to([1.6 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        tests = label(r"checked: \ \texttt{tests/philosophy/test\_freewill.py}", font_size=22,
                      color=GREY_B).to_corner(DL, buff=0.4)
        w = wall(upto=32, current=32).scale(0.36).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The Reasoner has a new module, free will. <bookmark mark='a'/>It models options and the operator N, "
            "checks the consequence argument's rules on every instance, models Frankfurt's case, replays an "
            "undetermined moment, rebuilds a readiness potential from a noisy accumulator and interrupts it, checks "
            "reasons-responsiveness and Lewis's miracles, diagonalizes against predictors, builds a world that is "
            "deterministic below and open at the agent's level, a torn decision and a deterministic avoider, counts "
            "moral luck in two ledgers, and measures degrees of responsibility. <bookmark mark='b'/>And the Wall "
            "has its thirty second brick."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(tests))
            vo.wait_until("b")
            self.play(FadeIn(w), Indicate(w.brick[32], color=P.CONCL, scale_factor=1.06))
        self.wait(1.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that rule $\beta$ is valid on every model in which each action leads to a single world.",
            r"Find a model on which $\beta$ fails but agglomeration holds, \ or prove there is none.",
            r"Give a buffered Frankfurt case on the options model, \ with no flicker at all.",
            r"For the rollback, \ how many replays make the share within 0.01 of 0.7, \ 95\% of the time?",
            r"Show that with no noise, \ the accumulator never crosses a threshold above $I/k$.",
            r"Write the diagonal agent for infinitely many predictors, \ and say what it needs to compute.",
        ], font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in this part's notes. <bookmark mark='a'/>Rule beta on deterministic "
            "models; beta without agglomeration; a buffered Frankfurt case; how many replays the rollback needs; "
            "the noiseless accumulator; and a diagonal agent against infinitely many predictors. Pause here, and "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ps.rows], lag_ratio=0.25), run_time=3)
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Newcomb's predictor, \ and rational choice", [33]),
            (r"agents in games, \ and the social contract", [34]),
            (r"desert and punishment", [35, 38]),
            (r"machines that decide about people", [41]),
            (r"aligned reasoners, \ and who answers for them", [42]),
        ], font_size=22)
        nxt = label(r"Next: \ Part 33, \textit{Rational Choice}", font_size=26, color=P.CONCL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/>Newcomb's predictor and rational choice, in Part 33. Agents "
            "in games and the social contract, in Part 34. Desert and punishment, in Parts 35 and 38. Machines that "
            "decide about people, in Part 41. And aligned reasoners, and who answers for them, in Part 42. "
            "<bookmark mark='b'/>Next, Part 33: rational choice."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def references(self):
        ref = reference_card(
            [r"Kane (ed.), \textit{The Oxford Handbook of Free Will} (2nd ed., 2011)",
             r"van Inwagen, \textit{An Essay on Free Will} (1983)",
             r"Fischer, Kane, Pereboom and Vargas, \textit{Four Views on Free Will} (2007)",
             r"McKenna and Pereboom, \textit{Free Will: A Contemporary Introduction} (2016)"],
            [r"Hobbes 1651; Hume 1748; Laplace 1814; Schopenhauer 1839; MacKay 1960; P. F. Strawson 1962",
             r"Chisholm 1964; Frankfurt 1969, 1971; Nozick 1969; Williams 1976; Nagel 1979; Lewis 1981",
             r"Libet et al. 1983; Watson 1987; G. Strawson 1994; Fischer 1994; Widerker 1995; Kane 1996",
             r"McKay and Johnson 1996; Finch and Warfield 1998; Fischer and Ravizza 1998; O'Connor 2000",
             r"Pereboom 2001, 2014; Matthias 2004; Conway and Kochen 2006; Sparrow 2007; Soon et al. 2008",
             r"Schurger, Sitt and Dehaene 2012; Maoz et al. 2019; Bourget and Chalmers 2023"])
        with self.voiceover(
            "The books and papers this part follows are on screen, and in the notes. Thanks for watching."
        ):
            self.play(FadeIn(ref))
            self.wait(4)
        self.clear_scene()
