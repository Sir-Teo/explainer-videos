from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403

LEARNERS = (("model_free", r"model-free", MF), ("successor", r"successor", VALUE), ("model_based", r"model-based", MB))


class Successor(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.revaluation()
        self.replay()

    def card(self):
        card = chapter_card(9, r"Between habit and plan", r"Can you cache predictions without caching values?",
                            lit={1993: r"Dayan", 2017: r"Momennejad et al."}, part=PART, scale=("circuit", "mind"),
                            marr=("what", "how"))
        with self.voiceover("Chapter nine. Between habit and plan."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"The successor representation")
        eqs = VGroup(
            MathTex(r"M(s, s') = \mathbb{E}\Big[\sum_t \gamma^t\,[\,s_t = s'\,] \;\Big|\; s_0 = s\Big]", font_size=42),
            MathTex(r"M = (I - \gamma T)^{-1}, \qquad V = M\,r", font_size=46, color=VALUE),
        ).arrange(DOWN, buff=0.45).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"cache, \ for each state, \ where you will tend to be: \ discounted future visits to every state", VALUE),
            (r"a value is then one multiplication: \ predicted visits times what each state pays", WHITE),
            (r"change what a state pays, \ and every value updates at once; \ change the paths, \ and they do not", YOU),
            (r"Peter Dayan, \ 1993; \ a middle way between caching values and planning from scratch", GREY_A),
        ], 12.4, 26, 0.32).move_to([0, -1.5, 0])
        with self.voiceover(
            "There's a middle way between caching values and planning from scratch. <bookmark mark='a'/> Instead of "
            "caching how good each state is, cache where you tend to go from it: for every other state, how often, "
            "discounted, you'll find yourself there. That table is the successor representation, M. For a known "
            "transition matrix it's the inverse of the identity minus gamma times T. <bookmark mark='b'/> A value is "
            "then a single multiplication: expected future visits, times what each state pays. "
            "<bookmark mark='c'/> Its strengths and weaknesses are exactly predictable. Change what a state pays, and "
            "every value updates at once, as if you'd planned. Change the paths between states, and the cached "
            "visits are out of date, as if it were a habit. <bookmark mark='d'/> Peter Dayan proposed it in 1993; "
            "twenty-five years later it became a serious candidate for what the hippocampus computes."
        ) as vo:
            self.play(FadeIn(head), Write(eqs[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Write(eqs[1]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def revaluation(self):
        d = load("successor")
        head = heading(r"Two kinds of revaluation, \ three learners")
        chain = VGroup()
        pos = {1: [-5.6, 2.1, 0], 3: [-4.2, 2.1, 0], 5: [-2.8, 2.1, 0], 2: [-5.6, 1.1, 0], 4: [-4.2, 1.1, 0],
               6: [-2.8, 1.1, 0]}
        for k, p in pos.items():
            c = Circle(radius=0.3, color=REWARD if k > 4 else WHITE, stroke_width=3).move_to(p)
            chain.add(VGroup(c, label(str(k), font_size=22).move_to(c)))
        arr = VGroup(*[Arrow(pos[a], pos[b], buff=0.32, color=GREY_B, stroke_width=3,
                             max_tip_length_to_length_ratio=0.25) for a, b in ((1, 3), (3, 5), (2, 4), (4, 6))])
        pays = VGroup(label(r"pays 10", font_size=18, color=REWARD).next_to(chain[2], RIGHT, buff=0.15),
                      label(r"pays 1", font_size=18, color=REWARD).next_to(chain[5], RIGHT, buff=0.15))
        panels = VGroup()
        for k, (kind, title) in enumerate((("reward", r"reward revaluation: \ 5 now pays 1, \ 6 pays 10"),
                                           ("transition", r"transition revaluation: \ 3 now leads to 6, \ 4 to 5"))):
            A = axes([0, 3], [-1, 1], x_length=4.6, y_length=2.4, xticks=[], yticks=[-1, 0, 1],
                     ylabel=r"preference for 2 over 1" if k == 0 else "", center=[-2.0 + 5.6 * k, -1.3, 0],
                     font_size=16)
            bars = VGroup()
            for j, (name, nm, col) in enumerate(LEARNERS):
                v = d[f"{kind}_{name}"]
                pref = float((v[1] - v[0]) / (abs(v[1]) + abs(v[0])))
                h = A.ax.c2p(0, pref)[1] - A.ax.c2p(0, 0)[1]
                b = Rectangle(width=0.8, height=max(abs(h), 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85)
                b.move_to(A.ax.c2p(j + 0.5, 0), aligned_edge=DOWN if h >= 0 else UP)
                bars.add(VGroup(b, label(nm, font_size=17, color=col).next_to(A.ax.c2p(j + 0.5, -1), DOWN, buff=0.1)))
            t = label(title, font_size=21, color=YOU).next_to(A.ax, UP, buff=0.5)
            panels.add(VGroup(A, bars, t))
        note = rows_of([
            (r"the change is learned only from states 3 to 6; \ states 1 and 2 are never revisited", GREY_A),
            (r"2017: \ people revalue better after reward changes than after transition changes, \ the successor "
             r"signature, \ though not perfectly", VALUE),
        ], 6.4, 21, 0.18).move_to([3.0, 1.7, 0])
        keep_in_frame(note)
        tag = published_tag(archive.MOMENNEJAD_2017.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{rl.revaluation}")
        with self.voiceover(
            "Ida Momennejad, Sam Gershman and colleagues turned this into a test in 2017. <bookmark mark='a'/> People "
            "learn two short paths: from state one, through three, to five, which pays ten; from two, through four, "
            "to six, which pays one. Then they learn a change, but only by visiting the later states. "
            "<bookmark mark='b'/> In reward revaluation, five now pays one and six pays ten. A model-free learner, "
            "with cached values for one and two, still prefers one. The successor learner and the planner both "
            "switch to two. <bookmark mark='c'/> In transition revaluation, three now leads to six and four to "
            "five. Now the successor learner is stuck too, because its cached predictions from one and two still say "
            "where they used to lead. Only the planner switches. <bookmark mark='d'/> People did better at reward "
            "revaluation than at transition revaluation: the successor signature, though they managed some "
            "transition revaluation too, suggesting a mixture with planning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(FadeIn(chain), Create(arr), FadeIn(pays), FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][2]),
                      LaggedStart(*[FadeIn(b) for b in panels[0][1]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]),
                      LaggedStart(*[FadeIn(b) for b in panels[1][1]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def replay(self):
        head = heading(r"Planning offline: \ replay")
        rows = rows_of([
            (r"1994: \ during sleep, \ place cells that fired together on a track fire together again", WHITE),
            (r"later: \ sequences of place cells replay paths, \ forwards and backwards, \ in fractions of a second",
             DELTA),
            (r"backward replay after a reward: \ the order that spreads value from the goal to the start", VALUE),
            (r"forward replay before a choice: \ candidate routes, \ tried out in the head", MB),
            (r"one proposal: \ the brain chooses which memories to replay by how much they would improve choices",
             GREY_A),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.75)
        # schematic: six place fields along a track; one slow pass while running, compressed replays at rest
        cols = [CUE, DELTA, VALUE, MB, REWARD, YOU]
        track = Line([-6.0, 2.45, 0], [-1.6, 2.45, 0], color=GREY_B, stroke_width=6)
        fields = VGroup(*[Circle(radius=0.3, stroke_width=0, fill_color=c, fill_opacity=0.55)
                          .move_to([-5.6 + 0.78 * k, 2.45, 0]) for k, c in enumerate(cols)])
        tl = label(r"a track, \ six place cells", font_size=19, color=GREY_A).next_to(track, DOWN, buff=0.4)

        def raster(x0, width, order, title, col):
            g = VGroup()
            for row, k in enumerate(range(6)):
                y = 2.85 - 0.22 * row
                pos = order.index(k)
                for j in range(3):
                    x = x0 + width * (pos + 0.25 * j + 0.2) / 6.4
                    g.add(Line([x, y - 0.08, 0], [x, y + 0.08, 0], color=cols[k], stroke_width=3))
            box = Rectangle(width=width + 0.2, height=1.55, stroke_color=GREY_D, stroke_width=1.5).move_to(
                [x0 + width / 2, 2.3, 0])
            t = label(title, font_size=18, color=col).next_to(box, DOWN, buff=0.1)
            return VGroup(box, g, t)

        run = raster(-0.9, 2.3, [0, 1, 2, 3, 4, 5], r"running: \ about 4 s", GREY_A)
        fwd = raster(1.75, 1.3, [0, 1, 2, 3, 4, 5], r"forward replay: \ 0.2 s", MB)
        bwd = raster(3.95, 1.3, [5, 4, 3, 2, 1, 0], r"backward replay: \ 0.2 s", VALUE)
        VGroup(track, fields, tl, run, fwd, bwd).scale_to_fit_width(12.6).move_to([0, 1.15, 0])
        cap = label(r"schematic, \ not recorded spikes", font_size=17, color=GREY_C).next_to(bwd, DOWN, buff=0.25).align_to(bwd, RIGHT)
        with self.voiceover(
            "How might a brain plan, or update its cached predictions, without acting? <bookmark mark='a'/> In 1994 "
            "Matthew Wilson and Bruce McNaughton found that place cells which had fired together while a rat ran a "
            "track fired together again while it slept. <bookmark mark='b'/> Later work found whole sequences: the "
            "place cells of a path firing in order, compressed into a fraction of a second, forwards and backwards. "
            "<bookmark mark='c'/> Backward replay, just after a reward, runs from the goal toward the start, the "
            "order that would spread value back along the path in a single sweep. <bookmark mark='d'/> Forward "
            "replay, before a choice, looks like trying routes out. <bookmark mark='e'/> One recent theory says the "
            "brain prioritizes which experiences to replay by how much replaying them would improve its choices. "
            "Memory and its consolidation are Part 21."
        ) as vo:
            self.play(FadeIn(head), FadeIn(track), FadeIn(fields), FadeIn(tl), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), FadeIn(run))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(fwd))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15), FadeIn(bwd))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15), Indicate(fwd, color=MB, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.15))
        self.clear_scene()
