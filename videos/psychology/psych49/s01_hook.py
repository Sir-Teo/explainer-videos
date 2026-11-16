from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


def yes_grid(yes, cell: float = 0.085, gap: float = 0.012) -> VGroup:
    """Paths as columns, hypotheses as rows: a filled square where a path says yes."""
    yes = np.asarray(yes)
    g = VGroup()
    for j in range(yes.shape[1]):
        for i in range(yes.shape[0]):
            sq = Square(cell, stroke_width=0, fill_color=THRESH if yes[i, j] else "#20252E", fill_opacity=1)
            sq.move_to([i * (cell + gap), -j * (cell + 4 * gap) * 3.2, 0])
            g.add(sq)
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.teams()
        self.multiverse()
        self.question()
        self.objectives()

    def teams(self):
        head = heading(r"Seventy teams, \ one dataset")
        rows = rows_of([
            (r"2020: \ one brain-imaging dataset, \ a gambling task in over a hundred people, \ given to seventy "
             r"teams", WHITE),
            (r"the same nine yes-or-no questions: \ does this region respond to gains? \ to losses?", PERSON),
            (r"no two teams chose the same analysis pipeline", AUTH),
            (r"for several questions, \ some teams said yes and others no, \ from the same data", AUTH),
            (r"the variation came from the analysis, \ not from the brains", YOU),
        ], 12.4, 23, 0.44).move_to([0, -0.4, 0])
        tag = published_tag(r"Botvinik-Nezer et al.\ (2020)")
        with self.voiceover(
            "In 2020, one brain-imaging dataset, from over a hundred people doing a gambling task, was given to "
            "seventy research teams. <bookmark mark='a'/> Each team got the same nine yes-or-no questions. Does this "
            "region respond to gains? To losses? <bookmark mark='b'/> No two teams chose the same analysis pipeline. "
            "<bookmark mark='c'/> And for several of the questions, some teams said yes and others said no, from the "
            "same data. <bookmark mark='d'/> The variation came from the analysis, not from the brains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for m, r in zip("abcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def multiverse(self):
        d = load("multiverse")
        head = heading(r"Seventy-two pipelines, \ five questions")
        grid = yes_grid(d["yes"]).move_to([-2.0, 0.6, 0])
        names = VGroup(*[label(rf"H{j + 1}: \ effect {e:g}", font_size=14, color=GREY_A)
                         .next_to(grid[j * d["n_paths"]], LEFT, buff=0.15) for j, e in enumerate(d["effects"])])
        shares = VGroup(*[label(rf"{100 * s:.0f}\% yes", font_size=15, color=THRESH)
                          .next_to(grid[j * d["n_paths"] + d["n_paths"] - 1], RIGHT, buff=0.15)
                          for j, s in enumerate(d["share"])])
        rows = rows_of([
            (r"Psyche's synthetic brain: \ 30 people, \ five regions with planted effects from none to large", WHITE),
            (r"72 defensible pipelines: \ 3 smoothings, \ 6 thresholds, \ 2 exclusion rules, \ 2 covariate choices", MODEL),
            (rf"no region: \ every pipeline says no; \ the largest: \ {100 * d['share'][-1]:.0f}\% say yes; \ "
             rf"in between, \ {100 * d['share'][2]:.0f}\% and {100 * d['share'][3]:.0f}\%", PERSON),
            (rf"72 pipelines, \ {d['distinct']} different maps", AUTH),
        ], 12.4, 20, 0.3).move_to([0, -2.4, 0])
        tag = psyche_tag(r"\texttt{neurodata.multiverse}")
        with self.voiceover(
            "Psyche can do the same where the truth is known. <bookmark mark='a'/> A synthetic brain, thirty people, "
            "and five regions with planted effects, from none to large. <bookmark mark='b'/> Seventy-two defensible "
            "pipelines: three amounts of smoothing, six thresholds, two exclusion rules, and with or without a "
            "covariate. Each column is a pipeline, each row a question, and gold means yes. <bookmark mark='c'/> "
            "Where nothing was planted, every pipeline says no. For the largest effect, about three quarters say yes. "
            "In between, the pipelines split. <bookmark mark='d'/> Seventy-two pipelines gave forty-four different "
            "maps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.003), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(shares))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what must be true for a brain map to be evidence?")
        rows = rows_of([
            (r"the pipeline: \ preprocessing, \ the model at two levels, \ and thresholds", SYMP),
            (r"patterns: \ decoding, \ geometry and encoding models", MODEL),
            (r"connections, \ waves and populations of neurons", PERSON),
            (r"reading out, \ and how many people a claim needs", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks what must be true for a brain map to be evidence. <bookmark mark='a'/> The pipeline: "
            "preprocessing, the model at two levels, and thresholds. <bookmark mark='b'/> Patterns: decoding, "
            "geometry, and encoding models. <bookmark mark='c'/> Connections, waves, and populations of neurons. "
            "<bookmark mark='d'/> And reading the brain out, and how many people a claim needs."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 49", font_size=34, color=GREY_B), label(r"Modelling the Brain's Data", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the analysis chain, \ and its forks",
            r"first and second levels: \ subjects as a sample",
            r"clusters, \ permutations and false discoveries",
            r"decoding, \ representational geometry and encoding",
            r"connectivity, \ EEG windows and neural populations",
            r"brain-computer interfaces, \ and samples of thousands",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 49 of Psychology, Built: modelling the brain's data. <bookmark mark='a'/> We'll walk the "
            "analysis chain and count its forks. We'll fit the model at two levels and see why subjects must be a "
            "sample. We'll test clusters by permutation and control false discoveries. We'll decode patterns, compare "
            "geometries, and fit encoding models against a noise ceiling. We'll see what motion does to "
            "connectivity, what choosing a time window does to an ERP, and how a population of neurons codes a "
            "movement. And we'll read the brain out, and ask how many people a brain-behaviour claim needs."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
