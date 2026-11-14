from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403

KINDS = ["original", "waltz", "minor", "march", "augmented"]
NAME = {"original": r"the beloved: \ the theme", "waltz": r"II: \ at the ball, \ a waltz", "minor": r"in minor: \ the dream darkens",
        "march": r"IV: \ the march to the scaffold", "augmented": r"augmented: \ slow, \ remembered"}


class Programme(SoundScene):
    def construct(self):
        chapter(self, 5, r"Music that tells a story", r"How can a theme be a character?", extra=((1830, r"Berlioz's \textit{Symphonie fantastique}"),))
        self.berlioz()
        self.idee()
        self.orchestra()
        self.treatise()
        self.liszt()

    # ------------------------------------------------------------------
    def berlioz(self):
        items = [
            (r"Hector Berlioz, \ \textit{Symphonie fantastique} \ (Paris, \ 1830): \ five movements and a printed programme", WHITE),
            (r"a young artist, \ in love and in opium dreams, \ sees his beloved everywhere", WHITE),
            (r"she is a melody: \ the \textit{idée fixe}, \ the obsession, \ in every movement", TUNE),
            (r"at a ball, \ in the fields, \ at his own execution, \ at a witches' sabbath", WHITE),
            (r"the theme changes as the story does: \ a character, \ not a subject to develop", GREY_A),
        ]
        rows_scene(self, r"a symphony with a story", items,
                   "Instrumental music began to tell stories. <bookmark mark='b'/> In 1830 Hector Berlioz performed his "
                   "Symphonie fantastique in Paris, five movements with a printed programme. <bookmark mark='c'/> A young "
                   "artist, desperately in love, dreams of his beloved in an opium haze, <bookmark mark='d'/> and she appears "
                   "as a melody, the idée fixe, the obsession, which returns in every movement: <bookmark mark='e'/> at a "
                   "ball, in the fields, at his own execution, at a witches' sabbath. <bookmark mark='f'/> The theme changes "
                   "as the story does. It is a character, not a subject to be developed in the Classical way.", marks="cdef")

    # ------------------------------------------------------------------
    def idee(self):
        d = load("idee")
        c = clip("idee.five")
        rows_ = VGroup()
        rolls = []
        for k in KINDS:
            ln = d["lines"][k]
            ac = d["acc"][k]
            total = max(n[1] + n[2] for n in ln + ac)
            g = voices_roll([ln, ac], width=6.8 * min(1.0, total / 16) + 0.6, height=0.7, colors=[TUNE, GREY_A], lo=34, hi=84, bar_h=0.06)
            rows_.add(VGroup(label(NAME[k], font_size=19, color=GREY_A), g).arrange(RIGHT, buff=0.4))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(UP * 0.05)
        head = label(r"the Tune's first phrase as an \textit{idée fixe} \ (ours, \ after Berlioz's plan)", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the idea with the Tune's first phrase standing in for Berlioz's melody. The theme, plainly. At the ball, "
            "as a waltz in three. In minor, the dream darkening. As the march to the scaffold, low and dotted. And "
            "augmented, twice as slow, remembered. Same notes, five characters; the transformations are ours, but each one "
            "follows a movement of Berlioz's plan."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"one theme, \ five guises", detail=r"Part 7's bowed string and piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(KINDS):
                st = d["starts"][k]
                flash_voices(snd, rolls[i], [d["lines"][k], d["acc"][k]], st, d["units"][k], colors=[TUNE, GREY_A])
                end = d["starts"][KINDS[i + 1]] - 0.4 if i < 4 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orchestra(self):
        d = load("orchestra")
        rws = d["rows"]
        bars = columns([r["players"] for r in rws], [str(r["year"]) for r in rws], width=7.6, height=2.8, color=GREY_B, hot=(3,), hot_color=TUNE, fmt="{:.0f}", font_size=18)
        bars.move_to(LEFT * 2.2 + DOWN * 0.4)
        t = label(r"wind, \ brass and timpani players the score calls for", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        names = VGroup(*[label(rf"{r['year']}: \ {r['name']}", font_size=18, color=TUNE if i == 3 else GREY_A) for i, r in enumerate(rws)]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        names.scale_to_fit_width(min(names.width, 4.6)).move_to(RIGHT * 4.3 + UP * 0.5)
        note = label(r"strings, \ harps and percussion not counted", font_size=19, color=GREY_A).next_to(names, DOWN, buff=0.45)
        with self.voiceover(
            "The story needed a bigger orchestra. Count the wind, brass and timpani players each score calls for. "
            "<bookmark mark='a'/> Haydn's first symphony, about 1759: five. Mozart's fortieth, nine. Beethoven's fifth, of "
            "1808, eighteen, with trombones in a symphony for the first time in his. <bookmark mark='b'/> Berlioz, in "
            "1830: twenty-seven, with cornets, ophicleides and four timpanists, and harps and bells besides, which the "
            "count leaves out, as it leaves out the strings. <bookmark mark='c'/> Brahms in 1876 is more classical again, at nineteen; the century "
            "did not move in one direction."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            vo.wait_until("a")
            self.play(FadeIn(names[:3]))
            vo.wait_until("b")
            self.play(FadeIn(names[3]), FadeIn(note))
            vo.wait_until("c")
            self.play(FadeIn(names[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def liszt(self):
        items = [
            (r"Franz Liszt: \ the symphonic poem, \ one movement after a poem, \ a painting, \ a legend", WHITE),
            (r"thematic transformation: \ one theme, \ changed in tempo, \ mode and character, \ holds a work together", WHITE),
            (r"programme or absolute? \ Hanslick \ (1854): \ music's content is `forms moved in sound'", WHITE),
            (r"Brahms against Wagner and Liszt: \ the century's quarrel over what music means", TUNE),
            (r"Part 44 returns to music that tells a story: \ film and games", GREY_A),
        ]
        rows_scene(self, r"the symphonic poem", items,
                   "Franz Liszt took the idea further. <bookmark mark='b'/> His symphonic poems are single movements after a "
                   "poem, a painting or a legend, <bookmark mark='c'/> held together by thematic transformation: one theme, "
                   "changed in tempo, mode and character, as we just did to the Tune. <bookmark mark='d'/> Not everyone "
                   "agreed that music should tell stories. The Viennese critic Eduard Hanslick argued in 1854 that music's "
                   "content is forms moved in sound, and nothing else. <bookmark mark='e'/> Brahms was claimed by one side and "
                   "Wagner and Liszt by the other, in the century's long quarrel about what music means. "
                   "<bookmark mark='f'/> Part 44 comes back to music that tells a story, in film and games.", marks="cdef")

    # ------------------------------------------------------------------
    def treatise(self):
        items = [
            (r"Berlioz, \ \textit{Treatise on Instrumentation} \ (1844): \ each instrument's range, \ colour and character", WHITE),
            (r"orchestration becomes a subject of its own: \ how a chord sounds depends on who plays it", WHITE),
            (r"valves for horns and trumpets \ (from the 1810s--30s): \ every note in tune, \ every key", WHITE),
            (r"Adolphe Sax's saxophones and saxhorns \ (1840s): \ new colours, \ invented in a workshop", TUNE),
            (r"Part 41 builds orchestration from Part 7's and Part 8's instruments", GREY_A),
        ]
        rows_scene(self, r"the orchestra as a palette", items,
                   "Berlioz also wrote the book on it. <bookmark mark='b'/> His Treatise on Instrumentation, of 1844, describes each instrument's range, colour and character, <bookmark mark='c'/> and made orchestration a subject of its own: how a chord sounds depends on who plays it. <bookmark mark='d'/> Instruments changed too. Valves, added to horns and trumpets from the 1810s on, let them play every note in tune in every key, <bookmark mark='e'/> and in the 1840s Adolphe Sax invented whole families of instruments in his Paris workshop. <bookmark mark='f'/> Part 41 builds orchestration from the instruments of Parts 7 and 8.", marks="cdef")
