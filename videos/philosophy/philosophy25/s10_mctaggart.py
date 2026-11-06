from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class McTaggart(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"McTaggart's paradox", r"Is time unreal?", lit=(1908,), part=PART)
        with self.voiceover("Chapter nine. McTaggart's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.series()
        self.argument()
        self.regress()
        self.replies()

    def series(self):
        hc = history_card(1908, r"J. M. E. McTaggart", r"`The Unreality of Time', \ \textit{Mind}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        line = Arrow([-5.5, 0.2, 0], [5.5, 0.2, 0], buff=0, color=GREY_B, stroke_width=3)
        evs = [(-3.6, r"Caesar crosses the Rubicon"), (0.0, r"this sentence"), (3.6, r"the first Moon base")]
        dots = VGroup(*[Dot([x, 0.2, 0], radius=0.11, color=MATTER) for x, _ in evs])
        names = VGroup(*[label(t, font_size=18, color=MATTER).next_to(d, UP, buff=0.2) for d, (_, t) in
                         zip(dots, evs)])
        a_tags = VGroup(*[label(t, font_size=20, color=LIGHT).next_to(d, DOWN, buff=0.3) for d, t in
                          zip(dots, (r"past", r"present", r"future"))])
        b_arrows = VGroup(CurvedArrow([-3.5, 0.9, 0], [-0.1, 0.9, 0], angle=-0.6, color=TIME),
                          CurvedArrow([0.1, 0.9, 0], [3.5, 0.9, 0], angle=-0.6, color=TIME))
        b_tag = label(r"earlier than \qquad earlier than", font_size=18, color=TIME).move_to([0, 2.0, 0])
        rows = stack([(r"the A-series: \ past, \ present, \ future: \ these change", LIGHT),
                      (r"the B-series: \ earlier than, \ later than: \ these never change", TIME),
                      (r"McTaggart: \ without the A-series there is no change, \ so no time", ABS)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1908 the Cambridge idealist J. M. E. McTaggart published a paper called The Unreality of Time. "
            "<bookmark mark='a'/>Take three events in order. <bookmark mark='b'/>There are two ways to locate them in "
            "time. The A-series: one is past, one present, one future. These positions change: the first Moon base "
            "is future now, and will one day be past. <bookmark mark='c'/>The B-series: one is earlier than another. "
            "These relations never change: Caesar's crossing is always earlier than this sentence. "
            "<bookmark mark='d'/>McTaggart argued first that time needs the A-series. Change is an event's ceasing "
            "to be future and becoming present and then past; the B-series alone is a static order, like the order "
            "of the letters of the alphabet."
        ) as vo:
            self.play(FadeIn(hc), GrowArrow(line))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(a_tags), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(b_arrows), FadeIn(b_tag), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def argument(self):
        head = label(r"The argument", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ there is time only if there is an A-series", WHITE),
                       (r"2. \ past, \ present and future are incompatible properties", LIGHT),
                       (r"3. \ every event has all three: \ every event is past, \ present \textit{and} future", BAD),
                       (r"4. \ so the A-series is contradictory, \ and cannot be real", BAD),
                       (r"5. \ so time is unreal", ABS)], font_size=23, aligned_edge=LEFT, width=11.6,
                      buff=0.36).move_to([0, -0.2, 0])
        with self.voiceover(
            "Then came the paradox. <bookmark mark='a'/>First: there is time only if there is an A-series. "
            "<bookmark mark='b'/>Second: being past, being present and being future are incompatible; nothing can "
            "have two of them at once. <bookmark mark='c'/>Third: yet every event has all three. Caesar's crossing "
            "is past, but it was present, and it was future. <bookmark mark='d'/>So the A-series is contradictory "
            "and cannot be real. <bookmark mark='e'/>And so, McTaggart concluded, time is unreal."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def regress(self):
        head = label(r"The regress", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = lambda s, c=WHITE: label(s, font_size=20, color=c)  # noqa: E731
        hd = [T(r"level", CONN), T(r"the reply", CONN), T(r"McTaggart's rejoinder", CONN)]
        rows = [[MathTex(r"1", font_size=24), T(r"not all at once: \ it \textit{is} past, \ \textit{was} present, "
                                                 r"\ \textit{was} future"),
                 T(r"`was present' means present at a past moment: \ A-terms again", BAD)],
                [MathTex(r"2", font_size=24), T(r"the past moment \textit{is} past, \ \textit{was} present \dots"),
                 T(r"the same problem, \ one level up", BAD)],
                [MathTex(r"\vdots", font_size=24), T(r"\dots"), T(r"a vicious regress: \ never discharged", BAD)]]
        grid = ValueGrid(hd, rows, col_w=[1.2, 5.8, 5.6], cell_h=0.72, font_size=20).move_to([0, 0.5, 0])
        foot = label(r"tensed language explains tense by tense: \ McTaggart says it never escapes the circle",
                     font_size=21, color=GOAL).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "The obvious reply is that no event has the three properties at once. <bookmark mark='a'/>Caesar's "
            "crossing is past, was present, and was future earlier still. McTaggart's rejoinder: was present means "
            "present at some past moment, which uses the A-series again. <bookmark mark='b'/>And that past moment "
            "is itself past, was present, was future, which raises the same problem one level up. "
            "<bookmark mark='c'/>Each attempt to remove the contradiction uses the very A-properties it is meant to "
            "explain, so the regress never ends. Whether the regress is really vicious is still debated; but the "
            "argument forced philosophers to say what tense is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            self.play(FadeIn(foot))
        self.clear_scene()

    def replies(self):
        head = label(r"Two ways out", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the A-theorist", r"tense is basic and real; \ the regress is benign: \ `is past' is just true, \ "
                                r"simply, \ now \ (Prior)", LIGHT),
            (r"the B-theorist", r"deny premise 1: \ time is the B-series; \ `now' is like `here', \ an indexical \ "
                                r"(Russell, \ Mellor, \ Smart)", TIME),
            (r"change, \ for the B-theorist", r"the poker is hot at one time and cold at another: \ that is all "
                                              r"change is", MATTER),
            (r"what each must explain", r"A: \ how relativity's frames fit a single now; \ B: \ why the present "
                                        r"seems to move", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4, x_text=-2.2, label_size=21, text_size=21)
        with self.voiceover(
            "There are two ways out, and they define the modern debate. <bookmark mark='a'/>The A-theorist, like "
            "Arthur Prior, takes tense as basic and real. There is no regress: is past is simply true, now, and "
            "needs no further analysis. <bookmark mark='b'/>The B-theorist denies McTaggart's first premise. Time is "
            "the B-series; the word now is like the word here, an indexical that picks out the moment of speaking, "
            "as Russell, Hugh Mellor and J. J. C. Smart held. <bookmark mark='c'/>Change, for the B-theorist, is "
            "just a thing being one way at one time and another way at another: the poker is hot at noon and cold at "
            "midnight. <bookmark mark='d'/>Each side owes something. The A-theorist owes an account of how a single "
            "real present fits relativity's many frames. The B-theorist owes an account of why the present seems to "
            "move."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
