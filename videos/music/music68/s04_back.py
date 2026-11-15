from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Back(SoundScene):
    def construct(self):
        chapter(self, 3, r"Back up the chain", r"Can a machine recover the score from what the chain delivers?")
        self.listener()
        self.calibration()
        self.results()
        self.which()
        self.score_()
        self.quiz()

    # ------------------------------------------------------------------
    def listener(self):
        items = [
            (r"onsets: \ where the spectrum's energy jumps \ (spectral flux, \ Part 61), \ or rises above everything in the last few frames \ (SuperFlux)", WHITE),
            (r"pitch, \ one way: \ YIN's period over the note \ (Part 61)", WHITE),
            (r"pitch, \ another: \ the note whose harmonics gained the most energy at the onset \ (harmonic summation, \ Part 61)", WHITE),
            (r"then a score: \ note values and a drifting tempo, \ by dynamic programming \ (Part 61); \ then a key \ (Part 15)", WHITE),
            (r"the Tune is one line, \ so the machine listens for one line", TUNE),
        ]
        rows_scene(self, r"how the machine listens", items,
                   "The way back starts with a machine that listens, assembled from Part 61's tools. <bookmark mark='b'/> It "
                   "finds onsets where the spectrum's energy jumps; or, in a refinement called SuperFlux, from Böck and Widmer, "
                   "where it rises above everything in the last few frames, so that energy which flickers on and off does not "
                   "count as a new note. <bookmark mark='c'/> It can read each note's pitch one way, "
                   "with YIN, from the period of the sound over the note. <bookmark mark='d'/> Or another way: the note whose "
                   "harmonics gained the most energy at the onset. <bookmark mark='e'/> Then it writes a score: note values and a "
                   "tempo that may drift, found by dynamic programming, and a key. <bookmark mark='f'/> The Tune is one line, so "
                   "the machine listens for one line.", marks="bcdef")

    # ------------------------------------------------------------------
    def calibration(self):
        d = load("calibrate")
        rates = [(r"YIN over the note", d["mean"][d["best_yin"]], GREY_B), (r"onset reading, \ spectral flux", d["mean"][d["best_flux"]], BLUE),
                 (r"onset reading, \ SuperFlux", d["mean"][d["best"]], TUNE)]
        top = max(v for _, v, _ in rates)
        bars = VGroup()
        for i, (name, v, col) in enumerate(rates):
            b = Rectangle(width=1.5, height=max(0.04, 3.0 * v / top), stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-3.6 + 3.6 * i, -1.6 + b.height / 2, 0])
            bars.add(VGroup(b, label(rf"{100 * v:.0f}\%", font_size=24, color=WHITE).next_to(b, UP, buff=0.1),
                            label(name, font_size=17, color=col).next_to([b.get_x(), -1.6, 0], DOWN, buff=0.2)))
        cap = label(rf"wrong keys per written note, \ averaged over all nine stages, \ {d['notes']} notes of four other tunes: \ "
                    + r", \ ".join(d["tunes"]), font_size=15, color=GREY_A).to_edge(DOWN, buff=0.35)
        if cap.width > 13:
            cap.scale_to_fit_width(13)
        head = label(r"choosing the settings, \ on other tunes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        rs = [round(100 * v) for _, v, _ in rates]
        with self.voiceover(
            "Before the Tune was sent, the machine's settings were chosen on four other tunes sent down the same chain: "
            f"{', '.join(d['tunes'][:-1])} and {d['tunes'][-1]}, {say(d['notes'])} notes in all. Each way of listening was "
            "given its best settings. <bookmark mark='a'/> With YIN, "
            f"{say(rs[0])} per cent of the keys came back wrong, averaged over all nine stages. The reason is the piano: "
            "each note rings on through its release while the next begins, and YIN, reading the whole sound, is pulled "
            "between the two; what changed at the onset is the new note alone. <bookmark mark='b'/> Reading the onset, "
            f"{say(rs[1])} per cent. <bookmark mark='c'/> With SuperFlux as well, {say(rs[2])} per cent, mostly because the "
            "coder's flickering bands stop counting as notes. So the machine listens that way, and the Tune was never used "
            "to choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            for m, bb in zip("abc", bars):
                vo.wait_until(m)
                self.play(FadeIn(bb))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = load("roundtrip")
        r = d["rows"]
        vals = {k: r[k]["pitch_errors"] for k in STAGES}
        top = max(max(vals.values()), 4)
        bars = stage_bars(vals, 0, top, width=11.6, height=2.8, fmt=lambda v: f"{v:d}", center=DOWN * 0.3)
        head = label(r"wrong keys, \ of 42, \ in the line the machine wrote down", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        f = VGroup(*[label(rf"{r[k]['note_f']:.2f}", font_size=14, color=EAR).next_to(bars.bars[i], DOWN, buff=0.55) for i, k in enumerate(STAGES)])
        fl = label(r"note F \ (pitch, \ and onset within 50 ms)", font_size=14, color=EAR).next_to(f, DOWN, buff=0.15)
        with self.voiceover(
            "And here is the Tune. For each stage, the number of the forty-two keys that came back wrong, counted by edit "
            f"distance. <bookmark mark='a'/> As written: {say(vals['score'])}. Performed: {say(vals['played'])}. In the room: "
            f"{say(vals['room'])}. Through the microphone: {say(vals['mic'])}. Mastered: {say(vals['master'])}. "
            f"<bookmark mark='b'/> Through the coder at a hundred and twenty-eight kilobits: {say(vals['codec128'])}; at "
            f"sixty-four, {say(vals['codec64'])}; at thirty-two, {say(vals['codec32'])}; at sixteen, {say(vals['codec16'])}. "
            "<bookmark mark='c'/> Below, the note F score, which also asks that each onset be within fifty milliseconds of "
            "the performance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars[-1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars.bars[:5]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars.bars[5:]], lag_ratio=0.2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(f), FadeIn(fl))
        self.wait(0.6)
        self.clear_scene()
        net = {k: r[k]["net_f"] for k in STAGES}
        items = [
            (rf"Part 61's network, \ trained on random polyphony: \ note F {net['played']:.2f} performed, \ {net['master']:.2f} mastered, \ {net['codec16']:.2f} at 16 kbit/s", WHITE),
            (rf"the one-line machine: \ {r['played']['note_f']:.2f}, \ {r['master']['note_f']:.2f}, \ {r['codec16']['note_f']:.2f}", TUNE),
            (r"a general tool loses to a narrow one on the narrow task: \ the network expects chords and finds ghosts of them in the room", WHITE),
        ]
        rows_scene(self, r"beside Part 61's network", items,
                   "How does that compare with Part 61's network, which was trained on random polyphony? <bookmark mark='b'/> Its "
                   f"note F is {say(net['played'], 2)} on the performance, {say(net['master'], 2)} mastered, and "
                   f"{say(net['codec16'], 2)} at sixteen kilobits. <bookmark mark='c'/> The one-line machine scores "
                   f"{say(r['played']['note_f'], 2)}, {say(r['master']['note_f'], 2)} and {say(r['codec16']['note_f'], 2)}. "
                   "<bookmark mark='d'/> A general tool can lose to a narrow one on a narrow task: the network expects chords, "
                   "and finds ghosts of them in the room's reverberation.", marks="bcd")

    # ------------------------------------------------------------------
    def which(self):
        r = load("roundtrip")["rows"]
        moves = {k: r[k]["moves_found"] for k in STAGES}
        rest = {k: r[k]["restrikes_found"] for k in STAGES}
        b1 = stage_bars(moves, 0, 24, width=11.6, height=1.5, fmt=lambda v: f"{v:d}", font_size=14, center=UP * 1.2)
        b2 = stage_bars(rest, 0, 18, width=11.6, height=1.5, fmt=lambda v: f"{v:d}", font_size=14, colors={k: BLUE for k in STAGES}, center=DOWN * 1.75)
        t1 = label(r"notes that change key: \ found, \ of 24", font_size=17, color=TUNE).next_to(b1, UP, buff=0.15)
        t2 = label(r"notes that repeat the key before: \ found, \ of 18", font_size=17, color=BLUE).next_to(b2, UP, buff=0.15)
        ex = r["codec32"]["extra"], r["codec16"]["extra"]
        with self.voiceover(
            "Which notes go wrong? Split them in two. <bookmark mark='a'/> The Tune has twenty-four notes that change key: "
            f"as written all {say(moves['score'])} come back, through the room and the microphone {say(moves['room'])}, and "
            f"after the master between {say(min(moves[k] for k in STAGES[4:]))} and {say(max(moves[k] for k in STAGES[4:]))}. "
            "<bookmark mark='b'/> And eighteen that repeat the key before: C, C; G, G. Those are the weak spot at every "
            f"stage, {say(rest['score'])} found as written and {say(min(rest.values()))} at worst. A re-struck key adds "
            "little that is new to the spectrum. And the master's limiter, which flattens every attack, costs notes of both "
            "kinds: most of the loss arrives there, and the coders add little to it. The two lowest rates add something else: {say(ex[0])} and "
            f"{say(ex[1])} onsets where there was no note, the coder's own."
        ) as vo:
            self.play(FadeIn(VGroup(t1, b1, t2, b2).copy().set_opacity(0.15)))   # a ghost of what is coming
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(b1))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(b2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def score_(self):
        d = load("roundtrip")
        r = d["rows"]["master"]
        n = 14
        want = list(zip(d["want_keys"][:n], d["want_values"][:n]))
        got = list(zip(r["keys"][:n], r["values"][:n]))
        name = lambda m: LETTER[m % 12]
        val = lambda v: {0.5: r"$\frac12$", 1.0: r"1", 1.5: r"$1\frac12$", 2.0: r"2", 3.0: r"3", 4.0: r"4"}.get(v, f"{v:g}")

        def row(seq, color):
            g = VGroup()
            for m, v in seq:
                g.add(VGroup(label(name(m), font_size=20, color=color), label(val(v), font_size=15, color=GREY_A)).arrange(DOWN, buff=0.08))
            return g.arrange(RIGHT, buff=0.32)

        a, b = row(want, WHITE), row(got, TUNE)
        for i, (w, g) in enumerate(zip(want, got)):
            if w != g:
                b[i][0].set_color(RED) if w[0] != g[0] else b[i][1].set_color(RED)
        grid = VGroup(VGroup(label(r"written", font_size=18, color=GREY_B), a).arrange(RIGHT, buff=0.4),
                      VGroup(label(r"recovered", font_size=18, color=GREY_B), b).arrange(RIGHT, buff=0.4)).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(UP * 0.4)
        tot = d["rows"]
        notes = VGroup(
            label(rf"from the master: \ {tot['master']['score_errors']} edits turn the whole recovered score into the written one \ (keys and note values)", font_size=17, color=WHITE),
            label(rf"its tempo: \ {tot['master']['bpm']:.0f} beats a minute \ (played at 120, \ with rubato)", font_size=17, color=WHITE),
            label(rf"its key, \ weighting notes by the lengths it wrote: \ {tot['played']['key']} from the performance on; \ counting notes alone: \ {tot['played']['key_by_count']}", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"the first two phrases, \ written and recovered from the master", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the score itself, keys and note values together, for the first two phrases recovered from the master. "
            "<bookmark mark='a'/> Red marks what differs. <bookmark mark='b'/> Over the whole Tune, "
            f"{say(tot['master']['score_errors'])} edits turn the recovered score into the written one. The tempo it found is "
            f"{say(round(tot['master']['bpm']))} beats a minute, for a performance played at a hundred and twenty with rubato. "
            f"And the key: from the performance on, the key finder names {tot['played']['key']}. Counting the recovered notes "
            f"alone, without the lengths the quantizer gave them, it names {tot['played']['key_by_count']}. The pitches were "
            "right; the rhythm misled it. A missed repeat lengthens the note before it, and the lengths it wrote give D "
            "and G more time than the score does, and C less: the weight of G major."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid[0]))
            vo.wait_until("a")
            self.play(FadeIn(grid[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in notes], lag_ratio=0.3), run_time=1.5)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("back")
        c = clip("back.three")
        card = listen_card(r"Three scores a machine wrote down, \ played back strictly: \ one from the master, \ "
                           r"one from 32 kbit/s, \ one from 16 kbit/s, \ in a shuffled order. \ Which came from where?", width=9.6)
        with self.voiceover(
            "Three scores the machine wrote down, played back strictly on the piano: one from the master, one from thirty-two "
            "kilobits, one from sixteen, in a shuffled order. Which came from where?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"A", r"B", r"C"], width=2.6, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        ks = ["A", "B", "C"]
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", kind="physical model", detail=r"recovered scores, \ replayed on Part 38's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        name = {"master": r"the master", "codec32": r"32 kbit/s", "codec16": r"16 kbit/s"}
        ans = VGroup(*[label(rf"{k}: \ {name[s]}, \ {d['errors'][s]} wrong keys in the whole Tune", font_size=19, color=TUNE) for k, s in zip(ks, d["order"])]).arrange(DOWN, buff=0.22).move_to(DOWN * 1.6)
        sp = {"master": "the master", "codec32": "thirty-two kilobits", "codec16": "sixteen kilobits"}
        with self.voiceover(
            f"A came from {sp[d['order'][0]]}, B from {sp[d['order'][1]]}, and C from {sp[d['order'][2]]}. Played back "
            "strictly, a recovered score keeps none of the coder's sound: only its mistakes, a wrong key here, a wrong length "
            "there. That is all the chain can do to a score; and it is why a score is such a durable thing to send."
        ):
            self.play(FadeIn(ans))
        self.wait(0.5)
        self.clear_scene()
