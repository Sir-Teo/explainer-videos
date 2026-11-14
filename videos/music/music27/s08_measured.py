from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403

KC = {"vocal": BLUE, "song": "#A3E635", "quartet": TUNE, "keyboard": EAR, "instrumental": TUNE, "concerto": TUNE, "chamber": TUNE}


class Measured(SoundScene):
    def construct(self):
        chapter(self, 7, r"The stretching, \ measured", r"Did harmony really grow more chromatic?")
        self.definition()
        self.scatter()
        self.trend()
        self.genre()
        self.quiz()
        self.caveats()

    # ------------------------------------------------------------------
    def definition(self):
        rows_ = text_rows([
            (r"the Library: \ 827 pieces, \ 1370 to 1924, \ from the collections earlier parts read and the music21 corpus", WHITE),
            (r"cut each piece into windows of four bars \ (sixteen beats), \ overlapping by half", WHITE),
            (r"find each window's key with Part 15's profiles", WHITE),
            (r"chromaticism: \ the share of sounding time on notes outside that key's scale", TUNE),
            (r"tonal clarity: \ how well the best key's profile fits the window \ (a correlation, \ at most 1)", BLUE),
        ], font_size=24)
        head = label(r"two measures", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The usual story says that through the century harmony was stretched until the key could barely hold. That is a "
            "claim about notes, so it can be measured. <bookmark mark='a'/> The Library is every piece the earlier parts "
            "read, plus every dated piece in the music21 corpus: eight hundred and twenty-seven pieces, from the "
            "fourteenth century to 1924. <bookmark mark='b'/> Each piece is cut into windows of sixteen beats, overlapping "
            "by half, <bookmark mark='c'/> and Part 15's key profiles find each window's key. <bookmark mark='d'/> "
            "Chromaticism is the share of sounding time spent on notes outside that key's scale, counting the raised sixth "
            "and seventh of minor as inside. <bookmark mark='e'/> Tonal clarity is how well the best key fits: the "
            "correlation between the window's notes and the key's profile."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _axes(self, y_range, ylab):
        ax = Axes(x_range=[1340, 1940, 100], y_range=y_range, x_length=10.0, y_length=4.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18},
                  x_axis_config={"include_numbers": True, "numbers_to_include": [1400, 1500, 1600, 1700, 1800, 1900], "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}},
                  y_axis_config={"include_numbers": True}).move_to(DOWN * 0.45 + RIGHT * 0.3)
        yl = label(ylab, font_size=19, color=GREY_A).next_to(ax.y_axis, UP, buff=0.15).shift(RIGHT * 1.0)
        return ax, yl

    def scatter(self):
        d = load("library")
        pts = d["points"]
        ax, yl = self._axes([0, 32, 8], r"chromaticism, \ in 100")
        jit = np.random.default_rng(0)
        dots = VGroup()
        for p in pts:
            r = 0.05 + 0.025 * np.log1p(p["n"])
            dots.add(Dot(ax.c2p(p["year"] + jit.uniform(-3, 3), 100 * p["chromaticism"]), radius=r, color=KC.get(p["kind"], GREY_A), fill_opacity=0.85))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=c_), label(t, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.12) for t, c_ in (
            (r"vocal collections", BLUE), (r"songs", "#A3E635"), (r"quartets and instruments", TUNE), (r"keyboard", EAR))]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.45)
        note = label(r"a larger dot: \ more pieces averaged", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.2).align_to(ax, RIGHT)
        early = [i for i, p in enumerate(pts) if p["year"] < 1680]
        mid = [i for i, p in enumerate(pts) if 1680 <= p["year"] <= 1900]
        late = [i for i, p in enumerate(pts) if p["year"] > 1900]
        with self.voiceover(
            "Here is every group in the Library, one dot for each collection or piece, placed by its date and its "
            "chromaticism. <bookmark mark='a'/> Before 1680: the trecento, Palestrina, Monteverdi, between three and six "
            "in a hundred. Some of that is the method: a modal piece measured against major and minor profiles shows its "
            "modal notes as outside. <bookmark mark='b'/> From Corelli to 1900, the Baroque, the Classical quartets and "
            "the Romantic pieces spread between nearly zero and fifteen. <bookmark mark='c'/> And then three pieces from "
            "1911 and 1924, by Schoenberg and Webern, at twenty-five to thirty: a different world."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(key), FadeIn(note))
            for mark, idx in zip("abc", (early, mid, late)):
                vo.wait_until(mark)
                self.play(LaggedStart(*[FadeIn(dots[i], scale=0.5) for i in idx], lag_ratio=0.05), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trend(self):
        d = load("library")
        pts = d["points"]
        ax, yl = self._axes([0, 32, 8], r"chromaticism, \ in 100")
        sel = [p for p in pts if 1680 <= p["year"] <= 1900]
        dots = VGroup(*[Dot(ax.c2p(p["year"], 100 * p["chromaticism"]), radius=0.07, color=KC.get(p["kind"], GREY_A), fill_opacity=0.85) for p in sel])
        others = VGroup(*[Dot(ax.c2p(p["year"], 100 * p["chromaticism"]), radius=0.06, color=GREY_B, fill_opacity=0.35) for p in pts if not 1680 <= p["year"] <= 1900])
        x = np.array([p["year"] for p in sel], float)
        y = np.array([100 * p["chromaticism"] for p in sel])
        ins = np.array([p["kind"] not in ("song", "vocal") for p in sel])
        b_all = np.polyfit(x, y, 1)
        b_ins = np.polyfit(x[ins], y[ins], 1)
        l_all = Line(ax.c2p(1680, np.polyval(b_all, 1680)), ax.c2p(1900, np.polyval(b_all, 1900)), color=WHITE, stroke_width=3)
        l_ins = Line(ax.c2p(1680, np.polyval(b_ins, 1680)), ax.c2p(1900, np.polyval(b_ins, 1900)), color=TUNE, stroke_width=4)
        t_all = label(rf"all {d['n_trend']}: \ {100 * d['slope_c']:+.1f} a century \ (95\% interval {100 * d['ci_c'][0]:+.1f} to {100 * d['ci_c'][1]:+.1f})", font_size=19, color=WHITE)
        t_ins = label(rf"instrumental, \ {d['n_i']}: \ {100 * d['slope_i']:+.1f} a century \ ({100 * d['ci_i'][0]:+.1f} to {100 * d['ci_i'][1]:+.1f})", font_size=19, color=TUNE)
        VGroup(t_all, t_ins).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_corner(UL, buff=0.45).shift(RIGHT * 1.2)
        with self.voiceover(
            "Is there a trend between 1680 and 1900? Fit a straight line to those points. <bookmark mark='a'/> "
            f"Over all {say(d['n_trend'])} of them, chromaticism rises by about {say(round(100 * d['slope_c'], 1))} points a "
            "century, but a bootstrap, which refits the line on resampled points four thousand times, gives an interval "
            f"from {say(round(100 * d['ci_c'][0], 1))} to {say(round(100 * d['ci_c'][1], 1))}: it includes no change at all. "
            f"<bookmark mark='b'/> Keep only the instrumental pieces, {say(d['n_i'])} of them, and the rise is "
            f"{say(round(100 * d['slope_i'], 1))} points a century, with an interval from {say(round(100 * d['ci_i'][0], 1))} "
            f"to {say(round(100 * d['ci_i'][1], 1))}, clear of zero. The stretching is real in instrumental music, and "
            "gradual: a few notes in a hundred per century."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(dots), FadeIn(others))
            vo.wait_until("a")
            self.play(Create(l_all), FadeIn(t_all))
            vo.wait_until("b")
            self.play(Create(l_ins), FadeIn(t_ins), dots.animate.set_opacity(0.6))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def genre(self):
        d = load("library")
        bars = columns([100 * d["songs"], 100 * d["instrumental"]], [r"songs", r"instrumental"], width=4.4, height=2.6, color="#A3E635", hot=(1,), hot_color=TUNE, fmt="{:.1f}", font_size=20)
        bars.move_to(LEFT * 3.4 + DOWN * 0.4)
        t = label(r"chromaticism, \ in 100: \ pieces from 1800 to 1900", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"{d['n_songs']} songs: \ Schubert to Johnson", WHITE),
            (rf"{d['n_inst']} instrumental pieces", WHITE),
            (r"genre matters as much as date", TUNE),
            (r"tunes stay home; \ accompaniments wander", EAR))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6))
        side.move_to(RIGHT * 3.1 + DOWN * 0.2)
        with self.voiceover(
            "Why does including the songs blur the trend? Compare the nineteenth-century pieces by kind. "
            f"<bookmark mark='a'/> The {say(d['n_songs'])} songs average about {say(round(100 * d['songs']))} in a hundred. "
            f"<bookmark mark='b'/> The {say(d['n_inst'])} instrumental pieces average about {say(round(100 * d['instrumental']))}, "
            "more than twice as much. <bookmark mark='c'/> In this Library genre matters as much as date. "
            "<bookmark mark='d'/> A tune meant to be sung by anyone stays close to its key; it is the accompaniments, "
            "developments and transitions that wander."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("library")
        q = d["quiz"]
        c = clip("library.quiz")
        card = listen_card(r"Two string-quartet passages, \ about fifty years apart. \ "
                           r"Which was written later, \ A or B? \ Listen for notes outside the key.", width=10.0)
        with self.voiceover(
            "Can you hear the difference? Two string-quartet passages, about fifty years apart. Which was written later, A or "
            "B? Listen for notes outside the key."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        cols = [TUNE, BLUE, EAR, GREY_A]
        gA = voices_roll(q["A"], width=5.4, height=2.8, colors=cols, bar_h=0.08).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(q["B"], width=5.4, height=2.8, colors=cols, bar_h=0.08).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"from the encodings, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, q["A"], d["starts"]["A"], q["unit"], colors=cols)
            flash_voices(snd, gB, q["B"], d["starts"]["B"], q["unit"], colors=cols)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(rf"Schumann, \ 1842: \ {100 * q['A_chrom']:.0f} in 100 outside the key", font_size=21, color=EAR).next_to(gA, DOWN, buff=0.35),
                     label(rf"Haydn, \ 1793: \ {100 * q['B_chrom']:.0f} in 100", font_size=21, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "A is later: Robert Schumann's first string quartet, of 1842, a passage the measure picked as its most chromatic, "
            f"with {say(round(100 * q['A_chrom']))} notes in a hundred outside the key. B is Haydn, 1793, a typical passage, "
            f"at {say(round(100 * q['B_chrom']))}. The comparison is loaded, extreme against typical, and that is the point: "
            "the averages move slowly, but the extremes moved a long way."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caveats(self):
        items = [
            (r"a small, \ accidental Library: \ what the corpus happens to hold, \ not a sample of the century", WHITE),
            (r"keys from a profile: \ modal music and quick modulations both count as `chromatic'", WHITE),
            (r"dates are of composition, \ some approximate; \ groups average different numbers of pieces", WHITE),
            (r"what holds anyway: \ instrumental music grew more chromatic, \ slowly; \ then a jump after 1900", TUNE),
            (r"the frontier \ (chapter ten): \ thousands of pieces, \ from audio as well as scores", GREY_A),
        ]
        rows_scene(self, r"what the measurement can and cannot say", items,
                   "How far can this be trusted? <bookmark mark='b'/> The Library is small and accidental: what the corpus "
                   "happens to hold, not a sample of the century. <bookmark mark='c'/> The key comes from a profile, so modal "
                   "music, and music that modulates quickly, both count as chromatic. <bookmark mark='d'/> Dates are of "
                   "composition and some are approximate, and the groups average different numbers of pieces. "
                   "<bookmark mark='e'/> What holds anyway is the shape: instrumental music grew more chromatic, slowly, and "
                   "then jumped after 1900. <bookmark mark='f'/> Chapter ten describes studies that do this with thousands of "
                   "pieces, from recordings as well as scores.", marks="cdef")
