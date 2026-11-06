from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class FullBoard(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. The full Coverage Board: every promise of the degree, tested.", 8,
                            r"The full Coverage Board", r"Every promise, \ kept or broken")
        self.recall()
        self.mosaic()
        self.breaks()
        self.keeps()
        self.stages_()
        self.memorable()
        self.cannot()
        self.lesson()

    def recall(self):
        f = load("fullboard")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The Coverage Board began in Part one. <bookmark mark='b'/> Each row is a promise a "
            f"method makes: a ninety-five percent interval, a five percent test. <bookmark mark='c'/> Each was tested by "
            f"simulation on the World or on the Museum's data, hundreds or thousands of times, and given a verdict: kept, "
            f"within three Monte Carlo standard errors of its promise; conservative, safely beyond it; or broken. <bookmark "
            f"mark='d'/> After sixty-five parts it holds {f['n']} rows from {f['parts']} parts.",
            [(r"\text{a row}", r":", r"\text{a method's promise}", 40),
             (r"\text{tested}", r":", r"\text{by simulation, \ many times}", 40),
             (r"\text{verdict}", r":", r"\text{kept, \ conservative, \ broken}", 40),
             (r"\text{now}", r":", rf"{f['n']} \ \text{{rows, \ {f['parts']} parts}}", 40)],
            [r"Part 1", r"nominal level", r"three Monte Carlo SEs", r"the degree"],
            colors=[(3, S.ACCENT)])

    def mosaic(self):
        f = load("fullboard")
        bm = BoardMosaic(f["rows"], width=12.6, tile_h=0.17, center=[0, -2.3, 0])
        ax = bm.axis()
        v = f["verdict"]
        head = label(r"The Coverage Board, \ the whole degree", font_size=34).to_edge(UP, buff=0.4)
        leg = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9), label(rf"{t}: \ {v.get(k, 0)}", font_size=24, color=c)).arrange(RIGHT, buff=0.15)
                       for k, c, t in (("kept", S.KEPT, r"kept"), ("conservative", S.EST, r"conservative"), ("broken", S.RESID, r"broken"))])
        leg.arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            f"<bookmark mark='a'/> Here it is, every row as a tile, stacked above its part, from the first course on the "
            f"left to the research frontier on the right. <bookmark mark='b'/> {v.get('kept', 0)} promises kept. <bookmark "
            f"mark='c'/> {v.get('conservative', 0)} conservative: honest, but paying in width or power. <bookmark mark='d'/> "
            f"And {v.get('broken', 0)} broken. Nearly half. That is not a failure of the course. Most broken rows were put "
            f"on the Board on purpose, as the naive method beside its repair: the iid error bar beside the clustered one, the "
            f"in-sample value beside the split one, the unweighted interval beside the weighted one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in bm.tiles()], lag_ratio=0.004), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(leg[0]), Indicate(bm.verdict("kept"), color=S.KEPT, scale_factor=1.0))
            vo.wait_until("c")
            self.play(FadeIn(leg[1]), Indicate(bm.verdict("conservative"), color=S.EST, scale_factor=1.0))
            vo.wait_until("d")
            self.play(FadeIn(leg[2]), Indicate(bm.verdict("broken"), color=S.RESID, scale_factor=1.0))
        self.wait(1.5)
        self.clear_scene()

    def breaks(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What breaks a promise, in the Board's own words. <bookmark mark='b'/> Ignored dependence: "
            "clustered pupils analysed as independent in Part thirty-five, two random walks regressed on each other in Part "
            "thirty-eight, benchmark questions in Part sixty-four. <bookmark mark='c'/> Selection and adaptivity: peeking at "
            "five looks in Part thirty-five, the winner's Wald interval in Part fifty-six, intervals after Thompson sampling in "
            "Part fifty-eight. <bookmark mark='d'/> A sample that is not the population: the opt-in poll of Part forty-one, the "
            "shifted sample of Part sixty, this part's unweighted intervals. <bookmark mark='e'/> And noise left out of the "
            "model: measurement error in Part forty-one, privacy noise in Part sixty-three, a judge's errors in Part "
            "sixty-four.",
            [(r"what breaks a promise:", GREY_A),
             (r"ignored dependence: \ clusters, \ random walks, \ benchmark passages", S.RESID),
             (r"selection and adaptivity: \ peeking, \ winners, \ bandits", S.RESID),
             (r"the wrong population: \ opt-in polls, \ shifted samples", S.RESID),
             (r"noise left out: \ measurement error, \ privacy noise, \ judges", S.RESID)],
            buff=0.42, font_size=25, head_size=32)

    def keeps(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What keeps one. <bookmark mark='b'/> Randomization, which makes a design's own "
            "probabilities the basis of inference: Fisher's tests, Neyman's intervals, PPI's random human labels. <bookmark "
            "mark='c'/> Exchangeability, used carefully: permutation tests, conformal prediction, and weights when it fails. "
            "<bookmark mark='d'/> Robust variances that do not trust the model: the sandwich, cluster-robust errors, the "
            "bootstrap of clusters. <bookmark mark='e'/> And honest bookkeeping of what was chosen from the data: sample "
            "splitting, selective inference, anytime-valid tests.",
            [(r"what keeps a promise:", GREY_A),
             (r"randomization: \ the design's own probabilities", S.KEPT),
             (r"exchangeability: \ permutations, \ conformal, \ weights", S.KEPT),
             (r"robust variances: \ sandwich, \ clusters, \ the bootstrap", S.KEPT),
             (r"honest selection: \ splitting, \ conditioning, \ anytime-valid", S.KEPT)],
            buff=0.42, font_size=25, head_size=32)

    def lesson(self):
        f = load("fullboard")
        self.lad_voiceover(
            "<bookmark mark='a'/> The degree's lesson, in one line of the Board. <bookmark mark='b'/> A procedure's "
            "promise is a statement about repeated use, and it can be checked: by proof where possible, by simulation "
            "always. <bookmark mark='c'/> The methods that keep their promises are the ones whose assumptions are made true "
            "by design, or made weak enough to be believable. <bookmark mark='d'/> And a broken row is not an embarrassment. "
            "It is the most useful thing a statistician can show a colleague: here is the method you were about to use, and "
            "here is what it actually does.",
            [(r"\text{a promise}", r":", r"\text{about repeated use, \ checkable}", 40),
             (r"\text{check it}", r":", r"\text{proof if possible, \ simulation always}", 40),
             (r"\text{kept by}", r":", r"\text{design, \ or weak assumptions}", 40),
             (r"\text{a broken row}", r":", r"\text{the most useful thing to show}", 40)],
            [r"frequentist calibration", r"Part 7", r"the pattern", r"the Board's purpose"],
            colors=[(2, HONC)])

    def stages_(self):
        f = load("fullboard")
        bs = f["by_stage"]
        names = {"1": r"I \ foundations", "2": r"II \ methods", "3": r"III \ the MSc", "4": r"IV \ theory", "5": r"V \ the frontier"}
        lines = [(r"the Board by stage: \ kept, \ conservative, \ broken", GREY_A)]
        for k in ("1", "2", "3", "4", "5"):
            c = bs.get(k, {})
            lines.append((rf"{names[k]}: \ {c.get('kept', 0)}, \ {c.get('conservative', 0)}, \ {c.get('broken', 0)}", WHITE))
        self.list_voiceover(
            "<bookmark mark='a'/> The Board by stage. <bookmark mark='b'/> The foundations tested a handful of promises, "
            "mostly the first intervals and their small-sample failures. <bookmark mark='c'/> The methods stage tested the "
            "everyday tools, and found the classic traps: unadjusted multiple comparisons, overdispersion, the wrong "
            "variance. <bookmark mark='d'/> The master's stage holds the most rows, because it holds the most methods. "
            "<bookmark mark='e'/> The theory stage tested what theorems promise in finite samples, and found many "
            "conservative rows, the price of worst-case guarantees. <bookmark mark='f'/> And the frontier tested the newest "
            "methods against the naive ones they replace.",
            lines, buff=0.38, font_size=25, head_size=30)

    def memorable(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five rows worth remembering. <bookmark mark='b'/> The opt-in poll of Part forty-one, "
            "whose ninety percent interval covered the truth four and a half percent of the time. <bookmark mark='c'/> The "
            "Cox model that counted immortal time in Part forty, and never covered. <bookmark mark='d'/> Peeking at a z test "
            "five times in Part thirty-five, which turned a five percent test into a fourteen percent one. <bookmark "
            "mark='e'/> A pupil-level interval for a school-randomized trial, covering thirty-six percent. <bookmark "
            "mark='f'/> And, from off the Board, the reused holdout of Part sixty-four, which reported sixty-four percent accuracy for a coin "
            "flip. Each is a method someone, somewhere, used last week.",
            [(r"rows to remember:", GREY_A),
             (r"Part 41: \ the opt-in poll, \ 4.5\% coverage", S.RESID),
             (r"Part 40: \ immortal time, \ 0\%", S.RESID),
             (r"Part 35: \ peeking five times, \ size 14\%", S.RESID),
             (r"Part 35: \ pupils for a school-randomized trial, \ 36\%", S.RESID),
             (r"Part 64: \ a reused holdout, \ 64\% for a coin flip", S.RESID)],
            buff=0.38, font_size=25, head_size=30)

    def cannot(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> What the Board cannot show. <bookmark mark='b'/> Coverage is one property. A kept interval "
            "can be uselessly wide, and a test of the right size can have no power: the Board's rows recorded widths and "
            "power where they mattered, but the verdict ignores them. <bookmark mark='c'/> Coverage is marginal, over "
            "repeated samples from one simulated world; Part fifty-seven showed that conditional coverage is a different, "
            "harder promise. <bookmark mark='d'/> And every row is about the World or the Museum as simulated. A method kept "
            "there can still break on data with a flaw nobody thought to simulate. The Board is evidence, not proof.",
            [(r"\text{not shown}", r":", r"\text{width, \ power}", 40),
             (r"\text{marginal}", r":", r"\text{not conditional}", 40),
             (r"\text{simulated}", r":", r"\text{flaws nobody imagined}", 40),
             (r"\text{so}", r":", r"\text{evidence, \ not proof}", 40)],
            [r"efficiency", r"Part 57", r"the World's limits", r"humility"],
            colors=[(3, NAIVEC)])
