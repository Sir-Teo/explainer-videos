from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Hard(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The hard problem", r"Why is there something it is like at all?", lit=(1995,),
                            part=PART)
        with self.voiceover("Chapter two. The hard problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.easy()
        self.hard()
        self.wall_brick()
        self.map()

    def easy(self):
        hc = history_card(1995, r"David Chalmers", r"`Facing Up to the Problem of Consciousness'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        items = [r"discriminating, \ categorizing and reacting to stimuli", r"integrating information",
                 r"reporting mental states", r"accessing one's own internal states", r"focusing attention",
                 r"deliberately controlling behaviour", r"the difference between waking and sleep"]
        col = VGroup(*[VGroup(MathTex(r"\checkmark", font_size=28, color=FUNC), label(s, font_size=24, color=WHITE)
                              ).arrange(RIGHT, buff=0.3) for s in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.3).move_to([0.4, -0.9, 0])
        tag = label(r"the `easy' problems: \ explain a function, \ find the mechanism", font_size=21,
                    color=FUNC).next_to(col, UP, buff=0.35)
        with self.voiceover(
            "In 1995 David Chalmers sorted the problems of consciousness into two piles. "
            "<bookmark mark='a'/>The easy problems are to explain how a system discriminates and reacts to stimuli, "
            "integrates information, reports its states, accesses its own internal states, focuses attention, "
            "controls behaviour deliberately, and differs awake from asleep. <bookmark mark='b'/>They are not easy "
            "in practice; they are the work of a century of neuroscience. They are easy in principle, because each "
            "is the explanation of a function: find the mechanism that performs it, and the problem is solved."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in col], lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(Indicate(tag, color=FUNC, scale_factor=1.04))
        self.clear_scene()

    def hard(self):
        q = quote_card(r"The really hard problem of consciousness is the problem of \textit{experience}. \dots\ "
                       r"Why is it that when our cognitive systems engage in visual and auditory "
                       r"information-processing, \ we have visual or auditory experience?", r"David Chalmers",
                       r"`Facing Up to the Problem of Consciousness' \ (1995)", width=10.0,
                       font_size=26).to_edge(UP, buff=0.5)
        rows = stack([(r"explain every function \dots", FUNC),
                      (r"\dots and a further question seems to remain: \ why is all this accompanied by experience?",
                       FEEL),
                      (r"not a function, \ so not answered by finding what performs one", GOAL)], font_size=22,
                     buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "And then there is the hard problem. <bookmark mark='a'/>The really hard problem of consciousness, "
            "Chalmers wrote, is the problem of experience. Why is it that when our cognitive systems engage in "
            "visual and auditory information processing, we have visual or auditory experience? "
            "<bookmark mark='b'/>Suppose every easy problem were solved, every function explained. "
            "<bookmark mark='c'/>A further question seems to remain: why is all that processing accompanied by "
            "experience, rather than going on in the dark? <bookmark mark='d'/>Experience is not obviously a "
            "function, so it is not obviously answered by finding the mechanism that performs one. Whether that "
            "appearance is to be trusted is what the next chapters argue about."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=31, current=31).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(31, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty first brick in the Wall. <bookmark mark='a'/>The dream was that consciousness, like "
            "everything else, would be entailed by the physical truths: given all of physics, the facts about "
            "experience would follow, as the facts about water follow from chemistry. The hard problem and the "
            "explanatory gap say that the entailment seems to fail. <bookmark mark='b'/>What it forces is a choice: "
            "new fundamental properties, new kinds of concept that hide an entailment we cannot see, or the "
            "conclusion that the felt quality we think needs explaining is an illusion."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[31], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def map(self):
        head = label(r"A map of the responses \ (Chalmers, \ 2003)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{type}", r"\text{the hard problem is \dots}", r"\text{held by}"]
        rows = [(r"A", r"a confusion: \ explain the functions and nothing is left", r"Dennett; \ Frankish", FUNC),
                (r"B", r"real, \ but experience is physical, \ by an identity we know only a posteriori",
                 r"Loar; \ Papineau; \ Block", PHYS),
                (r"C", r"real, \ and physics will one day close the gap", r"Nagel \ (in 1974); \ Churchland", PHYS),
                (r"D", r"real: \ experience is non-physical and acts on the physical", r"Descartes; \ Popper", FEEL),
                (r"E", r"real: \ experience is non-physical and does nothing", r"Huxley; \ Jackson \ (in 1982)", FEEL),
                (r"F", r"real: \ experience is the intrinsic nature that physics leaves out", r"Russell; \ Goff",
                 SIG)]
        cells = [[label(a, font_size=22, color=c), label(b, font_size=17, color=WHITE), label(w, font_size=17,
                                                                                               color=GREY_A)]
                 for a, b, w, c in rows]
        grid = ValueGrid(hd, cells, col_w=[1.2, 8.0, 3.6], cell_h=0.6, font_size=19).move_to([0, -0.5, 0])
        with self.voiceover(
            "Chalmers later mapped the responses, by letter. <bookmark mark='a'/>Type A: there is no hard problem; "
            "explain the functions and nothing is left over. Daniel Dennett and Keith Frankish. "
            "<bookmark mark='b'/>Type B: the problem is real, but experience is physical all the same, by an "
            "identity we can know only a posteriori, like water and H two O. <bookmark mark='c'/>Type C: there is a "
            "gap now, and some future physics will close it. <bookmark mark='d'/>Type D: experience is non-physical "
            "and acts on the physical: interactionist dualism. <bookmark mark='e'/>Type E: it is non-physical and "
            "does nothing: epiphenomenalism. <bookmark mark='f'/>And type F: experience is the intrinsic nature of "
            "matter, which physics describes only from outside, Russell's view, which chapter seven takes up. The "
            "next three chapters give the arguments that sort people into these rows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcdef", range(6)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
        self.clear_scene()
