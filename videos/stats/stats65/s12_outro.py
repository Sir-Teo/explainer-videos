from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403

PROBLEMS = [
    r"Show that weighted conformal with weights $c\,\hat w$ gives the same set for every constant $c > 0$.",
    r"Show that $\mathrm{TV}(N(a, 1), N(b, 1)) = 2\Phi(|a - b|/2) - 1$.",
    r"Show that reweighting $N(0, 1)$ by $e^{\lambda\mu x}$ gives $N(\lambda\mu, 1)$.",
    r"Show that if the scores do not depend on $x$, \ unweighted split conformal covers $Q$ at $\ge 1 - \alpha$ under any covariate shift.",
    r"Show that $|Q(A) - \tilde Q(A)| \le \mathrm{TV}(Q_X, \tilde Q_X)$ when $Q$ and $\tilde Q$ share $P_{Y \mid X}$.",
    r"Design a simulation, \ with ADEMP, \ that could refute the theorem if its independence assumption were dropped.",
]


class Outro(LectureMixin, VoiceoverScene):
    def construct(self):
        self.thesis()
        self.reflection()
        self.problems()
        self.references()
        self.three()
        self.farewell()

    def thesis(self):
        st = {(x["mu"], x["gamma"], x["method"]): x for x in load("study")["rows"]}
        nh = load("nhanes")
        held = sum(1 for x in st.values() if x["coverage"] >= x["bound"] - 3 * x["mcse"])
        items = [
            (r"the question: \ coverage of weighted conformal with estimated weights", THESISC),
            (r"the theorem: \ loss $\le \mathrm{TV}(P_{\hat w}, Q)$, \ with weights fixed in advance", THESISC),
            (rf"the study: \ the bound held in {held} of {len(st)} cells", HONC),
            (rf"NHANES: \ 73\% unweighted, \ {100 * nh['coverage']['estimated']:.0f}\% with estimated weights", ESTC),
            (r"open: \ cross-fitted weights, \ and a bound that sees the scores", S.ACCENT),
        ]
        rows = VGroup(*[label(t, font_size=27, color=c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        if rows.width > 12.8:
            rows.width = 12.8
        head = label(r"The dissertation, \ in five lines", font_size=38).to_edge(UP, buff=0.5)
        rows.next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            f"<bookmark mark='a'/> The dissertation in five lines. A question that matters to every deployed model whose "
            f"population drifts. A theorem, with weights fixed in advance: coverage falls by at most a total variation "
            f"distance. <bookmark mark='b'/> A preregistered study in which the bound held in {held} of {len(st)} cells. "
            f"An application in which estimated weights restored coverage from seventy-three to "
            f"{100 * nh['coverage']['estimated']:.0f} percent. <bookmark mark='c'/> And what is still open: weights "
            f"estimated on the same data, and a sharper bound that looks at the scores as well as the covariates."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(1.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six last problems, with full solutions in the README. <bookmark mark='a'/> Why the weights' scale does not "
            "matter; the total variation between two normals; the tilted normal; why unweighted conformal survives any "
            "shift when the scores ignore x; the step of the proof that drops the conditional law; and, as a research "
            "exercise, a simulation that could break the theorem if its independence assumption were dropped."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"T. Morris, \ I. White \& M. Crowther, \ \emph{Statistics in Medicine} (2019)",
             r"A. Angelopoulos, \ R. Barber \& S. Bates, \ \emph{Theoretical Foundations of Conformal Prediction} (2024)",
             r"J. Graunt, \ \emph{Natural and Political Observations Made upon the Bills of Mortality} (1662)"],
            [r"R. Tibshirani, \ R. Barber, \ E. Cand\`es \& A. Ramdas, \ NeurIPS (2019)",
             r"R. Barber, \ E. Cand\`es, \ A. Ramdas \& R. Tibshirani, \ \emph{Ann. Statist.} (2023)",
             r"L. Lei \& E. Cand\`es, \ \emph{JRSS B} (2021)",
             r"the Museum's NHANES extract; \ this part's \texttt{statkit.thesis} and protocol"])
        with self.voiceover(
            "The sources behind the dissertation: Morris, White and Crowther on simulation studies; Angelopoulos, Barber "
            "and Bates on conformal prediction; the weighted conformal papers; and, once more, Graunt."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def farewell(self):
        tr = transcript_card(done=65, current=None)
        tr.to_edge(UP, buff=0.8)
        end = VGroup(label(r"Statistics, Built", font_size=56), label(r"sixty-five parts, \ from Graunt's ledger to the frontier", font_size=30, color=GREY_A),
                     label(r"go and make some knowledge", font_size=34, color=S.ACCENT)).arrange(DOWN, buff=0.3)
        end.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Sixty-five parts of sixty-five. <bookmark mark='a'/> In 1662 a haberdasher read a ledger and saw what no "
            "single page showed. Every method since has been a way of seeing more from the page, and of saying honestly how "
            "much. <bookmark mark='b'/> That is the whole of statistics, and now it is yours. Go and make some knowledge."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(65)])
            vo.wait_until("a")
            self.play(FadeIn(end[0]), FadeIn(end[1]))
            vo.wait_until("b")
            self.play(FadeIn(end[2], shift=UP * 0.2))
        self.wait(3.0)
        self.clear_scene()

    def three(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> If the whole degree had to fit in three questions, they would be these. <bookmark "
            "mark='b'/> What could the data have been? That is the sampling distribution, the idea behind every interval "
            "and test since Part eight. <bookmark mark='c'/> What is assumed, and what makes it true? Randomization, "
            "exchangeability, a model checked against the data. <bookmark mark='d'/> And how sure, honestly? An interval "
            "whose promise has been tested, a Board row that says kept, or a broken one that says why not.",
            [(r"\text{one}", r":", r"\text{what could the data have been?}", 40),
             (r"\text{two}", r":", r"\text{what is assumed, \ and why is it true?}", 40),
             (r"\text{three}", r":", r"\text{how sure, \ honestly?}", 40),
             (r"\text{the answer}", r":", r"\text{a tested promise}", 40)],
            [r"Part 8", r"design", r"the Board", r"the degree"],
            colors=[(3, S.ACCENT)])

    def reflection(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A last reflection on the dissertation itself. <bookmark mark='b'/> It did not overturn "
            "anything. It took a method people already use, stated what it promises when its main assumption is only "
            "approximately true, proved it, measured how pessimistic the statement is, and showed the method on real data. "
            "<bookmark mark='c'/> One of its five predictions failed, and the failure taught something the theorem did not: "
            "infinite intervals are the hidden cost of large shifts. <bookmark mark='d'/> That is what most research is. A "
            "careful step, honestly reported, that the next person can stand on.",
            [(r"\text{did not}", r":", r"\text{overturn anything}", 40),
             (r"\text{did}", r":", r"\text{state, \ prove, \ measure, \ apply}", 40),
             (r"\text{a failed prediction}", r":", r"\text{taught the most}", 40),
             (r"\text{research}", r":", r"\text{a careful step, \ honestly reported}", 40)],
            [r"modest", r"complete", r"P3", r"what a thesis is"],
            colors=[(3, THESISC)])
