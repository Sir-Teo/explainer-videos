from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403


def sci(x):
    e = int(np.floor(np.log10(x)))
    return rf"${x / 10 ** e:.0f} \times 10^{{{e}}}$"


class Reproduce(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Reproducibility", r"Could someone else get the same answer?",
             "Chapter thirteen. Reproducibility.", lit={2019: r"the AEA's data editor"}, scale=("world",),
             horizon=("a decade",))
        self.report()
        self.seeds()
        self.known()
        self.package()

    def report(self):
        A = load("accuracy")
        r = next(x for x in A["table"] if x["method"].startswith("collocation, degree 8"))
        rows = [(r"model", r"the growth model, \ $\gamma = 2$, \ $\beta = 0.96$, \ $\delta = 0.08$"),
                (r"method", r"Chebyshev collocation, \ degree 8, \ 9 nodes on $[0.5, 1.5]\,k^*$"),
                (r"solver", r"Powell's hybrid method, \ tolerance $10^{-14}$, \ started from degree 1"),
                (r"time", rf"{1000 * r['seconds']:.0f} milliseconds"),
                (r"accuracy", rf"worst Euler error $10^{{{r['max']:.1f}}}$, \ mean $10^{{{r['mean']:.1f}}}$, \ on "
                              r"$[0.6, 1.4]\,k^*$")]
        g = VGroup()
        for k_, v_ in rows:
            g.add(VGroup(label(k_, font_size=21, color=GREY_A), label(v_, font_size=21, color=WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        for r_ in g:
            r_[1].shift(RIGHT * (1.8 - r_[0].width))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        frame = SurroundingRectangle(g, buff=0.4, corner_radius=0.12, color=EGM, stroke_width=1.6)
        head = label(r"every solution comes with its report", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "A computed answer that nobody can check is an anecdote. The habit this part has been building is "
            "simple: every solution comes with its report. <bookmark mark='a'/> What model, with which "
            "parameters. <bookmark mark='b'/> Which method, on which grid or with which basis. <bookmark mark='c'/> "
            "Which solver and tolerance, and where it started. <bookmark mark='d'/> How long it took. <bookmark "
            "mark='e'/> And how accurate it is, measured. Agora's solvers return such a report with every answer, "
            "and the films quote them."
        ) as vo:
            self.play(FadeIn(head), Create(frame))
            for mk, r_ in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def seeds(self):
        R = load("reproduce")
        est = R["estimates"]
        rows = VGroup(*[VGroup(label(k_, font_size=22, color=GREY_A), label(f"{v_:.6f}", font_size=24,
                                                                             color=WHITE)).arrange(RIGHT, buff=0.6)
                        for k_, v_ in est.items()])
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to(UP * 0.4)
        exact = label(rf"the exact answer: \ {R['exact']:.6f}", font_size=22, color=GAIN).next_to(rows, DOWN,
                                                                                               buff=0.5)
        head = label(r"10,000 random draws of $e^{\varepsilon/2}$, \ averaged".replace(",", "{,}"), font_size=24,
                     color=WHITE).to_edge(UP, buff=0.8)
        foot = label(r"fix the seed, \ record it, \ and report how much the answer moves when it changes",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Randomness needs the same care. Average ten thousand random draws. <bookmark mark='a'/> With the "
            "random number generator started from seed zero, one answer; <bookmark mark='b'/> started from seed "
            "zero again, exactly the same answer, to the last digit; <bookmark mark='c'/> from seed one, a "
            "different answer, in the third decimal place. <bookmark mark='d'/> Neither is the truth. So fix the "
            "seed and record it, so that a result can be repeated exactly, and report how much the answer moves "
            "when the seed changes, so that nobody mistakes simulation noise for a finding."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(exact), FadeIn(foot))
        self.clear_scene()

    def known(self):
        R = load("reproduce")
        eq = MathTex(r"\gamma = 1,\ \delta = 1 \;\Longrightarrow\; c = (1 - \alpha\beta)\, k^{\alpha}", font_size=42,
                     color=THEORY).move_to(UP * 1.6)
        rows = VGroup(
            label(r"Brock and Mirman's economy has a formula: \ test the solvers on it", font_size=22, color=WHITE),
            label(r"collocation, \ degree 8: \ largest error " + sci(R["bm_colloc_err"]), font_size=22,
                  color=PROJ),
            label(r"value iteration, \ 500 points: \ largest error " + sci(R["bm_vfi_err"]), font_size=22,
                  color=VFI),
            label(r"tests like these run every time Agora changes: \ \texttt{tests/economics/test\_solve.py}",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.6)
        with self.voiceover(
            "And test the solver where the answer is known. <bookmark mark='a'/> With log utility and full "
            "depreciation, the growth model of Brock and Mirman, from Part twenty-nine, has a formula: consume a "
            "fixed share of output. <bookmark mark='b'/> Collocation reproduces it to within a few parts in ten "
            "million; <bookmark mark='c'/> value iteration on five hundred points, to about five parts in ten "
            "thousand, the grid's limit. <bookmark mark='d'/> Tests like these run every time the code changes, so "
            "a mistake introduced next year is caught the day it is made."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def package(self):
        cards = point_cards([
            (r"the data", r"raw files, \ where each came from, \ its licence, \ the date it was taken", DATA),
            (r"the code", r"one command from the raw data to every table and figure", EGM),
            (r"the environment", r"the versions of the language and its libraries", VFI),
            (r"the numbers", r"seeds, \ tolerances, \ grids, \ and their reports", POLICY),
            (r"the tests", r"known answers the code must reproduce", PROJ),
            (r"the README", r"what to run, \ in what order, \ and how long it takes", WHITE),
        ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.2)
        head = label(r"a replication package", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Put together, these make a replication package, which leading journals now require. Since 2019 the "
            "American Economic Association's data editor has checked that a paper's package runs before the paper "
            "is published. <bookmark mark='a'/> The raw data, with where each file came from, its licence and the "
            "date it was taken. <bookmark mark='b'/> The code, ideally one command from raw data to every table "
            "and figure. <bookmark mark='c'/> The environment: the versions of everything it ran on. <bookmark "
            "mark='d'/> The numbers that steer it: seeds, tolerances, grids, and their reports. <bookmark "
            "mark='e'/> Tests with known answers. <bookmark mark='f'/> And a README that says what to run and how "
            "long it takes. This series is built the same way: every number in these films comes from a compute "
            "script that anyone can rerun."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcdef", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
