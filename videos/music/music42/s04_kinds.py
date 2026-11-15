from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Kinds(SoundScene):
    def construct(self):
        chapter(self, 3, r"Kinds of variation", r"What can change while a theme stays itself?")
        self.history()
        self.hear()
        self.what_kept()
        self.grounds()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"theme and variations: \ a tune stated, \ then varied again and again, \ each variation a section", WHITE),
            (r"Mozart wrote twelve variations on the Tune \ (K. 265, \ about 1781)", WHITE),
            (r"Bach's \textit{Goldberg Variations} \ (1741) \ keep the bass and harmony, \ not the melody", WHITE),
            (r"Beethoven's \textit{Diabelli Variations} \ (1823): \ thirty-three on a waltz he mocked", TUNE),
            (r"the question every variation answers: \ what is kept, \ and what is changed?", GREY_A),
        ]
        rows_scene(self, r"theme and variations", items,
                   "Variation is also a form of its own. <bookmark mark='b'/> In a theme and variations, a tune is stated and "
                   "then varied again and again, each variation a section. <bookmark mark='c'/> Mozart wrote twelve on our Tune, "
                   "about 1781. <bookmark mark='d'/> Bach's Goldberg Variations of 1741 keep the bass and the harmony, not the "
                   "melody. <bookmark mark='e'/> Beethoven's Diabelli Variations of 1823 make thirty-three out of a waltz he "
                   "mocked. <bookmark mark='f'/> Every variation answers one question: what is kept, and what is changed?",
                   marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("kinds")
        c = clip("kinds.five")
        vs = d["versions"]
        cells = VGroup()
        sub = {"the theme": r"the Tune's first two phrases", "ornamental": r"a neighbour note on every beat",
               "rhythmic": r"long-short on every beat", "harmonic": r"the same melody, \ new chords",
               "character": r"minor, \ slower, \ an octave down"}
        for k, v in vs.items():
            r = scored(v["melody"], None, width=3.6, height=1.05, lo=58, hi=86, bars=4 if k != "character" else 6, beats=4.0)
            cells.add(VGroup(label(k, font_size=19, color=TUNE if k == "the theme" else WHITE), r, label(sub[k], font_size=14, color=GREY_A)).arrange(DOWN, buff=0.12))
        cells.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.45)).move_to(DOWN * 0.1)
        head = label(r"the Tune, \ varied four ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Hear the Tune's first two phrases, and then four variations of ours, one of each classic kind. Ornamental: a "
            "neighbour note decorating every beat. Rhythmic: every beat made long and short. Harmonic: the same melody over "
            "new chords. And a character variation: minor, slower, an octave lower."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = list(vs)
        with self.listen(c) as snd:
            window(snd, r"a theme, \ four variations", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
                unit = 0.36
                flash(snd, cells[i][1].roll.notes, [st[k] + n[1] * unit for n in vs[k]["melody"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def what_kept(self):
        d = load("kinds")
        rows_ = VGroup()
        hdr = VGroup(*[label(t, font_size=19, color=GREY_A) for t in (r"variation", r"melody", r"harmony", r"rhythm", r"mode and speed")])
        table = [(r"ornamental", r"kept on the beats", r"kept", r"filled in", r"kept"),
                 (r"rhythmic", r"kept", r"kept", r"changed", r"kept"),
                 (r"harmonic", r"kept", r"changed", r"kept", r"kept"),
                 (r"character", r"kept, \ inflected", r"kept, \ in minor", r"stretched", r"changed")]
        grid = VGroup(*hdr, *[label(t, font_size=18, color=(TUNE if j == 0 else (EAR if ("changed" in t or "filled" in t or "stretched" in t or "inflected" in t or "minor" in t) else WHITE))) for row in table for j, t in enumerate(row)])
        grid.arrange_in_grid(rows=5, cols=5, buff=(0.55, 0.35))
        grid.move_to(UP * 0.2)
        sep = r" \ "
        new_c, old_c = sep.join(roman_tex(x) for x in d["harmonic_chords"]), sep.join(roman_tex(x) for x in d["chords"])
        cap = label(r"the harmonic variation's chords: \ " + new_c + r", \ against \ " + old_c, font_size=17, color=GREY_A).to_edge(DOWN, buff=0.8)
        head = label(r"what each variation keeps \ (white) \ and changes \ (pink)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Lay them out by feature. <bookmark mark='a'/> Each keeps most of the theme and changes one thing: the "
            "ornamental variation fills in between the beats; the rhythmic one changes only durations; the harmonic one "
            "only the chords, here starting on the sixth degree instead of the tonic; the character variation changes mode "
            "and speed, and lets the rest follow. A variation that changed everything would not be heard as a variation at "
            "all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in grid[5:]], lag_ratio=0.05), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grounds(self):
        items = [
            (r"some variations keep only a bass line: \ the ground, \ the passacaglia, \ the chaconne", WHITE),
            (r"Purcell's `Dido's Lament' \ (1689) \ sings over a falling ground bass repeated eleven times", WHITE),
            (r"jazz choruses \ (Part 39) \ keep the changes and invent a new line each time", WHITE),
            (r"the more that is kept, \ the more freedom the rest has: \ a constraint that frees", TUNE),
            (r"chapter 4: \ planning where a phrase rises and falls", GREY_A),
        ]
        rows_scene(self, r"keeping only the ground", items,
                   "Some variations keep even less. <bookmark mark='b'/> The ground bass, the passacaglia and the chaconne keep "
                   "only a bass line or a progression. <bookmark mark='c'/> In Purcell's Dido's Lament of 1689 the voice sings "
                   "over a falling ground bass repeated eleven times. <bookmark mark='d'/> Jazz choruses, Part 39's subject, keep "
                   "the changes and invent a new line each time. <bookmark mark='e'/> The more that is kept fixed, the more "
                   "freedom the rest has: a constraint that frees. <bookmark mark='f'/> Chapter four plans where a phrase rises "
                   "and falls.", marks="cdef")
