from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Contrast(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.gorilla()
        self.priming()

    def card(self):
        card = chapter_card(1, r"The contrastive method", r"How do you study experience with an experiment?",
                            lit={1988: r"Baars", 1990: r"Crick \& Koch", 1998: r"Dehaene et al.",
                                 1999: r"Simons \& Chabris"},
                            part=PART, scale=("mind", "brain"), marr=("what",))
        with self.voiceover("Chapter one. The contrastive method."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def method(self):
        head = heading(r"Hold the stimulus fixed; \ vary awareness")
        boxes = VGroup()
        for name, txt, col in [
            (r"masking", r"the same target, \ seen or not, \ by a few milliseconds of timing", SEEN),
            (r"binocular rivalry", r"a different image in each eye: \ the input is constant, \ the percept "
                                   r"alternates", GNW),
            (r"inattention", r"in plain view, \ unnoticed while attention is elsewhere", HOT),
            (r"neglect and extinction", r"after damage to the right parietal lobe, \ the left side ignored, \ "
                                        r"though processed", LOST),
        ]:
            box = RoundedRectangle(corner_radius=0.12, width=3.0, height=3.0, stroke_color=col, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            body = VGroup(label(name, font_size=23, color=col), wrapped_label(txt, 2.6, 19, WHITE)).arrange(
                DOWN, buff=0.3).move_to(box)
            boxes.add(VGroup(box, body))
        boxes.arrange(RIGHT, buff=0.25).move_to([0, 0.6, 0])
        rows = rows_of([
            (r"Baars, \ 1988: \ compare conscious and unconscious processing of the same thing; \ the difference is "
             r"what consciousness adds", WHITE),
            (r"Crick and Koch, \ 1990: \ look for the neural correlates of consciousness, \ the minimal activity "
             r"sufficient for an experience", MODEL),
        ], 12.0, 24, 0.3).to_edge(DOWN, buff=0.75)
        tag = historical_tag(r"Baars (1988); \ Crick \& Koch (1990)")
        with self.voiceover(
            "For most of the twentieth century, consciousness was thought too private to study. The way in was a "
            "simple design. <bookmark mark='a'/> Keep the stimulus the same and vary whether it's experienced. "
            "Masking does it with timing; binocular rivalry, by showing each eye a different image, so the input is "
            "constant while the percept alternates; inattention, by drawing attention elsewhere; and some patients "
            "with damage to the right parietal lobe ignore the left side of space, though their brains still "
            "process it. <bookmark mark='b'/> Bernard Baars called this the contrastive method, in 1988: whatever "
            "differs between conscious and unconscious processing of the same thing is what consciousness adds. "
            "<bookmark mark='c'/> Two years later Francis Crick and Christof Koch proposed looking for its neural "
            "correlates: the minimal activity in the brain sufficient for a particular experience."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.7), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def gorilla(self):
        head = heading(r"Inattentional blindness")
        court = RoundedRectangle(corner_radius=0.1, width=5.6, height=3.4, stroke_color=GREY_C, stroke_width=2,
                                 fill_color=GREY_E, fill_opacity=0.3).move_to([-3.4, 0.4, 0])
        rng = np.random.default_rng(3)
        players = VGroup()
        for k in range(6):
            col = WHITE if k < 3 else GREY_D
            p = np.array([-3.4 + rng.uniform(-2.2, 2.2), 0.4 + rng.uniform(-1.2, 1.2), 0])
            players.add(Circle(radius=0.2, color=col, fill_opacity=1).move_to(p))
        gor = VGroup(Circle(radius=0.32, color=GREY_B, fill_opacity=0.9, stroke_width=0),
                     label(r"?", font_size=26, color=BLACK)).move_to([-3.2, 0.4, 0])
        rows = rows_of([
            (r"Simons and Chabris, \ 1999: \ count the white team's passes", WHITE),
            (r"a person in a gorilla suit walks through the game, \ stops, \ thumps its chest, \ and leaves", HOT),
            (r"about half the watchers never noticed it", LOST),
            (r"the gorilla reached the eyes, \ and it was not experienced; \ attention and consciousness are "
             r"close, \ but not the same \ (chapter twelve)", MODEL),
        ], 5.6, 22, 0.32).move_to([3.4, 0.2, 0])
        tag = published_tag(r"Simons \& Chabris (1999)")
        with self.voiceover(
            "The most famous demonstration of inattention is a video. <bookmark mark='a'/> In 1999 Daniel Simons "
            "and Christopher Chabris asked people to count the passes made by a team in white while another team "
            "in black passed a second ball. <bookmark mark='b'/> Partway through, a person in a gorilla suit walks "
            "into the middle of the game, faces the camera, thumps its chest, and walks off. "
            "<bookmark mark='c'/> About half the watchers never noticed it. <bookmark mark='d'/> The gorilla was "
            "in plain view, on their retinas for several seconds, and it wasn't experienced. Attention and "
            "consciousness are close, but chapter twelve will show they're not the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(court), FadeIn(players))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(*[p.animate.shift(np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.4, 0.4), 0]))
                        for p in players], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(gor), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def priming(self):
        head = heading(r"What an unseen stimulus can do")
        seq = VGroup()
        for t, lab_, col in [(r"\#\#\#\#", r"mask", GREY_B), (r"7", r"prime, \ 43 ms", UNSEEN),
                             (r"\#\#\#\#", r"mask", GREY_B), (r"9", r"target", SEEN)]:
            box = Square(side_length=1.4, stroke_color=col, stroke_width=2, fill_color=BLACK, fill_opacity=0.6)
            seq.add(VGroup(box, label(t, font_size=36, color=col).move_to(box),
                           label(lab_, font_size=18, color=col).next_to(box, DOWN, buff=0.15)))
        seq.arrange(RIGHT, buff=0.35).move_to([0, 1.5, 0])
        rows = rows_of([
            (r"Dehaene and colleagues, \ 1998: \ is the target larger or smaller than 5? \ a masked prime on the same "
             r"side speeds the answer, \ though people cannot report it", WHITE),
            (r"the prime reached meaning, \ and even prepared a response in motor cortex", UNSEEN),
            (r"later work: \ masked priming is real but smaller than first reported, \ and claims that the prime "
             r"was truly invisible depend on how awareness was measured", LOST),
        ], 12.0, 24, 0.32).move_to([0, -1.4, 0])
        tag = published_tag(r"Dehaene et al.\ (1998); \ Van den Bussche et al.\ (2009)")
        with self.voiceover(
            "What can an unseen stimulus do? <bookmark mark='a'/> In 1998 Stanislas Dehaene and colleagues showed "
            "a number for about forty milliseconds, sandwiched between masks, then a second, visible number, and "
            "asked whether the visible one was larger or smaller than five. <bookmark mark='b'/> When the hidden "
            "prime fell on the same side of five as the target, answers were faster, though people couldn't report "
            "the prime, and brain imaging showed it had prepared a response in motor cortex. Meaning, it seemed, "
            "without awareness. <bookmark mark='c'/> Later work found masked priming real but smaller than the first "
            "reports, and showed that whether a prime was truly invisible depends on how awareness was measured, "
            "which is the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in seq], lag_ratio=0.5), FadeIn(rows[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
