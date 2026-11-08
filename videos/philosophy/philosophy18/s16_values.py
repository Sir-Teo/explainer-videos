from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Values(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Values in science", r"Can science be value-free?", lit=(1953, 2009), part=PART)
        with self.voiceover("Chapter fifteen. Values in science."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rudner()
        self.threshold()
        self.reply()
        self.social()

    def rudner(self):
        hc = history_card(1953, r"Richard Rudner", r"`The Scientist qua Scientist Makes Value Judgments'", width=7.0,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the premise", r"scientists accept or reject hypotheses", THEORY),
            (r"the gap", r"no evidence makes a hypothesis certain: \ acceptance means deciding the evidence is "
                         r"\textit{enough}", REAL),
            (r"the value", r"how much is enough depends on how bad a mistake would be", BAD),
            (r"his example", r"a toxic ingredient in a drug needs far stronger evidence of safety than a flaw in a "
                             r"batch of belt buckles", GREY_A),
            (r"the conclusion", r"`the scientist qua scientist makes value judgments'", GOAL),
        ]
        g = rows_table(rows, top=1.3, gap=0.5, width=8.6, x_text=-2.6)
        with self.voiceover(
            "The ideal of value-free science holds that ethical and political values may choose which questions "
            "science asks, but must not touch its answers. Richard Rudner argued in 1953 that this is impossible. "
            "<bookmark mark='a'/>Scientists accept and reject hypotheses. <bookmark mark='b'/>No evidence makes a "
            "hypothesis certain, so accepting one means deciding that the evidence is enough. "
            "<bookmark mark='c'/>How much evidence is enough depends on how bad it would be to be wrong. "
            "<bookmark mark='d'/>His example: before declaring that a drug contains no toxic ingredient, we need "
            "far stronger evidence than before declaring a batch of belt buckles free of defects. "
            "<bookmark mark='e'/>So the scientist, as a scientist, makes value judgements."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def threshold(self):
        d = load("risk")["cases"]
        head = label(r"Inductive risk, \ as a decision", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-3, 5, 1], y_range=[0, 0.45, 0.1], x_length=6.6, y_length=3.0,
                  axis_config={"color": GREY_B, "include_ticks": False}).move_to([-2.6, 1.0, 0])
        xs = np.linspace(-3, 5, 200)
        safe = ax.plot_line_graph(xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), add_vertex_dots=False,
                                  line_color=OK, stroke_width=3)
        toxic = ax.plot_line_graph(xs, np.exp(-(xs - 1.5) ** 2 / 2) / np.sqrt(2 * np.pi), add_vertex_dots=False,
                                   line_color=BAD, stroke_width=3)
        ls = label(r"if safe", font_size=17, color=OK).next_to(ax.c2p(-1.6, 0.3), UP, buff=0.05)
        lt = label(r"if toxic", font_size=17, color=BAD).next_to(ax.c2p(3.0, 0.3), UP, buff=0.05)
        xl = label(r"test statistic; \ declare `toxic' above the threshold", font_size=17, color=GREY_A).next_to(
            ax, DOWN, buff=0.15)
        names = [r"equal costs", r"missing a toxin costs $10\times$", r"a false alarm costs $10\times$"]
        lines = VGroup(*[DashedLine(ax.c2p(c["threshold"], 0), ax.c2p(c["threshold"], 0.42), color=col)
                         for c, col in zip(d, (GOAL, BAD, ANTI))])
        hd = [r"\text{costs}", r"\text{threshold}", r"\alpha", r"\text{power}"]
        rows = [[label(n, font_size=18), MathTex(f"{c['threshold']:.2f}", font_size=22),
                 MathTex(f"{c['alpha']:.3f}", font_size=22), MathTex(f"{c['power']:.2f}", font_size=22)]
                for n, c in zip(names, d)]
        grid = ValueGrid(hd, rows, col_w=[4.2, 1.8, 1.4, 1.4], cell_h=0.5, font_size=20).move_to([0, -2.1, 0])
        side = stack([(r"same data, \ same statistics", WHITE),
                      (r"the best threshold moves with the costs of error", GOAL),
                      (r"and the costs are value judgments", BAD)], font_size=20, aligned_edge=LEFT,
                     width=4.2).move_to([4.6, 1.0, 0])
        with self.voiceover(
            "The Reasoner turns Rudner's point into a calculation. <bookmark mark='a'/>A test statistic is "
            "distributed one way if a chemical is safe, and shifted if it is toxic. We declare it toxic above some "
            "threshold. <bookmark mark='b'/>If both errors cost the same, the threshold that minimizes expected "
            "loss sits at one point three, with a false-alarm rate of nearly ten percent. "
            "<bookmark mark='c'/>If missing a toxin is ten times worse than a false alarm, the best threshold drops "
            "below zero, and we call the chemical toxic more than half the time it is safe. "
            "<bookmark mark='d'/>If false alarms are ten times worse, the threshold rises to nearly three, and we "
            "catch fewer than one toxin in ten. <bookmark mark='e'/>Same data, same statistics, different "
            "conclusions. The difference is in the costs, and the costs are value judgements."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(safe), Create(toxic), FadeIn(ls), FadeIn(lt), FadeIn(xl))
            self.play(FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(VGroup(*grid.cell[i])))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r) for r in side], lag_ratio=0.3))
        self.clear_scene()

    def reply(self):
        head = label(r"Replies, \ and a new consensus", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Jeffrey \ (1956)", r"scientists should not accept hypotheses at all, \ but report probabilities \ "
                                  r"(Part 13); \ let decision-makers decide", ANTI),
            (r"the rejoinder", r"choosing models, \ priors and data to report already involves the same judgments", BAD),
            (r"Douglas \ (2009)", r"values may play an \textit{indirect} role, \ weighing evidence, \ never a "
                                  r"\textit{direct} one, \ standing in for it", OK),
            (r"the ideal revised", r"not value-free, \ but values made explicit, \ and kept from replacing evidence",
             GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Two replies shaped the debate. <bookmark mark='a'/>Richard Jeffrey answered Rudner in 1956: scientists "
            "should not accept hypotheses at all, but report probabilities, the programme of Part 13, and leave "
            "decisions to those who must make them. <bookmark mark='b'/>The rejoinder is that choosing models, "
            "priors and which results to report involves the same kind of judgement. "
            "<bookmark mark='c'/>Heather Douglas distinguished two roles: values may play an indirect role, "
            "deciding how much evidence is enough, but never a direct role, standing in for evidence that is "
            "missing. <bookmark mark='d'/>The ideal that results is not value-free science, but science whose "
            "values are explicit and kept in their place."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def social(self):
        head = label(r"Objectivity as a social achievement", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Merton \ (1942)", r"the norms of science: \ communism of results, \ universalism, \ "
                                  r"disinterestedness, \ organized scepticism", THEORY),
            (r"McMullin \ (1982)", r"epistemic values \ (accuracy, \ scope, \ simplicity) \ versus "
                                    r"non-epistemic ones", REAL),
            (r"Longino \ (1990)", r"objectivity belongs to communities, \ not individuals: \ it needs venues for "
                                   r"criticism, \ uptake, \ shared standards, \ and equality of authority", OK),
            (r"her example", r"research on sex differences, \ where background assumptions went unexamined until "
                             r"critics with other assumptions entered", GREY_A),
            (r"the upshot", r"diversity is an epistemic resource, \ a theme of Part 12's networks", GOAL),
        ]
        g = rows_table(rows, top=1.5, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "If values cannot be removed from individual scientists, perhaps objectivity lives elsewhere. "
            "<bookmark mark='a'/>Robert Merton described the norms of science as an institution in 1942: results "
            "are shared, claims are judged by impersonal criteria, scientists are disinterested, and scepticism is "
            "organized. <bookmark mark='b'/>Ernan McMullin separated epistemic values, like accuracy, scope and "
            "simplicity, from non-epistemic ones. <bookmark mark='c'/>Helen Longino argued that objectivity belongs "
            "to communities, not to individuals. A community is objective to the degree that it has public venues "
            "for criticism, responds to criticism, shares standards, and gives its members equal authority. "
            "<bookmark mark='d'/>Her examples came from research on sex differences, where background assumptions "
            "went unexamined until critics who did not share them took part. <bookmark mark='e'/>Diversity becomes "
            "an epistemic resource, a theme of Part twelve's models of scientific networks."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
