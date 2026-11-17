from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Curiosity(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzles()
        self.mice()
        self.sketch()
        self.gap()

    def card(self):
        card = chapter_card(3, r"Beyond drives: \ curiosity and arousal", r"Why work for nothing?",
                            lit={1908: r"Yerkes \& Dodson", 1950: r"Harlow et al.", 1955: r"Hebb",
                                 1994: r"Loewenstein"},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter three. Beyond drives: curiosity and arousal."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def puzzles(self):
        head = heading(r"Monkeys and puzzles")
        # a hasp puzzle: a plate, a hinge, a hook, a pin
        plate = RoundedRectangle(corner_radius=0.1, width=3.4, height=2.4, color=GREY_B, fill_opacity=0.1).move_to(
            [-3.6, 0.2, 0])
        pin = Line([-4.6, 0.9, 0], [-4.6, 0.2, 0], color=INTR, stroke_width=8)
        hook = Arc(radius=0.3, start_angle=0, angle=PI, color=INTR, stroke_width=6).move_to([-3.6, 0.6, 0])
        hasp = Rectangle(width=1.6, height=0.35, color=INTR, fill_opacity=0.5).move_to([-3.2, -0.2, 0])
        steps = VGroup(*[label(t, font_size=18, color=GREY_B) for t in (r"1. \ pull the pin", r"2. \ lift the hook",
                                                                         r"3. \ open the hasp")])
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(plate, DOWN, buff=0.3)
        rows = rows_of([
            (r"Harlow, \ Harlow and Meyer, \ 1950: \ rhesus monkeys given mechanical puzzles in their cages \ "
             r"took them apart, \ again and again, \ with no food and no other reward", INTR),
            (r"they got better at it, \ and fewer errors: \ learning with no drive reduced", WHITE),
            (r"Butler, \ 1953: \ monkeys learned a discrimination just to open a window onto the laboratory "
             r"outside, \ and a moving toy train held them longest", BODY),
            (r"Harlow called it a manipulation drive; \ the honest name is that exploring and solving are "
             r"rewarding in themselves", WANT),
        ], 5.8, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Harlow, \ Harlow \& Meyer (1950); \ Butler (1953)")
        with self.voiceover(
            "If animals only act to reduce needs, a satisfied animal should sit still. They don't. "
            "<bookmark mark='a'/> In 1950 Harry Harlow, Margaret Harlow and Donald Meyer left mechanical puzzles in "
            "rhesus monkeys' cages: a pin to pull, a hook to lift, a hasp to open. The monkeys took them apart, again "
            "and again, with no food or anything else as a reward. <bookmark mark='b'/> And they got better at it, "
            "making fewer errors over the days: learning, with no drive reduced. <bookmark mark='c'/> A few years "
            "later Robert Butler showed that monkeys would learn a discrimination for nothing more than the chance "
            "to open a small window and look out at the laboratory. <bookmark mark='d'/> Harlow called it a "
            "manipulation drive, which renames the problem. The plainer statement is that exploring and solving "
            "are rewarding in themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(plate), FadeIn(pin), FadeIn(hook), FadeIn(hasp))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(steps[0]), pin.animate.shift(UP * 0.6))
            self.play(FadeIn(steps[1]), hook.animate.rotate(PI / 2))
            self.play(FadeIn(steps[2]), hasp.animate.rotate(-PI / 6, about_point=hasp.get_left()))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mice(self):
        head = heading(r"What Yerkes and Dodson's mice showed")
        boxes = VGroup(*[Rectangle(width=1.4, height=1.0, color=c, fill_opacity=f) for c, f in
                         ((WHITE, 0.85), (GREY_D, 0.85))]).arrange(RIGHT, buff=0.6).move_to([-3.4, 0.6, 0])
        bl = VGroup(label(r"go: \ the light box", font_size=17, color=WHITE).next_to(boxes[0], DOWN, buff=0.15),
                    label(r"shock: \ the dark box", font_size=17, color=LOST).next_to(boxes[1], DOWN, buff=0.15))
        rows = rows_of([
            (r"1908: \ dancing mice learn to choose the lighter of two boxes; \ entering the darker gives a shock "
             r"of one of several strengths", WHITE),
            (r"easy discrimination: \ the stronger the shock, \ the faster the learning", BODY),
            (r"hard discrimination: \ fastest at an intermediate shock", WANT),
            (r"a handful of mice per condition; \ the variable was shock, \ not arousal; \ the outcome was speed of "
             r"learning, \ not performance", LOST),
            (r"the inverted U for arousal and performance, \ and the name law, \ came decades later \ "
             r"(Teigen, \ 1994)", MODEL),
        ], 5.8, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Yerkes \& Dodson (1908); \ Teigen (1994)")
        with self.voiceover(
            "The second challenge to drive theory was arousal, and its most famous evidence is a law that wasn't "
            "one. <bookmark mark='a'/> In 1908 Robert Yerkes and John Dodson trained dancing mice to choose the "
            "lighter of two boxes; entering the darker one gave a shock, of one of several strengths. "
            "<bookmark mark='b'/> When the two boxes were easy to tell apart, the stronger the shock, the faster "
            "the mice learned. <bookmark mark='c'/> When they were hard to tell apart, learning was fastest at an "
            "intermediate shock. <bookmark mark='d'/> There were only a handful of mice in each condition. The "
            "thing varied was the strength of a shock, not arousal, and the thing measured was how fast a habit "
            "formed, not how well anyone performed. <bookmark mark='e'/> The inverted U relating arousal to "
            "performance, and the word law, were attached decades later, as Karl Teigen traced in 1994. The "
            "textbook law is mostly a story told about this experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(boxes), FadeIn(bl))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sketch(self):
        d = load("arousal")
        head = heading(r"The later reading, \ as a sketch")
        A = axes([0, 1], [0, 1.05], x_length=5.8, y_length=3.6, xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"arousal", ylabel=r"performance \ (scaled)",
                 center=[-3.3, -0.2, 0], font_size=16)
        ce = curve(A.ax, d["a"], d["easy"], BODY, 4)
        ch = curve(A.ax, d["a"], d["hard"], WANT, 4)
        key = legend([(BODY, r"easy task"), (WANT, r"hard task")], font_size=17).move_to(A.ax.c2p(0.9, 0.95))
        me = Dot(A.ax.c2p(d["easy_best"], 1.0), color=BODY, radius=0.07)
        mh = Dot(A.ax.c2p(d["hard_best"], 1.0), color=WANT, radius=0.07)
        eq = MathTex(r"\text{performance} = \underbrace{(1 - e^{-3a})}_{\text{drive}} \times "
                     r"\underbrace{\sigma\!\Big(\tfrac{c - a}{0.08}\Big)}_{\text{cue still used}}", font_size=30)
        rows = rows_of([
            (r"Psyche's sketch: \ arousal speeds and energizes, \ and also narrows attention \ (Easterbrook, \ "
             r"1959)", MODEL),
            (r"a hard task depends on subtle cues, \ the first to be dropped as attention narrows", WANT),
            (rf"best arousal: \ {d['easy_best']:.2f} for the easy task, \ {d['hard_best']:.2f} for the hard one",
             WHITE),
            (r"a sketch of a hypothesis, \ not a fit to data: \ modern tests of the inverted U are mixed", LOST),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.arousal\_performance}: \ illustrative")
        with self.voiceover(
            "Here is why the later reading was attractive. <bookmark mark='a'/> In Psyche's sketch, arousal does "
            "two things. It energizes, which helps, and it narrows attention, which Easterbrook proposed in 1959. "
            "<bookmark mark='b'/> A hard task depends on subtle cues, and those are the first to be dropped as "
            "attention narrows. <bookmark mark='c'/> Multiply the two and you get inverted Us, with the best "
            f"arousal at {d['easy_best']:.2f} for the easy task and {d['hard_best']:.2f} for the hard one. "
            "<bookmark mark='d'/> But this is a sketch of a hypothesis, not a fit to anything. Modern tests of the "
            "inverted U are mixed, partly because arousal is several different things that don't move together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ce), Create(ch), FadeIn(key), FadeIn(me), FadeIn(mh), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def gap(self):
        head = heading(r"Curiosity as an information gap")
        rows = rows_of([
            (r"Berlyne: \ novelty, \ surprise and complexity draw exploration; \ too little is boring, \ too much "
             r"is aversive", INTR),
            (r"Loewenstein, \ 1994: \ curiosity is the feeling of a gap between what you know and what you want "
             r"to know; \ it is strongest when the gap is small enough to close", WANT),
            (r"Kang and colleagues, \ 2009: \ curiosity about trivia answers rose with confidence up to a point, "
             r"\ and people paid scarce tokens or waited to learn them", BODY),
            (r"Part 17's learner explores to reduce uncertainty; \ curiosity is that, \ felt", MODEL),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Berlyne (1960); \ Loewenstein (1994); \ Kang et al.\ (2009)")
        with self.voiceover(
            "Curiosity itself became a subject. <bookmark mark='a'/> Daniel Berlyne argued in 1960 that novelty, "
            "surprise and complexity draw exploration, with too little being boring and too much aversive. "
            "<bookmark mark='b'/> George Loewenstein's 1994 theory treats curiosity as the feeling of a gap between "
            "what you know and what you want to know, strongest when the gap seems small enough to close. "
            "<bookmark mark='c'/> In 2009 Min Jeong Kang and colleagues asked people trivia questions. Curiosity "
            "rose with how close people felt to the answer, up to a point, and they would spend scarce tokens or "
            "wait longer to find answers they were curious about. <bookmark mark='d'/> Part 17's learner explores "
            "to reduce its uncertainty about the world. Curiosity may be that computation, felt from the inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
