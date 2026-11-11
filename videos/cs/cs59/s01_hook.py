from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

PALETTE = [YES, DATA, HEAD, NO, LAM, KERN]


class Hook(VoiceoverScene):
    def construct(self):
        self.ring()
        self.questions()
        self.plan()

    def ring(self):
        c = load("cv")
        head = label(r"A million processes, \ seven rounds", font_size=36).to_edge(UP, buff=0.3)
        n = len(c["trace"][0])
        dots = VGroup()
        for i in range(n):
            d = Circle(radius=0.2, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.14).next_to(head, DOWN, buff=1.2)
        arrows = VGroup(*[Line(dots[i].get_right(), dots[i + 1].get_left(), stroke_width=1.5, color=GREY_C) for i in range(n - 1)])
        cap = label(rf"{n} neighbours on a ring of {c['n']:,}; \ each knows only its own id and its successor's",
                    font_size=19, color=GREY_A).next_to(dots, DOWN, buff=0.35)

        def labels(vals, small):
            g = VGroup()
            for d, v in zip(dots, vals):
                t = label(str(v), font_size=16 if not small else 20,
                          color=WHITE if not small else PALETTE[v % 6] if v < 6 else WHITE)
                if t.width > 0.34:
                    t.width = 0.34
                g.add(t.move_to(d))
            return g

        cur = labels(c["trace"][0], False)
        counter = label(rf"round 0: \ {c['colours'][0]:,} colours", font_size=24, color=HEAD).next_to(cap, DOWN,
                                                                                                    buff=0.5)
        foot = wrapped_label(r"Cole and Vishkin \ (1986): \ compare your colour with your successor's, \ keep the "
                             r"position of the first differing bit and its value; \ colours shrink from $b$ bits to "
                             r"about $\log b$ each round", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A million processes stand in a ring, each knowing only its own identifier and its successor's. They "
            "must colour themselves with three colours so that no two neighbours match. <bookmark mark='a'/> At the "
            "start every identifier is its own colour: a million colours. <bookmark mark='b'/> In each round, every "
            "process compares its colour with its successor's, finds the first bit where they differ, and takes as "
            "its new colour that bit's position and value. Neighbours still differ, and a colour of b bits shrinks "
            "to about log b bits. <bookmark mark='c'/> A million colours become thirty-eight, then twelve, then "
            "eight, then six, and three more rounds remove the colours above two. <bookmark mark='d'/> Seven rounds "
            "for a million processes, and it would be only a little more for a billion: the number of times you "
            "take a logarithm before reaching one, written log star."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(arrows), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(counter))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            for r in range(1, len(c["trace"])):
                vals = c["trace"][r]
                new = labels(vals, True)
                cnt = label(rf"round {r}: \ {c['colours'][r]:,} colours", font_size=24, color=HEAD).move_to(counter)
                fills = [d.animate.set_fill(PALETTE[v] if v < 6 else BG, opacity=0.35 if v < 6 else 1)
                         for d, v in zip(dots, vals)]
                self.play(Transform(cur, new), Transform(counter, cnt), *fills, run_time=0.9)
            vo.wait_until("d")
            self.play(Indicate(counter, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def questions(self):
        head = label(r"Locality, \ faults and impossibility", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup()
        for t, d, c in ((r"what can be computed locally?", r"in $t$ rounds a process sees only its $t$-hop "
                         r"neighbourhood; \ Linial \ (1992): \ three-colouring a ring needs $\Omega(\log^* n)$", HEAD),
                        (r"what can be agreed?", r"three processes cannot survive one liar; \ $f$ crashes need $f + 1$ "
                         r"rounds; \ asynchrony makes it impossible \ (FLP, \ Part 38)", NO),
                        (r"what can be computed at all?", r"$k$-set agreement is impossible, \ and the proof is "
                         r"Sperner's lemma from topology \ (1993)", LAM)):
            r = RoundedRectangle(width=4.1, height=2.8, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=21, color=c), wrapped_label(d, 3.7, font_size=18, color=GREY_A)).arrange(
                DOWN, buff=0.25).move_to(r)
            tiles.add(VGroup(r, g))
        tiles.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"Part 38 built Raft; \ this part is the theory underneath", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This part asks three questions. <bookmark mark='a'/> What can be computed locally, when each process "
            "sees only a few hops? Nathan Linial proved in 1992 that our seven rounds are essentially the best "
            "possible: no algorithm can three-colour a ring in fewer than about log star of n rounds. "
            "<bookmark mark='b'/> What can be agreed when processes fail? Three processes cannot reach agreement if "
            "one of them lies; f crashes need f plus one rounds; and with no clocks at all, Part 38's FLP theorem "
            "rules agreement out. <bookmark mark='c'/> And what can be computed at all? Some tasks are impossible "
            "for reasons that turned out to be topological. <bookmark mark='d'/> Part 38 built Raft. This part is the "
            "theory underneath it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Distributed Computing Theory", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"models: \ synchrony, \ asynchrony and faults",
            r"locality: \ Cole--Vishkin and Linial's lower bound",
            r"agreement: \ $f + 1$ rounds and the hexagon",
            r"randomized consensus and shared memory",
            r"topology and $k$-set agreement",
            r"failure detectors, \ costs and population protocols",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 59 of Computer Science, Built. <bookmark mark='a'/> We will fix the models; colour rings in "
            "log star rounds and prove no one can do better; prove the limits of agreement with crashes and liars; "
            "beat impossibility with randomness; climb the consensus hierarchy of shared objects; meet the "
            "topological proof that k-set agreement is impossible; and end with failure detectors, the cost of "
            "agreement, and protocols for chemical computers."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
