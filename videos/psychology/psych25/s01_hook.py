from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


def dot_field(center=(0, 0, 0), radius: float = 2.0, n: int = 90, coherence: float = 0.2, direction: float = 0.0,
              speed: float = 1.2, seed: int = 0) -> VGroup:
    """A random-dot kinematogram: on every frame a share ``coherence`` of the dots steps in ``direction`` (radians),
    the rest in random directions; dots that leave the aperture reappear at a random place inside it."""
    rng = np.random.default_rng(seed)
    c = np.array(center, float)
    r = radius * np.sqrt(rng.random(n))
    th = 2 * np.pi * rng.random(n)
    pos = np.stack([r * np.cos(th), r * np.sin(th)], 1)
    dots = VGroup(*[Dot(c + np.array([p[0], p[1], 0]), radius=0.045, color=WHITE) for p in pos])
    state = {"pos": pos}

    def step(group, dt):
        if dt <= 0:
            return
        p = state["pos"]
        coh = rng.random(n) < coherence
        ang = np.where(coh, direction, 2 * np.pi * rng.random(n))
        p = p + speed * dt * np.stack([np.cos(ang), np.sin(ang)], 1)
        out = (p ** 2).sum(1) > radius ** 2
        if out.any():
            k = out.sum()
            rr = radius * np.sqrt(rng.random(k))
            tt = 2 * np.pi * rng.random(k)
            p[out] = np.stack([rr * np.cos(tt), rr * np.sin(tt)], 1)
        state["pos"] = p
        for d, q in zip(group, p):
            d.move_to(c + np.array([q[0], q[1], 0]))

    dots.add_updater(step)
    return dots


