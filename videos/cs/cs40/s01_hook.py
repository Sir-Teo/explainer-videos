from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, load)

PKC = [DATA, LAM, YES, HEAD, KERN, NO, GREY_B]


class Hook(VoiceoverScene):
    def construct(self):
        self.crisis()
        self.repo()
        self.plan()

    def crisis(self):
        head = label(r"Garmisch, \ October 1968", font_size=38).to_edge(UP, buff=0.35)
        lines = VGroup(
            wrapped_label(r"a NATO conference with a deliberately provocative title: \ \textbf{Software Engineering}",
                          12.4, font_size=25, color=WHITE),
            wrapped_label(r"the ``software crisis'': \ systems delivered late, \ over budget, \ unreliable, \ and "
                          r"hard to change \ (Naur and Randell, \ eds., 1969)", 12.4, font_size=25, color=NO),
            wrapped_label(r"IBM's OS/360: \ more than a thousand people at its peak; \ its manager, \ Fred Brooks, \ "
                          r"wrote \textit{The Mythical Man-Month} \ (1975) \ about what went wrong", 12.4,
                          font_size=25, color=HEAD),
            wrapped_label(r"\textbf{Brooks' law}: \ adding manpower to a late software project makes it later", 12.4,
                          font_size=27, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "In October 1968, about fifty people met in the Bavarian town of Garmisch for a NATO conference with a "
            "deliberately provocative title. <bookmark mark='a'/> Software Engineering. Building bridges was "
            "engineering; writing programs, so far, was not. <bookmark mark='b'/> The participants spoke of a "
            "software crisis: large systems arriving years late, far over budget, unreliable, and almost impossible "
            "to change. <bookmark mark='c'/> The most famous example was IBM's operating system for the "
            "System/360, which at its peak occupied more than a thousand people. Fred Brooks, who managed it, wrote "
            "a book about what went wrong, The Mythical Man-Month. <bookmark mark='d'/> Its best-known sentence is "
            "Brooks' law: adding manpower to a late software project makes it later. We will test that, and much "
            "else, with simulations and with data."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def repo(self):
        r = load("repo")
        hist = load("history")
        head = label(r"The software you are watching", font_size=36).to_edge(UP, buff=0.3)
        pk = list(r["by_package"].items())
        groups = []
        for name, d in pk[:6]:
            groups.append((name, d["modules"]))
        other = sum(d["modules"] for _, d in pk[6:])
        if other:
            groups.append(("other", other))
        total = sum(n for _, n in groups)
        cols, step = 110, 0.114
        squares = VGroup()
        k = 0
        for gi, (name, n) in enumerate(groups):
            for _ in range(n):
                x, y = k % cols, k // cols
                squares.add(Square(step * 0.8, stroke_width=0, fill_color=PKC[gi % len(PKC)],
                                   fill_opacity=0.85).move_to([-6.2 + x * step, 2.85 - y * step, 0]))
                k += 1
        keys = VGroup(*[label(rf"\texttt{{{name.replace('_', chr(92) + '_')}}}: \ {n:,}", font_size=18,
                              color=PKC[i % len(PKC)]) for i, (name, n) in enumerate(groups)]).arrange_in_grid(
            rows=2, buff=(0.6, 0.18), col_alignments="l" * 4)
        keys.next_to(squares, DOWN, buff=0.4).set_x(0)
        stats = VGroup(
            label(rf"{total:,} Python modules, \ {r['lines']:,} lines", font_size=22, color=WHITE),
            label(rf"{r['n_edges']:,} imports between them", font_size=22, color=GREY_A),
            label(rf"{len(r['cycles'])} import cycles, \ {r['upward']} imports that break the layering", font_size=22,
                  color=NO),
            label(rf"{hist['commits']} commits between {hist['first']} and {hist['last']}", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18)
        stats.next_to(keys, DOWN, buff=0.5).set_x(0)
        with self.voiceover(
            "This part is about software as something large and long-lived, built and changed by many hands. So "
            "the first specimen is the software that made this series. <bookmark mark='a'/> Each square is one "
            "Python module of this repository, coloured by where it lives: the shared library, the scenes of each "
            "series, the tools and the tests. <bookmark mark='b'/> About two and a half thousand modules and six "
            "hundred thousand lines, joined by five and a half thousand imports. <bookmark mark='c'/> We will "
            "measure it like any other system: its dependencies, its cycles, the places where its own rules are "
            "broken. There are five import cycles, and two imports that run the wrong way between its layers. "
            "<bookmark mark='d'/> And it has a history: about a hundred and sixty commits in its first five days, every one of "
            "them recorded, which we will mine for a kind of coupling no import statement shows. It is not a large "
            "system by industrial standards, but it is large enough to show every problem in this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in squares], lag_ratio=0.0008), run_time=3)
            self.play(FadeIn(keys))
            vo.wait_until("b")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(stats[2]))
            vo.wait_until("d")
            self.play(FadeIn(stats[3]))
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Software Engineering", font_size=38).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"complexity, \ and Parnas' rule: \ one module per design decision",
            r"abstraction, \ contracts and behavioural subtyping",
            r"coupling, \ measured on this repository",
            r"design: \ SOLID, \ patterns, \ the expression problem",
            r"testing: \ flakiness, \ coverage and mutation",
            r"change, \ review, \ process; \ Conway, \ Brooks and estimates",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 40 of Computer Science, Built, and the start of Act Eight, Building Software. "
            "<bookmark mark='a'/> We begin where the discipline began, with complexity, and with David Parnas' rule "
            "for dividing a program into modules, tested by building one program both ways. Then abstraction and "
            "contracts; coupling, measured on this repository; the design principles and patterns of industry; "
            "testing, and how to tell whether tests are any good; and the human side: review, process, teams, and "
            "the estimates that are always wrong in the same direction."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN,)
