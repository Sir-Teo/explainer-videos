from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


def rat(color=GREY_B, scale: float = 1.0) -> VGroup:
    """A rat seen from above: body, head, ears, tail."""
    body = Ellipse(width=1.1, height=0.55, color=color, fill_opacity=0.85, stroke_width=0)
    head = Ellipse(width=0.5, height=0.36, color=color, fill_opacity=0.85, stroke_width=0).next_to(body, RIGHT,
                                                                                                    buff=-0.12)
    ears = VGroup(Circle(radius=0.08, color=color, fill_opacity=0.9, stroke_width=0).move_to(head.get_center()
                                                                                             + [-0.06, 0.17, 0]),
                  Circle(radius=0.08, color=color, fill_opacity=0.9, stroke_width=0).move_to(head.get_center()
                                                                                             + [-0.06, -0.17, 0]))
    tail = CubicBezier(body.get_left(), body.get_left() + [-0.4, 0.3, 0], body.get_left() + [-0.6, -0.3, 0],
                       body.get_left() + [-0.95, 0.05, 0], color=color, stroke_width=3)
    return VGroup(tail, body, head, ears).scale(scale)


class Hook(VoiceoverScene):
    def construct(self):
        self.corner()
        self.lever()
        self.psyche()
        self.question()
        self.objectives()

    def corner(self):
        box = Square(side_length=4.6, color=GREY_B, stroke_width=3).move_to([-3.2, -0.2, 0])
        hot = Square(side_length=1.2, color=WANT, fill_opacity=0.0, stroke_width=0).move_to(
            box.get_corner(UR) + [-0.6, -0.6, 0])
        r = rat(scale=0.8).move_to(box.get_center() + [-0.8, -0.9, 0])
        wire = Line(r[2].get_center(), r[2].get_center() + [0.2, 1.2, 0], color=WANT, stroke_width=2)
        rows = rows_of([
            (r"1954, \ McGill: \ James Olds and Peter Milner implant an electrode in a rat's brain, \ aimed at the "
             r"brainstem", WHITE),
            (r"it lands somewhere else, \ near the septal area; \ a mild current comes on whenever the rat is in one "
             r"corner", WANT),
            (r"the rat keeps coming back to that corner, \ and soon will go anywhere the current is given", WANT),
        ], 5.8, 24, 0.36).move_to([3.4, 0.0, 0])
        tag = historical_tag(r"Olds \& Milner (1954)")
        with self.voiceover(
            "Montreal, 1954. <bookmark mark='a'/> James Olds, a young psychologist, and Peter Milner, a graduate "
            "student, are implanting electrodes in rats' brains at McGill. The target is a region in the brainstem "
            "thought to control arousal. <bookmark mark='b'/> One electrode misses, and ends up further forward, near "
            "a region called the septal area. When the rat wanders into one corner of its box, the experimenters "
            "turn on a mild current. <bookmark mark='c'/> The rat comes back to that corner, and back again. Within "
            "a short while they can steer it anywhere in the box, simply by switching the current on where they "
            "want it to go."
        ) as vo:
            self.play(Create(box), FadeIn(r), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(wire))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), hot.animate.set_fill(WANT, opacity=0.35))
            vo.wait_until("c")
            self.play(VGroup(r, wire).animate.move_to(hot.get_center() + [-0.2, -0.3, 0]), FadeIn(rows[2]),
                      run_time=2.0)
            self.play(VGroup(r, wire).animate.shift(DOWN * 2.2 + LEFT * 2.0), run_time=1.2)
            self.play(VGroup(r, wire).animate.move_to(hot.get_center() + [-0.2, -0.3, 0]), run_time=1.2)
        self.clear_scene()

    def lever(self):
        head = heading(r"A lever, \ and nothing else")
        rows = rows_of([
            (r"given a lever that turns the current on, \ rats press it, \ and press it again, \ by the thousand "
             r"an hour in later studies, \ until exhausted", WANT),
            (r"they cross an electrified floor to reach it, \ and with only a short time each day to choose between "
             r"food and the lever, \ some choose the lever and stop eating", LOST),
            (r"the press-rate depends on exactly where the electrode is: \ a map of reward in the brain", WHITE),
            (r"the newspapers called it the pleasure centre; \ forty years later the word pleasure would turn out "
             r"to be the mistake \ (chapter four)", MODEL),
        ], 12.4, 26, 0.38).move_to([0, 0.9, 0])
        base = Line([-1.6, -2.6, 0], [1.6, -2.6, 0], color=GREY_C, stroke_width=3)
        post = Line([1.0, -2.6, 0], [1.0, -1.8, 0], color=GREY_B, stroke_width=5)
        arm = Line([1.0, -1.8, 0], [0.3, -1.65, 0], color=WANT, stroke_width=6)
        r = rat(scale=0.7).move_to([-0.6, -2.25, 0])
        bolt = label(r"current on", font_size=18, color=WANT).next_to(post, RIGHT, buff=0.25)
        lever = VGroup(base, post, arm, r)
        tag = historical_tag(r"Olds \& Milner (1954); \ Olds (1958); \ Routtenberg \& Lindy (1965)")
        with self.voiceover(
            "Then they gave rats the switch. <bookmark mark='a'/> With a lever that turns the current on, rats "
            "pressed, and pressed again. In later studies with well-placed electrodes the rates ran to thousands "
            "of presses an hour, until the animals were exhausted. <bookmark mark='b'/> They crossed an electrified "
            "grid to reach the lever. And in 1965 Aryeh Routtenberg and Janet Lindy gave rats only a short time "
            "each day in which to choose between a food lever and a stimulation lever. Some chose the stimulation, "
            "and stopped eating. <bookmark mark='c'/> How hard a rat worked depended on exactly where its electrode "
            "was, so the experiments drew a map of reward across the brain. <bookmark mark='d'/> The newspapers "
            "called it the pleasure centre. Forty years later, the word pleasure would turn out to be the mistake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lever))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for _ in range(3):
                self.play(Rotate(arm, -0.25, about_point=arm.get_start()), FadeIn(bolt), run_time=0.3)
                self.play(Rotate(arm, 0.25, about_point=arm.get_start()), FadeOut(bolt), run_time=0.3)
            for m, row in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(row, shift=RIGHT * 0.15))
        self.clear_scene()

    def psyche(self):
        d = load("stim")
        head = heading(r"Psyche's learner, \ given the current")
        A = axes([0.2, 2.0], [0, 1.05], x_length=5.8, y_length=3.6, xticks=[0.5, 1.0, 1.5, 2.0],
                 yticks=[0, 0.5, 1.0], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"what the current is worth \ (food at its hungriest = 1)", ylabel=r"share, \ or store",
                 center=[-3.3, -0.3, 0], font_size=16)
        cs = curve(A.ax, d["value"], d["share"], WANT, 4)
        ce = curve(A.ax, d["value"], d["energy"], BODY, 4)
        key = legend([(WANT, r"presses on the current"), (BODY, r"energy store")], font_size=17)
        key.move_to(A.ax.c2p(1.62, 0.55))
        line = DashedLine(A.ax.c2p(1.0, 0), A.ax.c2p(1.0, 1.02), color=GREY_B, stroke_width=2)
        line_l = label(r"food at its hungriest", font_size=14, color=GREY_B).next_to(A.ax.c2p(1.0, 1.02), UP,
                                                                                    buff=0.06)
        rows = rows_of([
            (r"Psyche: \ Part 17's learner, \ with two levers; \ food is worth as much as it is hungry, \ and feeding "
             r"lowers the hunger", MODEL),
            (r"the current is worth the same whatever its state, \ and changes nothing in the body", WANT),
            (r"while the current is worth less than food can be, \ the learner eats when hungry and the store holds",
             BODY),
            (rf"past about {d['starve_at']:.1f}, \ it presses the current {pct(d['hi_share_end'])} of the time, "
             r"\ and the store runs out", LOST),
            (r"the learner is not wrong: \ it maximizes the reward it is given; \ the reward signal is what was "
             r"hijacked", WHITE),
        ], 5.6, 21, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.self\_stimulation}: \ 3{,}000 presses, \ five runs each")
        with self.voiceover(
            "Psyche can show why that happens without any pleasure at all. <bookmark mark='a'/> Take Part 17's "
            "learner, which learns the value of its actions from reward, and give it two levers. Food is worth as "
            "much as the learner is hungry, and eating lowers the hunger. <bookmark mark='b'/> The current is worth "
            "the same whatever the body's state, and changes nothing in it. <bookmark mark='c'/> While the current "
            "is worth less than food can ever be, the learner presses it when it is full and eats when it is hungry, "
            "and its energy store holds. <bookmark mark='d'/> Make the current worth a little more than food at its "
            f"hungriest, past about {d['starve_at']:.1f} on this scale, and the learner presses the current "
            f"{100 * d['hi_share_end']:.0f} percent of the time. The store runs out. <bookmark mark='e'/> The learner isn't "
            "making a mistake. It is maximizing exactly the reward it is given. What went wrong is that something "
            "reached the reward signal directly, without passing through the body's needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(line), FadeIn(line_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs), Create(ce), FadeIn(key), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ why do anything at all?")
        rows = rows_of([
            (r"drives as control loops: \ a thermostat, \ hunger, \ and why diets are regained", BODY),
            (r"curiosity, \ arousal, \ and a law that was not one", INTR),
            (r"wanting is not liking: \ dopamine, \ and a cue that changes value without being relearned", WANT),
            (r"rewards that undermine, \ goals that work, \ and your own discount curve", EXTR),
            (r"self-control: \ the depletion story, \ the marshmallow test, \ grit, \ and effort as a cost", CTRL),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So: why does anything do anything at all? <bookmark mark='a'/> We'll start where the body starts, with "
            "drives as control loops: a thermostat, hunger, and why weight lost on a diet comes back. "
            "<bookmark mark='b'/> Then motives no drive explains: curiosity, play, and a famous law about arousal "
            "that was never quite a law. <bookmark mark='c'/> Then the discovery that wanting and liking are "
            "different systems, and a cue whose value changes without being relearned. <bookmark mark='d'/> Then "
            "rewards that can undermine what they reward, goals that work, and a measurement of your own patience. "
            "<bookmark mark='e'/> And finally self-control, where several of psychology's most famous findings did "
            "not survive: ego depletion, the marshmallow test, grit, and what effort costs."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 28", font_size=34, color=GREY_B), label(r"Motivation", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"homeostasis as negative feedback, \ derived; \ a defended body weight, \ computed",
            r"curiosity, \ and what Yerkes and Dodson's mice actually showed",
            r"wanting against liking, \ and incentive salience computed",
            r"overjustification, \ goal-setting, \ and your discount curve measured",
            r"ego depletion: \ a literature of hundreds, \ and twenty-three laboratories' answer",
            r"delay of gratification, \ grit, \ and effort as a cost to be paid",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 28 of Psychology, Built, the first part of Act Six, on feeling and wanting: motivation. "
            "<bookmark mark='a'/> We'll derive homeostasis as negative feedback and compute a body weight that "
            "defends itself. We'll see what Yerkes and Dodson's mice actually showed. We'll separate wanting from "
            "liking, and compute incentive salience. We'll look at rewards that backfire, goals that work, and "
            "measure your own discount curve. We'll follow ego depletion from a literature of hundreds of studies to "
            "the twenty-three laboratories that tested it together, with their data. And we'll finish with delay of "
            "gratification, grit, and the idea that effort is a cost the brain chooses to pay."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
