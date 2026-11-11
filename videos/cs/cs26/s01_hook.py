from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono, sci, words)

COLS = [DATA, HEAD, YES]


def graph60(h, r=2.6, center=ORIGIN, coloured=False):
    n = h["n"]
    pos = [center + r * np.array([np.cos(2 * PI * i / n), np.sin(2 * PI * i / n), 0]) for i in range(n)]
    edges = VGroup(*[Line(pos[u], pos[v], stroke_width=0.8, color=GREY_C, stroke_opacity=0.6)
                     for u, v in h["edge_list"]])
    dots_ = VGroup(*[Dot(pos[i], radius=0.07, color=COLS[h["colouring"][i]] if coloured else GREY_B)
                     for i in range(n)])
    return VGroup(edges, dots_)


class Hook(VoiceoverScene):
    def construct(self):
        self.letter()
        self.colouring()
        self.plan()

    def letter(self):
        head = label(r"Princeton, \ 20 March 1956", font_size=34).to_edge(UP, buff=0.4)
        quote = VGroup(
            label(r"``One can obviously easily construct a Turing machine which, \ for every formula $F$ in first "
                  r"order", font_size=23, color=WHITE),
            label(r"predicate logic and every natural number $n$, \ allows one to decide if there is a proof of $F$ "
                  r"of", font_size=23, color=WHITE),
            label(r"length $n$. \ \ldots \ The question is how fast $\varphi(n)$ grows for an optimal machine.''",
                  font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.6)
        sig = label(r"--- Kurt G\"odel, \ letter to John von Neumann \ (translated from German)", font_size=20,
                    color=GREY_A).next_to(quote, DOWN, buff=0.3).align_to(quote, RIGHT)
        then = VGroup(
            label(r"if $\varphi(n) \sim n$ or $n^2$: \ ``the mental work of a mathematician concerning yes-or-no "
                  r"questions \\ could be completely replaced by a machine''", font_size=22, color=HEAD),
            label(r"von Neumann was dying of cancer, \ and never replied", font_size=21, color=GREY_A),
            label(r"the letter was found in the 1980s: \ the P versus NP question, \ fifteen years early",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.28).next_to(sig, DOWN, buff=0.6)
        with self.voiceover(
            "In March 1956 Kurt Gödel wrote a letter to John von Neumann. <bookmark mark='a'/> A machine can "
            "obviously decide, for any formula and any number n, whether the formula has a proof of length n: "
            "just try them all. The question, Gödel wrote, is how fast the number of steps grows for the best "
            "possible machine. <bookmark mark='b'/> If it grew only like n, or n squared, then the mental work of a "
            "mathematician on yes-or-no questions could be completely replaced by a machine. <bookmark mark='c'/> "
            "Von Neumann was dying of cancer and never answered. <bookmark mark='d'/> The letter was found decades "
            "later. It asks, fifteen years before anyone else, the question of this part: is finding a proof as "
            "easy as checking one?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q) for q in quote], lag_ratio=0.4), FadeIn(sig), run_time=3.0)
            for mk, t in zip("bcd", then):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def colouring(self):
        h = load("hook")
        head = label(r"Finding against checking", font_size=34).to_edge(UP, buff=0.3)
        g0 = graph60(h, center=LEFT * 3.6 + DOWN * 0.4)
        g1 = graph60(h, center=LEFT * 3.6 + DOWN * 0.4, coloured=True)
        notes = VGroup(
            label(rf"{h['n']} vertices, \ {h['edges']} edges: \\ colour them with 3 colours, \\ no edge joining two "
                  r"of the same colour", font_size=22, color=WHITE),
            label(rf"\textbf{{checking}} a colouring: \\ look at {h['edges']} edges: \ "
                  rf"{h['check_s'] * 1e6:.1f} $\mu$s", font_size=22, color=YES),
            label(rf"enumeration scenario: $3^{{{h['n']}}}$ full checks \\ $\approx {sci(h['brute_years'])}$ years; \\ not a measured search or lower bound", font_size=22, color=NO),
            label(rf"this planted instance: {h['find_s']*1000:.1f} ms; \\ polynomial time for every graph remains open", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        fit_right(notes)
        with self.voiceover(
            "Here is the question in modern form. <bookmark mark='a'/> This planted three-colourable graph has sixty vertices and a hundred and twelve edges. Find a colouring with different colours at adjacent vertices. <bookmark mark='b'/> Checking a supplied valid colouring examines every edge. We measure that check repeatedly on this host. <bookmark mark='c'/> Multiplying its average duration by three to the sixtieth gives an exhaustive-enumeration scenario. It is neither a measured search nor a lower bound: a search can stop early and reject invalid candidates faster. <bookmark mark='d'/> Our clause-learning solver finds a colouring quickly for this instance, and every edge is checked. Whether every graph admits a polynomial-time decision algorithm remains open. This finite success does not answer P versus NP."
        ) as vo:
            self.play(FadeIn(head), Create(g0[0]), FadeIn(g0[1]), run_time=2.0)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Transform(g0[1], g1[1]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ P versus NP", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            'polynomial time; \\ hierarchy and Savitch proof ideas, with model assumptions',
            r"NP, \ reductions, \ and Cook--Levin's tableau, \ built and solved",
            r"the reduction web, \ computed: \ independent set, \ 3-colouring, \ subset sum",
            r"coNP, \ the polynomial hierarchy, \ PSPACE and games; \ time in square-root space",
            r"SAT solvers in practice, \ and the 3-SAT phase transition",
            r"why the question is hard, \ five possible worlds, \ and the frontier",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 26 of Computer Science, Built: P versus NP. <bookmark mark='a'/> In this part: what counts as "
            "efficient, and the theorems that separate time and space classes; NP, reductions, and the Cook-Levin "
            "theorem, built as a formula and solved; the web of reductions that ties a thousand problems together, "
            "each one computed; coNP, the polynomial hierarchy, games and space, and a 2025 surprise about time and "
            "space; SAT solvers in practice; why the question has resisted fifty years of attack; and the five "
            "worlds we might be living in."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
