from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"In 1930s America, \ a Chinese couple stopped at 251 hotels and restaurants. \ How many refused to "
           r"serve them?", CROWD),
    (r"2", r"Six months later the same places were asked by letter whether they would serve Chinese guests. \ What "
           r"share of those who replied said no?", AUTH),
    (r"3", r"People scoring in the bottom quarter of a test of logic or grammar: \ at what percentile did they "
           r"place themselves?", PERSON),
    (r"4", r"What share of American students rated themselves more skilful than the median driver?", MODEL),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.shapes()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ shapes and numbers", r"Can you see a mind in a moving triangle?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: shapes and numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def shapes(self):
        head = heading(r"Watch three shapes")
        room = VGroup(Line([-2, -1.6, 0], [-2, 1.6, 0]), Line([-2, 1.6, 0], [2, 1.6, 0]),
                      Line([2, 1.6, 0], [2, 0.5, 0]), Line([2, -0.5, 0], [2, -1.6, 0]),
                      Line([2, -1.6, 0], [-2, -1.6, 0])).set_stroke(GREY_B, 4).shift(LEFT * 1.0)
        door = Line([2, 0.5, 0], [2, -0.5, 0], color=GREY_B, stroke_width=4).shift(LEFT * 1.0)
        big = Triangle(color=AUTH, fill_opacity=0.6).scale(0.55).move_to([-1.6, 0.7, 0])
        small = Triangle(color=CROWD, fill_opacity=0.6).scale(0.32).move_to([4.6, 1.3, 0])
        dot = Circle(radius=0.22, color=PERSON, fill_opacity=0.7).move_to([-2.3, -0.9, 0])
        cap = label(r"an animation in the spirit of Heider and Simmel's, \ 1944", font_size=16, color=GREY_B)
        cap.to_edge(DOWN, buff=0.5)
        tag = historical_tag(r"Heider \& Simmel (1944)")
        with self.voiceover(
            "Before anything else, watch three shapes for a few seconds. <bookmark mark='a'/> A big triangle and "
            "a circle are inside a room. <bookmark mark='b'/> A small triangle arrives outside. "
            "<bookmark mark='c'/> The circle edges toward the door. The big triangle swings across to block it. "
            "<bookmark mark='d'/> The small triangle darts in, the big one turns to chase it, and the circle slips "
            "out through the door. The small triangle follows, and the two leave together. <bookmark mark='e'/> "
            "You probably saw a bully, a friend and a rescue. You were shown three shapes moving. In 1944 Heider "
            "and Simmel made a short film like this, and the people who watched it described the shapes as people "
            "with intentions and feelings. Reading minds is so automatic that we do it to triangles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(room), Create(door), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(big), FadeIn(dot))
            self.play(big.animate.shift(RIGHT * 0.5), run_time=0.8)
            self.play(big.animate.shift(LEFT * 0.5), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(small))
            self.play(small.animate.move_to([2.4, 1.0, 0]), run_time=1.5)
            vo.wait_until("c")
            self.play(dot.animate.move_to([-0.2, -0.4, 0]), run_time=1.2)
            self.play(big.animate.move_to([0.3, 0.0, 0]), run_time=0.8)
            self.play(Rotate(big, PI / 6), run_time=0.4)
            self.play(Rotate(big, -PI / 6), run_time=0.4)
            vo.wait_until("d")
            self.play(small.animate.move_to([1.6, 0.0, 0]), run_time=0.5)
            self.play(small.animate.move_to([-0.6, 1.1, 0]), big.animate.move_to([0.2, 0.6, 0]), run_time=0.9)
            self.play(big.animate.move_to([-1.4, 0.9, 0]), small.animate.move_to([-2.3, 0.2, 0]),
                      dot.animate.move_to([2.2, -0.3, 0]), run_time=1.4)
            self.play(small.animate.move_to([0.2, -0.1, 0]), big.animate.move_to([-1.9, 0.4, 0]), run_time=0.9)
            self.play(small.animate.move_to([2.6, 0.5, 0]), run_time=0.8)
            self.play(small.animate.move_to([4.8, 0.6, 0]), dot.animate.move_to([4.6, -0.2, 0]),
                      big.animate.move_to([0.2, 0.0, 0]), run_time=1.6)
            vo.wait_until("e")
            self.play(Indicate(big, color=AUTH), Indicate(small, color=CROWD), Indicate(dot, color=PERSON))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: in 1930s "
            "America, a Chinese couple stopped at two hundred and fifty-one hotels and restaurants. How many "
            "refused to serve them? <bookmark mark='b'/> Two: six months later the same places were asked by "
            "letter whether they would serve Chinese guests. What share of those who replied said no? "
            "<bookmark mark='c'/> Three: people who scored in the bottom quarter on a test of logic or grammar. At "
            "what percentile did they place themselves? <bookmark mark='d'/> And four: what share of American "
            "students rated themselves more skilful than the median driver? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
