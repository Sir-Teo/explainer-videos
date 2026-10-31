from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MAXC, PART, PATH, SYMBOL, load, node_box


def era_axis(y0=1948, y1=2000, width=12.4, y=0.0):
    """A plain year axis for the era (not the series' strip): returns (group, x-of-year function)."""
    x0 = -width / 2

    def X(yr):
        return x0 + width * (yr - y0) / (y1 - y0)

    g = VGroup(Line([X(y0), y, 0], [X(y1), y, 0], color=GREY_C, stroke_width=2))
    for yr in range(1950, y1 + 1, 10):
        g.add(Line([X(yr), y - 0.07, 0], [X(yr), y + 0.07, 0], color=GREY_C, stroke_width=2))
        year = Text(str(yr), font_size=18, color=GREY_B).next_to([X(yr), y, 0], DOWN, buff=0.15)
        # Event stems pass behind the tick labels without moving dates or events.
        year.add_background_rectangle(color=BACKGROUND, opacity=1.0, buff=0.035)
        year.set_z_index(2)
        year.background_rectangle.set_z_index(1)
        g.add(year)
    return g, X


class Hook(VoiceoverScene):
    def construct(self):
        self.prediction()
        self.era()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def prediction(self):
        quote = label(r"``That within ten years a digital computer will be the world's chess champion, \\ unless the "
                      r"rules bar it from competition.''", font_size=32).move_to(UP * 2.0)
        who = note(r"Herbert Simon \& Allen Newell, \textit{Heuristic Problem Solving: The Next Advance in "
                   r"Operations Research} (1958)", font_size=22).next_to(quote, DOWN, buff=0.3)
        y58 = label(r"$1958$", font_size=64, color=HIST).move_to([-3.6, -1.3, 0])
        y97 = label(r"$1997$", font_size=64, color=MAXC).move_to([3.6, -1.3, 0])
        arrow = Arrow(y58.get_right(), y97.get_left(), buff=0.4, color=GREY_B, stroke_width=4)
        gap = label(r"$39$ years", font_size=34, color=GREY_A).next_to(arrow, UP, buff=0.12)
        db = label(r"Deep Blue beats Garry Kasparov, \ $3\tfrac12$--$2\tfrac12$", font_size=26, color=MAXC)
        db.next_to(y97, DOWN, buff=0.3)
        db.set_x(min(db.get_x(), 6.9 - db.width / 2))
        p58 = label(r"the prediction", font_size=26, color=HIST).next_to(y58, DOWN, buff=0.3)
        with self.voiceover(
            "In 1958 Herbert Simon and Allen Newell predicted that within ten years a digital computer would be the world's "
            "chess champion, unless the rules barred it from competition. <bookmark mark='a'/> It took thirty-nine. "
            "<bookmark mark='b'/> In May 1997, in New York, IBM's Deep Blue beat the world champion, Garry Kasparov, three and a "
            "half games to two and a half."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(who))
            self.play(FadeIn(y58), FadeIn(p58))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(gap), FadeIn(y97))
            vo.wait_until("b")
            self.play(FadeIn(db, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        axis, X = era_axis(y=-0.4)
        events = [  # (year, text, colour, above?, level): short labels, staggered on two levels per side
            (1950, r"Turing's question", HIST, True, 1),
            (1956, r"Dartmouth", HIST, False, 1),
            (1959, r"Samuel's checkers", LEARN, True, 2),
            (1966, r"ELIZA", SYMBOL, False, 2),
            (1968, r"A* search", GCOST, True, 1),
            (1971, r"STRIPS", PATH, False, 1),
            (1973, r"Lighthill report", FAIL, True, 2),
            (1980, r"expert systems", HEUR, False, 2),
            (1987, r"Lisp machines collapse", FAIL, True, 1),
            (1997, r"Deep Blue", MAXC, False, 1),
        ]
        dots, labs = VGroup(), VGroup()
        for yr, txt, col, up, lev in events:
            d = Dot([X(yr), -0.4, 0], radius=0.08, color=col)
            t = label(rf"${yr}$ \ " + txt, font_size=20, color=col)
            off = 0.5 if lev == 1 else 1.15
            t.move_to([X(yr), -0.4 + (off if up else -off), 0])
            t.set_x(min(max(t.get_x(), -6.9 + t.width / 2), 6.9 - t.width / 2))
            end = [X(yr), (t.get_bottom() if up else t.get_top())[1], 0]
            stem = Line(d.get_center(), end, color=col, stroke_width=1.5, stroke_opacity=0.6)
            dots.add(VGroup(stem, d))
            labs.add(t)
        winters = VGroup()
        for a, b, txt in ((1974, 1980, r"first winter"), (1987, 1993, r"second winter")):
            band = Rectangle(width=X(b) - X(a), height=4.6, stroke_width=0, fill_color="#5A7BA8", fill_opacity=0.16)
            band.move_to([(X(a) + X(b)) / 2, -0.4, 0])
            winters.add(VGroup(band, label(txt, font_size=20, color="#9DB8E0").next_to(band, UP, buff=0.08)))
        winters.set_z_index(-1)
        head = label(r"The first age of AI, \ $1950$--$1997$", font_size=36).to_edge(UP, buff=0.35)
        tag = note(r"winters approximate, as usually dated").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Between those dates lies the first age of artificial intelligence, where this course's history begins. "
            "<bookmark mark='a'/> In 1950 Alan Turing asked whether machines could think. <bookmark mark='b'/> In 1956 a "
            "workshop at Dartmouth named the field. <bookmark mark='c'/> Programs learned checkers, held conversations, "
            "searched maps and planned a robot's moves. <bookmark mark='d'/> Then the promises outran the results, and the "
            "money dried up: a first winter. <bookmark mark='e'/> A boom in expert systems, and a second, harder winter when it "
            "collapsed. <bookmark mark='f'/> And at the end, a chess machine the founders would have recognized."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            for mk, idx in zip("abc", ((0,), (1,), (2, 3, 4, 5))):
                vo.wait_until(mk)
                self.play(*[AnimationGroup(FadeIn(dots[i]), FadeIn(labs[i], shift=UP * 0.1)) for i in idx],
                          run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(winters[0]), FadeIn(dots[6]), FadeIn(labs[6]), FadeIn(tag))
            vo.wait_until("e")
            self.play(FadeIn(dots[7]), FadeIn(labs[7]))
            self.play(FadeIn(winters[1]), FadeIn(dots[8]), FadeIn(labs[8]))
            vo.wait_until("f")
            # Indicate must begin after FadeIn has made this label visible.
            # Keep both actions inside the original one-second reveal window.
            self.play(FadeIn(dots[9]), Succession(FadeIn(labs[9], run_time=0.5),
                                                 Indicate(labs[9], color=MAXC, run_time=0.5)),
                      run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"Can intelligence be written down: \\ as search, \ as logic, \ as rules?", font_size=42)
        q.move_to(UP * 1.6)
        ideas = [(r"search", GCOST), (r"heuristics", HEUR), (r"game trees", MAXC), (r"logic", SYMBOL),
                 (r"satisfiability", PATH), (r"plans", FCOL), (r"knowledge", HIST)]
        row = VGroup(*[node_box(t, c, font_size=26) for t, c in ideas]).arrange(RIGHT, buff=0.22)
        if row.width > 13.2:
            row.width = 13.2
        row.move_to(DOWN * 0.4)
        today = VGroup(label(r"still inside today's systems:", font_size=26, color=GREY_A),
                       label(r"AlphaZero's search, \ chip verification, \ Lean and AlphaProof, \ agents that plan",
                             font_size=26, color=FCOL)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        tag = note(r"computed: \ every search, solver and learner in this part runs on this computer")
        tag.to_corner(DR, buff=0.2)
        with self.voiceover(
            "The bet of that age was that intelligence could be written down: <bookmark mark='a'/> as search through "
            "possibilities, guided by rules of thumb; as moves in a game; as logic; as knowledge typed in by experts. "
            "<bookmark mark='b'/> The bet was only half lost. Search runs inside AlphaZero, logic inside the tools that check "
            "computer chips, a proof checker grades DeepMind's AlphaProof, and today's agents make plans. "
            "<bookmark mark='c'/> And every algorithm in this part runs here, on this computer, so we can watch it work."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in row], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(today, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Thinking Machines", font_size=46).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.9).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"what a machine can compute; \ Turing's test; \ Dartmouth and the Logic Theorist",
            r"search: \ breadth-first, \ Dijkstra, \ A*, \ and where heuristics come from",
            r"local search: \ hill climbing, \ simulated annealing, \ genetic algorithms",
            r"games: \ minimax, \ alpha--beta, \ Samuel's checkers, \ Deep Blue",
            r"logic: \ resolution, \ SAT and its phase transition, \ constraints, \ planning",
            r"knowledge: \ expert systems, \ ELIZA, \ the winters, \ and what survives",
        ], font_size=26).move_to(DOWN * 0.3)
        with self.voiceover(
            "This is Part 2 of AI, Built. <bookmark mark='a'/> In this part: what machines can and cannot compute, and "
            "Turing's test; search, from breadth-first to A star, and where heuristics come from; local search and simulated "
            "annealing; games, from minimax and alpha-beta to Samuel's checkers and Deep Blue; logic, satisfiability and its "
            "phase transition, constraints and planning; and knowledge: expert systems, ELIZA, the two winters, and what "
            "survived them."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
