from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


def crowd_grid(n: int = 100, cols: int = 20, gap: float = 0.36, radius: float = 0.12) -> VGroup:
    """n people as dots, threshold 0 at the top left, rising along the rows."""
    g = VGroup(*[Circle(radius=radius, stroke_width=1.5, stroke_color=GREY_B, fill_color=OFF, fill_opacity=1)
                 for _ in range(n)])
    for i, d in enumerate(g):
        d.move_to([(i % cols) * gap, -(i // cols) * gap, 0])
    return g


class Thresholds(VoiceoverScene):
    def construct(self):
        self.card()
        self.riot()
        self.twin()
        self.spread()

    def card(self):
        card = chapter_card(9, r"Thresholds", r"Why can one person decide what a crowd does?",
                            lit={1978: r"Granovetter"}, part=PART, scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter nine. Thresholds."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def riot(self):
        d = load("riot")
        head = heading(r"A hundred people, \ a hundred thresholds")
        grid = crowd_grid(cols=10, gap=0.44, radius=0.19).move_to([-3.1, 0.35, 0])
        nums = VGroup(*[label(str(k), font_size=14, color=GREY_A).move_to(grid[k]) for k in range(100)])
        count = VGroup(label(r"in so far:", font_size=22, color=GREY_A),
                       Integer(0, font_size=34, color=PERSON)).arrange(RIGHT, buff=0.2).next_to(grid, DOWN, buff=0.3)
        rows = rows_of([
            (r"a threshold is how many others must already be rioting before a person joins", WHITE),
            (r"Granovetter's crowd: \ one person with threshold 0, \ one with 1, \ one with 2, \ and so on up "
             r"to 99", CROWD),
            (r"the one at 0 starts; \ that brings in the one at 1, \ which brings in the one at 2: \ everyone "
             r"ends up rioting", PERSON),
            (r"each joins only when the count reaches them: \ nobody needed to be a radical", MODEL),
        ], 5.0, 20, 0.34).move_to([4.2, 0.0, 0])
        tag = psyche_tag(r"\texttt{social.cascade}")
        path = list(d["path_a"])
        with self.voiceover(
            "Here's a way to think about crowds that the famous studies never had. <bookmark mark='a'/> Give each "
            "person a threshold: the number of others who must already be doing something before they'll join. "
            "<bookmark mark='b'/> In Granovetter's example, a hundred people stand in a square. One has a threshold "
            "of zero, one has a threshold of one, one of two, and so on, up to ninety-nine. <bookmark mark='c'/> "
            "The one at zero throws a stone. That's enough for the one at one, which makes two, which is enough "
            "for the one at two. Watch the count. <bookmark mark='d'/> Every person joins, and every one of them "
            "joined only when the count reached their own threshold. Nobody here needed to be a radical. "
            "<bookmark mark='e'/>"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(count))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            for k in range(1, len(path)):
                lo, hi = path[k - 1], path[k]
                self.play(*[grid[j].animate.set_fill(PERSON) for j in range(lo, hi)],
                          *[nums[j].animate.set_color(BLACK) for j in range(lo, hi)],
                          count[1].animate.set_value(hi), run_time=0.09)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
        self.clear_scene()

    def twin(self):
        d = load("riot")
        head = heading(r"Change one person")
        left = crowd_grid(gap=0.27, radius=0.09).move_to([-3.6, 0.6, 0])
        right = crowd_grid(gap=0.27, radius=0.09).move_to([3.0, 0.6, 0])
        for j in range(100):
            left[j].set_fill(PERSON)
        right[0].set_fill(PERSON)
        right[1].set_stroke(AUTH, width=3)
        cap = VGroup(label(rf"crowd A: \ {d['size_a']} rioting", font_size=24, color=PERSON).next_to(left, UP, buff=0.25),
                     label(rf"crowd B: \ {d['size_b']} rioting", font_size=24, color=CROWD).next_to(right, UP, buff=0.25))
        rows = rows_of([
            (r"crowd B is the same crowd, \ except that the person with threshold 1 has threshold 2", AUTH),
            (r"the instigator throws a stone; \ nobody else's threshold is reached; \ one person riots, \ and is "
             r"arrested", CROWD),
            (r"a reporter would call crowd A a mob of radicals and crowd B a crowd of moderates: \ the two differ "
             r"in one person, \ by one unit", YOU),
            (r"what a crowd does depends on the whole distribution of thresholds, \ not on its average member",
             MODEL),
        ], 12.4, 21, 0.28).move_to([0, -2.35, 0])
        tag = psyche_tag(r"\texttt{social.cascade\_size}")
        with self.voiceover(
            "Now change one person. <bookmark mark='a'/> Crowd B is the same crowd, except that the person whose "
            "threshold was one now has a threshold of two. <bookmark mark='b'/> The instigator throws a stone. "
            "Nobody else's threshold is reached. One person riots, and gets arrested. <bookmark mark='c'/> A "
            "reporter would describe crowd A as a mob of radicals and crowd B as a crowd of moderates. They differ "
            "in one person, by one unit. <bookmark mark='d'/> What a crowd does depends on the whole distribution "
            "of its thresholds, not on its average member. That's why it's so hard to read people's minds from "
            "what a crowd did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left), FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(FadeIn(right), FadeIn(cap[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(right[0], color=PERSON), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def spread(self):
        d = load("riot")
        head = heading(r"Smooth crowds, \ sudden outcomes")
        A = axes([0, 30], [0, 105], x_length=6.2, y_length=3.8, xticks=[0, 5, 10, 15, 20, 25, 30],
                 yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"spread of the thresholds \ (SD; \ mean 25)", ylabel=r"how many end up rioting",
                 center=[-2.9, -0.4, 0], font_size=15)
        c = curve(A.ax, d["sd"], d["size"], PERSON, stroke_width=4)
        jump = DashedLine(A.ax.c2p(d["jump"], 0), A.ax.c2p(d["jump"], 100), color=AUTH, stroke_width=2)
        rows = rows_of([
            (r"now give a crowd of 100 thresholds from a bell curve with mean 25, \ and widen it a little at a "
             r"time", WHITE),
            (rf"narrow crowds: \ nobody starts, \ so nobody joins; \ at a spread of about {d['jump']:.0f}, \ the "
             r"outcome jumps from none to everyone", PERSON),
            (r"a smooth change in the people, \ a sudden change in what they do together: \ a tipping point, \ "
             r"like Part 27's ignition", MODEL),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.cascade\_curve}")
        with self.voiceover(
            "Real crowds aren't arranged one per threshold. <bookmark mark='a'/> So give a crowd of a hundred "
            "people thresholds from a bell curve, centred on twenty-five, and widen it a little at a time. "
            "<bookmark mark='b'/> When the crowd is uniform, nobody has a low enough threshold to start, so nobody "
            f"joins. At a spread of about {d['jump']:.0f}, the outcome jumps from no one to everyone. "
            "<bookmark mark='c'/> A smooth change in the people gives a sudden change in what they do together. "
            "It's a tipping point, like the ignition of Part 27."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]), run_time=2.5)
            self.play(Create(jump))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
