from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403

LANG_C = {"French": BLUE, "English": TUNE, "German": EAR, "Polish": GOLD, "Italian": RED, "Hawaiian": "#A3E635"}


class Language(SoundScene):
    def construct(self):
        chapter(self, 9, r"Music and language", r"Does a composer's language leave a trace in the music?")
        self.overlap()
        self.npvi()
        self.hear()
        self.patel()
        self.folk()
        self.library()
        self.speech()

    # ------------------------------------------------------------------
    def overlap(self):
        items = [
            (r"both are sequences of sounds built from a small set of units: \ phonemes, \ notes", WHITE),
            (r"both have rhythm, \ phrasing and pitch contour, \ and both are learned in infancy by exposure", WHITE),
            (r"both have structure that a listener tracks: \ syntax, \ harmony \ (Part 22)", WHITE),
            (r"Aniruddh Patel's question: \ which mental resources do they share, \ and which are separate?", TUNE),
            (r"one testable link: \ the rhythm of a language and the rhythm of its music", GREY_A),
        ]
        rows_scene(self, r"two sound systems", items,
                   "Music and language are the two great sound systems of our species. <bookmark mark='b'/> Both are sequences "
                   "built from a small set of units: phonemes, notes. <bookmark mark='c'/> Both have rhythm, phrasing and pitch "
                   "contour, and both are learned in infancy by exposure. <bookmark mark='d'/> Both have structure that a "
                   "listener tracks: syntax, harmony. <bookmark mark='e'/> Aniruddh Patel's question is which mental resources "
                   "they share, and which are separate. <bookmark mark='f'/> One link can be tested with a ruler: the rhythm "
                   "of a language and the rhythm of its music.", marks="bcdef")

    # ------------------------------------------------------------------
    def npvi(self):
        d = load("npvi")
        ex = d["examples"]
        eq = MathTex(r"\mathrm{nPVI} = \frac{100}{m-1}\sum_{k=1}^{m-1}\left|\frac{d_k - d_{k+1}}{(d_k + d_{k+1})/2}\right|", font_size=40).to_edge(UP, buff=0.9)
        def bars(ds, color):
            g = VGroup()
            x = 0.0
            for v in ds:
                g.add(Rectangle(width=0.55 * v - 0.06, height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x + 0.55 * v / 2, 0, 0]))
                x += 0.55 * v
            return g
        rows_ = VGroup()
        for ds, name, val, col in (([1, 1, 1, 1, 1, 1], r"even", ex["even"], GREY_A), ([1, 1, 2, 1, 1, 2], r"two short, \ one long", ex["mixed"], BLUE),
                                    ([1.5, 0.5, 1.5, 0.5, 1.5, 0.5], r"long, \ short, \ long, \ short", ex["dotted"], TUNE)):
            rows_.add(VGroup(label(name, font_size=19, color=WHITE).set_width(3.0) if len(name) > 30 else label(name, font_size=19, color=WHITE),
                             bars(ds, col), label(rf"nPVI = {val:.0f}", font_size=20, color=col)))
        for i, r in enumerate(rows_):
            y = 0.6 - 0.95 * i
            r[0].move_to([-3.6, y, 0], aligned_edge=RIGHT)
            r[1].move_to([0.0, y, 0])
            r[2].move_to([3.6, y, 0], aligned_edge=LEFT)
        head = label(r"how much neighbouring durations differ", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The ruler is the normalized pairwise variability index, nPVI, which phoneticians invented for speech. Take "
            "each pair of neighbouring durations, their difference divided by their average, and average over the "
            "sequence, times a hundred. <bookmark mark='a'/> An even rhythm scores zero. <bookmark mark='b'/> Two short notes "
            f"and a long one, repeated, score {say(ex['mixed'])}. <bookmark mark='c'/> Long, short, long, short, in a "
            f"three-to-one ratio, scores {say(ex['dotted'])}. In speech, English, where stressed syllables are long and "
            "unstressed ones squeezed, scores high; French, whose syllables are more even, scores lower."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("rhythms")
        c = clip("rhythms.two")
        beat = d["beat"]
        rows_ = VGroup()
        for i, name in enumerate(d["order"]):
            t = d["tunes"][name]
            mel = t["melody"]
            col = BLUE if i == 0 else TUNE
            bars = VGroup()
            x = 0.0
            for _, b in mel:
                bars.add(Rectangle(width=0.62 * b - 0.06, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x + 0.31 * b, 0, 0]))
                x += 0.62 * b
            nm = name.replace("'", "'")
            rows_.add(VGroup(label(rf"{nm} \ ({t['origin']}): \ nPVI {t['npvi']:.0f}", font_size=19, color=col), bars).arrange(DOWN, buff=0.2, aligned_edge=LEFT))
        rows_.arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(UP * 0.1)
        cap = label(r"each bar: \ one note's length; \ the whole tune's nPVI, \ its first two phrases drawn", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the two ends of the corpus", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        a, b = (d["tunes"][n]["npvi"] for n in d["order"])
        with self.voiceover(
            f"Hear the two ends of the series' corpus. Sur le pont d'Avignon, from France, scores {say(a)}: nearly every "
            f"note the same length. Oh My Darling, Clementine, from the United States, scores {say(b)}: long and short "
            "notes alternating, like stressed and unstressed syllables."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"low and high nPVI", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for key, r, name in zip(("first", "second"), rows_, d["order"]):
                mel = d["tunes"][name]["melody"]
                on = np.concatenate([[0.0], np.cumsum([x[1] for x in mel])[:-1]])
                flash(snd, list(r[1]), [st[key] + beat * o for o in on], hot=WHITE, base=r[0].get_color())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def patel(self):
        items = [
            (r"Esther Grabe and Ee Ling Low \ (2002): \ the nPVI of vowels separates English and German from French and Spanish", WHITE),
            (r"Patel and Joseph Daniele \ (2003): \ instrumental themes by English and French composers around 1900", WHITE),
            (r"Elgar, \ Holst, \ Vaughan Williams and others against Debussy, \ Faur\'e, \ Ravel and others", WHITE),
            (r"the English themes had a higher nPVI than the French, \ as their languages do", TUNE),
            (r"a matched sample: \ one era, \ one genre, \ one kind of melody; \ only the language differs", GREY_A),
        ]
        rows_scene(self, r"Elgar and Debussy", items,
                   "In 2002 Esther Grabe and Ee Ling Low showed that the nPVI of vowel durations separates English and German "
                   "from French and Spanish. <bookmark mark='b'/> In 2003 Patel and Joseph Daniele measured instrumental themes "
                   "by English and French composers who worked around 1900: <bookmark mark='c'/> Elgar, Holst, Vaughan Williams "
                   "and others against Debussy, Fauré, Ravel and others. <bookmark mark='d'/> The English themes had a higher "
                   "nPVI than the French, as their languages do. <bookmark mark='e'/> And notice the design: one era, one "
                   "genre, one kind of melody, so that only the language differs.", marks="bcde")

    # ------------------------------------------------------------------
    def folk(self):
        d = load("npvi")
        f = d["folk"]
        t = d["test"]
        x0, W = -4.5, 9.0
        def X(v):
            return x0 + W * v / 80.0
        axis = VGroup(Line([x0, -1.6, 0], [x0 + W, -1.6, 0], color=GREY_B, stroke_width=1.5),
                      *[VGroup(Line([X(v), -1.68, 0], [X(v), -1.52, 0], color=GREY_B), label(f"{v}", font_size=15, color=GREY_A).move_to([X(v), -1.9, 0])) for v in (0, 20, 40, 60, 80)],
                      label(r"nPVI of the tune's note lengths", font_size=16, color=GREY_A).move_to([x0 + W / 2, -2.3, 0]))
        rows_ = VGroup()
        rng = np.random.default_rng(0)
        for i, k in enumerate(("French", "English", "German")):
            y = 1.3 - 1.0 * i
            vals = f[k]["values"]
            dots = VGroup(*[Dot([X(v), y + 0.18 * rng.uniform(-1, 1), 0], radius=0.06, color=LANG_C[k], fill_opacity=0.8) for v in vals])
            m = f[k]["mean"]
            rows_.add(VGroup(label(rf"{k} \ ({f[k]['n']})", font_size=19, color=LANG_C[k]).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT), dots,
                             Line([X(m), y - 0.35, 0], [X(m), y + 0.35, 0], color=WHITE, stroke_width=4)))
        res = label(rf"English minus French: \ {t['diff']:.1f}; \ bootstrap interval {t['lo']:.1f} to {t['hi']:.1f}; \ permutation test $p = {t['p']:.2f}$", font_size=18, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"the series' folk tunes, \ by the language of their country", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "We can try it on the series' own corpus: the folk and traditional tunes, grouped by the language of the country "
            f"they come from. <bookmark mark='a'/> Five French-language tunes average {say(f['French']['mean'], 1)}; "
            f"<bookmark mark='b'/> thirty-five English-language ones {say(f['English']['mean'], 1)}; <bookmark mark='c'/> "
            f"eight German ones {say(f['German']['mean'], 1)}. The direction is Patel's. <bookmark mark='d'/> But is it real? "
            f"English minus French is {say(t['diff'], 1)}. Resampling each group gives an interval from {say(t['lo'], 1)} to "
            f"{say(t['hi'], 1)}, which excludes zero; but shuffling the labels, a permutation test, gives a p-value of "
            f"{say(t['p'], 2)}. With only five French tunes the bootstrap is overconfident, and the honest answer is that "
            "we cannot tell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(ghost(VGroup(*[r[0] for r in rows_]))))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def library(self):
        d = load("npvi")
        lib = d["library"]
        kinds = ["song", "keyboard", "quartet", "concerto", "chamber"]
        x0, W = -3.6, 9.0
        def X(v):
            return x0 + W * v / 80.0
        rows_ = VGroup()
        for i, k in enumerate(kinds):
            y = 1.7 - 0.75 * i
            pts = [r for r in lib if r["kind"] == k]
            dots = VGroup(*[Dot([X(r["npvi"]), y, 0], radius=0.08, color=LANG_C[r["language"]], fill_opacity=0.9) for r in pts])
            rows_.add(VGroup(label(rf"{k} \ ({len(pts)})", font_size=19, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT), dots))
        axis = VGroup(Line([x0, -2.0, 0], [x0 + W, -2.0, 0], color=GREY_B, stroke_width=1.5),
                      *[label(f"{v}", font_size=15, color=GREY_A).move_to([X(v), -2.25, 0]) for v in (0, 20, 40, 60, 80)])
        key = VGroup(*[VGroup(Dot(radius=0.07, color=c), label(k, font_size=15, color=GREY_A)).arrange(RIGHT, buff=0.1) for k, c in LANG_C.items() if k != "French"]).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.3)
        bk = d["by_kind"]
        bl = d["by_language"]
        ger = [r for r in lib if r["language"] == "German"]
        lo, hi = min(ger, key=lambda r: r["npvi"]), max(ger, key=lambda r: r["npvi"])
        lo_t = f"{lo['composer']}'s {lo['title'].split(',')[0]}"
        hi_t = f"{hi['composer']}'s {hi['title'].split(',')[0]}"
        head = label(r"the Library's 23 pieces: \ the melody line's nPVI, \ by kind and language", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now the Library, the twenty-three pieces of Part 27 and after, with the melody line of each: the voice, the "
            f"first violin, the solo clarinet, or the top note of the piano. <bookmark mark='a'/> Songs average "
            f"{say(bk['song'], 1)}, keyboard pieces {say(bk['keyboard'], 1)}. The German composers average "
            f"{say(bl['German'], 1)} and the English {say(bl['English'], 1)}; but within the German group alone the melody "
            f"lines run from {say(lo['npvi'], 1)}, in {lo_t}, to {say(hi['npvi'], 1)}, in {hi_t}, and the English group "
            "is mostly songs. What a piece is for, a sung text or running piano figuration, moves the number far more than "
            "the composer's language. That is why Patel and Daniele compared like with like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(VGroup(*[r[0] for r in rows_])), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r[1]) for r in rows_], lag_ratio=0.3), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speech(self):
        items = [
            (r"Yuto Ozaki and colleagues \ (2024): \ 75 researchers each sang, \ recited and spoke in their own language: \ 55 languages", WHITE),
            (r"a Registered Report: \ the predictions were reviewed and fixed before the data were collected", WHITE),
            (r"songs were higher, \ slower, \ and used more stable pitches than speech, \ almost everywhere", WHITE),
            (r"the sizes of pitch intervals, \ and the brightness of the voice, \ were about the same", TUNE),
            (r"song is speech made regular in time and pitch: \ easier to sing together", GREY_A),
        ]
        rows_scene(self, r"song against speech", items,
                   "The largest direct comparison of song and speech is recent. <bookmark mark='b'/> In 2024 Yuto Ozaki and "
                   "colleagues, seventy-five researchers in all, each sang, recited and spoke in their own language, fifty-five "
                   "languages in all, "
                   "<bookmark mark='c'/> as a Registered Report, with the predictions reviewed and fixed before the data were "
                   "collected. <bookmark mark='d'/> Songs were higher, slower and used more stable pitches than speech, almost "
                   "everywhere. <bookmark mark='e'/> The sizes of pitch intervals, and the brightness of the voice, were about "
                   "the same. <bookmark mark='f'/> Song looks like speech made regular in time and pitch: easier to sing "
                   "together.", marks="bcdef")
