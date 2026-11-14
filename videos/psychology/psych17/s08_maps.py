from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


def maze_drawing(text, size=0.42):
    rows = text.split("\n")
    g = VGroup()
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            pos = [c * size, -r * size, 0]
            if ch == "#":
                g.add(Square(size, stroke_width=0, fill_color=GREY_D, fill_opacity=1).move_to(pos))
            elif ch == "S":
                g.add(Square(size, stroke_width=0, fill_color=CUE, fill_opacity=0.6).move_to(pos))
            elif ch == "G":
                g.add(Square(size, stroke_width=0, fill_color=REWARD, fill_opacity=0.8).move_to(pos))
    return g


class Maps(VoiceoverScene):
    def construct(self):
        self.card()
        self.latent()
        self.maps()
        self.cells()

    def card(self):
        card = chapter_card(7, r"Tolman's maps", r"Do rats learn where things are, \ or only what to do?",
                            lit={1930: r"Tolman \& Honzik", 1971: r"O'Keefe", 2005: r"the Mosers"}, part=PART,
                            scale=("neuron", "circuit", "mind"), marr=("what", "tissue"))
        with self.voiceover("Chapter seven. Tolman's maps."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def latent(self):
        d = load("maze")
        head = heading(r"Latent learning, \ Tolman and Honzik, \ 1930")
        mz = maze_drawing(d["maze"], 0.36).move_to([-4.9, 1.45, 0])
        ml = VGroup(label(r"start", font_size=18, color=CUE), label(r"goal box", font_size=18, color=REWARD))
        ml.arrange(RIGHT, buff=0.5).next_to(mz, DOWN, buff=0.15)
        A = axes([1, 20], [0, 200], x_length=6.2, y_length=3.6, xticks=[1, 5, 10, 15, 20], yticks=[0, 100, 200],
                 xlabel=r"day", ylabel=r"steps to the goal box", center=[1.6, 0.6, 0])
        ax = A.ax
        x = np.arange(1, 21)
        ca = curve(ax, x, d["always"], GOOD, 3)
        cn = curve(ax, x, d["never"], GREY_B, 3)
        cd = curve(ax, x, d["delayed"], YOU, 4)
        cf = curve(ax, x, d["delayed_free"], MF, 3)
        food = DashedLine(ax.c2p(10.5, 0), ax.c2p(10.5, 200), color=REWARD, stroke_width=2)
        fl = label(r"food from day 11", font_size=18, color=REWARD).next_to(ax.c2p(10.5, 200), UP, buff=0.05)
        lg = legend([(GOOD, r"food every day"), (GREY_B, r"never food"), (YOU, r"food from day 11"),
                     (MF, r"food from day 11, \ a learner with no map")], font_size=19)
        lg.next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"rats ran a maze daily; \ one group found no food until day 11", WHITE),
            (r"the day after food appeared, \ they ran as well as rats fed all along", YOU),
            (r"they had learned the maze without reward: \ learning is not the same as performance", DELTA),
        ], 4.2, 23, 0.26).move_to([-4.6, -1.55, 0])
        keep_in_frame(rows)
        tag = historical_tag(archive.TOLMAN_HONZIK_1930.cite)
        tag2 = psyche_tag(r"the curves: \ Psyche, \ \texttt{rl.latent\_learning}, \ medians of 40")
        with self.voiceover(
            "Edward Tolman, at Berkeley, thought rats learned more than responses. <bookmark mark='a'/> In 1930 he "
            "and Charles Honzik ran rats through a maze once a day. One group found food in the goal box every day; "
            "one never did; and one found nothing for ten days, then food from the eleventh. <bookmark mark='b'/> "
            "The rats fed every day improved steadily. The unfed rats wandered. And the third group, on the day "
            "after food first appeared, ran the maze about as well as rats that had been fed all along. "
            "<bookmark mark='c'/> They had been learning the maze all the while, without any reward to strengthen "
            "anything, and showed it only when there was a reason to. Here are the same three groups run on Psyche, "
            "with a learner that builds a map and plans on it. It learns far faster than any rat, so the fed group "
            "masters the maze in two days; what matters is the late group's jump. In blue, a learner without a map, "
            "which has nothing to show when the food appears."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mz), FadeIn(ml), FadeIn(A), FadeIn(tag), FadeIn(tag2), Create(food),
                      FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ca), Create(cn), Create(cd), FadeIn(lg[:3]), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(lg[3]), FadeIn(rows[2]), run_time=1.5)
        self.clear_scene()

    def maps(self):
        head = heading(r"Cognitive maps, \ 1948")
        rows = rows_of([
            (r"Tolman: \ rats build a map of their environment, \ not a chain of stimulus and response", WHITE),
            (r"with a map, \ a rat can take a shortcut it has never run, \ or reroute around a block", MB),
            (r"the behaviourists' answer was to explain each result away; \ the debate ran for decades", GREY_A),
            (r"in reinforcement learning the map is a model: \ which states lead to which, \ and what they pay", VALUE),
        ], 6.6, 26, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        # a schematic arena: the trained route winds round; the map offers a straight line
        start = Dot([2.0, -2.0, 0], radius=0.14, color=CUE)
        goal = Dot([5.6, 1.9, 0], radius=0.16, color=REWARD)
        route = VMobject(color=GREY_B, stroke_width=5).set_points_as_corners(
            [[2.0, -2.0, 0], [2.0, 0.2, 0], [0.9, 0.2, 0], [0.9, 2.0, 0], [3.6, 2.0, 0], [3.6, 0.9, 0], [5.6, 0.9, 0],
             [5.6, 1.9, 0]])
        sl = label(r"start", font_size=20, color=CUE).next_to(start, DOWN, buff=0.12)
        gl = label(r"food", font_size=20, color=REWARD).next_to(goal, UP, buff=0.12)
        rl_ = label(r"the route it was trained on", font_size=19, color=GREY_B).move_to([2.25, 2.35, 0])
        block = VGroup(Line([1.65, 0.0, 0], [2.35, 0.4, 0], color=BAD, stroke_width=6),
                       Line([1.65, 0.4, 0], [2.35, 0.0, 0], color=BAD, stroke_width=6))
        cut = DashedLine([2.15, -1.85, 0], [5.45, 1.75, 0], color=MB, stroke_width=4, buff=0.1)
        cut.add_tip(tip_length=0.25)
        cl = label(r"a shortcut never run", font_size=20, color=MB).move_to([4.6, -0.5, 0])
        cap = label(r"schematic, \ not a figure from a study", font_size=17, color=GREY_C).move_to([3.3, -2.75, 0])
        tag = historical_tag(archive.TOLMAN_1948.cite)
        with self.voiceover(
            "In 1948 Tolman gave the idea its name. <bookmark mark='a'/> Rats, he argued, build cognitive maps of "
            "their environment, not chains of stimulus and response. <bookmark mark='b'/> A rat with a map can "
            "take a shortcut it has never run, or find a way round a blocked path. <bookmark mark='c'/> His "
            "opponents explained each result some other way, and the argument lasted decades. "
            "<bookmark mark='d'/> In reinforcement learning, the map is what's called a model: knowledge of which "
            "states lead to which, and what each pays. With a model you can plan. Without one, you can only repeat "
            "what paid before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(start), FadeIn(goal), FadeIn(sl), FadeIn(gl), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), Create(route), FadeIn(rl_), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(block))
            self.play(Create(cut), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
        self.clear_scene()

    def cells(self):
        head = heading(r"A map in the brain")
        arena = Circle(radius=1.5, color=GREY_B, stroke_width=3).move_to([-3.6, 0.95, 0])
        field = Circle(radius=0.35, stroke_width=0, fill_color=DELTA, fill_opacity=0.7).move_to(
            arena.get_center() + np.array([0.6, 0.5, 0]))
        lp = label(r"a place cell: \ one place", font_size=22, color=DELTA).next_to(arena, DOWN, buff=0.2)
        arena2 = Circle(radius=1.5, color=GREY_B, stroke_width=3).move_to([3.6, 0.95, 0])
        grid = VGroup()
        a1 = np.array([0.62, 0, 0])
        a2 = np.array([0.31, 0.537, 0])
        for i in range(-4, 5):
            for j in range(-4, 5):
                p = arena2.get_center() + i * a1 + j * a2
                if np.linalg.norm(p - arena2.get_center()) < 1.45:
                    grid.add(Circle(radius=0.15, stroke_width=0, fill_color=VALUE, fill_opacity=0.75).move_to(p))
        lg_ = label(r"a grid cell: \ a lattice of places", font_size=22, color=VALUE).next_to(arena2, DOWN, buff=0.2)
        cap = label(r"drawn: \ where each cell fires as a rat explores a round arena", font_size=18, color=GREY_B)
        cap.next_to(VGroup(lp, lg_), DOWN, buff=0.2)
        rows = rows_of([
            (r"1971: \ John O'Keefe finds hippocampal neurons that fire in one place in the room", DELTA),
            (r"2005: \ May-Britt and Edvard Moser find entorhinal cells firing on a triangular lattice", VALUE),
            (r"Nobel Prize, \ 2014; \ grid-like signals have since been seen in human brains", GREY_A),
        ], 12.4, 25, 0.22).to_edge(DOWN, buff=0.85)
        tag = published_tag(archive.HAFTING_2005.cite)
        with self.voiceover(
            "Tolman's map turned out to be literal. <bookmark mark='a'/> In 1971 John O'Keefe, recording in the "
            "hippocampus of rats, found neurons that fire whenever the animal is in one particular place in the room, "
            "and almost never elsewhere: place cells. <bookmark mark='b'/> In 2005 May-Britt and Edvard Moser, in "
            "Trondheim, found cells next door, in the entorhinal cortex, that fire at many places, arranged in a "
            "triangular lattice that tiles the whole floor: grid cells, a coordinate system for space. "
            "<bookmark mark='c'/> The three shared the Nobel Prize in 2014, and grid-like signals have since been "
            "found in human brains, during navigation and even when people move through abstract spaces of ideas."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(arena), FadeIn(arena2), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(field), FadeIn(lp), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.03), FadeIn(lg_), FadeIn(rows[1]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
