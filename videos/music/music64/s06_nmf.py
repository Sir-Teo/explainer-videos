from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403

STEM_NAMES = (("vocals", r"vocals", TUNE), ("bass", r"bass", BLUE), ("drums", r"drums", EAR), ("other", r"other", GREY_B))


class Nmf(SoundScene):
    def construct(self):
        chapter(self, 5, r"Factorization, \ again", r"Can Part 61's templates pull a mix apart?")
        self.idea()
        self.templates()
        self.results()
        self.rank()
        self.heard()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"Part 61 used NMF to find notes; \ here each source gets its own set of templates", WHITE),
            (r"learn twelve templates from each stem's recordings in other phrases: \ the voice's vowels, \ the drums' hits", WHITE),
            (r"fit the mixture with all 48 templates fixed; \ each source is the part of the fit its templates explain", WHITE),
            (r"turn each part into a share of every bin, \ a soft mask, \ and apply it to the mixture", WHITE),
            (r"supervised: \ it needs examples of each source, \ but not of this mixture", TUNE),
        ]
        rows_scene(self, r"templates for sources", items,
                   "Factorization works for sources as well as notes. <bookmark mark='b'/> Part 61 used it to find notes; here each "
                   "source gets its own set of templates. <bookmark mark='c'/> Learn twelve templates from each stem's recordings in "
                   "other phrases: the voice's vowels, the drums' hits. <bookmark mark='d'/> Fit the mixture with all forty-eight "
                   "templates fixed; each source is the part of the fit that its own templates explain. <bookmark mark='e'/> Turn "
                   "each part into its share of every bin, a soft mask, and apply it to the mixture. <bookmark mark='f'/> It is "
                   "supervised: it needs examples of each source, but not of this mixture.", marks="bcdef")

    # ------------------------------------------------------------------
    def results(self):
        d = load("nmf")["sdr"]
        top = max(max(d.values()), 1.0)
        rows_ = VGroup()
        for k, name, col in STEM_NAMES:
            v = d[k]
            rows_.add(VGroup(label(name, font_size=20, color=col), Rectangle(width=max(0.03, 5.0 * max(v, 0) / top), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8),
                             label(f"{v:.1f} dB", font_size=18, color=WHITE)))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(LEFT * 1.0)
        for r in rows_:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(rows_, LEFT).shift(RIGHT * 1.6)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        note = label(r"SDR against each true stem \ (higher is better; \ 0 dB: \ as much error as signal)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"supervised NMF on the session", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is how close each separated stem comes to the truth, in decibels of signal to distortion: nought decibels "
            "would mean as much error as signal. <bookmark mark='a'/> The drums come out best, at "
            f"{say(d['drums'], 1)} decibels, with the vocals close behind at {say(d['vocals'], 1)}. The bass and the piano and "
            f"guitar come out worst, near {say(d['bass'], 0)}: they share the low and middle frequencies, and the piano and "
            "guitar change their spectra from chord to chord, so a few templates describe them only roughly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.25), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("nmf")
        c = clip("nmf.vocals")
        box = choice_boxes([r"the vocals, \ by NMF"], width=4.0, height=0.9, size=20).move_to(UP * 0.5)
        head = label(r"the vocal stem, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(f"Hear the vocal stem as the factorization separates it, {say(d['sdr']['vocals'], 1)} decibels from the truth."):
            self.play(FadeIn(head), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"vocals, \ separated", kind="physical model", detail=r"Part 56's session, \ NMF", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.08)
        with self.voiceover("The voice is there, with traces of the others: the guitar where it shares a vowel's formants, the hi-hat's hiss in the consonants."):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def templates(self):
        d = load("nmfrank")
        Wv, Wd = np.array(d["W_vocals"]), np.array(d["W_drums"])
        pa = heat_image(Wv[::-1], -3, 0, width=4.2, height=3.4, smooth=False).move_to(LEFT * 3.0 + DOWN * 0.3)
        pb = heat_image(Wd[::-1], -3, 0, width=4.2, height=3.4, smooth=False).move_to(RIGHT * 3.0 + DOWN * 0.3)
        la = label(r"the voice's twelve templates", font_size=17, color=TUNE).next_to(pa, UP, buff=0.2)
        lb = label(r"the drums' twelve templates", font_size=17, color=EAR).next_to(pb, UP, buff=0.2)
        fa = VGroup(label(r"4.7 kHz", font_size=13, color=GREY_A).next_to(pa, LEFT, buff=0.12).align_to(pa, UP),
                    label(r"0", font_size=13, color=GREY_A).next_to(pa, LEFT, buff=0.12).align_to(pa, DOWN))
        note = label(r"each column a template, \ frequency up, \ ordered by its strongest bin", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"what the templates learnt", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what the templates learnt. <bookmark mark='a'/> The voice's are combs: a few strong harmonics, spaced by "
            "the pitch of a note, with the bright bands of its vowels. <bookmark mark='b'/> The drums' are smears: the kick's "
            "low thump, the snare's broad noise, the hi-hat's hiss at the top. The mixture is fitted as a sum of these columns, "
            "and each source keeps what its own columns explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(la), FadeIn(fa))
            vo.wait_until("b")
            self.play(FadeIn(pb), FadeIn(lb))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rank(self):
        d = load("nmfrank")
        r = np.array(d["ranks"], float)
        v, o = np.array(d["vocals"]), np.array(d["other"])
        lo, hi = min(v.min(), o.min()) - 1, max(v.max(), o.max()) + 1
        ax = frame_axes(width=8.0, height=3.0, xlo=0, xhi=np.log2(r[-1]), ylo=lo, yhi=hi, center=DOWN * 0.5 + LEFT * 0.8)
        cv = VGroup(curve(np.log2(r), v, ax.to, color=TUNE, width=3), curve(np.log2(r), o, ax.to, color=GREY_B, width=3))
        ticks = VGroup(*[label(f"{int(x)}", font_size=14, color=GREY_A).move_to(ax.to(np.log2(x), lo) + DOWN * 0.25) for x in r])
        xl = label(r"templates per source", font_size=14, color=GREY_A).next_to(ticks, DOWN, buff=0.15)
        yl = label(r"SDR \ (dB)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        key = VGroup(label(r"vocals", font_size=16, color=TUNE), label(r"piano and guitar", font_size=16, color=GREY_B)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        head = label(r"how many templates?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        i = int(np.argmax(v))
        with self.voiceover(
            "How many templates should each source get? <bookmark mark='a'/> With one, each source is a single fixed "
            f"spectrum, and the vocals score {say(v[0], 1)} decibels. More templates describe more of a source, "
            f"up to {say(v[i], 1)} decibels at {int(r[i])}. <bookmark mark='b'/> But templates that describe everything also "
            "describe the other sources: a voice's templates start to explain the guitar. The best number is a compromise, "
            "found on examples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.6)
        self.wait(0.6)
        self.clear_scene()
