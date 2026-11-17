from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.radar()
        self.clock()
        self.objection()
        self.objectives()

    def _scope(self, radius: float = 2.2):
        disc = Circle(radius=radius, color=GREY_C, stroke_width=3, fill_color="#0d1a14", fill_opacity=1.0)
        rings = VGroup(*[Circle(radius=radius * f, color="#2f5a45", stroke_width=1.5) for f in (0.33, 0.66)])
        cross = VGroup(Line(LEFT * radius, RIGHT * radius, color="#2f5a45", stroke_width=1.5),
                       Line(DOWN * radius, UP * radius, color="#2f5a45", stroke_width=1.5))
        rng = np.random.default_rng(4)
        speck = VGroup()
        for _ in range(70):
            r, a = radius * np.sqrt(rng.random()) * 0.97, rng.random() * TAU
            speck.add(Dot([r * np.cos(a), r * np.sin(a), 0], radius=0.025, color="#3f8f66", fill_opacity=0.25 + 0.4 * rng.random()))
        sweep = Line(ORIGIN, UP * radius, color="#5BD18B", stroke_width=4)
        return VGroup(disc, rings, cross, speck), sweep

    def radar(self):
        head = heading(r"Over the sea, \ the 1940s")
        scope, sweep = self._scope()
        g = VGroup(scope, sweep).move_to([-3.6, -0.3, 0])
        blip = Dot(scope[0].get_center() + np.array([0.9, 0.7, 0]), radius=0.13, color="#b8ffd6", fill_opacity=0.95)
        ghost = Dot(scope[0].get_center() + np.array([-1.1, -0.5, 0]), radius=0.12, color="#b8ffd6", fill_opacity=0.85)
        rows = rows_of([
            (r"an aircraft hunting submarines by radar; \ an observer watching a screen for hours", WHITE),
            (r"a real contact is a faint blip among specks of noise", SIGNALC),
            (r"observers missed real contacts, \ and more as the watch went on", MISS),
            (r"and sometimes they reported a blip that was nothing", FA),
        ], 5.4, 30, 0.34).move_to([3.6, 0.0, 0])
        keep_in_frame(rows)
        tag = note(r"a drawing of a radar screen, \ not a record").to_corner(DR, buff=0.3)
        with self.voiceover(
            "In the Second World War, British aircraft hunted submarines by radar. Hour after hour, an "
            "observer watched a dim screen for a small blip. <bookmark mark='a'/> A real contact was a faint "
            "spot among specks of noise that came and went with every sweep. <bookmark mark='b'/> The Royal "
            "Air Force found that its observers missed real contacts, and missed more as a patrol wore on. "
            "<bookmark mark='c'/> And sometimes they reported a contact that was nothing at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(scope), FadeIn(rows[0]))
            self.play(Rotate(sweep, -TAU, about_point=scope[0].get_center(), rate_func=linear), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(blip), FadeIn(rows[1]))
            self.play(Rotate(sweep, -TAU, about_point=scope[0].get_center(), rate_func=linear), blip.animate.set_opacity(0.4),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(blip, color=MISS), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(ghost), Indicate(ghost, color=FA), FadeIn(rows[3]))
        self.clear_scene()

    def clock(self):
        src = archive.MACKWORTH_1948
        head = heading(r"The Clock Test, \ 1948")
        face = Circle(radius=2.0, color=GREY_B, stroke_width=4).move_to([-3.6, -0.3, 0])
        ticks = VGroup(*[Line(face.get_center() + 1.8 * np.array([np.sin(a), np.cos(a), 0]),
                              face.get_center() + 1.95 * np.array([np.sin(a), np.cos(a), 0]), color=GREY_C, stroke_width=2)
                         for a in np.linspace(0, TAU, 100, endpoint=False)])
        hand = Line(face.get_center(), face.get_center() + UP * 1.7, color=WHITE, stroke_width=5)
        rows = rows_of([
            (r"Norman Mackworth's laboratory version: \ a pointer that jumps one step every second", WHITE),
            (r"now and then it jumps two: \ report it", SIGNALC),
            (r"two hours of watching: \ the reports of double jumps fell as the watch went on", MISS),
            (r"the vigilance decrement. \ But what fell?", THRESH),
        ], 5.4, 30, 0.34).move_to([3.6, 0.0, 0])
        keep_in_frame(rows)
        tags = VGroup(historical_tag(src.cite), note(r"the clock: \ a drawing").to_corner(DR, buff=0.3))
        step = TAU / 100
        with self.voiceover(
            "The Air Force asked a psychologist, Norman Mackworth, why. In 1948 he published a laboratory "
            "version of the watch. <bookmark mark='a'/> A pointer moves round a blank clock face in small "
            "jumps, one a second. <bookmark mark='b'/> Now and then it jumps twice as far, and the observer "
            "presses a key. <bookmark mark='c'/> Two hours of this, and the double jumps reported fell as "
            "the watch went on. <bookmark mark='d'/> It's called the vigilance decrement, and it's real. But "
            "a miss can mean two different things. The observer didn't see the jump. Or the observer saw "
            "something, and wasn't sure enough to say so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), Create(face), FadeIn(ticks), FadeIn(hand))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for _ in range(3):
                self.play(Rotate(hand, -step, about_point=face.get_center()), run_time=0.35)
                self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            self.play(Rotate(hand, -2 * step, about_point=face.get_center()), hand.animate.set_color(SIGNALC), run_time=0.4)
            self.play(hand.animate.set_color(WHITE), run_time=0.4)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def objection(self):
        board = wager_board((
            (r"a law of the mind with a constant in it; \ thresholds fitted with intervals. \ Whether a sensation has a size: \ "
             r"still argued", STATUS_COLOR["replicated, smaller"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave", STATUS_COLOR["replicated"]),
            (r"every ``yes'' mixes what was seen with the willingness to say so: \ can the two be separated?",
             STATUS_COLOR["contested"]),
        ))
        hl = SurroundingRectangle(board.rows[2], color=KANT, buff=0.15, corner_radius=0.1)
        q = wrapped_label(r"Today's question: \ when you say ``yes, I saw it'', \ how much is seeing and how much is "
                          r"saying?", 12.0, 30, THRESH).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Kant's third objection was that observing the mind disturbs it: whatever a person reports is "
            "coloured by the reporting. Part 11 gave the first objection a strong reply. "
            "<bookmark mark='a'/> The third is still open, and the radar observer shows why. Every yes "
            "mixes what was seen with the willingness to say so. <bookmark mark='b'/> Today's question is "
            "whether the two can be pulled apart. When you say yes, I saw it, how much of that is seeing, "
            "and how much is saying?"
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows], *[FadeIn(r.reply) for r in board.rows])
            vo.wait_until("a")
            self.play(Create(hl))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 12", font_size=34, color=GREY_B), label(r"Signal and Noise", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"four outcomes, \ and why a hit rate alone means nothing",
            r"two distributions and a line: \ sensitivity $d'$ and criterion $c$",
            r"the ROC, \ and your own from a memory test",
            r"the ideal observer: \ where to draw the line, \ given base rates and payoffs",
            r"rival models, \ and how the shape of an ROC tells them apart",
            r"rare targets, \ base rates and the screens that run on this theory",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part twelve: signal and noise. <bookmark mark='a'/> We'll start with the four outcomes of a "
            "detection, and why a hit rate on its own means nothing. <bookmark mark='b'/> Then the theory: two "
            "distributions and a line, giving two numbers, one for seeing and one for saying. "
            "<bookmark mark='c'/> The ROC, and your own, from a memory test. <bookmark mark='d'/> The ideal "
            "observer, and where the line should go. <bookmark mark='e'/> Rival models, and how the shape of a "
            "curve decides between them. <bookmark mark='f'/> And rare targets, base rates, and the screens "
            "and alarms that run on this theory every day."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
