from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403

INST = (("piano", r"piano \ (trained on)", TUNE), ("harp", r"plucked harp", BLUE), ("organ", r"organ", EAR), ("strings", r"bowed strings", GREY_B))


class Timbre(SoundScene):
    def construct(self):
        chapter(self, 7, r"Timbres never heard", r"Does a transcriber trained on a piano hear an organ?")
        self.four()
        self.table()
        self.quiz()
        self.why()

    # ------------------------------------------------------------------
    def four(self):
        d = load("timbres")
        c = clip("timbres.four")
        boxes = choice_boxes([n for _, n, _ in INST], width=2.9, height=0.9, buff=0.3, size=18, colors=[col for _, _, col in INST]).move_to(UP * 0.5)
        note = label(r"the same notes, \ the same answer key: \ only the timbre changes", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"one piece, \ four instruments", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is one test piece on four instruments: the piano both transcribers learnt from, then a plucked harp, an organ and bowed strings, none of which either has ever heard."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        keys = [k for k, _, _ in INST]
        with self.listen(c) as snd:
            window(snd, r"four timbres", kind="physical model", detail=r"piano, \ harp, \ organ, \ strings", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        n, m = load("nmf")["scores"], load("net")["scores"]
        g = VGroup()
        for k, name, col in INST:
            g.add(VGroup(label(name, font_size=20, color=col), label(f"{n[k]['f']:.2f}", font_size=22, color=WHITE), label(f"{m[k]['f']:.2f}", font_size=22, color=WHITE)))
        g.arrange(DOWN, buff=0.45)
        for r in g:
            r[0].set_x(-3.4)
            r[1].set_x(0.8)
            r[2].set_x(3.6)
        top = VGroup(label(r"NMF \ (piano templates)", font_size=17, color=GREY_A).move_to([0.8, g.get_top()[1] + 0.5, 0]),
                     label(r"the network \ (piano-trained)", font_size=17, color=GREY_A).move_to([3.6, g.get_top()[1] + 0.5, 0]))
        note = label(r"note F-measure on 12 test pieces per instrument \ (onset within 50 ms)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"trained on one timbre, \ tested on four", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        worst_n = min((k for k, _, _ in INST), key=lambda k: n[k]["f"])
        worst_m = min((k for k, _, _ in INST), key=lambda k: m[k]["f"])
        with self.voiceover(
            "And the scores. <bookmark mark='a'/> On the piano, both do well. <bookmark mark='b'/> On the instruments they never "
            f"heard, both fall: the factorization worst on the {worst_n}, the network worst on the {worst_m}. A template of a "
            "piano note does not fit an organ's partials, and a network that has only seen hammers does not know what a bow "
            "does to the start of a note. <bookmark mark='c'/> This is the field's central difficulty, measured exactly: "
            "transcribers are only as general as what they were shown."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g[1:]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(g[1:], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("net")
        c = clip("net.two")
        card = listen_card(r"A piece on the organ, \ and the network's transcription of it played back on the same organ. \ "
                           r"Which was the original?", width=9.5)
        with self.voiceover("Your turn. A piece on the organ, and the network's transcription of it, played back on the same organ. Which was the original?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"original or copy?", kind="synthesized", detail=r"an additive organ", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        ps = d["piece_scores"]
        res = label(rf"the first: \ the copy found {ps['hits']} of {ps['ref']} notes \ and added {ps['est'] - ps['hits']} that were not there", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The first was the original. The copy found {say(ps['hits'])} of its {say(ps['ref'])} notes and added "
            f"{say(ps['est'] - ps['hits'])} that were not there; you may have heard notes drop out, or stray notes an octave or "
            "a twelfth away, where the organ's partials fooled the network."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"train on many timbres: \ the remedy, \ and Monochord can render as many as it likes", WHITE),
            (r"augment: \ change the brightness, \ the room, \ the noise, \ the tuning, \ at random, \ in training", WHITE),
            (r"but rendered sound is not recorded sound: \ the `sim-to-real' gap of robotics, \ in music", WHITE),
            (r"the honest test is always a timbre, \ a room and a player the system never met", TUNE),
        ]
        rows_scene(self, r"what to do about it", items,
                   "What to do about it? <bookmark mark='b'/> Train on many timbres: the obvious remedy, and Monochord can render as "
                   "many as it likes. <bookmark mark='c'/> Augment: change the brightness, the room, the noise and the tuning at "
                   "random during training. <bookmark mark='d'/> But rendered sound is not recorded sound; robotics calls it the "
                   "gap from simulation to reality, and music has it too. <bookmark mark='e'/> The honest test is always a timbre, "
                   "a room and a player the system never met.", marks="bcde")
