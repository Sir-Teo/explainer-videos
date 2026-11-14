from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Concerto(SoundScene):
    def construct(self):
        chapter(self, 6, r"Ritornello and concerto", r"How do you build a fast movement from returns?", extra=((1711, r"Vivaldi's \textit{L'estro armonico}"),))
        self.history()
        self.heard()
        self.finder()
        self.seasons()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"the concerto grosso: \ a small group of soloists against the full string band \ (Corelli, \ Op. 6, \ 1714)", WHITE),
            (r"the solo concerto: \ one violin against the band \ (Antonio Vivaldi, \ Venice; \ \textit{L'estro armonico}, \ 1711)", WHITE),
            (r"ritornello form: \ the band's theme returns, \ in different keys; \ the soloist's episodes travel between", WHITE),
            (r"the plan: \ R in I, \ solo, \ R in V, \ solo, \ R in vi, \ solo, \ R in I", TUNE),
            (r"Bach copied Vivaldi's concertos for keyboard to learn the form", GREY_A),
        ]
        rows_scene(self, r"the concerto", items,
                   "The largest instrumental form of the age was the concerto. <bookmark mark='b'/> Corelli's concertos "
                   "set a small group of soloists against the full string band; Antonio Vivaldi, a violinist-priest in "
                   "Venice, set one violin against it, in a set printed in 1711 as L'estro armonico, harmonic inspiration. "
                   "<bookmark mark='c'/> Vivaldi's fast movements use ritornello form: the band's opening theme, the "
                   "ritornello, returns again and again, in different keys, and between its returns the soloist's "
                   "episodes travel from key to key. <bookmark mark='d'/> A typical plan: the ritornello in the home key, "
                   "an episode, the ritornello in the dominant, an episode, the ritornello in a minor key, often only its "
                   "head, an episode, and the ritornello at home. <bookmark mark='e'/> Bach copied out Vivaldi's concertos "
                   "for keyboard, in his twenties, to learn how it was done.", marks="bcdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ritornello")
        c = clip("ritornello.concerto")
        g = voices_roll([d["melody"], d["bass"]], width=11.6, height=3.0, colors=[TUNE, GREY_A], bar_h=0.11).move_to(DOWN * 0.4)
        spans = VGroup()
        for kind, key, t0 in d["plan"]:
            nxt = [p[2] for p in d["plan"] if p[2] > t0]
            t1 = min(nxt) if nxt else g.total
            x0 = g.frame.get_left()[0] + g.frame.width * t0 / g.total
            x1 = g.frame.get_left()[0] + g.frame.width * t1 / g.total
            col = TUNE if kind == "R" else BLUE
            box = Rectangle(width=x1 - x0 - 0.04, height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.35).move_to([(x0 + x1) / 2, g.frame.get_top()[1] + 0.45, 0])
            spans.add(VGroup(box, label(rf"{'R' if kind == 'R' else 'solo'}: \ {key.replace('#', '$\\sharp$')}", font_size=15, color=WHITE).move_to(box)))
        head = label(r"a concerto movement in ritornello form \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is a short movement in that plan, computed for the film: the ritornello in C, a solo episode, the "
            "ritornello in G, an episode, its head in A minor, an episode, and the ritornello in C again. Listen for the "
            "theme each time it comes back, and for where it is."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(spans))
        with self.listen(c) as snd:
            window(snd, r"ritornello form", detail=r"Part 7's bowed string, \ harpsichord", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["melody"], d["bass"]], 0.0, d["unit"], colors=[TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def finder(self):
        d = load("ritornello")
        f = d["found"]
        rs = [p for p in d["plan"] if p[0] == "R"]
        rows_ = VGroup()
        for kind, key, t0 in rs:
            hit = next((x for x in f if abs(x["onset"] - t0) < 1e-6), None)
            txt = rf"beat {t0:.0f}: \ ritornello in {key.replace('#', '$\\sharp$')} \ $\to$ \ " + (rf"found, \ transposed {hit['transpose']:+d}".replace("+", "$+$") if hit else r"missed")
            rows_.add(label(txt, font_size=24, color=TUNE if hit else RED))
        rows_.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.6)
        cap = VGroup(label(r"the finder: \ compare the opening's first six melodic intervals with every place in the line", font_size=21, color=GREY_A),
                     label(r"intervals, \ not pitches: \ a transposed return matches exactly", font_size=21, color=WHITE),
                     label(r"but in the minor the third shrinks: \ two intervals change, \ and the return is missed", font_size=21, color=EAR)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Now a program finds the returns, as Part 21's novelty curve found sections. <bookmark mark='a'/> It takes "
            "the first six melodic intervals of the opening and slides them along the whole line, allowing one mismatch. "
            "<bookmark mark='b'/> Because it compares intervals, not pitches, a transposed return matches exactly: it finds "
            f"the returns in C, in G, a fifth up, and in C again. <bookmark mark='c'/> But it misses the head in A minor, "
            "where the major third has become a minor one and two intervals have changed. A real ritornello finder must "
            "allow for mode, and for the fragments and variations that Vivaldi's returns usually are; in real concertos "
            "the band's harmony and scoring help as much as the melody."
        ) as vo:
            self.play(FadeIn(rows_))
            vo.wait_until("a")
            self.play(FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def seasons(self):
        items = [
            (r"1725: \ Vivaldi's \textit{The Four Seasons}, \ each concerto printed with a sonnet", WHITE),
            (r"birdsong, \ a storm, \ a barking dog, \ a drunken peasant, \ ice: \ marked in the score", WHITE),
            (r"the ritornello is the season; \ the episodes are its events", WHITE),
            (r"program music: \ instruments telling a story without words", TUNE),
            (r"the same form carries both the abstract and the pictorial", GREY_A),
        ]
        rows_scene(self, r"concertos with a story", items,
                   "Vivaldi also showed what the form could depict. <bookmark mark='b'/> In 1725 he printed four violin concertos, The Four Seasons, each with a sonnet, and the lines of the sonnet are written into the score where the music illustrates them: <bookmark mark='c'/> birdsong, a summer storm, a barking dog, a drunken peasant, walking on ice. <bookmark mark='d'/> In spring's first movement the ritornello is the season itself and the solo episodes are its events. <bookmark mark='e'/> It is program music, instruments telling a story without words, <bookmark mark='f'/> in exactly the same ritornello form that elsewhere carries nothing but notes.", marks="cdef")