class Hook(VoiceoverScene):
    def construct(self):
        self.dots()
        self.story()
        self.question()
        self.objectives()

    def dots(self):
        stage = demo_stage(12.4, 5.2, center=[0, 0.35, 0])
        ap = Circle(radius=1.95, color=GREY_D, stroke_width=2).move_to([0, 0.35, 0])
        fix = Cross(scale_factor=0.08, stroke_color=YOU, stroke_width=3).move_to([0, 0.35, 0])
        ask1 = label(r"Which way are the dots drifting, \ left or right? \ Answer when you are sure.", font_size=28,
                     color=YOU).to_edge(DOWN, buff=0.75)
        ask2 = label(r"Now faster: \ answer the moment you have a guess.", font_size=28, color=SPEED
                     ).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Let's start on you. <bookmark mark='a'/> In a moment a cloud of dots will appear. Most move at random, "
            "but a few drift together, left or right. Decide which way, and say it out loud when you're sure."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(ap), FadeIn(fix), FadeIn(ask1))
        f1 = dot_field(center=[0, 0.35, 0], radius=1.9, coherence=0.12, direction=0.0, seed=1)
        self.add(f1)
        self.wait(7.0)
        self.remove(f1)
        f1.clear_updaters()
        with self.voiceover(
            "Right. They were drifting to the right. <bookmark mark='a'/> Now again, but this time as fast as you "
            "can: say the direction the moment you have any idea at all."
        ) as vo:
            arrow = Arrow([-1.0, 0.35, 0], [1.0, 0.35, 0], color=MODEL, buff=0)
            self.play(GrowArrow(arrow))
            vo.wait_until("a")
            self.play(FadeOut(arrow), FadeOut(ask1), FadeIn(ask2))
        f2 = dot_field(center=[0, 0.35, 0], radius=1.9, coherence=0.12, direction=np.pi, seed=2)
        self.add(f2)
        self.wait(2.0)
        self.remove(f2)
        f2.clear_updaters()
        arrow2 = Arrow([1.0, 0.35, 0], [-1.0, 0.35, 0], color=MODEL, buff=0)
        note = rows_of([
            (r"the first time you probably waited, \ and were right", WHITE),
            (r"the second time you answered sooner, \ and were less sure; \ often you would have been wrong",
             SPEED),
        ], 11.6, 25, 0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Left, this time. <bookmark mark='a'/> The first time, you probably waited, and you were probably right. "
            "<bookmark mark='b'/> The second time you answered sooner and felt less sure, and with dots this faint "
            "you'd often have been wrong. You traded accuracy for time, and you chose the rate of exchange."
        ) as vo:
            self.play(GrowArrow(arrow2), FadeOut(ask2))
            vo.wait_until("a")
            self.play(FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def story(self):
        head = heading(r"A walk to a boundary")
        items = [
            (r"1943", r"the Navy asks Columbia's Statistical Research Group: \ can a firing test stop as soon as the "
                      r"answer is clear? \ Abraham Wald: \ add up the evidence until it crosses a line", BOUND),
            (r"1978", r"Roger Ratcliff: \ a person deciding in half a second does the same; \ one model for accuracy, "
                      r"speed and the whole shape of the response-time distribution", EVIDENCE),
            (r"1996--2002", r"Michael Shadlen, \ William Newsome, \ Jamie Roitman: \ neurons in a monkey's parietal "
                            r"cortex climb toward a level, \ and the monkey answers when they reach it", MODEL),
        ]
        rows = VGroup()
        for yr, txt, c in items:
            rows.add(VGroup(label(yr, font_size=30, color=c), wrapped_label(txt, 10.4, 26, WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        for r in rows:
            r[1].shift(RIGHT * (2.3 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 1.0, 0])
        rng = np.random.default_rng(43)
        xs = np.linspace(-6.2, 4.6, 120)
        ys = np.cumsum(0.035 + 0.11 * rng.standard_normal(len(xs)))
        ys = -3.0 + ys - ys[0]
        hit = int(np.argmax(ys >= -1.75)) if (ys >= -1.75).any() else len(ys) - 1
        walk = VMobject(color=EVIDENCE, stroke_width=3).set_points_as_corners(
            [np.array([x, max(y, -3.3), 0]) for x, y in zip(xs[:hit + 1], ys[:hit + 1])])
        line_b = DashedLine([-6.4, -1.75, 0], [6.4, -1.75, 0], color=BOUND, stroke_width=2)
        bl = label(r"a boundary", font_size=18, color=BOUND).next_to(line_b, UP, buff=0.05).align_to(line_b, RIGHT)
        stop = Dot(walk.get_end(), radius=0.08, color=MODEL)
        tag = historical_tag(r"Wallis (1980); \ Wald (1945, \ 1947); \ Ratcliff (1978); \ Roitman \& Shadlen (2002)")
        with self.voiceover(
            "What you just did has a history in three steps. <bookmark mark='a'/> In 1943 the US Navy asked a "
            "statistics group at Columbia University whether a firing test of ammunition could be stopped early, once "
            "the answer was clear. Milton Friedman and W. Allen Wallis couldn't settle it, and took it to Abraham "
            "Wald. He worked out how: add up the evidence, shot by shot, until it crosses a line. Five years later "
            "he and Jacob Wolfowitz proved that no test with the same error rates stops sooner on average. "
            "<bookmark mark='b'/> In 1978 Roger Ratcliff proposed that a person deciding in half a second does the "
            "same, and showed that the proposal accounts for accuracy, speed, and the whole shape of the "
            "distribution of response times at once. <bookmark mark='c'/> And around the turn of the century "
            "Michael Shadlen, William Newsome and Jamie Roitman recorded neurons in a monkey's parietal cortex that "
            "climb toward a level while the monkey watches moving dots, and the monkey answers when they reach it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(line_b), FadeIn(bl))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "a":
                    self.play(Create(walk), run_time=4, rate_func=linear)
                    self.play(FadeIn(stop, scale=1.5))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ why does a decision take the time it takes?")
        rows = rows_of([
            (r"two old laws, \ Hick's and Fitts's, \ and the trade between speed and accuracy", BOUND),
            (r"what a response-time distribution looks like, \ and why its mean misleads", EVIDENCE),
            (r"Wald's test, \ and the diffusion model it became, \ fitted to 17 people and 3 people's open data",
             DRIFT),
            (r"fast errors, \ slow errors, \ and accumulators recorded in the brain", MODEL),
            (r"races, \ stopping, \ and the feeling of being sure", TIME),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So why does a decision take the time it takes? <bookmark mark='a'/> We'll start with two old laws of "
            "response time, and the trade between speed and accuracy that every model has to produce. "
            "<bookmark mark='b'/> Then what a distribution of response times looks like, and why its mean misleads. "
            "<bookmark mark='c'/> Then Wald's test, and the diffusion model it became, fitted to the open data of "
            "seventeen people and then of three. <bookmark mark='d'/> Then fast errors and slow errors, and "
            "accumulators in the brain. <bookmark mark='e'/> And finally races, stopping, and the feeling of being "
            "sure."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 25", font_size=34, color=GREY_B), label(r"Deciding in Time", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Hick's and Fitts's laws, \ and the speed--accuracy trade-off drawn",
            r"Wald's sequential test, \ and why it is optimal",
            r"the diffusion model: \ closed forms derived, \ distributions computed",
            r"selective influence tested on 17 people's speed and accuracy blocks",
            r"accumulators in parietal cortex, \ and the ramping--stepping dispute",
            r"the stop-signal race, \ and confidence as the balance of evidence",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 25 of Psychology, Built, the eighth part of Act Five, on thinking: deciding in time. "
            "<bookmark mark='a'/> We'll draw the old laws of choice time and the trade between speed and accuracy. "
            "We'll run Wald's test and see why nothing beats it. We'll derive the diffusion model's predictions, "
            "compute its distributions, and test, on seventeen people's open data, whether its parameters mean what "
            "they claim. We'll look at accumulators in the brain and the dispute over whether they ramp or step, and "
            "finish with the race to stop and the balance of evidence we call confidence."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
