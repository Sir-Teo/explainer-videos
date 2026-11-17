from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


def puzzle_box_drawing(scale=1.0):
    """A slatted crate with a door, a loop of string to pull, and a dish outside: drawn, not to scale."""
    crate = Rectangle(width=3.0, height=2.2, stroke_color=GREY_B, stroke_width=3)
    slats = VGroup(*[Line(crate.get_corner(DL) + RIGHT * x, crate.get_corner(UL) + RIGHT * x, color=GREY_D,
                          stroke_width=2) for x in np.linspace(0.3, 2.7, 9)])
    door = Rectangle(width=0.7, height=1.3, stroke_color=CR, stroke_width=3).move_to(crate.get_right() +
                                                                                    LEFT * 0.36 + DOWN * 0.45)
    loop = Circle(radius=0.16, color=US, stroke_width=3).move_to(crate.get_top() + DOWN * 0.45 + LEFT * 0.6)
    string = Line(loop.get_top(), crate.get_top() + LEFT * 0.6, color=US, stroke_width=2)
    dish = VGroup(Arc(radius=0.3, start_angle=PI, angle=PI, color=US, stroke_width=3)).next_to(crate, RIGHT,
                                                                                              buff=0.5).shift(DOWN * 0.8)
    cat = VGroup(Circle(radius=0.28, color=WHITE, stroke_width=3),
                 Triangle(color=WHITE, stroke_width=3).scale(0.12).shift(UP * 0.3 + LEFT * 0.15),
                 Triangle(color=WHITE, stroke_width=3).scale(0.12).shift(UP * 0.3 + RIGHT * 0.15)).move_to(
        crate.get_center() + LEFT * 0.6 + DOWN * 0.4)
    g = VGroup(crate, slats, door, loop, string, dish, cat).scale(scale)
    g.door, g.loop, g.cat = door, loop, cat
    return g


