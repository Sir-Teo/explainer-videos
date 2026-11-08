from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Muddy(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The muddy children", r"How can saying what everyone knows change anything?",
                            lit=(), part=PART)
        with self.voiceover("Chapter three. The muddy children."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cube()
        self.reasoning()
        self.eight()

    def cube(self):
        d = load("muddy")
        head = label(r"Three children, \ eight worlds", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        g = muddy_cube(scale=2.0, center=[-2.6, -0.5, 0], radius=0.32, font_size=20)
        key = VGroup(*[VGroup(Line(LEFT * 0.25, RIGHT * 0.25, color=AG[i], stroke_width=5),
                              label(nm, font_size=20, color=AG[i])).arrange(RIGHT, buff=0.12)
                       for i, nm in enumerate((r"Ann", r"Bob", r"Cy"))]).arrange(RIGHT, buff=0.4).to_corner(
            DL, buff=0.4)
        rounds = [set(map(tuple, r)) for r in d["cube"]]
        notes = [r"110: \ Ann and Bob muddy, \ Cy clean", r"each child confuses two worlds: \ her own forehead",
                 r"father: \ `at least one of you is muddy' \ removes 000",
                 r"`nobody knows': \ removes the worlds with one muddy child",
                 r"in 110 that is enough: \ Ann and Bob now know"]
        nl = VGroup(*[label(t, font_size=21, color=c) for t, c in
                      zip(notes, [GREY_A, GREY_A, COMMON, GOAL, OK])]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        nl.add(label(r"(had all three been muddy, \ a second round would leave only 111)", font_size=19,
                     color=GREY_B))
        nl.move_to([3.6, -0.2, 0])
        for m in nl:
            if m.width > 6.4:
                m.width = 6.4
        nl.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, -0.2, 0])
        act = Circle(radius=0.42, color=COMMON, stroke_width=3).move_to(g.world[(1, 1, 0)])
        sizes = label(r"worlds left, \ if all three are muddy: \ " + r" $\to$ ".join(str(len(r)) for r in rounds),
                      font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.4).shift(RIGHT * 2.5)

        def drop(before, after):
            gone = [w for w in before if w not in after]
            es = [e for k, e in g.edge.items() if k[1] in gone or k[2] in gone]
            return [FadeOut(g.world[w]) for w in gone] + [e.animate.set_opacity(0.08) for e in es]
        with self.voiceover(
            "Now the puzzle from the start. <bookmark mark='a'/>With three children there are eight worlds, one for "
            "each way the mud could lie: one means muddy, zero clean. They form a cube. The actual world is one one "
            "zero: Ann and Bob are muddy, Cy is clean. <bookmark mark='b'/>Each child sees every forehead but her "
            "own, so she cannot tell apart two worlds that differ only at her own place: the cube's edges, one "
            "colour per child. <bookmark mark='c'/>The father announces that at least one child is muddy. That "
            "deletes world zero zero zero. <bookmark mark='d'/>He asks: does anyone know whether you are muddy? "
            "Nobody does, and they say so. That public fact deletes every world where some child would have known: "
            "the three worlds with exactly one muddy child, since that child would have seen only clean faces. "
            "<bookmark mark='e'/>In our world, one one zero, that is already enough: Ann and Bob can now tell where "
            "they are, as we will see. Had all three been muddy, a second round of 'nobody knows' would delete the "
            "worlds with two muddy children, leaving only one one one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.discs), Create(act), FadeIn(nl[0]))
            vo.wait_until("b")
            self.play(Create(g.edges), FadeIn(key), FadeIn(nl[1]), run_time=2)
            vo.wait_until("c")
            self.play(*drop(rounds[0], rounds[1]), FadeIn(nl[2]))
            vo.wait_until("d")
            self.play(*drop(rounds[1], rounds[2]), FadeIn(nl[3]))
            vo.wait_until("e")
            self.play(FadeIn(nl[4]))
            self.play(FadeIn(nl[5]), FadeIn(sizes))
        self.clear_scene()

    def reasoning(self):
        d = load("muddy")
        head = label(r"Ann's reasoning, \ in the actual world 110", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Ann sees Bob muddy, \ Cy clean: \ the world is 110 or 010", font_size=24),
            label(r"if it were 010, \ Bob would see two clean faces", font_size=24, color=GREY_A),
            label(r"and, told that someone is muddy, \ he would know at once that it is he", font_size=24,
                  color=GREY_A),
            label(r"round 1: \ Bob says he doesn't know", font_size=24, color=GOAL),
            label(r"so the world is not 010: \ it is 110, \ and Ann is muddy", font_size=26, color=OK),
            label(rf"the Reasoner: \ the muddy children know in round {d['n3']['knows_at'][0]}, \ Cy in round "
                  rf"{d['n3']['knows_at'][2]}", font_size=22, color=KNOW)).arrange(DOWN, buff=0.28).move_to(
            [0, -0.3, 0])
        assert d["n3"]["knows_at"][:2] == [2, 2]
        with self.voiceover(
            "Here is the same thing from inside Ann's head. <bookmark mark='a'/>She sees that Bob is muddy and Cy "
            "is clean. So the world is one one zero, if she is muddy, or zero one zero, if she is not. "
            "<bookmark mark='b'/>If it were zero one zero, Bob would see two clean faces, <bookmark mark='c'/>and, "
            "told that someone is muddy, he would know at once that it was him. <bookmark mark='d'/>But in the first "
            "round, Bob says he does not know. <bookmark mark='e'/>So the world is not zero one zero. It is one one "
            "zero, and Ann is muddy. Bob reasons the same way about Ann. <bookmark mark='f'/>The Reasoner, running "
            "the announcements on the model, confirms it: the two muddy children know in round two, and Cy, hearing "
            "them, in round three."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def eight(self):
        d = load("muddy")
        n8 = d["n8"]
        head = label(r"Eight children, \ 256 worlds", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        act = label(r"actual: \ " + "".join(map(str, d["n8_actual"])) + rf" \ ({n8['muddy']} muddy)", font_size=24,
                    color=COMMON).next_to(head, DOWN, buff=0.3)
        names = ([r"start", r"father speaks"] + [rf"`nobody knows' \#{i}" for i in range(1, len(n8["sizes"]) - 2)]
                 + [r"the five say `I know'"])
        vals = n8["sizes"]
        bars = bar_row(vals, names, [GREY_B, COMMON] + [GOAL] * (len(vals) - 2), width=7.0, height=0.34,
                       font_size=20, vmax=256)
        bars.move_to([0, -0.6, 0])
        foot = VGroup(label(rf"with $k$ muddy children, \ they all know in round $k$: \ here round "
                            rf"{n8['knows_at'][0]}", font_size=24, color=OK),
                      label(r"and without the father's sentence, \ `nobody knows' never removes a world", font_size=23,
                            color=BAD)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        assert d["no_father"]
        with self.voiceover(
            "The Reasoner does not need to stop at three. <bookmark mark='a'/>With eight children there are two "
            "hundred and fifty-six worlds, and in the actual one, five children are muddy. <bookmark mark='b'/>The "
            "father's sentence removes one world. Then each 'nobody knows' removes every world with one fewer muddy "
            "child than the last: from two hundred and fifty-five, to two hundred and forty-seven, two hundred and "
            "nineteen, one hundred and sixty-three, ninety-three, and then the muddy children know. "
            "<bookmark mark='c'/>With k muddy children, they all know in round k. <bookmark mark='d'/>And the Reasoner "
            "checks the counterfactual: without the father's sentence, the children can say 'nobody knows' forever, "
            "and not one world is removed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(act))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.3), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
