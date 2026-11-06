from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Antinomies(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Reason against itself", r"What happens when reason goes beyond experience?",
                            lit=(1781,), part=PART)
        with self.voiceover("Chapter twelve. Reason against itself."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.race()
        self.four()
        self.brick()

    def race(self):
        head = label(r"The first antinomy: \ two proofs, \ side by side", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        th = [r"\textbf{Thesis:} \ the world has a beginning in time",
              r"suppose it has none:",
              r"then an infinite series of states has elapsed \ up to now",
              r"but an infinite series can never be completed",
              r"so the world had a beginning"]
        an = [r"\textbf{Antithesis:} \ the world has no beginning",
              r"suppose it has one:",
              r"then before it there was empty time",
              (r"but nothing can come to be in empty time:", r"\quad no moment differs from another"),
              r"so the world has no beginning"]
        def item(t, color):
            if isinstance(t, tuple):
                return VGroup(*[label(x, font_size=22, color=color) for x in t]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
            return label(t, font_size=22, color=color)
        left = VGroup(*[item(t, REASON if i in (0, 4) else WHITE) for i, t in enumerate(th)])
        right = VGroup(*[item(t, SENSE if i in (0, 4) else WHITE) for i, t in enumerate(an)])
        for col in (left, right):
            for m in col:
                if m.width > 6.2:
                    m.width = 6.2
            col.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        left.move_to([-3.45, 0.2, 0])
        right.move_to([3.45, 0.2, 0])
        div = DashedLine([0, 2.6, 0], [0, -2.2, 0], color=GREY_D)
        bad = label(r"two valid-looking proofs \ of contradictory conclusions", font_size=26, color=BAD).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "And when reason goes beyond any possible experience? Kant answered with four antinomies, pairs of "
            "arguments that prove opposite conclusions. Here is the first, as two proofs racing side by side. "
            "<bookmark mark='a'/>The thesis: the world has a beginning in time. Suppose it had none. Then up to now an "
            "infinite series of states has elapsed. But an infinite series can never be completed by successive "
            "steps. So the world had a beginning. <bookmark mark='b'/>The antithesis: the world has no beginning. "
            "Suppose it had one. Then before it there was empty time. But in empty time nothing can come to be, since "
            "no moment of it differs from any other, and so none could be the moment of creation. So the world has no "
            "beginning. <bookmark mark='c'/>Both proofs look valid. Both reason by reductio from the other's "
            "conclusion. And they contradict each other."
        ) as vo:
            self.play(FadeIn(head), Create(div))
            vo.wait_until("a")
            for i in range(5):
                self.play(FadeIn(left[i], shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("b")
            for i in range(5):
                self.play(FadeIn(right[i], shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(bad), Indicate(left[4], color=BAD), Indicate(right[4], color=BAD))
        self.clear_scene()

    def four(self):
        head = label(r"The four antinomies, \ and Kant's diagnosis", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [label(r"", font_size=22), label(r"thesis", font_size=22, color=REASON),
              label(r"antithesis", font_size=22, color=SENSE)]
        rows = [[label(r"1", font_size=22), label(r"a beginning in time, \ a limit in space", font_size=20),
                 label(r"no beginning, \ no limit", font_size=20)],
                [label(r"2", font_size=22), label(r"everything is made of simple parts", font_size=20),
                 label(r"nothing is simple", font_size=20)],
                [label(r"3", font_size=22), label(r"there is freedom", font_size=20),
                 label(r"everything follows natural law", font_size=20)],
                [label(r"4", font_size=22), label(r"a necessary being exists", font_size=20),
                 label(r"nothing is necessary", font_size=20)]]
        grid = ValueGrid(hd, rows, col_w=[0.8, 5.4, 4.6], cell_h=0.55, font_size=22).move_to([0, 0.9, 0])
        diag = VGroup(label(r"both sides assume the world is a completed whole, \ given in itself", font_size=24,
                            color=GOAL),
                      label(r"but the world is never given whole, \ only experienced, \ step by step", font_size=24,
                            color=KANT),
                      label(r"1 and 2: \ both false; \ 3 and 4: \ both may be true, \ of different aspects", font_size=22,
                            color=GREY_A)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There are four antinomies. <bookmark mark='a'/>A beginning in time and a limit in space, or neither. "
            "Simple parts, or nothing simple. Freedom, or natural law throughout. A necessary being, or nothing "
            "necessary. <bookmark mark='b'/>Kant's diagnosis is that both sides make the same mistake: they treat the "
            "world as a completed whole, given in itself, about which there must be a fact of the matter. "
            "<bookmark mark='c'/>But the world is never given to us whole. It is only ever experienced, step by "
            "step, and the series of experiences is never complete. <bookmark mark='d'/>So in the first two "
            "antinomies both sides are false; in the last two, both may be true, of different aspects of things: "
            "nature as it appears, and things as they are in themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.6), run_time=5)
            for mk, r in zip("bcd", diag):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brick(self):
        w = wall(upto=10, current=10).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(10, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "This is the tenth brick in the Wall, and it has two halves. <bookmark mark='a'/>The dream: necessary "
            "knowledge of the world from experience. The wall: Hume's problem, that experience never shows necessity, "
            "and Kant's antinomies, that reason left to itself proves contradictions. What it forces: either the "
            "mind's own contribution to experience, as Kant proposed, or skepticism."
        ) as vo:
            self.play(FadeIn(w))
            self.play(Indicate(w.brick[10], color=P.CONCL, scale_factor=1.08))
            vo.wait_until("a")
            self.play(FadeIn(wc))
        self.wait(1)
        self.clear_scene()