class Effect(VoiceoverScene):
    def construct(self):
        self.card()
        self.thorndike()
        self.watson()
        self.albert()

    def card(self):
        card = chapter_card(2, r"The law of effect", r"How do consequences change what an animal does?",
                            lit={1898: r"Thorndike", 1920: r"Watson \& Rayner"}, part=PART, scale=("mind", "person"),
                            marr=("what",))
        with self.voiceover("Chapter two. The law of effect."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def thorndike(self):
        d = load("thorndike")
        head = heading(r"Thorndike's cats, \ 1898")
        pb = puzzle_box_drawing(0.95).move_to([-4.3, 1.2, 0])
        cap = label(r"drawn, \ not to scale", font_size=18, color=GREY_B).next_to(pb, DOWN, buff=0.15)
        A = axes([0, 25], [0, 100], x_length=6.6, y_length=3.6, xticks=[1, 6, 12, 18, 24], yticks=[0, 25, 50, 75, 100],
                 xlabel=r"trial", ylabel=r"seconds to escape", center=[2.7, 0.9, 0])
        ax = A.ax
        x = np.arange(1, 25)
        one = curve(ax, x, d["one"], GREY_B, stroke_width=2)
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(x, d["q75"])], *[ax.c2p(a, b) for a, b in zip(x[::-1], d["q25"][::-1])],
                       stroke_width=0, fill_color=CR, fill_opacity=0.25)
        med = curve(ax, x, d["median"], CR, stroke_width=4)
        lg = legend([(GREY_B, r"one cat"), (CR, r"median of 200, \ middle half shaded")], font_size=20)
        lg.move_to(ax.c2p(17, 88))
        rows = rows_of([
            (r"a hungry cat in a crate; \ food outside; \ one act, \ pulling a loop, \ opens the door", WHITE),
            (r"the time to escape falls, \ but gradually and unevenly: \ no sign of a sudden insight", CR),
            (r"the law of effect: \ acts followed by satisfaction are ``stamped in'', \ the rest ``stamped out''", US),
        ], 12.4, 26, 0.26).to_edge(DOWN, buff=0.75)
        tag = psyche_tag(r"computed: \ Psyche's cat, \ \texttt{conditioning.puzzle\_box}")
        with self.voiceover(
            "While Pavlov was studying digestion, a young American, Edward Thorndike, was putting cats in boxes. "
            "<bookmark mark='a'/> A hungry cat goes into a slatted crate with food outside. One act opens the door: "
            "pulling a loop of string, say, or pressing a lever. The cat scratches, bites, squeezes, and eventually, "
            "by accident, pulls the loop and gets out. Thorndike put it back and timed it again. "
            "<bookmark mark='b'/> The times fell, but gradually and unevenly, not in the sudden drop you'd expect if "
            "the cat had understood. Here is Psyche's cat, a learner that just strengthens whatever act preceded "
            "escape, with the median of two hundred such cats. <bookmark mark='c'/> Thorndike called the principle the "
            "law of effect: acts followed by a satisfying state of affairs are stamped in, and acts followed by "
            "discomfort are stamped out. Pavlov's dogs learned what signals what. Thorndike's cats learned what to do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pb), FadeIn(cap), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(pb.loop, color=US))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(one), run_time=2.0)
            self.play(FadeIn(band), Create(med), FadeIn(lg), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def watson(self):
        head = heading(r"Behaviourism, \ 1913")
        rows = rows_of([
            (r"John B. Watson: \ psychology should study behaviour, \ not consciousness", WHITE),
            (r"its goal: \ to predict and control behaviour, \ by the methods of Pavlov and Thorndike", CS),
            (r"and a bold claim: \ fears, \ loves and habits are conditioned, \ and could be conditioned differently",
             US),
            (r"for forty years, \ much of American psychology followed him", GREY_A),
        ], 12.4, 30, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "In 1913 John Watson published a manifesto. <bookmark mark='a'/> Psychology, he said, should give up "
            "studying consciousness by introspection, the method of Part 1, and study behaviour instead. "
            "<bookmark mark='b'/> Its goal was the prediction and control of behaviour, by the methods of Pavlov and "
            "Thorndike. <bookmark mark='c'/> And Watson made a bold claim: human emotions, fears, loves and habits, are "
            "conditioned responses, learned, and so could be learned differently. <bookmark mark='d'/> For about forty "
            "years much of American psychology followed him. To show the claim in action, he ran one experiment on "
            "one baby."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def albert(self):
        p = archive.WATSON_RAYNER_1920.data
        head = heading(r"Little Albert, \ as the notes record it")
        steps = [
            (r"about 9 months", r"a white rat, \ a rabbit, \ a dog, \ masks, \ cotton wool: \ no fear", WHITE),
            (r"8 months 26 days", r"a hammer on a steel bar behind his head: \ startle, \ then crying", US),
            (r"11 months 3 days", r"the rat, \ and as he touches it, \ the bar is struck: \ twice", INHIB),
            (r"11 months 10 days", r"five more pairings; \ seven in all; \ now he cries at the rat alone", INHIB),
            (r"11 months 15 days", r"a rabbit, \ a dog, \ a fur coat, \ a Santa Claus mask: \ fear; \ his blocks: "
                                   r"\ none", CS),
            (r"1 year 21 days", r"weaker, \ but still there; \ he leaves the hospital that day; \ no attempt to "
                                r"remove the fear", GREY_A),
        ]
        rows = VGroup()
        for when, what, col in steps:
            w = label(when, font_size=24, color=col)
            t = wrapped_label(what, 8.6, 25, WHITE if col is GREY_A else col)
            rows.add(VGroup(w, t))
        for r in rows:
            r[0].move_to([-4.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-1.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.1, 0])
        for r in rows:
            r[1].align_to(rows[0][1], LEFT)
        keep_in_frame(rows)
        tag = historical_tag(archive.WATSON_RAYNER_1920.cite)
        with self.voiceover(
            "The experiment is famous, and the version most people know isn't quite the one in the paper, so here are "
            "Watson and Rayner's own notes. <bookmark mark='a'/> Albert, the son of a wet nurse at a Baltimore "
            "hospital, was tested at about nine months with a white rat, a rabbit, a dog, masks and cotton wool. "
            "He showed no fear of any of them. <bookmark mark='b'/> A hammer struck on a steel bar behind his head "
            "made him start and, on the third blow, cry. <bookmark mark='c'/> At eleven months, as he reached for the "
            "rat, the bar was struck. Twice. <bookmark mark='d'/> A week later, five more pairings, seven in all, and "
            "now he cried and crawled away from the rat alone. <bookmark mark='e'/> Five days later the fear had "
            "spread: to a rabbit, a dog, a sealskin coat, a Santa Claus mask, but not to his toy blocks. "
            "<bookmark mark='f'/> A month later it was weaker but still there. That day Albert left the hospital, and "
            "the experimenters noted that they had lost the chance to remove the fear. Nobody did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
        head = heading(r"And as it was retold")
        rows = rows_of([
            (r"one infant; \ notes and a film; \ no measure that a second observer scored", WHITE),
            (r"in textbooks the result grew: \ more objects, \ stronger fear, \ even a cure that never happened "
             r"\ (Harris, \ 1979)", INHIB),
            (r"who Albert was is still disputed: \ two candidates, \ one who died at six, \ one who lived to 87", GREY_A),
            (r"a demonstration, \ and an ethical lesson; \ the Ledger's row is in chapter thirteen", YOU),
        ], 12.4, 28, 0.4).move_to([0, -0.1, 0])
        tag = published_tag(archive.HARRIS_1979.cite)
        with self.voiceover(
            "So what does it show? <bookmark mark='a'/> One infant, with the results kept as notes and a film, and no "
            "measure scored by anyone blind to the condition. <bookmark mark='b'/> In 1979 the historian Ben Harris "
            "traced how textbooks retold it. The story grew: more objects, stronger fear, and in some versions a cure "
            "that never happened. <bookmark mark='c'/> Even Albert's identity is disputed. Historians have proposed "
            "two different children, one who died of hydrocephalus at six, and one who lived to eighty-seven, and "
            "never knew. <bookmark mark='d'/> It's a demonstration that fear can be conditioned in a child, and a "
            "lesson in what research ethics now forbids. It isn't evidence for a theory of phobias. The Ledger has "
            "its row."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
