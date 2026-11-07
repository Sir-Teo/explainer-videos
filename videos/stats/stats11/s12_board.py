from __future__ import annotations

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats11.common import *  # noqa: F403


class Board(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.mcse()
        self.replications()
        self.rows()
        self.lessons()

    def card(self):
        card = chapter_card(11, r"The Coverage Board, \ formally", r"How every promise in the series is checked", part=PART)
        with self.voiceover("Chapter eleven. The Coverage Board, formally."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def protocol(self):
        items = [
            (r"A", r"aim: \ does the method keep its promise in this setting?"),
            (r"D", r"data: \ draw from the World, \ where the truth is known (or from a stated model)"),
            (r"E", r"estimand: \ the exact population value, \ \texttt{World.truth}"),
            (r"M", r"method: \ the interval or test exactly as a user would compute it"),
            (r"P", r"performance: \ coverage (or size) over $R$ seeded replications, \ with its MC SE; \ mean width"),
        ]
        rows = VGroup()
        for k, t in items:
            rows.add(VGroup(Circle(radius=0.26, color=OBS, fill_opacity=0.15).add(label(k, font_size=24, color=OBS)), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.1, 0])
        head = label(r"the protocol: \ Part 7's ADEMP (Morris, White \& Crowther, 2019)", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Since Part 8, every promise in the series has gone through the same check. Here it is, formally, using Part "
            "7's ADEMP framework for simulation studies. <bookmark mark='a'/> The aim: does this method keep its promise in "
            "this setting? <bookmark mark='b'/> The data: drawn from the World, the synthetic population whose truth we "
            "know exactly, or from a model we state. <bookmark mark='c'/> The estimand: the exact population value. "
            "<bookmark mark='d'/> The method: computed exactly as a user would, with no peeking at the truth. "
            "<bookmark mark='e'/> And the performance measure: the coverage, or for a test the false-alarm rate, over a "
            "fixed number of seeded replications, reported with its Monte Carlo standard error, alongside the mean width."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mcse(self):
        rows = [
            cmath(r"\widehat{\mathrm{cov}}", r"=", r"\frac1R \sum_{r=1}^R \mathbf 1\{\theta \in C_r\}", font_size=34),
            cmath(r"\mathrm{SE}_{\mathrm{MC}}", r"=", r"\sqrt{\frac{0.95 \times 0.05}{R}} = 0.22\% \quad (R = 10{,}000)", font_size=32),
            cmath(r"\text{verdict}", r"=", r"\begin{cases}\text{kept} & |\widehat{\mathrm{cov}} - 0.95| \le 3\,\mathrm{SE}_{\mathrm{MC}} \\ "
                  r"\text{broken} & \text{below} \\ \text{conservative} & \text{above}\end{cases}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a proportion of $R$ independent successes"), why(r"at the nominal level: \ Part 7's Monte Carlo error"),
                why(r"3 SEs: \ a false ``broken'' about once in 700 rows")]
        with self.voiceover(
            "<bookmark mark='a'/> The achieved coverage is the fraction of replications in which the interval caught the "
            "truth. <bookmark mark='b'/> It's a proportion, so its Monte Carlo standard error, evaluated at the nominal "
            "level, is root point nine five times point zero five over R: with ten thousand replications, a fifth of a "
            "percentage point. <bookmark mark='c'/> The verdict: kept if within three Monte Carlo standard errors of the "
            "promise; broken if further below; conservative if further above. With three standard errors, a method whose "
            "coverage equals the nominal level is falsely called broken about once in seven hundred rows."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rows(self):
        rows = load_all(upto=11)
        b = coverage_board(rows, lit_part=11, placeholders=0, font_size=16, row_h=0.36)
        b.scale_to_fit_height(min(b.height, 7.5)).move_to(ORIGIN)
        mine = [i for i, r in enumerate(rows) if r.part == 11]
        with self.voiceover(
            "Here's the board with Part 11's rows, a proportion of five percent and fifty trials, the kind of rare-event "
            "setting where it matters. <bookmark mark='a'/> Wald: ninety-one point four. Broken. <bookmark mark='b'/> "
            "Wilson: ninety-six point one, conservative at this particular p. <bookmark mark='c'/> Agresti–Coull, also "
            "ninety-six point one, conservative. <bookmark mark='d'/> Clopper–Pearson: ninety-eight point six. "
            "Conservative, as designed. <bookmark mark='e'/> And Jeffreys, eighty-seven point eight: broken, because p "
            "equals point zero five happens to sit in one of its dips near the edge. A single row is a spot check at one "
            "point of a sawtooth; the coverage curves of chapter four give the whole picture. <bookmark mark='f'/> Then the "
            "prediction interval for a new man's height: ninety-five point oh. Kept. <bookmark mark='g'/> And for a new "
            "income: ninety-three point nine. Broken, because the pivot needed normal data."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend), *[FadeIn(b.body[i]) for i in range(len(b.body)) if i not in mine])
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                if k < len(mine):
                    self.play(FadeIn(b.body[mine[k]], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"what the Board has taught so far", font_size=32, color=OBS),
            label(r"exact theory keeps exact promises \ ($z$, $t$: normal model; \ permutation: exchangeability)", font_size=24),
            label(r"plugging in an estimate without paying for it breaks them \ (Wald, \ $z$ with $s$)", font_size=24, color=MISS),
            label(r"assumptions about shape break them in the tails \ (skewed incomes: \ $t$, \ $F$, \ prediction)", font_size=24, color=MISS),
            label(r"habits break them \ (peeking)", font_size=24, color=MISS),
            label(r"every later part adds rows; \ Part 65 reads the whole board", font_size=24, color=GREY_A),
        ), 12.6, 0.4, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Four parts in, the board has a pattern. <bookmark mark='b'/> Exact theory keeps exact "
            "promises: z and t in their normal models, and permutation tests under exchangeability. Welch's t approximation is not exact under unequal variances. <bookmark mark='c'/> Plugging in "
            "an estimate without paying for its uncertainty breaks them: Wald, and z with s. <bookmark mark='d'/> "
            "Assumptions about shape break them in the tails, as skewed incomes did to t, to F and to prediction. "
            "<bookmark mark='e'/> And habits break them, like peeking. <bookmark mark='f'/> Every part from here on adds "
            "rows, and Part 65 reads the whole board."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def replications(self):
        rows = [
            cmath(r"R", r"=", r"\frac{0.95 \times 0.05}{\mathrm{SE}_{\mathrm{MC}}^2}", font_size=34),
            cmath(r"\mathrm{SE}_{\mathrm{MC}} = 0.22\%", r"\Rightarrow", r"R = 10{,}000;\quad \text{to detect } 94\% \text{ vs } 95\%:\ \ 3\,\mathrm{SE} \approx 0.65\%", font_size=28),
            cmath(r"\text{seeds}", r"=", r"\text{fixed and published}", r"\quad\text{every row is reproducible}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"choose the precision first, \ then $R$ (Part 7)"), why(r"a 3-SE threshold is resolution, \ not guaranteed detection power"),
                why(r"\texttt{python -m videos.stats.statsN.compute --force board}")]
        intro = label('Choose Monte Carlo precision before the simulation', font_size=36)
        with self.voiceover(
            "How many replications does a row need? <bookmark mark='a'/> Choose the precision first. The Monte Carlo "
            "standard error is root point nine five times point zero five over R, so R is that product over the squared "
            "standard error you want. <bookmark mark='b'/> With ten thousand, the standard error is a fifth of a point, and "
            "the three-standard-error cutoff is about point six five percentage points. A true coverage just below that cutoff can still escape detection; resolution is not guaranteed power. "
            "That's the resolution of every verdict on it. <bookmark mark='c'/> And every row uses fixed, published seeds, "
            "so anyone can regenerate the board exactly with one command."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=0.0, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()
