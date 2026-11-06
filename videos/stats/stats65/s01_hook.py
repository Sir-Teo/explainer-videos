from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.graunt()
        self.who()
        self.doctorate()
        self.dissertation()
        self.plan()
        self.upgrade()
        self.objectives()

    def graunt(self):
        tl = timeline(lit=(1662,)).to_edge(UP, buff=0.35)
        hc = history_card(1662, r"John Graunt, \ haberdasher of London",
                          r"\emph{Natural and Political Observations Made upon the Bills of Mortality}: \ decades of weekly lists "
                          r"of the dead, \ read for patterns that no single list showed", color=THESISC, width=11.4,
                          font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"Part 1 began here: \ a ledger became knowledge", font_size=26, color=GREY_A),
            label(r"sixty-four parts later: \ the tools to say how much a ledger can know", font_size=26, color=HONC),
            label(r"one question left: \ how is new statistical knowledge made?", font_size=26, color=THESISC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The degree began in 1662, with a London haberdasher. John Graunt read decades of the weekly "
            "Bills of Mortality, the lists of London's dead, and found patterns that no single list showed: more boys born "
            "than girls, year after year, and the toll of the plague. <bookmark mark='b'/> A ledger became knowledge. "
            "<bookmark mark='c'/> Sixty-four parts later we have the tools to say how much any ledger can know, and how "
            "sure to be. <bookmark mark='d'/> One question is left, and it is the one a doctorate answers: how is new "
            "statistical knowledge made?"
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def who(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Graunt worked alone, from data no one had collected for his purpose. <bookmark mark='b'/> "
            "The statisticians of this series each added a piece: Gauss and Laplace the normal law, Fisher the likelihood "
            "and the experiment, Neyman the interval, Wald the decision, Efron the bootstrap, and the frontier's many "
            "names. <bookmark mark='c'/> Each piece began as an open question, a conjecture, a proof for a special case, "
            "evidence that it worked, and a paper that others could check. <bookmark mark='d'/> This part carries out that "
            "process once, on screen, on one of the open problems from the last ten parts, and reports the result "
            "honestly, whatever it turns out to be.",
            [(r"\text{Graunt}", r":", r"\text{a ledger, \ alone}", 40),
             (r"\text{since}", r":", r"\text{each method a contribution}", 40),
             (r"\text{each one}", r":", r"\text{question, \ conjecture, \ proof, \ evidence, \ paper}", 40),
             (r"\text{this part}", r":", r"\text{the process, \ once, \ in full}", 40)],
            [r"1662", r"Parts 1--64", r"how research works", r"a dissertation"],
            colors=[(3, THESISC)])

    def dissertation(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The dissertation in one sentence. <bookmark mark='b'/> Weighted conformal prediction "
            "keeps its coverage under covariate shift when the shift is known; in practice it is estimated, and the "
            "question is how much coverage the estimation costs. <bookmark mark='c'/> The answer here: a theorem that "
            "bounds the loss by a total variation distance, a preregistered simulation study that tests the bound and five "
            "predictions, and an application to the Museum's NHANES data. <bookmark mark='d'/> Some predictions will "
            "hold and some may not; the report says which.",
            [(r"\text{the question}", r":", r"\text{coverage with estimated weights}", 40),
             (r"\text{the theorem}", r":", r"\text{loss} \le \mathrm{TV}(P_{\hat w}, Q)", 40),
             (r"\text{the evidence}", r":", r"\text{a preregistered study, \ NHANES}", 40),
             (r"\text{the report}", r":", r"\text{whatever it shows}", 40)],
            [r"one sentence", r"chapters 1--4", r"chapters 5--6", r"chapter 7"],
            colors=[(1, THESISC)])

    def plan(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one to four: choosing the question, reading the "
            "literature, stating a conjecture, and proving a theorem. <bookmark mark='c'/> Chapters five to seven: the "
            "preregistered simulation study, the real-data application, and writing it up for review. <bookmark mark='d'/> "
            "Chapters eight to ten: the full Coverage Board of the whole degree, the completed transcript, and where to go "
            "next.",
            [(r"the plan:", GREY_A),
             (r"1--4: \ the question, \ the literature, \ a conjecture, \ a theorem", THESISC),
             (r"5--7: \ a preregistered study, \ NHANES, \ writing and review", HONC),
             (r"8--10: \ the full Board, \ the transcript, \ what next", S.ACCENT)])

    def upgrade(self):
        cards = [
            upgrade_card(57, r"weighted conformal coverage under covariate shift", r"the likelihood ratio is known",
                         r"chapters 3--6: \ when it is estimated"),
            upgrade_card(7, r"simulation as a tool for checking methods", r"simulations are designed after the fact",
                         r"chapter 5: \ a protocol written before the run"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> The last two promises. Part fifty-seven's weighted conformal prediction assumed the "
            "shift's likelihood ratio was known; chapters three to six estimate it, and count the cost. <bookmark "
            "mark='b'/> Part seven taught simulation as a way to check methods, without saying when to decide what to "
            "simulate; chapter five writes the protocol down before running it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 65", font_size=34, color=GREY_B), label(r"The Dissertation", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"choosing a question; \ reading a paper; \ a precise conjecture",
            r"a theorem with its proof; \ a preregistered simulation study, \ reported whatever it shows",
            r"a real application with known selection; \ writing, \ review and reproducibility",
            r"the full Coverage Board; \ the completed transcript; \ where to go next",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ everything").to_corner(DL, buff=0.3)
        built = note(r"built: \ the thesis, \ \texttt{statkit.thesis}, \ the board mosaic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-five: the dissertation. <bookmark mark='b'/> Choosing a question; reading the "
            "papers; stating a conjecture precisely; proving a theorem; a simulation study whose protocol was written "
            "before it ran; an application to real data; writing and review; and then the whole degree, every promise on "
            "the Coverage Board, the completed transcript, and the road beyond the series."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def doctorate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What a doctorate certifies. <bookmark mark='b'/> Not that its author knows everything "
            "in the field: the earlier parts' exams did that. <bookmark mark='c'/> That its author has added something to "
            "what is known, however small, and can defend it: state it precisely, prove what can be proved, test what can be "
            "tested, and say plainly where it stops. <bookmark mark='d'/> A committee of experts reads it, as referees "
            "would, and asks the questions chapter seven anticipates. The rest of this part is that process, at the scale of "
            "one question.",
            [(r"\text{not}", r":", r"\text{knowing everything}", 40),
             (r"\text{but}", r":", r"\text{adding something, \ defensibly}", 40),
             (r"\text{how}", r":", r"\text{state, \ prove, \ test, \ limit}", 40),
             (r"\text{judged by}", r":", r"\text{a committee, \ like referees}", 40)],
            [r"Parts 42 and 55", r"a contribution", r"the method", r"chapter 7"],
            colors=[(1, THESISC)])
