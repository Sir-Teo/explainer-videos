from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Search(SoundScene):
    def construct(self):
        chapter(self, 9, r"Orchestration as search", r"Can a computer orchestrate a sound?")
        self.problem()
        self.how()
        self.target()
        self.solve()
        self.bell()
        self.hear()
        self.limits()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"turn Ravel around: \ given a sound, \ which instruments, \ on which notes, \ make it?", WHITE),
            (r"candidates: \ each instrument playing each harmonic of the target's pitch, \ within its range", WHITE),
            (r"fit: \ choose loudnesses so the sum's spectrum is close to the target's", WHITE),
            (r"search: \ among all small groups of instruments, \ keep the best", TUNE),
            (r"a target of ours: \ a sung `ah' on C3", GREY_A),
        ]
        rows_scene(self, r"the problem", items,
                   "Now turn Ravel's idea around. <bookmark mark='b'/> Given a sound, which instruments, on which notes, would "
                   "make it? <bookmark mark='c'/> The candidates are each instrument playing each harmonic of the target's pitch, "
                   "within its range. <bookmark mark='d'/> Fit loudnesses so the sum's spectrum is close to the target's, "
                   "<bookmark mark='e'/> and search among all small groups of instruments for the best. <bookmark mark='f'/> Our "
                   "target is a sung vowel, ah, on C three.", marks="cdef")

    # ------------------------------------------------------------------
    def bands(self, vals, col, h=2.4, w=10.0):
        v = np.asarray(vals, float)
        db = 10 * np.log10(v / v.max() + 1e-6)
        g = VGroup(Line([0, 0, 0], [w, 0, 0], color=GREY_D))
        n = len(v)
        for i, x in enumerate(db):
            hh = h * max(0.0, 1 + x / 50.0)
            g.add(Rectangle(width=w / n * 0.8, height=max(hh, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.8).move_to([w * (i + 0.5) / n, hh / 2, 0]))
        return g

    def target(self):
        d = load("match")
        tb = self.bands(d["target_bands"], BLUE).move_to(DOWN * 0.3)
        edges = d["edges"]
        ticks = VGroup()
        for f in (100, 300, 1000, 3000, 8000):
            x = tb[0].get_left()[0] + 10.0 * np.log(f / edges[0]) / np.log(edges[-1] / edges[0])
            ticks.add(label(f"{f} Hz", font_size=14, color=GREY_A).move_to([x, tb[0].get_bottom()[1] - 0.3, 0]))
        cap = label(r"power in 32 bands from 80 Hz to 8 kHz \ (decibels): \ the formants of `ah' near 730 and 1,090 Hz", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"the target: \ a sung `ah' on C3", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the target's spectrum, in thirty-two bands from eighty hertz to eight kilohertz, the kind of resolution "
            "the ear's filters have. The two humps are the vowel's formants, near seven hundred and thirty and a thousand and "
            "ninety hertz, from Part 8."
        ):
            self.play(FadeIn(head), FadeIn(tb), FadeIn(ticks), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def solve(self):
        d = load("match")
        res = d["results"]
        e = res["4"]["error_by_size"]
        x0 = -5.0
        bars = VGroup()
        mx = max(float(v) for v in e.values())
        for i, (k, v) in enumerate(sorted(e.items(), key=lambda kv: int(kv[0]))):
            w = 5.0 * float(v) / mx
            bars.add(VGroup(label(rf"{k} instrument{'s' if int(k) > 1 else ''}", font_size=19, color=WHITE).move_to([x0, 1.4 - 0.75 * i, 0], aligned_edge=RIGHT),
                            Rectangle(width=w, height=0.4, stroke_width=0, fill_color=EAR, fill_opacity=0.85).move_to([x0 + 0.3 + w / 2, 1.4 - 0.75 * i, 0]),
                            label(f"{float(v):.1f} dB", font_size=17, color=WHITE).move_to([x0 + 0.8 + w, 1.4 - 0.75 * i, 0])))
        chosen = VGroup(*[label(rf"{c['instrument'].replace(' f', '')}: \ harmonic {c['harmonic']}", font_size=19, color=TUNE) for c in res["4"]["chosen"]]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 0.4)
        cl = label(r"the best four", font_size=19, color=GREY_A).next_to(chosen, UP, buff=0.25)
        cap = label(r"error: \ the root-mean-square difference in band level, \ in decibels", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.8)
        head = label(rf"the solver: \ {res['4']['candidates']} candidates, \ every group of up to four", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"The solver has {say(res['4']['candidates'])} candidates. It fits all of them at once by non-negative least "
            "squares, keeps the most promising, and then tries every group of one, two, three and four, refitting each. "
            f"<bookmark mark='a'/> With one instrument the best match is {float(e['1']):.0f} decibels off per band; with "
            f"four, {float(e['4']):.0f}. <bookmark mark='b'/> The best four put instruments on the harmonics that carry the "
            "formants, and one low instrument for the fundamental: a vowel spelled with an orchestra."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(chosen))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("match")
        c = clip("match.four")
        cells = VGroup(*[label(t, font_size=21, color=col) for t, col in ((r"the sung vowel", BLUE), (r"one instrument", GREY_A), (r"two", GREY_A), (r"four", TUNE))]).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        with self.voiceover(
            "Hear the target, sung by Part 17's model bass voice, and then the solver's matches with one, two and four "
            "instruments. The match will not sound like a voice, because a voice also moves, breathes and articulates; but "
            "listen for the vowel colour arriving as instruments are added."
        ):
            self.play(FadeIn(cells))
        st = d["starts"]
        ks = ["voice", "1", "2", "4"]
        with self.listen(c) as snd:
            window(snd, r"a vowel and its matches", kind="synthesized", detail=r"a model voice, \ additive instruments", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                pulse(snd, cells[i], st[k], st[k] + 2.3, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"real tools \ (IRCAM's \textit{Orchid\'ee}, \ \textit{Orchids}, \ \textit{Orchidea}) \ search large sample libraries", WHITE),
            (r"they match how the spectrum moves in time, \ not only its average", WHITE),
            (r"composers use them for unusual targets: \ a bell, \ a bird, \ a recorded noise", WHITE),
            (r"the search proposes; \ the orchestrator chooses what can be played and balanced", TUNE),
            (r"Part 42 treats composing itself as search", GREY_A),
        ]
        rows_scene(self, r"computer-aided orchestration", items,
                   "This is a toy of a real research field. <bookmark mark='b'/> IRCAM's tools, Orchidée, Orchids and "
                   "Orchidea, search large libraries of recorded instrument samples, <bookmark mark='c'/> and match how a "
                   "spectrum moves in time, not only its average. <bookmark mark='d'/> Composers use them for unusual targets: a "
                   "bell, a bird, a recorded noise. <bookmark mark='e'/> The search proposes; the orchestrator chooses what can "
                   "be played and balanced. <bookmark mark='f'/> Part 42 treats composing itself as search.", marks="cdef")

    # ------------------------------------------------------------------
    def bell(self):
        d = load("bell")
        c = clip("bell.two")
        side = VGroup(label(r"a church bell's partials \ (Part 9): \ hum, \ prime, \ a minor-third `tierce', \ quint, \ nominal ...", font_size=20, color=WHITE),
                      label(rf"the solver's best four: \ {d['errors']['4']:.0f} dB off per band, \ against {d['vowel_error']:.0f} for the vowel", font_size=20, color=EAR),
                      label(r"harmonic instruments cannot supply the minor third: \ it is not a harmonic", font_size=20, color=TUNE)).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        head = label(r"a harder target: \ a bell", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now a harder target: Part 9's church bell, whose partials include a minor third above the strike note, the "
            f"tierce. The solver's best four instruments are {say(round(d['errors']['4']))} decibels off per band, against "
            f"{say(round(d['vowel_error']))} for the vowel, because harmonic instruments cannot supply a partial that is not "
            "a harmonic. Hear the bell, and then the best the orchestra can do."
        ):
            self.play(FadeIn(head), FadeIn(side))
        with self.listen(c) as snd:
            window(snd, r"a bell, \ then its match", kind="synthesized", detail=r"Part 9's bell model, \ additive instruments", corner=DL, tag_corner=DR)
            pulse(snd, side[0], 0.0, d["starts"]["match"] - 0.3, buff=0.1)
            pulse(snd, side[1], d["starts"]["match"], c.duration, buff=0.1)
        ans = label(r"composers imitate bells with dissonant chords for exactly this reason", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover("That is why composers who imitate bells with an orchestra write dissonant chords: a bell's spectrum is itself a dissonant chord."):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how(self):
        eq = VGroup(label(r"columns of A: \ the band spectra of the candidates \ (instrument, \ harmonic)", font_size=20, color=WHITE),
                    label(r"b: \ the target's band spectrum; \ w: \ the loudness of each candidate", font_size=20, color=WHITE),
                    label(r"minimise \ $\lVert A w - b \rVert$ \ with every $w \geq 0$: \ non-negative least squares", font_size=22, color=TUNE),
                    label(r"then try every small group of the best candidates, \ and refit: \ sparsity by brute force", font_size=20, color=WHITE),
                    label(r"the error is measured in decibels per band, \ as the ear compares loudness", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        head = label(r"how the solver works", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How does the solver work? <bookmark mark='a'/> Put each candidate's spectrum, measured in bands, into a column "
            "of a matrix A, and the target's spectrum into a vector b. <bookmark mark='b'/> Then find loudnesses w, none "
            "negative, since an instrument cannot play less than silence, that make A times w as close to b as possible: "
            "non-negative least squares. <bookmark mark='c'/> An orchestra cannot use every candidate at once, so the solver "
            "then tries every small group of the most promising, and refits each: sparsity by brute force. "
            "<bookmark mark='d'/> And it judges the fit in decibels per band, the way the ear compares loudness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq[0]))
            vo.wait_until("a")
            self.play(FadeIn(eq[1]))
            vo.wait_until("b")
            self.play(FadeIn(eq[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq[3]))
            vo.wait_until("d")
            self.play(FadeIn(eq[4]))
        self.wait(0.4)
        self.clear_scene()
