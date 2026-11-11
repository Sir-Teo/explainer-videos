from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


class Space(VoiceoverScene):
    def construct(self):
        self.card()
        self.tqbf()
        self.geography()
        self.games()
        self.logspace()

    def card(self):
        card = chapter_card(10, r"Space: \ games and alternation", r"What can you do with polynomial memory?",
                            lit=(1973, 1988), extra=((1973, r"Stockmeyer--Meyer"), (1988, r"NL = coNL")), part=PART)
        with self.voiceover("Chapter ten. Space: games and alternation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tqbf(self):
        g = load("games")
        head = label(r"TQBF: \ is a fully quantified formula true?", font_size=32).to_edge(UP, buff=0.35)
        ex = MathTex(r"\exists x_1\, \forall x_2\, \exists x_3\, \forall x_4 \cdots \;\; \varphi(x_1, \ldots, x_n)",
                     font_size=38, color=HEAD).next_to(head, DOWN, buff=0.35)
        rows = [[str(r["n"]), words(r["nodes"]), words(r["full_tree"])] for r in g["tqbf"]]
        tab = grid_table([r"variables", r"nodes evaluated", r"full tree"], rows, widths=[1.8, 2.4, 2.0],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(rows))
        tab.next_to(ex, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        notes = VGroup(
            label(r"evaluate by recursion: \ try $x_1$ = 0 and 1, \\ the rest recursively", font_size=21,
                  color=WHITE),
            label('space: depth $n$; polynomial \\\\ assignment storage; this code \\\\ copies partial assignments', font_size=21,
                  color=YES),
            label(r"\textbf{time}: \ exponential in the worst case \\ (pruning cuts our random ones)", font_size=21,
                  color=NO),
            label(r"Stockmeyer and Meyer \ (1973): \\ TQBF is \textbf{PSPACE-complete}", font_size=22, color=HEAD),
            label(r"SAT is the case with only $\exists$", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "Polynomial space has its own complete problem. <bookmark mark='a'/> Take a formula with quantifiers in "
            "front, alternating: there exists x one, for all x two, there exists x three, and so on. Is the whole "
            "thing true? <bookmark mark='b'/> Evaluate it by recursion: try both values of the first variable, and "
            "evaluate the rest for each. <bookmark mark='c'/> The recursion only needs one assignment and a stack, so "
            "the space is polynomial. <bookmark mark='d'/> The time can be exponential, although on our random "
            "formulas early answers prune most of the tree. <bookmark mark='e'/> Larry Stockmeyer and Albert Meyer "
            "proved in 1973 that this problem is complete for polynomial space. <bookmark mark='f'/> Satisfiability "
            "is the special case with only existential quantifiers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            for mk, n_ in zip("cdef", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def geography(self):
        g = load("games")["geo"]
        head = label(r"A quantifier is a move", font_size=34).to_edge(UP, buff=0.3)
        adj = {int(k): v for k, v in g["adj"].items()}
        P = {0: (-5.4, 0.3), 1: (-4.2, 1.4), 2: (-4.2, -0.8), 3: (-2.9, 2.0), 4: (-2.9, 0.3), 5: (-2.9, -1.6),
             6: (-1.6, 1.3), 7: (-1.6, -0.9), 8: (-0.4, 0.2)}
        nodes = VGroup(*[VGroup(Circle(radius=0.26, color=HEAD if k == 0 else DATA, stroke_width=2.5).set_fill(BG, 1)
                                .move_to([*P[k], 0]), mono(str(k), 18, WHITE).move_to([*P[k], 0])) for k in P])
        edges = VGroup(*[Arrow([*P[a], 0], [*P[b], 0], buff=0.28, stroke_width=2, color=GREY_B,
                               max_tip_length_to_length_ratio=0.15) for a, vs in adj.items() for b in vs])
        notes = VGroup(
            label(r"\textbf{generalized geography}: \ move the token along an arrow \\ to a vertex not yet visited; \ "
                  r"stuck loses", font_size=21, color=WHITE),
            label(rf"here: \ the player who puts the token on 0 \\ {'wins' if g['first_wins'] else 'loses'}, \ "
                  rf"found by searching {g['positions']} positions", font_size=21, color=YES),
            label(r"$\exists$ = my move, \ $\forall$ = every reply: \\ TQBF $\le_p$ geography, \ so it is "
                  r"PSPACE-complete \ (Schaefer, 1978)", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        fit_right(notes)
        with self.voiceover(
            "Quantifier alternation also describes games. <bookmark mark='a'/> Generalized geography moves a token along a directed edge to a vertex not visited before; a player unable to move loses. Here player one places the starting token, and player two moves next. <bookmark mark='b'/> The displayed winner and position count follow that initial-placer convention. A separate recursive set search checks the result. Our actual instrument memoizes positions and can use exponential storage. <bookmark mark='c'/> For the PSPACE membership proof, traverse possible plays depth first, keeping only the current path of at most the number of vertices. Generalized geography is PSPACE-complete under the standard rules. That theorem and the storage cost of our finite memoized implementation are distinct claims."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(nodes))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def games(self):
        head = label(r"Real games, \ generalized to $n \times n$ boards", font_size=32).to_edge(UP, buff=0.35)
        rows = [[r"Hex", r"PSPACE-complete", r"Reisch \ (1981)"],
                [r"Go \ (no ko fights)", r"PSPACE-hard", r"Lichtenstein and Sipser \ (1980)"],
                [r"Go \ (Japanese ko rule)", r"EXPTIME-complete", r"Robson \ (1983)"],
                [r"chess, \ checkers", r"EXPTIME-complete", r"Fraenkel and Lichtenstein \ (1981); \ Robson \ (1984)"],
                ['offline Tetris: clear target rows', r"NP-complete", r"chapter 7"]]
        tab = grid_table([r"game", 'decision objective / complexity', r"by"], rows, widths=[3.6, 3.0, 5.6], row_h=0.5, font_size=20,
                         mono_cols=(), colors=[[WHITE, LAM, GREY_A], [WHITE, LAM, GREY_A], [WHITE, NO, GREY_A],
                                               [WHITE, NO, GREY_A], [WHITE, HEAD, GREY_A]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('polynomial play length gives a PSPACE upper bound; exact game rules determine hardness results',
                  font_size=21, color=WHITE),
            label(r"EXPTIME-complete means \textbf{provably} not in P \ (chapter 2's hierarchy)", font_size=21,
                  color=NO),
            label(r"one of the few natural problems we \textbf{know} to be hard", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Generalized games require precise rules. <bookmark mark='a'/> Hex winner decision is PSPACE-complete. Results for Go depend on the ko and repetition rules, while suitable generalized chess and checkers rules yield EXPTIME-complete problems. These statements concern growing boards and formal move conventions. <bookmark mark='b'/> A polynomially bounded play length gives a depth-first polynomial-space upper bound when positions and legal moves are efficiently represented. Exponentially long play requires a separate configuration or game-graph analysis; length alone proves no completeness result. <bookmark mark='c'/> EXPTIME-complete problems are outside P by the time hierarchy. PSPACE versus P remains open. <bookmark mark='d'/> Offline Tetris concerns achieving a stated one-player objective with known pieces, rather than a two-player winner question. A fixed everyday board is a finite instance of a generalized family."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), run_time=3.0)
            for mk, n_ in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def logspace(self):
        head = label(r"And below P: \ logarithmic space", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"L: \ a read-only input and $O(\log n)$ bits of work space: \ a few counters and pointers",
                  font_size=22, color=WHITE),
            label(r"NL: \ the same, \ guessing: \ \textbf{directed reachability} is NL-complete", font_size=22,
                  color=DATA),
            label(r"Immerman \ (1988) \ and Szelepcs\'enyi \ (1987): \ NL = coNL, \ by \textbf{counting} the reachable "
                  r"vertices", font_size=22, color=YES),
            label(r"Reingold \ (2005): \ \textbf{undirected} reachability is in L", font_size=22, color=HEAD),
            label(r"L = P? \ \ NL = P? \ \ L = NL? \ \ All open", font_size=24, color=NO),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Space also matters at the bottom. <bookmark mark='a'/> Logarithmic space allows a read-only input and "
            "a handful of counters and pointers. <bookmark mark='b'/> Its nondeterministic version, NL, has a "
            "natural complete problem: is there a path from s to t in a directed graph? <bookmark mark='c'/> In 1987 "
            "and 1988 Róbert Szelepcsényi and Neil Immerman independently proved a surprise: NL is closed under "
            "complement. The trick is to count the reachable vertices, layer by layer, nondeterministically but "
            "verifiably. So for space, unlike what we expect for time, guessing a no is as easy as guessing a yes. "
            "<bookmark mark='d'/> In 2005 Omer Reingold showed that reachability in undirected graphs needs no "
            "guessing at all. <bookmark mark='e'/> Whether logarithmic space equals polynomial time is as open as "
            "P versus NP."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
