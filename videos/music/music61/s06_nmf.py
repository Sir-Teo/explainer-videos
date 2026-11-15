from __future__ import annotations

import numpy as np

from videos.music.music61.common import *  # noqa: F403


class Nmf(SoundScene):
    def construct(self):
        chapter(self, 5, r"Factorizing the spectrogram", r"Can a spectrogram be taken apart into notes?")
        self.idea()
        self.updates()
        self.blind()
        self.templates()
        self.heard()
        self.replayed()
        self.limits()

    # ------------------------------------------------------------------
    def idea(self):
        lines = VGroup(
            MathTex(r"V \;\approx\; W\,H, \qquad V, W, H \ge 0", font_size=44, color=TUNE),
            label(r"$V$: \ the spectrogram, \ frequency by time", font_size=21, color=WHITE),
            label(r"$W$: \ one column per note: \ its spectrum, \ its comb of partials", font_size=21, color=WHITE),
            label(r"$H$: \ one row per note: \ how loud it is in each frame, \ its activation", font_size=21, color=WHITE),
            label(r"non-negative: \ sounds only add; \ no note can cancel another's energy", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"non-negative matrix factorization", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In 2003 Paris Smaragdis and Judith Brown proposed treating the problem as algebra. <bookmark mark='a'/> Write the "
            "spectrogram V as the product of two matrices, W times H, all three non-negative. <bookmark mark='b'/> V is "
            "frequency by time. <bookmark mark='c'/> Each column of W is a note's spectrum, its comb of partials. "
            "<bookmark mark='d'/> Each row of H is that note's activation: how loud it is in each frame. "
            "<bookmark mark='e'/> Non-negative because sounds only add, roughly, in a magnitude spectrogram: no note can cancel "
            "another's energy, so the parts must be additive, like notes."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def updates(self):
        d = load("nmf")
        cost = np.array(d["cost"])
        ax = frame_axes(width=6.0, height=2.6, xlo=0, xhi=len(cost), ylo=0, yhi=1.05, center=DOWN * 1.2 + RIGHT * 2.6)
        cv = curve(np.arange(len(cost)), cost / cost[0], ax.to, color=TUNE, width=3)
        yl = label(r"divergence, \ relative to the first iteration", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.1)
        xl = label(r"iterations", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        eqs = VGroup(
            MathTex(r"H \leftarrow H \odot \frac{W^\top \left(V / WH\right)}{W^\top \mathbf{1}}", font_size=34, color=WHITE),
            MathTex(r"W \leftarrow W \odot \frac{\left(V / WH\right) H^\top}{\mathbf{1}\, H^\top}", font_size=34, color=WHITE),
            label(r"Lee and Seung \ (1999, \ 2001): \ the Kullback-Leibler divergence never increases", font_size=16, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(LEFT * 3.2 + DOWN * 0.6)
        head = label(r"multiplicative updates", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How are W and H found? <bookmark mark='a'/> By Daniel Lee and Sebastian Seung's multiplicative updates: multiply "
            "each entry of H by a ratio that compares the spectrogram with its current reconstruction, and then do the same for "
            "W. Entries that start non-negative stay non-negative, and the divergence between V and W H never increases. "
            "<bookmark mark='b'/> Here it is falling, iteration by iteration, on a test piece."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(xl), Create(cv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blind(self):
        d = load("nmf")
        B = np.array(d["blind_W"])
        A = np.log10(B / B.max() + 1e-4)
        pic = picture(A, -3, 0, 5.4, 3.0).move_to(LEFT * 2.8 + DOWN * 0.4)
        names = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
        cw = 5.4 / len(d["blind_match"])
        tags = VGroup(*[label(f"{names[m['pitch'] % 12]}{m['pitch'] // 12 - 1}", font_size=11, color=TUNE if m["cos"] > 0.8 else EAR)
                        .rotate(PI / 2).move_to([pic.get_left()[0] + cw * (i + 0.5), pic.get_bottom()[1] - 0.35, 0]) for i, m in enumerate(d["blind_match"])])
        good = sum(1 for m in d["blind_match"] if m["cos"] > 0.8)
        found = len({m["pitch"] for m in d["blind_match"] if m["cos"] > 0.8} & set(d["piece_pitches"]))
        notes = VGroup(
            label(r"12 components, \ learnt from this piece alone", font_size=18, color=WHITE),
            label(rf"{good} look like one piano note \ (gold: \ cosine above 0.8 with its template)", font_size=18, color=TUNE),
            label(r"the rest: \ mixtures of notes that often sound together, \ or of attacks", font_size=18, color=EAR),
            label(rf"the piece uses {len(d['piece_pitches'])} pitches: \ too many for 12 parts", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.3 + DOWN * 0.4)
        head = label(r"left to itself", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Left to itself, what does the factorization find? <bookmark mark='a'/> Here are twelve components learnt from one "
            f"test piece alone, each labelled with the piano note it most resembles. <bookmark mark='b'/> {say(good)} of them "
            "look like a single piano note. <bookmark mark='c'/> The rest are mixtures: notes that often sounded together, or "
            f"the noise of attacks. <bookmark mark='d'/> The piece uses {say(len(d['piece_pitches']))} pitches, more than twelve "
            "parts can hold, and nothing told the factorization that a part should be a note."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(tags), FadeIn(notes[0]))
            for mark, n in zip("bcd", notes[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def templates(self):
        d = load("nmf")
        Wt = np.array(d["templates"])           # bins/2 x pitches
        keys = d["keys"]
        A = np.log10(Wt / Wt.max() + 1e-4)
        pic = picture(A, -3, 0, 5.0, 3.2).move_to(LEFT * 3.0 + DOWN * 0.3)
        lx = label(r"the 37 notes, \ C3 to C6", font_size=15, color=GREY_A).next_to(pic, DOWN, buff=0.15)
        ly = label(r"frequency \ (log)", font_size=15, color=GREY_A).rotate(PI / 2).next_to(pic, LEFT, buff=0.15)
        notes = VGroup(
            label(r"each column: \ one piano note's spectrum, \ learnt from the note alone", font_size=18, color=WHITE),
            label(r"the diagonal lines: \ the partials, \ 1, \ 2, \ 3, \dots \ times $f_0$, \ rising with the note", font_size=18, color=WHITE),
            label(r"fix $W$, \ learn only $H$: \ supervised transcription", font_size=18, color=TUNE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.0 + DOWN * 0.3)
        head = label(r"the templates: \ $W$", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Left to itself, NMF finds parts, but not necessarily notes. So Monochord learns W in advance. "
            "<bookmark mark='a'/> Each column is one piano note's spectrum, learnt from that note played alone; the diagonal "
            "lines are the partials, rising with the note. <bookmark mark='b'/> Then W is fixed, and only the activations are "
            "learnt from the music: supervised transcription."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(lx), FadeIn(ly), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("nmf")
        c = clip("nmf.piece")
        H = np.array(d["H"])
        hop = 2 * 960 / 48000
        dur = H.shape[1] * hop
        w, h = 10.5, 3.6
        pic = picture(np.log10(H + 1e-3), -2.0, 0, w, h).move_to(DOWN * 0.2)
        x0, y0 = pic.get_left()[0], pic.get_bottom()[1]
        ph = h / H.shape[0]
        truth = VGroup(*[Rectangle(width=max(0.03, w * (b - a) / dur), height=ph * 0.9, stroke_color=WHITE, stroke_width=1.2, fill_opacity=0)
                         .move_to([x0 + w * (a + b) / 2 / dur, y0 + ph * (m - 48 + 0.5), 0]) for m, a, b in d["truth"]])
        ps = d["piece_scores"]
        note = label(rf"the activations $H$ \ (bright: \ loud); \ white boxes: \ the notes played. \ This piece: \ F = {ps['f']:.2f}", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.3)
        ly = label(r"C3 \ to \ C6", font_size=14, color=GREY_A).next_to(pic, LEFT, buff=0.15)
        head = label(r"a test piece, \ factorized", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is a test piece of random polyphony on the piano, never used to learn the templates, and its activations, with the notes really played boxed in white."):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(ly), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"a test piece", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            head_line = Line(pic.get_corner(DL), pic.get_corner(UL), color=WHITE, stroke_width=2)
            snd.show(head_line)
            snd.drive(head_line, lambda m, t: m.move_to([x0 + w * min(t, dur) / dur, pic.get_center()[1], 0]))
        with self.voiceover(
            f"The boxes fill with light where the factorization agrees. Scored note by note, it finds {say(100 * ps['recall'])} "
            f"percent of the notes, and {say(100 * ps['precision'])} percent of what it reports is right."
        ):
            self.play(Create(truth), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        d = load("nmf")
        p = d["scores"]["piano"]
        items = [
            (r"templates assume every note of a pitch has one spectrum: \ but loud notes are brighter, \ and notes change as they decay", WHITE),
            (r"activations leak: \ a note's partials are partly explained by its neighbours", WHITE),
            (rf"on our piano test pieces: \ F = {p['f']:.2f}; \ on other timbres, \ worse \ (Chapter 7)", WHITE),
            (r"refinements: \ sparsity, \ temporal continuity, \ templates that change over a note, \ harmonic constraints", WHITE),
            (r"NMF's virtue: \ every part of it can be read; \ its vice: \ it knows nothing it was not told", TUNE),
        ]
        rows_scene(self, r"what NMF cannot do", items,
                   "NMF has limits. <bookmark mark='b'/> Its templates assume every note of a pitch has one spectrum, but loud "
                   "notes are brighter, and notes change as they decay. <bookmark mark='c'/> Activations leak: a note's partials "
                   f"are partly explained by its neighbours. <bookmark mark='d'/> On our piano test pieces its F-measure is "
                   f"{say(p['f'], 2)}, and on other timbres it is worse, as Chapter 7 shows. <bookmark mark='e'/> There are "
                   "refinements: sparsity, continuity in time, templates that change over a note, harmonic constraints. "
                   "<bookmark mark='f'/> NMF's virtue is that every part of it can be read; its vice is that it knows nothing it "
                   "was not told.", marks="bcdef")

    # ------------------------------------------------------------------
    def replayed(self):
        d = load("nmfheard")
        c = clip("nmfheard.two")
        sc = d["scores"]
        boxes = choice_boxes([r"played", r"NMF's transcription, \ re-played"], width=4.0, height=0.9, buff=0.9, size=18).move_to(UP * 0.6)
        res = label(rf"{d['n_true']} notes played; \ {d['n_est']} reported, \ {sc['hits']} of them right: \ precision {sc['precision']:.2f}, \ recall {sc['recall']:.2f}", font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        why = label(r"most extras sit at the edges of the range, \ C3 and C6, \ or re-strike a note still sounding", font_size=16, color=GREY_A).next_to(res, DOWN, buff=0.3)
        head = label(r"the transcription, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Transcriptions are easiest to judge by playing them back. Hear the test piece, then NMF's transcription of it on the same piano."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"played, \ then re-played", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["played"], st["transcribed"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["transcribed"], c.duration, buff=0.08)
        with self.voiceover(
            f"It found {say(sc['hits'])} of the {say(d['n_true'])} notes, and added {say(d['n_est'] - sc['hits'])} that were "
            "never played. The playback sounds busier. Most of the extras sit at the very edges of the range, on the lowest "
            "and highest templates, which soak up whatever energy no other template explains, a thump or a hiss; the rest "
            "strike again a note that is still sounding, as its decay drifts away from the template's shape."
        ):
            self.play(FadeIn(res), FadeIn(why))
        self.wait(0.4)
        self.clear_scene()
